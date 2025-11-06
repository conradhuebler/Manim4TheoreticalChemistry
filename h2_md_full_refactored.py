from manimlib import *
import numpy as np
import os

# Ensure directories exist
os.makedirs("./videos", exist_ok=True)
os.makedirs("./images", exist_ok=True)

# Multilingual support
LANGUAGE = "EN"  # Set to "EN" for English or "DE" for German

STRINGS = {
    "DE": {
        "title": "H₂ Molekülbildung: Von freien Atomen zur Born-Oppenheimer-Näherung",
        "phase1": "Phase 1: Freie H-Atome in einer Box",
        "phase2": "Phase 2: Zwei H-Atome mit Wechselwirkung",
        "phase3": "Phase 3: Born-Oppenheimer-Näherung",
        "phase4": "Phase 4: H₂-Molekül Formation",
        "phase5": "Phase 5: H₂-Dissociation",
        "energy_title": "Energie (eV)",
        "distance_title": "Atomabstand (Å)",
        "time_title": "Zeit (fs)",
        "temperature": "T = 300 K",
        "box_confinement": "Box-Begrenzung",
        "electron_cloud": "Elektronenwolke",
        "nuclear_motion": "Kernbewegung",
        "bo_explanation": "Elektronen folgen Kernen adiabatisch",
        "morse_potential": "Morse-Potential",
        "harmonic_walls": "Harmonische Wände",
        "h1_energy": "H₁ Energie",
        "h2_energy": "H₂ Energie",
        "interaction": "Wechselwirkung",
        "harmonic_approx": "Harmonische Näherung",
        "bo_title": "Born-Oppenheimer-Näherung:",
        "bo_slow_nuclei": "• Kerne bewegen sich langsam",
        "bo_adiabatic": "• Elektronen folgen adiabatisch",
        "bo_separation": "• Separation der Bewegung",
        "harmonic_title": "Harmonische Näherung:",
        "harmonic_small_osc": "• Kleine Schwingungen um r_e",
        "harmonic_formula": "• V ≈ -D_e + ½k(r-r_e)²",
        "harmonic_compare": "• Vergleich mit Morse-Potential",
        "simulation_time": "Simulationszeit",
        "bond_length": "H₂-Bindungslänge",
        "unit_fs": "fs",
        "unit_angstrom": "Å"
    },
    "EN": {
        "title": "H₂ Molecule Formation: From Free Atoms to Born-Oppenheimer Approximation",
        "phase1": "Phase 1: Free H-Atoms in a Box",
        "phase2": "Phase 2: Two H-Atoms with Interaction",
        "phase3": "Phase 3: Born-Oppenheimer Approximation",
        "phase4": "Phase 4: H₂ Molecule Formation",
        "phase5": "Phase 5: H₂ Dissociation",
        "energy_title": "Energy (eV)",
        "distance_title": "Atomic Distance (Å)",
        "time_title": "Time (fs)",
        "temperature": "T = 300 K",
        "box_confinement": "Box Confinement",
        "electron_cloud": "Electron Cloud",
        "nuclear_motion": "Nuclear Motion",
        "bo_explanation": "Electrons follow nuclei adiabatically",
        "morse_potential": "Morse Potential",
        "harmonic_walls": "Harmonic Walls",
        "h1_energy": "H₁ Energy",
        "h2_energy": "H₂ Energy",
        "interaction": "Interaction",
        "harmonic_approx": "Harmonic Approximation",
        "bo_title": "Born-Oppenheimer Approximation:",
        "bo_slow_nuclei": "• Nuclei move slowly vs electrons",
        "bo_adiabatic": "• Electrons follow adiabatically",
        "bo_separation": "• Separation of motion",
        "harmonic_title": "Harmonic Approximation:",
        "harmonic_small_osc": "• Small oscillations around r_e",
        "harmonic_formula": "• V ≈ -D_e + ½k(r-r_e)²",
        "harmonic_compare": "• Comparison with Morse potential",
        "simulation_time": "Simulation time",
        "bond_length": "H₂ bond length",
        "unit_fs": "fs",
        "unit_angstrom": "Å"
    }
}

def get_string(key):
    return STRINGS[LANGUAGE][key]

class H2MDFull(Scene):
    """H₂ molecule formation: Free atoms → Born-Oppenheimer → Formation → Dissociation.

    GUI-compatible PARAMETERS structure for MD simulation of H₂ molecule.
    """

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # ========================================================================
        # PHYSICAL CONSTANTS
        # ========================================================================
        "k_B": {
            "value": 8.617e-5,
            "type": float,
            "unit": "eV/K",
            "description": "Boltzmann constant",
            "min": 1e-6,
            "max": 1e-3
        },
        "T": {
            "value": 1500,
            "type": int,
            "unit": "K",
            "description": "Temperature for initial kinetic energy",
            "min": 100,
            "max": 5000
        },
        "dt": {
            "value": 0.5,
            "type": float,
            "unit": "fs",
            "description": "MD integration timestep (femtoseconds)",
            "min": 0.01,
            "max": 2.0
        },

        # ========================================================================
        # BOX PARAMETERS
        # ========================================================================
        "box_size": {
            "value": 4.0,
            "type": float,
            "unit": "Å",
            "description": "Simulation box half-width (harmonic walls)",
            "min": 2.0,
            "max": 10.0
        },
        "box_k": {
            "value": 5.0,
            "type": float,
            "unit": "eV/Å²",
            "description": "Harmonic wall force constant",
            "min": 0.1,
            "max": 50.0
        },

        # ========================================================================
        # ATOM PARAMETERS
        # ========================================================================
        "mass": {
            "value": 1.0,
            "type": float,
            "unit": "amu",
            "description": "H-atom mass (simplified units)",
            "min": 0.5,
            "max": 2.0
        },

        # ========================================================================
        # LENNARD-JONES PARAMETERS (Phase 2)
        # ========================================================================
        "epsilon": {
            "value": 0.1,
            "type": float,
            "unit": "eV",
            "description": "LJ potential well depth for H-H interaction",
            "min": 0.01,
            "max": 1.0
        },
        "sigma": {
            "value": 1.5,
            "type": float,
            "unit": "Å",
            "description": "LJ zero-crossing distance",
            "min": 0.5,
            "max": 3.0
        },

        # ========================================================================
        # H₂ MORSE POTENTIAL PARAMETERS (Phases 4-5)
        # ========================================================================
        "D_e": {
            "value": 4.478,
            "type": float,
            "unit": "eV",
            "description": "Morse potential well depth (H₂ dissociation energy)",
            "min": 1.0,
            "max": 10.0
        },
        "r_e": {
            "value": 0.741,
            "type": float,
            "unit": "Å",
            "description": "H₂ equilibrium bond length",
            "min": 0.5,
            "max": 1.5
        },
        "alpha": {
            "value": 1.5,
            "type": float,
            "unit": "Å⁻¹",
            "description": "Morse potential width parameter",
            "min": 0.5,
            "max": 5.0
        },

        # ========================================================================
        # VISUALIZATION PARAMETERS
        # ========================================================================
        "plot_time_window": {
            "value": 500.0,
            "type": float,
            "unit": "fs",
            "description": "Time window displayed in plots (sliding window)",
            "min": 100.0,
            "max": 2000.0
        },
        "min_points_for_snake": {
            "value": 10,
            "type": int,
            "unit": "points",
            "description": "Minimum data points before enabling sliding window",
            "min": 5,
            "max": 50
        },
        "disable_sliding_window": {
            "value": False,
            "type": bool,
            "unit": "-",
            "description": "Disable sliding window for didactic purposes (show full history)",
            "min": None,
            "max": None
        },

        # ========================================================================
        # PHASE DURATION PARAMETERS
        # ========================================================================
        "phase1_steps": {
            "value": 200,
            "type": int,
            "unit": "steps",
            "description": "Phase 1 duration: Free H-atoms in box",
            "min": 50,
            "max": 1000
        },
        "phase1_wait": {
            "value": 0.004,
            "type": float,
            "unit": "s",
            "description": "Phase 1 animation frame wait time",
            "min": 0.001,
            "max": 0.1
        },
        "phase2_steps": {
            "value": 800,
            "type": int,
            "unit": "steps",
            "description": "Phase 2 duration: Two H-atoms with interaction",
            "min": 200,
            "max": 2000
        },
        "phase2_wait": {
            "value": 0.001,
            "type": float,
            "unit": "s",
            "description": "Phase 2 animation frame wait time",
            "min": 0.0001,
            "max": 0.01
        },
        "phase4_steps": {
            "value": 200,
            "type": int,
            "unit": "steps",
            "description": "Phase 4 duration: H₂ formation (per loop)",
            "min": 50,
            "max": 1000
        },
        "phase4_wait": {
            "value": 0.02,
            "type": float,
            "unit": "s",
            "description": "Phase 4 animation frame wait time",
            "min": 0.001,
            "max": 0.1
        },
        "phase5_steps": {
            "value": 200,
            "type": int,
            "unit": "steps",
            "description": "Phase 5 duration: H₂ dissociation",
            "min": 50,
            "max": 1000
        },
        "phase5_wait": {
            "value": 0.005,
            "type": float,
            "unit": "s",
            "description": "Phase 5 animation frame wait time",
            "min": 0.001,
            "max": 0.05
        }
    }

    def construct(self):
        # Initialize parameters
        self.setup_parameters()

        # Setup 4-quadrant layout
        self.setup_layout()

        # Run animation phases
        self.phase_1_free_atoms()
        self.phase_2_two_atoms()
        self.phase_3_born_oppenheimer()
        self.phase_4_h2_formation()
        self.phase_5_dissociation()

        self.wait(3)

    def setup_parameters(self):
        """Extract parameters from central PARAMETERS dictionary"""
        # Physical constants
        self.k_B = self.PARAMETERS["k_B"]["value"]
        self.T = self.PARAMETERS["T"]["value"]
        self.dt = self.PARAMETERS["dt"]["value"]

        # Box parameters
        self.box_size = self.PARAMETERS["box_size"]["value"]
        self.box_k = self.PARAMETERS["box_k"]["value"]

        # H-atom parameters
        self.mass = self.PARAMETERS["mass"]["value"]

        # Lennard-Jones parameters (for Phase 2)
        self.epsilon = self.PARAMETERS["epsilon"]["value"]
        self.sigma = self.PARAMETERS["sigma"]["value"]

        # H2 Morse potential parameters (for later phases)
        self.D_e = self.PARAMETERS["D_e"]["value"]
        self.r_e = self.PARAMETERS["r_e"]["value"]
        self.alpha = self.PARAMETERS["alpha"]["value"]

        # Visualization parameters
        self.plot_time_window = self.PARAMETERS["plot_time_window"]["value"]
        self.min_points_for_snake = self.PARAMETERS["min_points_for_snake"]["value"]
        self.disable_sliding_window = self.PARAMETERS["disable_sliding_window"]["value"]

        # Phase duration parameters
        self.phase1_steps = self.PARAMETERS["phase1_steps"]["value"]
        self.phase1_wait = self.PARAMETERS["phase1_wait"]["value"]
        self.phase2_steps = self.PARAMETERS["phase2_steps"]["value"]
        self.phase2_wait = self.PARAMETERS["phase2_wait"]["value"]
        self.phase4_steps = self.PARAMETERS["phase4_steps"]["value"]
        self.phase4_wait = self.PARAMETERS["phase4_wait"]["value"]
        self.phase5_steps = self.PARAMETERS["phase5_steps"]["value"]
        self.phase5_wait = self.PARAMETERS["phase5_wait"]["value"]

        # Initialize single H-atom (initial conditions, not parameters)
        self.h1_pos = np.array([0.0, 0.0])  # x, y position
        self.h1_vel = np.array([0.02, 0.015])  # x, y velocity
        self.h1_electron_phase = 0.0

        # Second H-atom (starts off-screen)
        self.h2_pos = np.array([6.0, 2.0])  # Initially outside
        self.h2_vel = np.array([-0.01, -0.01])
        self.h2_electron_phase = np.pi  # π phase difference

        # Tracking data (internal state, not parameters)
        self.time_data = []
        self.h1_energy_data = []
        self.h2_energy_data = []
        self.distance_data = []
        self.interaction_energy_data = []
        self.current_time = 0.0

        # Animation phase control (internal state)
        self.current_phase = 1
        self.phase_timer = 0

    def box_potential(self, pos):
        """Harmonic confinement potential at box walls"""
        energy = 0.0
        for coord in pos:
            if abs(coord) > self.box_size:
                excess = abs(coord) - self.box_size
                energy += 0.5 * self.box_k * excess**2
        return energy

    def box_force(self, pos):
        """Force from box confinement (negative gradient)"""
        force = np.zeros_like(pos)
        for i, coord in enumerate(pos):
            if coord > self.box_size:
                force[i] = -self.box_k * (coord - self.box_size)
            elif coord < -self.box_size:
                force[i] = -self.box_k * (coord + self.box_size)
        return force

    def lennard_jones_potential(self, r):
        """Lennard-Jones potential: V(r) = 4ε[(σ/r)¹² - (σ/r)⁶]"""
        if r < 0.1:  # Avoid singularity
            return 100.0

        sigma_r = self.sigma / r
        sigma_r6 = sigma_r**6
        sigma_r12 = sigma_r6**2

        return 4.0 * self.epsilon * (sigma_r12 - sigma_r6)

    def lennard_jones_force(self, r_vec):
        """Lennard-Jones force: F = 24ε/r [2(σ/r)¹² - (σ/r)⁶] * r̂"""
        r = np.linalg.norm(r_vec)
        if r < 0.1:  # Avoid singularity
            return np.zeros_like(r_vec)

        r_hat = r_vec / r
        sigma_r = self.sigma / r
        sigma_r6 = sigma_r**6
        sigma_r12 = sigma_r6**2

        # Force magnitude: F = 24ε/r [2(σ/r)¹² - (σ/r)⁶]
        F_mag = 24.0 * self.epsilon / r * (2.0 * sigma_r12 - sigma_r6)

        return F_mag * r_hat


    def h2_interaction_force(self, r_vec):
        """Force between H-atoms"""
        r = np.linalg.norm(r_vec)
        if r < 0.1:
            return np.zeros_like(r_vec)

        r_hat = r_vec / r

        if r < 1.0:
            F_mag = 10.0 / r**2  # Repulsive force magnitude
        elif r < 5.0:
            F_mag = -1.0 / r**2  # Attractive force magnitude
        else:
            F_mag = 0.0

        return F_mag * r_hat

    def morse_potential(self, r):
        """Morse potential for H2 (used in final phase)"""
        arg = -self.alpha * (r - self.r_e)
        if abs(arg) > 20:
            return 0.0 if arg < 0 else -self.D_e
        exp_term = np.exp(arg)
        return self.D_e * (1 - exp_term)**2 - self.D_e

    def harmonic_potential(self, r):
        """Harmonic approximation to Morse potential"""
        # Taylor expansion around equilibrium: V ≈ V0 + (1/2)k(r-re)²
        k = 2 * self.D_e * self.alpha**2  # Second derivative of Morse at r_e
        return -self.D_e + 0.5 * k * (r - self.r_e)**2

    def get_snake_time_range(self):
        """Get time range for snake-style sliding window"""
        if self.disable_sliding_window or len(self.time_data) < self.min_points_for_snake:
            # Show from start until now (full history)
            return (0, max(500.0, self.current_time))  # Extend to 500 fs
        else:
            # Sliding window: show last 200 fs
            time_end = self.current_time
            time_start = max(0, time_end - 200.0)  # Keep 200 fs window
            return (time_start, time_end)

    def md_step_single_atom(self, pos, vel, forces_func):
        """Single MD step for one atom using Velocity Verlet"""
        # Current forces
        F_current = forces_func(pos)

        # Update position
        pos_new = pos + vel * self.dt + 0.5 * F_current / self.mass * self.dt**2

        # Calculate forces at new position
        F_new = forces_func(pos_new)

        # Update velocity
        vel_new = vel + 0.5 * (F_current + F_new) / self.mass * self.dt

        # Clamp velocities for stability
        vel_new = np.clip(vel_new, -0.2, 0.2)

        return pos_new, vel_new

    def setup_layout(self):
        """Setup 4-quadrant layout"""
        # Title
        title = Text(get_string("title"), font_size=20)
        title.to_edge(UP, buff=0.15)
        self.play(Write(title))

        # Define areas - flexible layout for plot transitions
        self.mol_area_center = LEFT * 3.5
        # 2-plot layout for phases 1-3
        self.energy_plot_center = RIGHT * 3.5 + UP * 1.5
        self.distance_plot_center = RIGHT * 3.5 + DOWN * 1.5
        # 1-plot layout for phase 4
        self.potential_plot_center = RIGHT * 3.5 + UP * 0.0

        # Create simulation box visualization
        self.setup_simulation_box()

        # Setup initial plots (only time plots for phases 1-3)
        self.setup_energy_plot()
        self.setup_distance_plot()

    def setup_simulation_box(self):
        """Setup the MD simulation box visualization"""
        # Box boundary
        box_width = 4.0  # Visual representation
        box_height = 4.0

        self.sim_box = Rectangle(
            width=box_width, height=box_height,
            stroke_color=WHITE, stroke_width=2, fill_opacity=0.1
        )
        self.sim_box.move_to(self.mol_area_center)

        # Box label
        box_label = Text(get_string("phase1"), font_size=16, color=YELLOW)
        box_label.move_to(self.mol_area_center + UP * 2.5)

        self.current_phase_label = box_label

        self.play(ShowCreation(self.sim_box), Write(box_label))

        # Create H-atoms
        self.create_h_atoms()

    def create_h_atoms(self):
        """Create H-atom visualizations"""
        # First H-atom
        self.h1_nucleus = Circle(radius=0.12, color=RED, fill_opacity=0.8)
        self.h1_label = Text("H", font_size=14, color=WHITE)
        self.h1_electron = Dot(radius=0.03, color=BLUE)
        self.h1_orbit = Circle(radius=0.25, color=BLUE, stroke_opacity=0.3, stroke_width=1)

        # Position first atom
        screen_pos1 = self.mol_area_center + RIGHT * self.h1_pos[0] * 0.4 + UP * self.h1_pos[1] * 0.4
        self.h1_nucleus.move_to(screen_pos1)
        self.h1_label.move_to(screen_pos1)
        self.h1_orbit.move_to(screen_pos1)

        self.h1_group = VGroup(self.h1_nucleus, self.h1_label, self.h1_electron, self.h1_orbit)

        # Second H-atom (initially hidden)
        self.h2_nucleus = Circle(radius=0.12, color=RED, fill_opacity=0.8)
        self.h2_label = Text("H", font_size=14, color=WHITE)
        self.h2_electron = Dot(radius=0.03, color=BLUE)
        self.h2_orbit = Circle(radius=0.25, color=BLUE, stroke_opacity=0.3, stroke_width=1)

        self.h2_group = VGroup(self.h2_nucleus, self.h2_label, self.h2_electron, self.h2_orbit)

        # Show first atom
        self.play(ShowCreation(self.h1_group))

    def setup_energy_plot(self):
        """Setup energy vs time plot"""
        self.energy_axes = Axes(
            x_range=(0, self.plot_time_window, 50),
            y_range=(-0.005, 0, 0.001),
            height=2.5,  # Larger for 2-plot layout
            width=3.2,
            axis_config={
                "stroke_color": GREY,
                "stroke_width": 1,
                "include_tip": True,
            }
        )
        self.energy_axes.move_to(self.energy_plot_center)

        # Labels
        energy_x_label = Text(get_string("time_title"), font_size=14)
        energy_x_label.next_to(self.energy_axes, DOWN, buff=0.1)
        energy_y_label = Text(get_string("energy_title"), font_size=14)
        energy_y_label.next_to(self.energy_axes, LEFT, buff=0.1)

        # Legend
        energy_legend = VGroup(
            #Text(get_string("h1_energy"), font_size=12, color=GREEN),
            #Text(get_string("h2_energy"), font_size=12, color=ORANGE),
            Text(get_string("interaction"), font_size=12, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        energy_legend.move_to(self.energy_plot_center + UP * 1.0)

        self.play(
            ShowCreation(self.energy_axes),
            Write(energy_x_label), Write(energy_y_label),
            Write(energy_legend)
        )

        # Initialize curves
        self.h1_energy_curve = VMobject(color=GREEN)
        self.h2_energy_curve = VMobject(color=ORANGE)
        self.interaction_curve = VMobject(color=PURPLE)

        self.add(self.h1_energy_curve, self.h2_energy_curve, self.interaction_curve)

        # Store all energy plot elements as a group
        self.energy_plot_group = VGroup(
            self.energy_axes, energy_x_label, energy_y_label, energy_legend,
            self.h1_energy_curve, self.h2_energy_curve, self.interaction_curve
        )

    def setup_distance_plot(self):
        """Setup distance vs time plot with appropriate time range"""
        # Increase the time range to accommodate the full simulation
        self.distance_axes = Axes(
            x_range=(0, self.plot_time_window, 50),  # Extend to 500 fs
            y_range=(0, 10, 2),
            height=2.5,  # Larger for 2-plot layout
            width=3.2,
            axis_config={
                "stroke_color": GREY,
                "stroke_width": 1,
                "include_tip": True,
            }
        )
        self.distance_axes.move_to(self.distance_plot_center)

        # Labels
        dist_x_label = Text(get_string("time_title"), font_size=14)
        dist_x_label.next_to(self.distance_axes, DOWN, buff=0.1)
        dist_y_label = Text(get_string("distance_title"), font_size=14)
        dist_y_label.next_to(self.distance_axes, LEFT, buff=0.1)

        self.play(
            ShowCreation(self.distance_axes),
            Write(dist_x_label), Write(dist_y_label)
        )

        # Initialize distance curve
        self.distance_curve = VMobject(color=YELLOW)
        self.add(self.distance_curve)

        # Store all distance plot elements as a group
        self.distance_plot_group = VGroup(
            self.distance_axes, dist_x_label, dist_y_label, self.distance_curve
        )

    def setup_potential_plot(self):
        """Setup potential plot elements (called only when needed)"""
        # Create axes
        self.potential_axes = Axes(
            x_range=(0, 2.0, 0.5),  # Start from 0, wider range
            y_range=(-5, 10, 2),    # Include repulsive region
            height=4.0,  # Full height for single plot
            width=3.2,
            axis_config={
                "stroke_color": GREY,
                "stroke_width": 1,
                "include_tip": True,
            }
        )
        self.potential_axes.move_to(self.potential_plot_center)

        # Labels
        self.pot_x_label = Text(get_string("distance_title"), font_size=14)
        self.pot_x_label.next_to(self.potential_axes, DOWN, buff=0.1)
        self.pot_y_label = Text(get_string("energy_title"), font_size=14)
        self.pot_y_label.next_to(self.potential_axes, LEFT, buff=0.1)

        # Create Morse potential curve (full range from 0)
        r_values = np.linspace(0.1, 2.0, 500)  # Increased resolution to 500
        morse_values = [self.morse_potential_full_range(r) for r in r_values]
        morse_points = [self.potential_axes.coords_to_point(r, min(max(v, -5), 10))
                       for r, v in zip(r_values, morse_values)]

        self.morse_curve = VMobject(color=BLUE)
        self.morse_curve.set_points_as_corners(morse_points)

        # Create harmonic approximation curve
        harmonic_values = [self.harmonic_potential(r) for r in r_values]
        harmonic_points = [self.potential_axes.coords_to_point(r, min(max(v, -5), 10))
                          for r, v in zip(r_values, harmonic_values)]

        self.harmonic_curve = VMobject(color=ORANGE, stroke_opacity=0)
        self.harmonic_curve.set_points_as_corners(harmonic_points)

        # Legend for potential curves
        self.potential_legend = VGroup(
            Text(get_string("morse_potential"), font_size=12, color=BLUE),
            Text(get_string("harmonic_approx"), font_size=12, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        self.potential_legend.move_to(self.potential_plot_center + UP * 1.5 + LEFT * 1.0)

        # Current position dot on potential curve
        self.potential_dot = Dot(radius=0.12, color=RED, fill_opacity=1.0)
        self.potential_dot.set_stroke(color=WHITE, width=2)  # White outline

        # Real-time value displays
        self.energy_display = Text("E = 0.0 eV", font_size=14, color=YELLOW)
        self.distance_display = Text("r = 0.0 Å", font_size=14, color=YELLOW)
        self.value_displays = VGroup(self.distance_display, self.energy_display)
        self.value_displays.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        self.value_displays.move_to(self.potential_plot_center + RIGHT * 2.5)

        # Add elements to scene
        self.add(self.potential_axes, self.pot_x_label, self.pot_y_label,
                 self.morse_curve, self.harmonic_curve, self.potential_legend, self.potential_dot, self.value_displays)

        # Store all potential plot elements as a group
        self.potential_plot_group = VGroup(
            self.potential_axes, self.pot_x_label, self.pot_y_label,
            self.morse_curve, self.harmonic_curve, self.potential_legend, self.potential_dot, self.value_displays
        )

    def morse_potential_full_range(self, r):
        """Morse potential including repulsive region at small r"""
        arg = -self.alpha * (r - self.r_e)
        if abs(arg) > 20:
            return 0.0 if arg < 0 else -self.D_e
        exp_term = np.exp(arg)
        return self.D_e * (1 - exp_term)**2 - self.D_e

    def update_plots(self):
        """Update all plots with snake-style sliding window"""
        if len(self.time_data) < 2:
            return

        # Get current time window for snake behavior
        time_start, time_end = self.get_snake_time_range()

        # Filter data to current time window
        times = np.array(self.time_data)
        mask = (times >= time_start) & (times <= time_end)

        if not np.any(mask):
            return

        display_times = times[mask]

        # Update energy plot
        if len(display_times) > 1:
            # H1 energy
            h1_energies = np.array(self.h1_energy_data)[mask]
            # Map times to plot coordinates (0 to plot_time_window)
            plot_times = display_times - time_start
            h1_points = [self.energy_axes.coords_to_point(t, min(max(e, -0.06), 0.15))
                        for t, e in zip(plot_times, h1_energies)]

            # H2 energy (if available)
            if len(self.h2_energy_data) > 0:
                h2_energies = np.array(self.h2_energy_data)[mask]
                h2_points = [self.energy_axes.coords_to_point(t, min(max(e, -0.06), 0.15))
                            for t, e in zip(plot_times, h2_energies)]

            # Interaction energy
            if len(self.interaction_energy_data) > 0:
                interaction_energies = np.array(self.interaction_energy_data)[mask]
                int_points = [self.energy_axes.coords_to_point(t, min(max(e, -0.06), 0.15))
                             for t, e in zip(plot_times, interaction_energies)]
                if len(int_points) > 1:
                    new_int_curve = VMobject(color=PURPLE)
                    new_int_curve.set_points_as_corners(int_points)
                    self.interaction_curve.become(new_int_curve)

        # Update distance plot
        if len(self.distance_data) > 0 and len(display_times) > 1:
            distances = np.array(self.distance_data)[mask]
            plot_times = display_times - time_start
            distance_points = [self.distance_axes.coords_to_point(t, d)
                              for t, d in zip(plot_times, distances)]
            if len(distance_points) > 1:
                new_distance_curve = VMobject(color=YELLOW)
                new_distance_curve.set_points_as_corners(distance_points)
                self.distance_curve.become(new_distance_curve)

        # Update potential plot dot position
        if hasattr(self, 'potential_dot') and len(self.distance_data) > 0:
            current_r = self.distance_data[-1]  # Most recent distance
            current_potential = self.morse_potential(current_r)
            if 0.4 <= current_r <= 2.0:  # Within plot range
                dot_pos = self.potential_axes.coords_to_point(current_r, min(max(current_potential, -5), 2))
                self.potential_dot.move_to(dot_pos)

    def update_h_atom_visualization(self, atom_idx):
        """Update H-atom visualization"""
        if atom_idx == 1:
            pos = self.h1_pos
            nucleus = self.h1_nucleus
            label = self.h1_label
            electron = self.h1_electron
            orbit = self.h1_orbit
            phase = self.h1_electron_phase
        else:
            pos = self.h2_pos
            nucleus = self.h2_nucleus
            label = self.h2_label
            electron = self.h2_electron
            orbit = self.h2_orbit
            phase = self.h2_electron_phase

        # Convert simulation coordinates to screen coordinates
        screen_pos = self.mol_area_center + RIGHT * pos[0] * 0.4 + UP * pos[1] * 0.4

        # Update nucleus and label
        nucleus.move_to(screen_pos)
        label.move_to(screen_pos)
        orbit.move_to(screen_pos)

        # Update electron position (circular orbit)
        orbit_radius = 0.25
        electron_pos = screen_pos + orbit_radius * (np.cos(phase) * RIGHT + np.sin(phase) * UP)
        electron.move_to(electron_pos)

    def phase_1_free_atoms(self):
        """Phase 1: Single H-atom free movement in box"""
        # Update phase label
        phase_text = Text(get_string("phase1"), font_size=16, color=YELLOW)
        phase_text.move_to(self.mol_area_center + UP * 2.5)
        self.play(Transform(self.current_phase_label, phase_text))

        # Run MD for single atom
        for step in range(self.phase1_steps):
            # Update H1 atom
            def h1_forces(pos):
                return self.box_force(pos)

            self.h1_pos, self.h1_vel = self.md_step_single_atom(self.h1_pos, self.h1_vel, h1_forces)

            # Update electron phase
            self.h1_electron_phase += 0.3  # Fast electron motion

            # Update time
            self.current_time += self.dt

            # Store data
            h1_kinetic = 0.5 * self.mass * np.sum(self.h1_vel**2)
            h1_potential = self.box_potential(self.h1_pos)
            h1_total = h1_kinetic + h1_potential

            self.time_data.append(self.current_time)
            self.h1_energy_data.append(h1_total)
            self.h2_energy_data.append(0.0)  # Not present yet
            self.distance_data.append(0.0)  # No second atom
            self.interaction_energy_data.append(0.0)

            # Update visualization every few steps
            if step % 1 == 0:
                self.update_h_atom_visualization(1)
                self.update_plots()
                self.wait(self.phase1_wait)

        self.wait(1)

    def phase_2_two_atoms(self):
        """Phase 2: Two H-atoms with interaction"""
        # Update phase label
        phase_text = Text(get_string("phase2"), font_size=16, color=YELLOW)
        phase_text.move_to(self.mol_area_center + UP * 2.5)
        self.play(Transform(self.current_phase_label, phase_text))

        # Disable sliding window for Phase 2 to show full distance history
        self.disable_sliding_window = True

        # Reset H1 position to lower-left corner
        self.h1_pos = np.array([-3.0, -2.0])
        # Random velocity direction (roughly towards upper-right, 0-90°)
        angle_h1 = np.random.uniform(0, np.pi/2)  # 0 to 90 degrees in radians
        speed = 0.08
        self.h1_vel = np.array([speed * np.cos(angle_h1), speed * np.sin(angle_h1)])

        # Introduce second atom at upper-right corner
        self.h2_pos = np.array([3.0, 2.0])
        # Random velocity direction (roughly towards lower-left, 180-270°)
        angle_h2 = np.random.uniform(np.pi, 3*np.pi/2)  # 180 to 270 degrees in radians
        self.h2_vel = np.array([speed * np.cos(angle_h2), speed * np.sin(angle_h2)])

        # Show second atom
        self.play(ShowCreation(self.h2_group))

        # Run MD for both atoms
        for step in range(self.phase2_steps):
            # Forces on H1
            def h1_forces(pos):
                box_f = self.box_force(pos)
                r_vec = self.h2_pos - pos
                interaction_f = self.lennard_jones_force(r_vec)
                return box_f + interaction_f

            # Forces on H2
            def h2_forces(pos):
                box_f = self.box_force(pos)
                r_vec = self.h1_pos - pos
                interaction_f = self.lennard_jones_force(r_vec)
                return box_f + interaction_f

            # Update both atoms
            self.h1_pos, self.h1_vel = self.md_step_single_atom(self.h1_pos, self.h1_vel, h1_forces)
            self.h2_pos, self.h2_vel = self.md_step_single_atom(self.h2_pos, self.h2_vel, h2_forces)

            # Update electron phases
            self.h1_electron_phase += 0.3
            self.h2_electron_phase += 0.3

            # Update time
            self.current_time += self.dt

            # Calculate energies
            h1_kinetic = 0.5 * self.mass * np.sum(self.h1_vel**2)
            h1_potential = self.box_potential(self.h1_pos)
            h2_kinetic = 0.5 * self.mass * np.sum(self.h2_vel**2)
            h2_potential = self.box_potential(self.h2_pos)

            distance = np.linalg.norm(self.h2_pos - self.h1_pos)
            interaction_energy = self.lennard_jones_potential(distance)

            h1_total = h1_kinetic + h1_potential
            h2_total = h2_kinetic + h2_potential

            # Store data
            self.time_data.append(self.current_time)
            self.h1_energy_data.append(h1_total)
            self.h2_energy_data.append(h2_total)
            self.distance_data.append(distance)
            self.interaction_energy_data.append(interaction_energy)

            # Update visualization
            if step % 1 == 0:
                self.update_h_atom_visualization(1)
                self.update_h_atom_visualization(2)
                self.update_plots()
                self.wait(self.phase2_wait)

        self.wait(2)

    def phase_3_born_oppenheimer(self):
        """Phase 3: Born-Oppenheimer approximation transition"""
        # Re-enable sliding window for Phase 3 and beyond
        self.disable_sliding_window = False

        # Update phase label
        phase_text = Text(get_string("phase3"), font_size=16, color=YELLOW)
        phase_text.move_to(self.mol_area_center + UP * 2.5)
        self.play(Transform(self.current_phase_label, phase_text))

        # Show BO explanation
        bo_explanation = VGroup(
            Text(get_string("bo_title"), font_size=18, color=ORANGE, weight=BOLD),
            Text(get_string("bo_slow_nuclei"), font_size=16),
            Text(get_string("bo_adiabatic"), font_size=16),
            Text(get_string("bo_separation"), font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        # Add background rectangle for better visibility
        bo_bg = Rectangle(
            width=bo_explanation.get_width() + 0.4,
            height=bo_explanation.get_height() + 0.3,
            fill_color=BLACK, fill_opacity=0.8, stroke_color=ORANGE, stroke_width=1
        )
        bo_bg.move_to(bo_explanation.get_center())

        # Position with more buffer from edges
        bo_group = VGroup(bo_bg, bo_explanation)
        bo_group.to_corner(UL, buff=0.6)

        self.play(FadeIn(bo_group))
        self.wait(4)

        # Remove electrons and focus on nuclei
        self.play(
            FadeOut(self.h1_electron),
            FadeOut(self.h2_electron),
            FadeOut(self.h1_orbit),
            FadeOut(self.h2_orbit),
            self.h1_nucleus.animate.scale(1.3),
            self.h2_nucleus.animate.scale(1.3)
        )

        self.play(FadeOut(bo_group))
        self.wait(1)

    def phase_4_h2_formation(self):
        """Phase 4: H2 molecule formation with Morse potential"""
        # Update phase label
        phase_text = Text(get_string("phase4"), font_size=16, color=YELLOW)
        phase_text.move_to(self.mol_area_center + UP * 2.5)
        self.play(Transform(self.current_phase_label, phase_text))

        # Transition plots: fade out time plots only
        self.play(
            FadeOut(self.energy_plot_group),
            FadeOut(self.distance_plot_group)
        )

        # Keep box visible (do not fade out sim_box)

        # Gradual bond formation sequence
        center_pos = self.mol_area_center

        # Step 1: Annäherung (atoms approach each other)
        self.play(
            self.h1_nucleus.animate.move_to(center_pos + LEFT * 1.0),
            self.h2_nucleus.animate.move_to(center_pos + RIGHT * 1.0),
            self.h1_label.animate.move_to(center_pos + LEFT * 1.0),
            self.h2_label.animate.move_to(center_pos + RIGHT * 1.0),
            run_time=2
        )

        # Step 2: Slow approach to bond length
        self.play(
            self.h1_nucleus.animate.move_to(center_pos + LEFT * 0.4),
            self.h2_nucleus.animate.move_to(center_pos + RIGHT * 0.4),
            self.h1_label.animate.move_to(center_pos + LEFT * 0.4),
            self.h2_label.animate.move_to(center_pos + RIGHT * 0.4),
            run_time=3
        )

        # Step 3: Show bond formation
        self.bond_line = Line(center_pos + LEFT * 0.4, center_pos + RIGHT * 0.4, color=WHITE, stroke_width=3)
        self.play(ShowCreation(self.bond_line))
        self.wait(1)

        # Setup potential plot (now visible)
        self.setup_potential_plot()
        self.play(FadeIn(self.potential_plot_group))
        self.play(self.morse_curve.animate.set_stroke(opacity=1))

        self.wait(2)

        # Step 4: Begin molecular vibration
        # Initialize H2 distance coordinate
        self.r_h2 = 0.8  # Start near equilibrium
        self.v_h2 = 0.05  # Small initial velocity

        # Show harmonic approximation after some Morse motion
        for step in range(self.phase4_steps):
            # Morse potential dynamics
            F_morse = -2 * self.D_e * self.alpha * (1 - np.exp(-self.alpha * (self.r_h2 - self.r_e))) * np.exp(-self.alpha * (self.r_h2 - self.r_e))

            # Update H2 coordinate
            r_new = self.r_h2 + self.v_h2 * self.dt + 0.5 * F_morse / (0.5 * self.mass) * self.dt**2
            F_new = -2 * self.D_e * self.alpha * (1 - np.exp(-self.alpha * (r_new - self.r_e))) * np.exp(-self.alpha * (r_new - self.r_e))
            v_new = self.v_h2 + 0.5 * (F_morse + F_new) / (0.5 * self.mass) * self.dt

            # Clamp for stability
            self.r_h2 = max(0.4, min(1.5, r_new))
            self.v_h2 = max(-0.3, min(0.3, v_new))

            # Update time
            self.current_time += self.dt

            # Update H2 visualization
            half_bond = (self.r_h2 / self.r_e) * 0.4
            h1_pos = center_pos + LEFT * half_bond
            h2_pos = center_pos + RIGHT * half_bond

            self.h1_nucleus.move_to(h1_pos)
            self.h2_nucleus.move_to(h2_pos)
            self.h1_label.move_to(h1_pos)
            self.h2_label.move_to(h2_pos)

            # Update bond line
            self.bond_line.put_start_and_end_on(h1_pos, h2_pos)

            # Calculate energies
            kinetic = 0.5 * 0.5 * self.mass * self.v_h2**2
            potential = self.morse_potential_full_range(self.r_h2)
            total_energy = kinetic + potential

            # Store data
            self.time_data.append(self.current_time)
            self.h1_energy_data.append(kinetic)
            self.h2_energy_data.append(potential)
            self.distance_data.append(self.r_h2)
            self.interaction_energy_data.append(total_energy)

            # Update potential dot position on Morse curve
            current_potential = self.morse_potential_full_range(self.r_h2)
            dot_pos = self.potential_axes.coords_to_point(self.r_h2, min(max(current_potential, -5), 10))
            self.potential_dot.move_to(dot_pos)

            # Update real-time value displays
            self.distance_display.become(Text(f"r = {self.r_h2:.3f} Å", font_size=14, color=YELLOW))
            self.energy_display.become(Text(f"E = {current_potential:.3f} eV", font_size=14, color=YELLOW))
            # Re-arrange and position the displays
            new_value_displays = VGroup(self.distance_display, self.energy_display)
            new_value_displays.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            new_value_displays.move_to(self.potential_plot_center + RIGHT * 2.5)

            # Update plots - slow down animation for better tracking
            if step % 1 == 0:
                self.wait(self.phase4_wait)

        # Show harmonic approximation explanation
        harmonic_explanation = VGroup(
            Text(get_string("harmonic_title"), font_size=18, color=ORANGE, weight=BOLD),
            Text(get_string("harmonic_small_osc"), font_size=16),
            Text(get_string("harmonic_formula"), font_size=16),
            Text(get_string("harmonic_compare"), font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        # Add background rectangle for better visibility
        harmonic_bg = Rectangle(
            width=harmonic_explanation.get_width() + 0.4,
            height=harmonic_explanation.get_height() + 0.3,
            fill_color=BLACK, fill_opacity=0.8, stroke_color=ORANGE, stroke_width=1
        )
        harmonic_bg.move_to(harmonic_explanation.get_center())

        # Position with more buffer from edges
        harmonic_group = VGroup(harmonic_bg, harmonic_explanation)
        harmonic_group.to_corner(UL, buff=0.6)

        self.play(FadeIn(harmonic_group))

        # Show harmonic curve
        self.play(self.harmonic_curve.animate.set_stroke(opacity=1))
        self.wait(4)

        self.play(FadeOut(harmonic_group))

        # Continue with motion showing both potentials
        for step in range(self.phase4_steps):
            # Morse potential dynamics
            F_morse = -2 * self.D_e * self.alpha * (1 - np.exp(-self.alpha * (self.r_h2 - self.r_e))) * np.exp(-self.alpha * (self.r_h2 - self.r_e))

            # Update H2 coordinate
            r_new = self.r_h2 + self.v_h2 * self.dt + 0.5 * F_morse / (0.5 * self.mass) * self.dt**2
            F_new = -2 * self.D_e * self.alpha * (1 - np.exp(-self.alpha * (r_new - self.r_e))) * np.exp(-self.alpha * (r_new - self.r_e))
            v_new = self.v_h2 + 0.5 * (F_morse + F_new) / (0.5 * self.mass) * self.dt

            # Clamp for stability
            self.r_h2 = max(0.4, min(1.5, r_new))
            self.v_h2 = max(-0.3, min(0.3, v_new))

            # Update time
            self.current_time += self.dt

            # Update H2 visualization
            half_bond = (self.r_h2 / self.r_e) * 0.4
            h1_pos = center_pos + LEFT * half_bond
            h2_pos = center_pos + RIGHT * half_bond

            self.h1_nucleus.move_to(h1_pos)
            self.h2_nucleus.move_to(h2_pos)
            self.h1_label.move_to(h1_pos)
            self.h2_label.move_to(h2_pos)

            # Update bond line
            self.bond_line.put_start_and_end_on(h1_pos, h2_pos)

            # Calculate energies
            kinetic = 0.5 * 0.5 * self.mass * self.v_h2**2
            potential = self.morse_potential_full_range(self.r_h2)
            total_energy = kinetic + potential

            # Store data
            self.time_data.append(self.current_time)
            self.h1_energy_data.append(kinetic)
            self.h2_energy_data.append(potential)
            self.distance_data.append(self.r_h2)
            self.interaction_energy_data.append(total_energy)

            # Update potential dot position on Morse curve
            current_potential = self.morse_potential_full_range(self.r_h2)
            dot_pos = self.potential_axes.coords_to_point(self.r_h2, min(max(current_potential, -5), 10))
            self.potential_dot.move_to(dot_pos)

            # Update real-time value displays
            self.distance_display.become(Text(f"r = {self.r_h2:.3f} Å", font_size=14, color=YELLOW))
            self.energy_display.become(Text(f"E = {current_potential:.3f} eV", font_size=14, color=YELLOW))
            # Re-arrange and position the displays
            new_value_displays = VGroup(self.distance_display, self.energy_display)
            new_value_displays.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            new_value_displays.move_to(self.potential_plot_center + RIGHT * 2.5)

            # Update plots - slow down animation for better tracking
            if step % 1 == 0:
                self.wait(self.phase4_wait)

        # Add bond line
        self.bond_line = Line(
            self.h1_nucleus.get_center(),
            self.h2_nucleus.get_center(),
            color=WHITE, stroke_width=3
        )
        self.play(ShowCreation(self.bond_line))

        self.wait(2)

    def phase_5_dissociation(self):
        """Phase 5: H₂ dissociation"""
        # Update phase label
        phase_text = Text(get_string("phase5"), font_size=16, color=YELLOW)
        phase_text.move_to(self.mol_area_center + UP * 2.5)
        self.play(Transform(self.current_phase_label, phase_text))

        # Increase velocity to dissociate
        self.v_h2 = 2  # Higher velocity to overcome potential barrier

        # Dissociation sequence
        for step in range(self.phase5_steps):
            # Morse potential dynamics
            F_morse = -2 * self.D_e * self.alpha * (1 - np.exp(-self.alpha * (self.r_h2 - self.r_e))) * np.exp(-self.alpha * (self.r_h2 - self.r_e))

            # Update H2 coordinate
            r_new = self.r_h2 + self.v_h2 * self.dt + 0.5 * F_morse / (0.5 * self.mass) * self.dt**2
            F_new = -2 * self.D_e * self.alpha * (1 - np.exp(-self.alpha * (r_new - self.r_e))) * np.exp(-self.alpha * (r_new - self.r_e))
            v_new = self.v_h2 + step/10 + 0.5 * (F_morse + F_new) / (0.5 * self.mass) * self.dt

            # Clamp for stability (no upper limit for dissociation)
            self.r_h2 = max(0.4, r_new)
            self.v_h2 = max(-0.3, min(0.3, v_new))

            # Update time
            self.current_time += self.dt

            # Update H2 visualization
            half_bond = (self.r_h2 / self.r_e) * 0.4
            h1_pos = self.mol_area_center + LEFT * half_bond
            h2_pos = self.mol_area_center + RIGHT * half_bond

            self.h1_nucleus.move_to(h1_pos)
            self.h2_nucleus.move_to(h2_pos)
            self.h1_label.move_to(h1_pos)
            self.h2_label.move_to(h2_pos)

            # Update bond line
            if self.r_h2 <= 1.2:
                self.bond_line.put_start_and_end_on(h1_pos, h2_pos)

            # Calculate energies
            kinetic = 0.5 * 0.5 * self.mass * self.v_h2**2
            potential = self.morse_potential_full_range(self.r_h2)
            total_energy = kinetic + potential

            # Store data
            self.time_data.append(self.current_time)
            self.h1_energy_data.append(kinetic)
            self.h2_energy_data.append(potential)
            self.distance_data.append(self.r_h2)
            self.interaction_energy_data.append(total_energy)

            # Update potential dot position
            current_potential = self.morse_potential_full_range(self.r_h2)
            dot_pos = self.potential_axes.coords_to_point(self.r_h2, min(max(current_potential, -5), 10))
            self.potential_dot.move_to(dot_pos)

            # Update real-time displays
            self.distance_display.become(Text(f"r = {self.r_h2:.3f} Å", font_size=14, color=YELLOW))
            self.energy_display.become(Text(f"E = {current_potential:.3f} eV", font_size=14, color=YELLOW))
            new_value_displays = VGroup(self.distance_display, self.energy_display)
            new_value_displays.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            new_value_displays.move_to(self.potential_plot_center + RIGHT * 2.5)

            if self.r_h2 > 1.2:
                # Fade out bond line as atoms separate
                self.play(FadeOut(self.bond_line), run_time=0.5)
            # Update plots with smoother animation
            if step % 1 == 0:
                self.wait(self.phase5_wait)

        # After dissociation, show atoms as free
        self.play(
            FadeOut(self.bond_line),
            self.h1_nucleus.animate.scale(1.0),
            self.h2_nucleus.animate.scale(1.0)
        )
        self.wait(2)

    def show_final_statistics(self):
        """Show final statistics"""
        stats = VGroup(
            Text(f"{get_string('simulation_time')}: {self.current_time:.1f} {get_string('unit_fs')}", font_size=12),
            Text(f"{get_string('bond_length')}: {self.r_h2:.3f} {get_string('unit_angstrom')}", font_size=12),
            Text(get_string("temperature"), font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        stats.move_to(self.mol_area_center + DOWN * 2.0)

        self.play(Write(stats))
        self.wait(2)