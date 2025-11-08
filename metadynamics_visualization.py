#!/usr/bin/env python3
"""
Metadynamics Visualization
Metadynamik-Visualisierung

Demonstrates metadynamics enhanced sampling:
- Phase 1: Naive MD - particles trapped in local minimum
- Phase 2: Metadynamics - Gaussian bias functions drive particles to global minimum

Left: Simulation box WITH potential landscape and 5 particles
Right: Collective variable (center of mass) evolution
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "EN"  # Set to "EN" for English

STRINGS = {
    "DE": {
        "title": "Metadynamik: Enhanced Sampling",
        "phase0_title": "Phase 0: Freie Bewegung - Nur harmonische Wände",
        "phase1_title": "Phase 1: Y-Confinement - Teilchen zu y=0",
        "phase2_title": "Phase 2: Harmonisches Potential - Ein Minimum",
        "phase2_transition": "Übergang zum Doppel-Minimum-Potential",
        "phase3_title": "Phase 3: Naive MD - Gefangen im lokalen Minimum",
        "phase3b_title": "Phase 3b: Hohe Temperatur - Thermisches Überwinden",
        "phase4_title": "Phase 4: Metadynamik - Gaußfunktionen treiben heraus",
        "temperature": "Temperatur",
        "simulation_box": "Simulationsbox mit Potential",
        "cv_plot": "Collective Variable",
        "local_min": "Lokal",
        "global_min": "Global",
        "time_fs": "Zeit (fs)",
        "position_x": "Schwerpunkt x",
        "external_pot": "V_ext",
        "bias_pot": "V_bias",
        "total_pot": "V_total",
    },
    "EN": {
        "title": "Metadynamics: Enhanced Sampling",
        "phase0_title": "Phase 0: Free Movement - Only Harmonic Walls",
        "phase1_title": "Phase 1: Y-Confinement - Particles to y=0",
        "phase2_title": "Phase 2: Harmonic Potential - One Minimum",
        "phase2_transition": "Transition to Double-Well Potential",
        "phase3_title": "Phase 3: Naive MD - Trapped in Local Minimum",
        "phase3b_title": "Phase 3b: High Temperature - Thermal Crossing",
        "phase4_title": "Phase 4: Metadynamics - Gaussians Drive Out",
        "temperature": "Temperature",
        "simulation_box": "Simulation Box with Potential",
        "cv_plot": "Collective Variable",
        "local_min": "Local",
        "global_min": "Global",
        "time_fs": "Time (fs)",
        "position_x": "Center of Mass x",
        "external_pot": "V_ext",
        "bias_pot": "V_bias",
        "total_pot": "V_total",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class MetadynamicsVisualization(Scene):
    """Metadynamics enhanced sampling visualization with 6 phases."""

    PARAMETERS = {
        # Particle count
        "n_particles": {
            "value": 5,
            "type": int,
            "unit": "-",
            "description": "Number of particles in simulation",
            "min": 1,
            "max": 10
        },
        # Harmonic potential parameters (Phase 2)
        "harmonic_k": {
            "value": 5.0,
            "type": float,
            "unit": "kcal/(mol·Å²)",
            "description": "Spring constant for harmonic potential",
            "min": 0.1,
            "max": 20.0
        },
        "harmonic_center": {
            "value": -0.97,
            "type": float,
            "unit": "Å",
            "description": "Center of harmonic well (matches double-well local min)",
            "min": -2.0,
            "max": 2.0
        },
        # Double-well potential parameters
        "pot_a": {
            "value": 3.0,
            "type": float,
            "unit": "kcal/mol/Å⁴",
            "description": "Double-well parameter a in V(x)=a*(x²-b)²+c*x",
            "min": 0.1,
            "max": 10.0
        },
        "pot_b": {
            "value": 1.0,
            "type": float,
            "unit": "Å²",
            "description": "Double-well parameter b in V(x)=a*(x²-b)²+c*x",
            "min": 0.1,
            "max": 5.0
        },
        "pot_c": {
            "value": -0.7,
            "type": float,
            "unit": "kcal/mol/Å",
            "description": "Double-well parameter c (asymmetry) in V(x)=a*(x²-b)²+c*x",
            "min": -2.0,
            "max": 2.0
        },
        # Y-confinement parameters
        "k_y_weak": {
            "value": 1.0,
            "type": float,
            "unit": "kcal/(mol·Å²)",
            "description": "Weak y-confinement for Phase 0",
            "min": 0.0,
            "max": 10.0
        },
        "k_y_strong": {
            "value": 5.0,
            "type": float,
            "unit": "kcal/(mol·Å²)",
            "description": "Strong y-confinement for Phase 1+",
            "min": 1.0,
            "max": 20.0
        },
        # Harmonic wall parameters
        "wall_k": {
            "value": 200.0,
            "type": float,
            "unit": "kcal/(mol·Å²)",
            "description": "Strength of harmonic walls at box boundaries",
            "min": 50.0,
            "max": 500.0
        },
        "wall_x_min": {
            "value": -2.22,
            "type": float,
            "unit": "Å",
            "description": "Left wall position",
            "min": -5.0,
            "max": 0.0
        },
        "wall_x_max": {
            "value": 2.22,
            "type": float,
            "unit": "Å",
            "description": "Right wall position",
            "min": 0.0,
            "max": 5.0
        },
        "wall_y_min": {
            "value": -2.33,
            "type": float,
            "unit": "Å",
            "description": "Bottom wall position",
            "min": -5.0,
            "max": 0.0
        },
        "wall_y_max": {
            "value": 14.33,
            "type": float,
            "unit": "Å",
            "description": "Top wall position",
            "min": 5.0,
            "max": 20.0
        },
        # Lennard-Jones parameters
        "epsilon_lj": {
            "value": 0.02,
            "type": float,
            "unit": "kcal/mol",
            "description": "LJ well depth (reduced for stability)",
            "min": 0.0,
            "max": 0.1
        },
        "sigma_lj": {
            "value": 0.01,
            "type": float,
            "unit": "Å",
            "description": "LJ sigma parameter",
            "min": 0.001,
            "max": 0.1
        },
        "cutoff_lj": {
            "value": 1.0,
            "type": float,
            "unit": "Å",
            "description": "LJ cutoff distance",
            "min": 0.5,
            "max": 3.0
        },
        # MD parameters
        "mass": {
            "value": 10.0,
            "type": float,
            "unit": "amu",
            "description": "Particle mass",
            "min": 1.0,
            "max": 100.0
        },
        "dt": {
            "value": 0.05,
            "type": float,
            "unit": "fs",
            "description": "MD timestep",
            "min": 0.001,
            "max": 0.5
        },
        "max_velocity": {
            "value": 0.2,
            "type": float,
            "unit": "Å/fs",
            "description": "Velocity clamp (unused, legacy)",
            "min": 0.1,
            "max": 1.0
        },
        # Thermostat parameters
        "temperature": {
            "value": 300.0,
            "type": float,
            "unit": "K",
            "description": "Berendsen thermostat target temperature",
            "min": 50.0,
            "max": 500.0
        },
        "k_B": {
            "value": 0.001987,
            "type": float,
            "unit": "kcal/(mol·K)",
            "description": "Boltzmann constant",
            "min": 0.001,
            "max": 0.01
        },
        "tau_berendsen": {
            "value": 1.0,
            "type": float,
            "unit": "fs",
            "description": "Berendsen coupling time constant",
            "min": 0.1,
            "max": 10.0
        },
        # Metadynamics parameters
        "gaussian_height": {
            "value": 0.08,
            "type": float,
            "unit": "kcal/mol",
            "description": "Height of deposited Gaussians",
            "min": 0.01,
            "max": 0.5
        },
        "gaussian_width": {
            "value": 0.25,
            "type": float,
            "unit": "Å",
            "description": "Width (σ) of deposited Gaussians",
            "min": 0.05,
            "max": 1.0
        },
        "gaussian_frequency": {
            "value": 100,
            "type": int,
            "unit": "steps",
            "description": "Add Gaussian every N MD steps",
            "min": 10,
            "max": 500
        },
        # Visualization scaling
        "pot_x_scale": {
            "value": 1.8,
            "type": float,
            "unit": "-",
            "description": "Scale factor for x-coordinates in potential plot",
            "min": 0.5,
            "max": 5.0
        },
        "pot_y_scale": {
            "value": 0.6,
            "type": float,
            "unit": "-",
            "description": "Scale factor for potential energy in plot",
            "min": 0.1,
            "max": 2.0
        },
        # Phase duration parameters (in MD steps)
        "phase0_steps": {
            "value": 600,
            "type": int,
            "unit": "steps",
            "description": "Phase 0 duration: Free movement with only walls",
            "min": 100,
            "max": 2000
        },
        "phase1_steps": {
            "value": 300,
            "type": int,
            "unit": "steps",
            "description": "Phase 1 duration: Y-confinement activation",
            "min": 100,
            "max": 1000
        },
        "phase2_steps": {
            "value": 900,
            "type": int,
            "unit": "steps",
            "description": "Phase 2 duration: Harmonic potential well",
            "min": 300,
            "max": 3000
        },
        "morph_steps": {
            "value": 300,
            "type": int,
            "unit": "steps",
            "description": "Morph duration: Harmonic to double-well transition",
            "min": 100,
            "max": 1000
        },
        "phase3_steps": {
            "value": 1500,
            "type": int,
            "unit": "steps",
            "description": "Phase 3 duration: Naive MD in double-well (trapped)",
            "min": 500,
            "max": 5000
        },
        "phase4_steps": {
            "value": 6000,
            "type": int,
            "unit": "steps",
            "description": "Phase 4 duration: Metadynamics exploration",
            "min": 2000,
            "max": 20000
        },
        # Temperature ramp parameters (Phase 3b)
        "temp_initial": {
            "value": 300.0,
            "type": float,
            "unit": "K",
            "description": "Initial temperature for Phase 3b ramp",
            "min": 100.0,
            "max": 500.0
        },
        "temp_target": {
            "value": 2000.0,
            "type": float,
            "unit": "K",
            "description": "Target high temperature for Phase 3b",
            "min": 500.0,
            "max": 5000.0
        },
        "temp_ramp_steps": {
            "value": 500,
            "type": int,
            "unit": "steps",
            "description": "Duration of temperature ramp up/down",
            "min": 100,
            "max": 2000
        },
        "temp_equilibration_steps": {
            "value": 1000,
            "type": int,
            "unit": "steps",
            "description": "Equilibration time at high temperature",
            "min": 200,
            "max": 5000
        }
    }

    def construct(self):
        # Setup
        self.setup_parameters()
        self.create_title()
        self.create_simulation_box_with_potential()
        self.create_cv_plot()

        self.wait(2)

        # Phase 0: Free movement (no potential)
        self.run_phase_0()

        self.wait(2)

        # Phase 1: Y-confinement activation
        self.run_phase_1()

        self.wait(2)

        # Phase 2: Harmonic potential well
        self.run_phase_2()

        self.wait(2)

        # Transition: Morph to double-well
        self.morph_to_double_well()

        self.wait(2)

        # Phase 3: Naive MD in double-well
        self.run_phase_3()

        self.wait(2)

        # Phase 3b: High temperature MD
        self.run_phase_3b()

        self.wait(2)

        # Phase 4: Metadynamics
        self.run_phase_4()

        self.wait(3)

    def setup_parameters(self):
        """Initialize all simulation parameters from PARAMETERS dictionary"""
        # Extract parameters from central dictionary
        self.n_particles = self.PARAMETERS["n_particles"]["value"]

        # Harmonic potential parameters
        self.harmonic_k = self.PARAMETERS["harmonic_k"]["value"]
        self.harmonic_center = self.PARAMETERS["harmonic_center"]["value"]

        # Double-well potential parameters
        self.pot_a = self.PARAMETERS["pot_a"]["value"]
        self.pot_b = self.PARAMETERS["pot_b"]["value"]
        self.pot_c = self.PARAMETERS["pot_c"]["value"]

        # Y-confinement parameters
        self.k_y_weak = self.PARAMETERS["k_y_weak"]["value"]
        self.k_y_strong = self.PARAMETERS["k_y_strong"]["value"]

        # Harmonic wall parameters
        self.wall_k = self.PARAMETERS["wall_k"]["value"]
        self.wall_x_min = self.PARAMETERS["wall_x_min"]["value"]
        self.wall_x_max = self.PARAMETERS["wall_x_max"]["value"]
        self.wall_y_min = self.PARAMETERS["wall_y_min"]["value"]
        self.wall_y_max = self.PARAMETERS["wall_y_max"]["value"]

        # LJ parameters
        self.epsilon_lj = self.PARAMETERS["epsilon_lj"]["value"]
        self.sigma_lj = self.PARAMETERS["sigma_lj"]["value"]
        self.cutoff_lj = self.PARAMETERS["cutoff_lj"]["value"]

        # MD parameters
        self.mass = self.PARAMETERS["mass"]["value"]
        self.dt = self.PARAMETERS["dt"]["value"]
        self.max_velocity = self.PARAMETERS["max_velocity"]["value"]

        # Thermostat parameters
        self.temperature = self.PARAMETERS["temperature"]["value"]
        self.k_B = self.PARAMETERS["k_B"]["value"]
        self.tau_berendsen = self.PARAMETERS["tau_berendsen"]["value"]

        # Metadynamics parameters
        self.gaussian_height = self.PARAMETERS["gaussian_height"]["value"]
        self.gaussian_width = self.PARAMETERS["gaussian_width"]["value"]
        self.gaussian_frequency = self.PARAMETERS["gaussian_frequency"]["value"]

        # Visualization scaling
        self.pot_x_scale = self.PARAMETERS["pot_x_scale"]["value"]
        self.pot_y_scale = self.PARAMETERS["pot_y_scale"]["value"]

        # Phase duration parameters
        self.phase0_steps = self.PARAMETERS["phase0_steps"]["value"]
        self.phase1_steps = self.PARAMETERS["phase1_steps"]["value"]
        self.phase2_steps = self.PARAMETERS["phase2_steps"]["value"]
        self.morph_steps = self.PARAMETERS["morph_steps"]["value"]
        self.phase3_steps = self.PARAMETERS["phase3_steps"]["value"]
        self.phase4_steps = self.PARAMETERS["phase4_steps"]["value"]

        # Temperature ramp parameters
        self.temp_initial = self.PARAMETERS["temp_initial"]["value"]
        self.temp_target = self.PARAMETERS["temp_target"]["value"]
        self.temp_ramp_steps = self.PARAMETERS["temp_ramp_steps"]["value"]
        self.temp_equilibration_steps = self.PARAMETERS["temp_equilibration_steps"]["value"]

        # Potential type control (state variables, not parameters)
        self.no_potential = True  # Phase 0: No external potential in x
        self.use_harmonic = True  # Start with harmonic, then switch to double-well
        self.morph_alpha = 0.0  # Interpolation parameter (0=harmonic, 1=double-well)
        self.current_k_y = self.k_y_weak  # Start with weak confinement

        # Initialize particle positions distributed (for Phase 0: free movement)
        self.positions = np.zeros((self.n_particles, 2))
        for i in range(self.n_particles):
            self.positions[i] = np.array([
                np.random.uniform(-0.8, 0.8),  # Distributed in x
                np.random.uniform(-0.4, 0.4)   # Distributed in y
            ])
            print(self.positions[i])  # Debug: print initial positions

        # Initialize velocities (thermal motion at 300K)
        # v_thermal ~ sqrt(k_B * T / m) ≈ 0.025 for our units
        self.velocities = np.random.uniform(-0.03, 0.03, (self.n_particles, 2))

        # Simulation state
        self.time = 0.0
        self.step = 0
        self.metadynamics_active = False

        # Metadynamics state
        self.gaussians = []  # List of (center, height, width)

        # Tracking
        self.time_history = []
        self.cv_history = []

    def create_title(self):
        """Create title"""
        self.title = Text(get_string("title"), color=YELLOW).scale(0.6)
        self.title.to_edge(UP, buff=0.15)
        self.add(self.title)

    def create_simulation_box_with_potential(self):
        """Create simulation box with embedded potential visualization"""
        # Box center and dimensions
        self.box_center = LEFT * 2.5 + DOWN * 0.3
        box_width = 8.0
        box_height = 5.0

        # Draw box boundary
        sim_box = Rectangle(
            width=box_width, height=box_height,
            stroke_color=WHITE, stroke_width=2, fill_opacity=0.02
        )
        sim_box.move_to(self.box_center)
        self.add(sim_box)

        # Box label (shows current phase)
        self.box_label = Text(get_string("phase0_title"), color=BLUE).scale(0.4)
        self.box_label.move_to(self.box_center + UP * 30.0)
        self.add(self.box_label)

        # Create axes for potential (embedded in box)
        self.pot_origin = self.box_center + DOWN * 1.8

        # X-axis
        x_axis = Line(
            self.pot_origin + LEFT * 3.5,
            self.pot_origin + RIGHT * 3.5,
            color=GREY, stroke_width=1
        )
        self.add(x_axis)

        # Y-axis (energy)
        y_axis = Line(
            self.pot_origin,
            self.pot_origin + UP * 3.5,
            color=GREY, stroke_width=1
        )
        self.add(y_axis)

        # Axis labels
        x_label = Text("x", color=WHITE).scale(0.3)
        x_label.next_to(x_axis, RIGHT, buff=0.1)
        self.add(x_label)

        y_label = Text("E", color=WHITE).scale(0.3)
        y_label.next_to(y_axis, LEFT, buff=0.15)
        y_label.shift(UP * 1.5)  # Position at mid-height of axis
        self.add(y_label)

        # Add force field heatmap (background layer)
        self.force_heatmap = self.create_force_heatmap()
        self.add(self.force_heatmap)

        # Plot current potential (starts as harmonic)
        self.external_pot_curve = self.create_potential_curve(
            lambda x: self.current_potential(x),
            color=BLUE, stroke_width=3
        )
        self.add(self.external_pot_curve)

        # Bias potential curve (initially empty)
        self.bias_pot_curve = VMobject(color=RED, stroke_width=2)
        self.add(self.bias_pot_curve)

        # Total potential curve (initially same as external)
        self.total_pot_curve = VMobject(color=YELLOW, stroke_width=4, stroke_opacity=0.7)
        self.add(self.total_pot_curve)
        self.update_total_potential()

        # Gaussian curves storage
        self.gaussian_curves = []

        # Mark minima (actual positions from double-well potential)
        local_min_x = -0.97
        global_min_x = 1.03

        # Local minimum marker
        local_mark = Line(
            self.pot_origin + RIGHT * (local_min_x * self.pot_x_scale) + UP * 0.1,
            self.pot_origin + RIGHT * (local_min_x * self.pot_x_scale) + DOWN * 0.2,
            color=RED, stroke_width=4
        )
        self.add(local_mark)

        local_label = Text(get_string("local_min"), color=RED).scale(0.25)
        local_label.next_to(local_mark, DOWN, buff=0.1)
        self.add(local_label)

        # Global minimum marker
        global_mark = Line(
            self.pot_origin + RIGHT * (global_min_x * self.pot_x_scale) + UP * 0.1,
            self.pot_origin + RIGHT * (global_min_x * self.pot_x_scale) + DOWN * 0.2,
            color=GREEN, stroke_width=4
        )
        self.add(global_mark)

        global_label = Text(get_string("global_min"), color=GREEN).scale(0.25)
        global_label.next_to(global_mark, DOWN, buff=0.1)
        self.add(global_label)

        # Create particles
        self.particle_dots = []
        for i in range(self.n_particles):
            dot = Dot(radius=0.12, color=BLUE, fill_opacity=0.9)
            self.particle_dots.append(dot)
            self.add(dot)

        # Update initial positions
        self.update_particle_positions()

        # Legend
        legend = VGroup(
            Text(get_string("external_pot"), color=BLUE).scale(0.25),
            Text(get_string("bias_pot"), color=RED).scale(0.25),
            Text(get_string("total_pot"), color=YELLOW).scale(0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        legend.move_to(self.box_center + RIGHT * 3.0 + UP * 2.2)
        #self.add(legend)

    def create_cv_plot(self):
        """Create CV evolution plot on the right"""
        # CV plot center
        cv_center = RIGHT * 4.5 + DOWN * 0.3

        # Create axes (extended range for longer simulation)
        self.cv_axes = Axes(
            x_range=[0, 1200, 200],  # 3x longer to accommodate extended simulation
            y_range=[-1.5, 1.5, 0.5],
            width=4.5,
            height=4.0,
            #axis_config={"include_tip": True, "include_numbers": True}
        )
        self.cv_axes.move_to(cv_center)
        self.add(self.cv_axes)

        # Labels
        cv_x_label = Text(get_string("time_fs"), color=WHITE).scale(0.3)
        cv_x_label.next_to(self.cv_axes.get_x_axis(), DOWN, buff=0.2)
        self.add(cv_x_label)

        cv_y_label = Text(get_string("position_x"), color=WHITE).scale(0.3)
        cv_y_label.next_to(self.cv_axes.get_y_axis(), LEFT, buff=0.2)
        cv_y_label.rotate(90 * DEGREES)
        self.add(cv_y_label)

        # Plot label
        plot_label = Text(get_string("cv_plot"), color=ORANGE).scale(0.35)
        plot_label.move_to(cv_center + UP * 2.5)
        self.add(plot_label)

        # Reference lines (extended to match new time range)
        local_line = DashedVMobject(
            Line(
                self.cv_axes.coords_to_point(0, -0.97),
                self.cv_axes.coords_to_point(1200, -0.97)
            ),
            num_dashes=60, color=RED
        )
        self.add(local_line)

        global_line = DashedVMobject(
            Line(
                self.cv_axes.coords_to_point(0, 1.03),
                self.cv_axes.coords_to_point(1200, 1.03)
            ),
            num_dashes=60, color=GREEN
        )
        self.add(global_line)

        # CV curve
        self.cv_curve = VMobject(color=ORANGE, stroke_width=2)
        self.add(self.cv_curve)

        # Temperature display (initially hidden, above plot)
        self.temp_display = VGroup()
        temp_label = Text(get_string("temperature") + ":", color=YELLOW).scale(0.5)
        self.temp_value = Text("300 K", color=YELLOW).scale(0.8)
        self.temp_display.add(temp_label, self.temp_value)
        self.temp_display.arrange(RIGHT, buff=0.3)  # Horizontal arrangement
        self.temp_display.move_to(cv_center + UP * 2.7)  # Above plot, near plot_label
        self.temp_display.set_opacity(0)  # Hidden initially
        self.add(self.temp_display)

    def create_potential_curve(self, func, color=BLUE, stroke_width=2):
        """Create a potential curve from a function"""
        x_vals = np.linspace(-2.0, 2.0, 200)
        points = []
        for x in x_vals:
            y = func(x)
            # Clamp y for visualization
            y = np.clip(y, -1.0, 4.0)
            screen_pos = self.pot_origin + RIGHT * (x * self.pot_x_scale) + UP * (y * self.pot_y_scale)
            points.append(screen_pos)

        curve = VMobject(color=color, stroke_width=stroke_width)
        curve.set_points_as_corners(points)
        return curve

    def calculate_force_magnitude(self, x, y):
        """Calculate total force magnitude at position (x, y)"""
        pos = np.array([x, y])

        # External force in x
        f_ext_x = self.current_force_x(x)

        # Y-confinement force
        f_y = -self.current_k_y * y

        # Wall forces
        wall_f = self.wall_force(pos)

        # Total force
        f_total = np.array([f_ext_x + wall_f[0], f_y + wall_f[1]])

        # Return magnitude
        return np.linalg.norm(f_total)

    def create_force_heatmap(self):
        """Create a heatmap showing force magnitude in the simulation box"""
        # Grid parameters - match wall boundaries exactly
        x_min, x_max = self.wall_x_min, self.wall_x_max
        y_min, y_max = self.wall_y_min, self.wall_y_max
        grid_res = 50  # Resolution

        # Calculate force magnitude at each grid point
        x_vals = np.linspace(x_min, x_max, grid_res)
        y_range = y_max - y_min
        x_range = x_max - x_min
        y_res = int(grid_res * y_range / x_range)  # Proportional to physical size
        y_vals = np.linspace(y_min, y_max, y_res)

        force_magnitudes = []
        for y in y_vals:
            for x in x_vals:
                f_mag = self.calculate_force_magnitude(x, y)
                force_magnitudes.append(f_mag)

        # Normalize forces for color mapping
        force_magnitudes = np.array(force_magnitudes)
        f_max = np.percentile(force_magnitudes, 95)  # Use 95th percentile to avoid outliers
        force_magnitudes = np.clip(force_magnitudes / f_max, 0, 1)

        # Create colored rectangles
        heatmap = VGroup()
        cell_width = (x_max - x_min) / grid_res * self.pot_x_scale
        cell_height = (y_max - y_min) / len(y_vals) * 0.3  # 2D view: same scale as particle Y-component

        idx = 0
        for j, y in enumerate(y_vals):
            for i, x in enumerate(x_vals):
                # Color from blue (low force) to red (high force)
                intensity = force_magnitudes[idx]
                color = interpolate_color(BLUE, RED, intensity)

                # Screen position (2D view)
                screen_x = x * self.pot_x_scale
                screen_y = y * 0.3  # Same Y-scaling as particle Y-component
                screen_pos = self.pot_origin + RIGHT * screen_x + UP * screen_y

                # Create small rectangle
                rect = Rectangle(
                    width=cell_width,
                    height=cell_height,
                    fill_color=color,
                    fill_opacity=0.15,  # Low opacity for debug view
                    stroke_width=0
                )
                rect.move_to(screen_pos)
                heatmap.add(rect)

                idx += 1

        return heatmap

    def update_force_heatmap(self):
        """Update the force heatmap to reflect current potential state"""
        # Fade out old heatmap
        old_heatmap = self.force_heatmap

        # Create new heatmap with current potential settings
        new_heatmap = self.create_force_heatmap()
        new_heatmap.set_z_index(-1)
        new_heatmap.set_opacity(0)  # Start invisible
        #self.add(new_heatmap)

        # Smooth transition: fade out old, fade in new
        #self.play(
        #    old_heatmap.animate.set_opacity(0),
        #    new_heatmap.animate.set_opacity(1),
        #    run_time=1.0
        #)

        # Remove old heatmap, keep new one
        #self.remove(old_heatmap)
        #self.force_heatmap = new_heatmap

    def harmonic_potential(self, x):
        """Harmonic potential V(x) = 0.5*k*(x-x0)²"""
        return 0.5 * self.harmonic_k * (x - self.harmonic_center)**2

    def harmonic_force_x(self, x):
        """Force from harmonic potential"""
        return -self.harmonic_k * (x - self.harmonic_center)

    def double_well_potential(self, x):
        """Double-well potential V(x) = a*(x²-b)² + c*x"""
        return self.pot_a * (x**2 - self.pot_b)**2 + self.pot_c * x

    def double_well_force_x(self, x):
        """Force from double-well potential in x direction"""
        return -(4 * self.pot_a * x * (x**2 - self.pot_b) + self.pot_c)

    def current_potential(self, x):
        """Current potential (interpolated between no/harmonic/double-well)"""
        if self.no_potential:
            return 0.0
        elif self.use_harmonic:
            # Interpolate between harmonic and double-well
            harm = self.harmonic_potential(x)
            dwell = self.double_well_potential(x)
            return (1 - self.morph_alpha) * harm + self.morph_alpha * dwell
        else:
            return self.double_well_potential(x)

    def current_force_x(self, x):
        """Current force (interpolated between no/harmonic/double-well)"""
        if self.no_potential:
            return 0.0
        elif self.use_harmonic:
            # Interpolate between harmonic and double-well forces
            harm_f = self.harmonic_force_x(x)
            dwell_f = self.double_well_force_x(x)
            return (1 - self.morph_alpha) * harm_f + self.morph_alpha * dwell_f
        else:
            return self.double_well_force_x(x)

    def wall_force(self, pos):
        """Calculate force from harmonic walls"""
        force = np.zeros(2)

        # X-walls: harmonic repulsion when outside boundaries
        if pos[0] < self.wall_x_min:
            force[0] = self.wall_k * (self.wall_x_min - pos[0])
        elif pos[0] > self.wall_x_max:
            force[0] = self.wall_k * (self.wall_x_max - pos[0])

        # Y-walls: harmonic repulsion when outside boundaries
        if pos[1] < self.wall_y_min:
            force[1] = self.wall_k * (self.wall_y_min - pos[1])
        elif pos[1] > self.wall_y_max:
            force[1] = self.wall_k * (self.wall_y_max - pos[1])

        return force

    def calculate_cv(self):
        """Calculate collective variable (mean x position)"""
        return np.mean(self.positions[:, 0])

    def bias_potential(self, x):
        """Calculate bias potential at position x"""
        bias = 0.0
        for center, height, width in self.gaussians:
            bias += height * np.exp(-((x - center)**2) / (2 * width**2))
        return bias

    def bias_force_x(self, x):
        """Calculate bias force at position x (numerical derivative)"""
        if not self.gaussians:
            return 0.0

        delta = 0.01
        return -(self.bias_potential(x + delta) - self.bias_potential(x - delta)) / (2 * delta)

    def berendsen_thermostat(self):
        """Apply Berendsen thermostat: velocity rescaling"""
        # Calculate current kinetic energy
        E_kin = 0.5 * self.mass * np.sum(self.velocities**2)

        # Calculate current temperature from equipartition theorem
        # E_kin = N_dof * 0.5 * k_B * T, where N_dof = 2 * N_particles (2D)
        N_dof = 2 * self.n_particles
        T_current = 2.0 * E_kin / (N_dof * self.k_B)

        # Avoid division by zero
        if T_current < 1e-6:
            T_current = self.temperature

        # Berendsen scaling factor
        # lambda = sqrt(1 + dt/tau * (T_target/T_current - 1))
        scaling = np.sqrt(1.0 + self.dt / self.tau_berendsen * (self.temperature / T_current - 1.0))

        # Scale all velocities
        self.velocities *= scaling

    def add_gaussian(self):
        """Add a Gaussian at current CV"""
        cv = self.calculate_cv()
        self.gaussians.append((cv, self.gaussian_height, self.gaussian_width))

        # Create visual representation as dashed curve
        def gaussian_func(x):
            return self.gaussian_height * np.exp(-((x - cv)**2) / (2 * self.gaussian_width**2))

        gaussian_curve = self.create_potential_curve(
            gaussian_func,
            color=GREY, stroke_width=1.5
        )

        # Make it dashed
        gaussian_curve = DashedVMobject(gaussian_curve, num_dashes=40)
        gaussian_curve.set_stroke(opacity=0.5)

        self.gaussian_curves.append(gaussian_curve)
        self.add(gaussian_curve)

        # Update bias and total potentials
        self.update_bias_potential()
        self.update_total_potential()

    def update_bias_potential(self):
        """Update bias potential curve"""
        if not self.gaussians:
            return

        bias_curve = self.create_potential_curve(
            lambda x: self.bias_potential(x),
            color=RED, stroke_width=2
        )
        self.bias_pot_curve.become(bias_curve)

    def update_total_potential(self):
        """Update total potential curve"""
        total_curve = self.create_potential_curve(
            lambda x: self.current_potential(x) + self.bias_potential(x),
            color=YELLOW, stroke_width=4
        )
        total_curve.set_stroke(opacity=0.7)
        self.total_pot_curve.become(total_curve)

    def md_step(self):
        """Perform one MD step with Velocity Verlet"""
        # Calculate forces
        forces = np.zeros((self.n_particles, 2))

        # External forces
        for i in range(self.n_particles):
            x = self.positions[i, 0]
            y = self.positions[i, 1]

            # Force in x from current potential
            forces[i, 0] = self.current_force_x(x)

            # Force in y (harmonic confinement)
            forces[i, 1] = -self.current_k_y * y

            # Bias force in x (if active)
            if self.metadynamics_active:
                forces[i, 0] += self.bias_force_x(x)

            # Harmonic wall forces
            wall_f = self.wall_force(self.positions[i])
            forces[i] += wall_f

        # LJ forces between particles
        for i in range(self.n_particles):
            for j in range(i + 1, self.n_particles):
                r_vec = self.positions[j] - self.positions[i]
                r = np.linalg.norm(r_vec)

                if r < self.cutoff_lj and r > 0.01:
                    r_hat = r_vec / r
                    sigma_r = self.sigma_lj / r
                    F_mag = 24.0 * self.epsilon_lj / r * (2.0 * sigma_r**12 - sigma_r**6)
                    f_lj = F_mag * r_hat

                    forces[i] += f_lj
                    forces[j] -= f_lj

        # Velocity Verlet: x(t+dt) = x(t) + v*dt + 0.5*a*dt²
        self.positions += self.velocities * self.dt + 0.5 * forces / self.mass * self.dt**2
        #print(self.positions)  # Debug: print positions after update
        #self.wait(0.1)  # Small wait to allow print output
        # Safety: Hard clamp if particles go WAY outside (emergency fallback only)
        # Harmonics walls should prevent this from ever happening
        #self.positions[:, 0] = np.clip(self.positions[:, 0], -4.0, 4.0)
        #self.positions[:, 1] = np.clip(self.positions[:, 1], -3.0, 3.0)

        # Calculate new forces
        forces_new = np.zeros((self.n_particles, 2))

        for i in range(self.n_particles):
            x = self.positions[i, 0]
            y = self.positions[i, 1]

            forces_new[i, 0] = self.current_force_x(x)
            forces_new[i, 1] = -self.current_k_y * y

            if self.metadynamics_active:
                forces_new[i, 0] += self.bias_force_x(x)

            # Harmonic wall forces
            wall_f = self.wall_force(self.positions[i])
            forces_new[i] += wall_f

        for i in range(self.n_particles):
            for j in range(i + 1, self.n_particles):
                r_vec = self.positions[j] - self.positions[i]
                r = np.linalg.norm(r_vec)

                if r < self.cutoff_lj and r > 0.01:
                    r_hat = r_vec / r
                    sigma_r = self.sigma_lj / r
                    F_mag = 24.0 * self.epsilon_lj / r * (2.0 * sigma_r**12 - sigma_r**6)
                    f_lj = F_mag * r_hat

                    forces_new[i] += f_lj
                    forces_new[j] -= f_lj

        # Velocity Verlet: v(t+dt) = v(t) + 0.5*[a(t) + a(t+dt)]*dt
        self.velocities += 0.5 * (forces + forces_new) / self.mass * self.dt

        # Apply Berendsen thermostat
        self.berendsen_thermostat()

        # Update state
        self.time += self.dt
        self.step += 1

        # Record CV
        cv = self.calculate_cv()
        self.time_history.append(self.time)
        self.cv_history.append(cv)

    def update_particle_positions(self):
        """Update particle visual positions"""
        for i in range(self.n_particles):
            x = self.positions[i, 0]
            y = self.positions[i, 1]

            # Position particles on the potential energy surface
            # y-coordinate of particle = potential energy at x position
            potential_energy = self.current_potential(x)

            # Clamp potential energy for visualization
            potential_energy = np.clip(potential_energy, -2.0, 5.0)

            # Screen position: x follows particle x, y follows potential energy + small offset from y-position
            screen_x = self.pot_origin + RIGHT * (x * self.pot_x_scale)
            screen_y = UP * (potential_energy * self.pot_y_scale + y * 0.3)  # y as small deviation

            screen_pos = screen_x + screen_y
            self.particle_dots[i].move_to(screen_pos)

            # Color based on x position
            if x < -0.5:
                self.particle_dots[i].set_color(BLUE)
            elif x > 0.5:
                self.particle_dots[i].set_color(GREEN)
            else:
                self.particle_dots[i].set_color(YELLOW)

    def update_cv_curve(self):
        """Update CV evolution curve"""
        if len(self.cv_history) < 2:
            return

        # Extend x-range if needed
        max_time = max(self.time_history)
        if max_time > self.cv_axes.x_range[1] - 50:
            self.cv_axes.x_range[1] = max_time + 100

        # Create curve
        points = []
        for t, cv in zip(self.time_history, self.cv_history):
            if self.cv_axes.x_range[0] <= t <= self.cv_axes.x_range[1]:
                if -1.5 <= cv <= 1.5:  # Within plot range
                    points.append(self.cv_axes.coords_to_point(t, cv))

        if len(points) > 1:
            new_curve = VMobject(color=ORANGE, stroke_width=2)
            new_curve.set_points_as_corners(points)
            self.cv_curve.become(new_curve)

    def run_phase_0(self):
        """Phase 0: Free movement - no external potential, only walls"""
        phase_text = Text(get_string("phase0_title"), color=BLUE).scale(0.4)
        phase_text.move_to(self.box_center + UP * 2.7)
        self.play(Transform(self.box_label, phase_text), run_time=1.5)

        # No external potential in x
        self.no_potential = True
        self.current_k_y = 0.0  # No y-confinement (completely free movement)

        # Update heatmap to show only wall forces
        #self.update_force_heatmap()

        # Run for configured number of steps to see free movement
        for _ in range(self.phase0_steps):
            self.md_step()

            if self.step % 3 == 0:
                self.update_particle_positions()
                self.update_cv_curve()
                self.wait(0.01)

    def run_phase_1(self):
        """Phase 1: Activate y-confinement - particles collapse to y=0"""
        phase_text = Text(get_string("phase1_title"), color=GREEN).scale(0.4)
        phase_text.move_to(self.box_center + UP * 2.7)
        self.play(Transform(self.box_label, phase_text), run_time=1.5)

        # Still no x-potential, but increase y-confinement
        self.no_potential = True

        # Gradually increase y-confinement over configured steps
        for i in range(self.phase1_steps):
            # Linearly interpolate k_y from weak to strong
            alpha = i / self.phase1_steps
            self.current_k_y = (1 - alpha) * self.k_y_weak + alpha * self.k_y_strong

            self.md_step()

            if self.step % 2 == 0:
                self.update_particle_positions()
                self.update_cv_curve()
                self.wait(0.008)

    def run_phase_2(self):
        """Phase 2: MD in harmonic potential well"""
        phase_text = Text(get_string("phase2_title"), color=PURPLE).scale(0.4)
        phase_text.move_to(self.box_center + UP * 2.7)
        self.play(Transform(self.box_label, phase_text), run_time=1.5)

        # Activate harmonic potential in x
        self.no_potential = False
        self.use_harmonic = True
        self.morph_alpha = 0.0
        self.current_k_y = self.k_y_strong  # Keep strong y-confinement

        # Update heatmap to show harmonic potential
        #self.update_force_heatmap()

        # Update total potential curve to show harmonic well
        self.update_total_potential()

        # Run for configured number of steps to see oscillations
        for _ in range(self.phase2_steps):
            self.md_step()

            if self.step % 3 == 0:
                self.update_particle_positions()
                self.update_cv_curve()
                self.wait(0.01)

    def morph_to_double_well(self):
        """Smoothly morph from harmonic to double-well potential"""
        phase_text = Text(get_string("phase2_transition"), color=ORANGE).scale(0.4)
        phase_text.move_to(self.box_center + UP * 2.7)
        self.play(Transform(self.box_label, phase_text), run_time=1.5)

        # Morph over configured steps for smoother transition
        for i in range(self.morph_steps):
            # Update morph parameter
            self.morph_alpha = i / self.morph_steps

            # Update potential curve visualization
            new_curve = self.create_potential_curve(
                lambda x: self.current_potential(x),
                color=BLUE, stroke_width=3
            )
            self.external_pot_curve.become(new_curve)

            # Update total potential curve
            self.update_total_potential()

            # Continue MD simulation during morph
            self.md_step()

            if self.step % 2 == 0:
                self.update_particle_positions()
                self.update_cv_curve()
                self.wait(0.008)

        # After morphing, switch to pure double-well
        self.use_harmonic = False
        self.morph_alpha = 1.0

        # Update heatmap to show double-well
        #self.update_force_heatmap()

    def run_phase_3(self):
        """Phase 3: Naive MD in double-well"""
        phase_text = Text(get_string("phase3_title"), color=RED).scale(0.4)
        phase_text.move_to(self.box_center + UP * 2.7)
        self.play(Transform(self.box_label, phase_text), run_time=1.5)

        # Run for configured number of steps to clearly show particles are trapped
        for _ in range(self.phase3_steps):
            self.md_step()

            if self.step % 3 == 0:
                self.update_particle_positions()
                self.update_cv_curve()
                self.wait(0.01)

    def run_phase_3b(self):
        """Phase 3b: High temperature MD - thermal crossing attempt"""
        phase_text = Text(get_string("phase3b_title"), color=ORANGE).scale(0.4)
        phase_text.move_to(self.box_center + UP * 2.7)
        self.play(Transform(self.box_label, phase_text), run_time=1.5)

        # Show temperature display (CV curve stays visible)
        self.play(
            self.temp_display.animate.set_opacity(1),
            run_time=0.5
        )

        # Ramp up temperature
        for i in range(self.temp_ramp_steps):
            # Linear temperature increase
            alpha = i / self.temp_ramp_steps
            self.temperature = self.temp_initial + alpha * (self.temp_target - self.temp_initial)

            # Update temperature display
            new_temp_text = Text(f"{int(self.temperature)} K", color=YELLOW).scale(0.8)
            new_temp_text.move_to(self.temp_value.get_center())
            self.temp_value.become(new_temp_text)

            self.md_step()

            if self.step % 3 == 0:
                self.update_particle_positions()
                self.update_cv_curve()
                self.wait(0.008)

        # Equilibration at high temperature
        for _ in range(self.temp_equilibration_steps):
            self.md_step()

            if self.step % 3 == 0:
                self.update_particle_positions()
                self.update_cv_curve()
                self.wait(0.008)

        # Ramp down temperature back to normal
        for i in range(self.temp_ramp_steps):
            alpha = i / self.temp_ramp_steps
            self.temperature = self.temp_target - alpha * (self.temp_target - self.temp_initial)

            # Update temperature display
            new_temp_text = Text(f"{int(self.temperature)} K", color=YELLOW).scale(0.8)
            new_temp_text.move_to(self.temp_value.get_center())
            self.temp_value.become(new_temp_text)

            self.md_step()

            if self.step % 3 == 0:
                self.update_particle_positions()
                self.update_cv_curve()
                self.wait(0.008)

        # Hide temperature display (CV curve stays visible)
        self.play(
            self.temp_display.animate.set_opacity(0),
            run_time=0.5
        )

        # Reset particles to local minimum for fair comparison with metadynamics
        self.positions[:, 0] = np.random.uniform(-1.1, -0.85, self.n_particles)  # Around x ≈ -0.97
        self.positions[:, 1] = np.random.uniform(-0.2, 0.2, self.n_particles)  # Small y spread

        # Thermalize velocities at 300K
        sigma_v = np.sqrt(self.k_B * self.temperature / self.mass)
        self.velocities = np.random.normal(0, sigma_v, size=(self.n_particles, 2))

        # Update visual to show reset
        self.update_particle_positions()
        self.wait(0.5)

    def run_phase_4(self):
        """Phase 4: Metadynamics"""
        phase_text = Text(get_string("phase4_title"), color=ORANGE).scale(0.4)
        phase_text.move_to(self.box_center + UP * 2.7)
        self.play(Transform(self.box_label, phase_text), run_time=1.5)

        # Activate metadynamics
        self.metadynamics_active = True

        # Run for configured number of steps for full metadynamics exploration
        for i in range(self.phase4_steps):
            # Add Gaussian periodically
            if i % self.gaussian_frequency == 0:
                self.add_gaussian()

            self.md_step()

            if self.step % 3 == 0:
                self.update_particle_positions()
                self.update_cv_curve()
                self.wait(0.008)


if __name__ == "__main__":
    # Run with: manimgl metadynamics_visualization.py MetadynamicsVisualization
    pass
