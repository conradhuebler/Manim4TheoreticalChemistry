#!/usr/bin/env python3
"""
Polarization in Force Fields
Polarisation in Kraftfeldern

Bilingual animation demonstrating the difference between:
1. Simple force fields (no polarization): static partial charges
2. Polarizable force fields: dynamic charges that respond to environment

Uses proper Molecular Dynamics with:
- Lennard-Jones potential for all atom interactions
- Velocity Verlet integration
- Berendsen thermostat for temperature control
- Periodic boundary conditions

Zweisprachige Animation zur Demonstration des Unterschieds zwischen:
1. Einfache Kraftfelder (keine Polarisation): statische Partialladungen
2. Polarisierbare Kraftfelder: dynamische Ladungen, die auf Umgebung reagieren

Mit korrekter Molekulardynamik:
- Lennard-Jones-Potential für alle Atom-Wechselwirkungen
- Velocity-Verlet-Integration
- Berendsen-Thermostat zur Temperaturkontrolle
- Periodische Randbedingungen
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "DE"  # Set to "EN" for English

STRINGS = {
    "DE": {
        "title": "Polarisation in Kraftfeldern",
        "scenario1": "Szenario 1: Einfaches Kraftfeld",
        "scenario2": "Szenario 2: Polarisierbares Kraftfeld",
        "no_polarization": "(Keine Polarisation)",
        "with_polarization": "(Mit Polarisation)",
        "atom_of_interest": "Atom von Interesse",
        "environment": "Umgebung",
        "partial_charge": "Partialladung:",
        "charge_fixed": "Ladung bleibt konstant",
        "charge_dynamic": "Ladung ändert sich dynamisch",
        "charge_scale": "Ladungsskala",
        "distance_label": "Abstand",
        "explanation1": "Partialladungen bleiben konstant",
        "explanation2": "Partialladungen ändern sich mit Abstand",
        "temperature": "Temperatur:",
        "thermostat": "Berendsen-Thermostat",
    },
    "EN": {
        "title": "Polarization in Force Fields",
        "scenario1": "Scenario 1: Simple Force Field",
        "scenario2": "Scenario 2: Polarizable Force Field",
        "no_polarization": "(No Polarization)",
        "with_polarization": "(With Polarization)",
        "atom_of_interest": "Atom of Interest",
        "environment": "Environment",
        "partial_charge": "Partial charge:",
        "charge_fixed": "Charge remains constant",
        "charge_dynamic": "Charge changes dynamically",
        "charge_scale": "Charge Scale",
        "distance_label": "Distance",
        "explanation1": "Partial charges remain constant",
        "explanation2": "Partial charges change with distance",
        "temperature": "Temperature:",
        "thermostat": "Berendsen Thermostat",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class MDSimulator:
    """Molecular Dynamics simulator with Lennard-Jones potential and Velocity Verlet"""

    def __init__(self, n_atoms, box_size, epsilon=0.1, sigma=0.4, dt=0.005):
        """
        Initialize MD simulator

        Parameters:
        - n_atoms: number of atoms (including atom of interest)
        - box_size: size of simulation box
        - epsilon: LJ well depth
        - sigma: LJ size parameter (collision radius)
        - dt: integration timestep
        """
        self.n_atoms = n_atoms
        self.box_size = box_size
        self.epsilon = epsilon
        self.sigma = sigma
        self.dt = dt
        self.r_cut = 2.5 * sigma  # Cutoff radius

        # Arrays for positions, velocities, forces, masses
        self.positions = np.zeros((n_atoms, 3))
        self.velocities = np.zeros((n_atoms, 3))
        self.forces = np.zeros((n_atoms, 3))
        self.masses = np.ones(n_atoms)  # All masses = 1

        # Thermostat parameters
        self.target_temperature = 10.0
        self.tau_T = 0.2  # Thermostat coupling constant (larger = softer coupling)
        self.current_temperature = 0.0

    def initialize_positions(self, center_fixed=True):
        """Initialize random positions, optionally fix first atom at center"""
        if center_fixed:
            self.positions[0] = np.array([0, 0, 0])
            start_idx = 1
        else:
            # Place first atom (atom of interest) near center but not exactly at center
            angle = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0.2, 0.5)
            self.positions[0] = np.array([r * np.cos(angle), r * np.sin(angle), 0])
            start_idx = 1

        for i in range(start_idx, self.n_atoms):
            # Random position avoiding overlaps
            max_attempts = 100
            for attempt in range(max_attempts):
                pos = np.random.uniform(-self.box_size * 0.8, self.box_size * 0.8, 3)
                pos[2] = 0  # Keep in 2D

                # Check distance to all previously placed atoms
                valid = True

                # Check distance to all already-placed atoms (including atom 0)
                for j in range(i):
                    dist = np.linalg.norm(pos - self.positions[j])
                    if dist < self.sigma * 1.5:  # Minimum separation
                        valid = False
                        break

                if valid:
                    break

            self.positions[i] = pos

    def initialize_velocities(self, temperature=1.0, center_fixed=True):
        """Initialize Maxwell-Boltzmann velocity distribution"""
        start_idx = 1 if center_fixed else 0

        for i in range(start_idx, self.n_atoms):
            # Random velocities
            v = np.random.normal(0, np.sqrt(temperature / self.masses[i]), 3)
            v[2] = 0  # Keep in 2D
            self.velocities[i] = v

        # Remove center of mass motion
        if not center_fixed:
            vcm = np.sum(self.velocities * self.masses[:, np.newaxis], axis=0) / np.sum(self.masses)
            self.velocities -= vcm

    def calculate_lj_force(self, r_vec):
        """Calculate Lennard-Jones force for distance vector r_vec"""
        r = np.linalg.norm(r_vec)

        if r > self.r_cut or r < 0.01:  # Cutoff or avoid singularity
            return np.zeros(3)

        # LJ force: F = 24*epsilon/r * [2*(sigma/r)^12 - (sigma/r)^6] * r_vec/r
        sigma_over_r = self.sigma / r
        force_magnitude = 24 * self.epsilon / r * (2 * sigma_over_r**12 - sigma_over_r**6)

        return force_magnitude * r_vec / r

    def calculate_forces(self, center_fixed=True):
        """Calculate forces on all atoms from LJ potential"""
        self.forces[:] = 0

        start_idx = 1 if center_fixed else 0

        # Pairwise interactions
        for i in range(start_idx, self.n_atoms):
            for j in range(i + 1, self.n_atoms):
                r_vec = self.positions[j] - self.positions[i]

                # Periodic boundary conditions
                r_vec = self.apply_pbc(r_vec)

                # Calculate force
                f_ij = self.calculate_lj_force(r_vec)

                self.forces[i] += f_ij
                self.forces[j] -= f_ij

            # Interaction with fixed center atom (if applicable)
            if center_fixed:
                r_vec = self.positions[i] - self.positions[0]
                r_vec = self.apply_pbc(r_vec)
                f_i0 = self.calculate_lj_force(r_vec)
                self.forces[i] += f_i0

    def apply_pbc(self, r_vec):
        """Apply periodic boundary conditions (minimum image convention)"""
        box_length = 2 * self.box_size
        r_vec[0] = r_vec[0] - box_length * np.round(r_vec[0] / box_length)
        r_vec[1] = r_vec[1] - box_length * np.round(r_vec[1] / box_length)
        return r_vec

    def apply_walls(self, center_fixed=True):
        """Reflect atoms off walls (alternative to PBC)"""
        start_idx = 1 if center_fixed else 0

        for i in range(start_idx, self.n_atoms):
            for dim in range(2):  # x, y only
                if abs(self.positions[i, dim]) > self.box_size:
                    self.positions[i, dim] = np.sign(self.positions[i, dim]) * self.box_size
                    self.velocities[i, dim] *= -0.9  # Inelastic collision

    def velocity_verlet_step(self, center_fixed=True):
        """Perform one Velocity Verlet integration step"""
        start_idx = 1 if center_fixed else 0

        # Calculate current forces
        self.calculate_forces(center_fixed)

        # Update positions: x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2
        for i in range(start_idx, self.n_atoms):
            acc = self.forces[i] / self.masses[i]
            self.positions[i] += self.velocities[i] * self.dt + 0.5 * acc * self.dt**2

        # Apply boundary conditions
        self.apply_walls(center_fixed)

        # Store old forces
        old_forces = self.forces.copy()

        # Calculate new forces at updated positions
        self.calculate_forces(center_fixed)

        # Update velocities: v(t+dt) = v(t) + 0.5*[a(t) + a(t+dt)]*dt
        for i in range(start_idx, self.n_atoms):
            acc_old = old_forces[i] / self.masses[i]
            acc_new = self.forces[i] / self.masses[i]
            self.velocities[i] += 0.5 * (acc_old + acc_new) * self.dt

    def apply_berendsen_thermostat(self, center_fixed=True):
        """Apply Berendsen thermostat to control temperature"""
        start_idx = 1 if center_fixed else 0

        # Calculate current kinetic energy
        ke = 0
        n_free = 0
        for i in range(start_idx, self.n_atoms):
            ke += 0.5 * self.masses[i] * np.sum(self.velocities[i]**2)
            n_free += 2  # 2 degrees of freedom (2D)

        if n_free == 0:
            self.current_temperature = 0.0
            return

        # Current temperature (kB = 1)
        T_current = 2 * ke / n_free
        self.current_temperature = T_current

        if T_current < 0.01:  # Avoid division by zero
            return

        # Velocity rescaling factor (Berendsen thermostat)
        lambda_factor = np.sqrt(1 + (self.dt / self.tau_T) * (self.target_temperature / T_current - 1))

        # Rescale velocities
        for i in range(start_idx, self.n_atoms):
            self.velocities[i] *= lambda_factor

    def run_steps(self, n_steps, center_fixed=True):
        """Run multiple MD steps"""
        for _ in range(n_steps):
            self.velocity_verlet_step(center_fixed)
            self.apply_berendsen_thermostat(center_fixed)


class PolarizationForceField(Scene):
    """Polarization force field comparison with MD simulation."""

    PARAMETERS = {
        # MD simulation parameters
        "n_environment_atoms": {
            "value": 3,
            "type": int,
            "unit": "-",
            "description": "Number of environment atoms around central atom",
            "min": 3,
            "max": 12
        },
        "box_size": {
            "value": 2.5,
            "type": float,
            "unit": "-",
            "description": "Size of simulation box",
            "min": 1.0,
            "max": 5.0
        },
        "epsilon": {
            "value": 0.1,
            "type": float,
            "unit": "kcal/mol",
            "description": "LJ well depth (reduced for softer interactions)",
            "min": 0.01,
            "max": 1.0
        },
        "sigma": {
            "value": 0.03,
            "type": float,
            "unit": "Å",
            "description": "LJ collision radius (smaller particles)",
            "min": 0.01,
            "max": 0.1
        },
        "dt_md": {
            "value": 0.003,
            "type": float,
            "unit": "fs",
            "description": "MD timestep (smaller for stability)",
            "min": 0.001,
            "max": 0.01
        },
        "steps_per_frame": {
            "value": 3,
            "type": int,
            "unit": "-",
            "description": "MD steps per animation frame (fewer for slower motion)",
            "min": 1,
            "max": 10
        },
        # Visual parameters
        "visual_radius_central": {
            "value": 0.15,
            "type": float,
            "unit": "-",
            "description": "Visual radius for central atom of interest",
            "min": 0.05,
            "max": 0.5
        },
        "visual_radius_env": {
            "value": 0.1,
            "type": float,
            "unit": "-",
            "description": "Visual radius for environment atoms",
            "min": 0.05,
            "max": 0.3
        },
        # Polarization parameters
        "base_charge": {
            "value": 0.2,
            "type": float,
            "unit": "e",
            "description": "Base partial charge for non-polarizable model",
            "min": 0.0,
            "max": 1.0
        },
        "polarization_strength": {
            "value": 0.65,
            "type": float,
            "unit": "-",
            "description": "Polarization sensitivity (higher = more sensitive)",
            "min": 0.1,
            "max": 2.0
        },
        "distance_decay": {
            "value": 0.6,
            "type": float,
            "unit": "1/Å",
            "description": "Exponential decay parameter for polarization",
            "min": 0.1,
            "max": 2.0
        },
        "max_charge": {
            "value": 1.5,
            "type": float,
            "unit": "e",
            "description": "Maximum partial charge in polarizable model",
            "min": 0.5,
            "max": 3.0
        },
        "min_charge": {
            "value": 0.0,
            "type": float,
            "unit": "e",
            "description": "Minimum partial charge in polarizable model",
            "min": 0.0,
            "max": 1.0
        },
        # Animation parameters
        "total_time": {
            "value": 10.0,
            "type": float,
            "unit": "s",
            "description": "Total animation duration",
            "min": 1.0,
            "max": 60.0
        },
        "fps": {
            "value": 30,
            "type": int,
            "unit": "frames/s",
            "description": "Frames per second for animation",
            "min": 10,
            "max": 120
        }
    }

    def construct(self):
        # Extract parameters from central dictionary
        self.setup_parameters()

        # Create title
        title = Text(get_string("title"), color=YELLOW).scale(0.7)
        title.to_edge(UP, buff=0.3)
        self.add(title)

        # Create scenario labels
        self.create_scenario_labels()

        # Create simulation boxes
        self.create_simulation_boxes()

        # Create charge scale legend
        self.create_charge_scale()

        # Initialize MD simulators
        self.init_md_simulators()

        # Initialize atom visualizations
        self.init_atom_visuals()

        # Run simulation
        self.run_simulation()

        self.wait(2)

    def setup_parameters(self):
        """Extract all parameters from PARAMETERS dictionary"""
        # MD parameters
        self.n_environment_atoms = self.PARAMETERS["n_environment_atoms"]["value"]
        self.box_size = self.PARAMETERS["box_size"]["value"]
        self.epsilon = self.PARAMETERS["epsilon"]["value"]
        self.sigma = self.PARAMETERS["sigma"]["value"]
        self.dt_md = self.PARAMETERS["dt_md"]["value"]
        self.steps_per_frame = self.PARAMETERS["steps_per_frame"]["value"]

        # Visual parameters
        self.visual_radius_central = self.PARAMETERS["visual_radius_central"]["value"]
        self.visual_radius_env = self.PARAMETERS["visual_radius_env"]["value"]

        # Polarization parameters
        self.base_charge = self.PARAMETERS["base_charge"]["value"]
        self.polarization_strength = self.PARAMETERS["polarization_strength"]["value"]
        self.distance_decay = self.PARAMETERS["distance_decay"]["value"]
        self.max_charge = self.PARAMETERS["max_charge"]["value"]
        self.min_charge = self.PARAMETERS["min_charge"]["value"]

        # Animation parameters
        self.total_time = self.PARAMETERS["total_time"]["value"]
        self.fps = self.PARAMETERS["fps"]["value"]

    def create_scenario_labels(self):
        """Create labels for both scenarios"""
        # Left scenario
        scenario1_title = Text(get_string("scenario1"), color=BLUE_C).scale(0.5)
        scenario1_title.move_to(LEFT * 3.5 + UP * 3.2)

        scenario1_sub = Text(get_string("no_polarization"), color=GREY).scale(0.35)
        scenario1_sub.move_to(LEFT * 3.5 + UP * 2.8)

        # Right scenario
        scenario2_title = Text(get_string("scenario2"), color=GREEN_C).scale(0.5)
        scenario2_title.move_to(RIGHT * 3.5 + UP * 3.2)

        scenario2_sub = Text(get_string("with_polarization"), color=GREY).scale(0.35)
        scenario2_sub.move_to(RIGHT * 3.5 + UP * 2.8)

        self.add(scenario1_title, scenario1_sub, scenario2_title, scenario2_sub)

    def create_simulation_boxes(self):
        """Create simulation boxes for both scenarios"""
        # Left box (simple FF)
        self.box_left = Square(side_length=self.box_size * 2, color=BLUE, stroke_width=2)
        self.box_left.move_to(LEFT * 3.5 + UP * 0.2)

        # Right box (polarizable FF)
        self.box_right = Square(side_length=self.box_size * 2, color=GREEN, stroke_width=2)
        self.box_right.move_to(RIGHT * 3.5 + UP * 0.2)

        self.add(self.box_left, self.box_right)

        # Store centers
        self.center_left = self.box_left.get_center()
        self.center_right = self.box_right.get_center()

    def create_charge_scale(self):
        """Create vertical color scale in the center with sliders"""
        # Vertical scale parameters
        scale_x = 0  # Center position
        scale_top = 2.2
        scale_bottom = -1.8
        scale_height = scale_top - scale_bottom
        scale_width = 0.4

        # Title above scale
        legend_title = Text(get_string("charge_scale"), color=WHITE).scale(0.45)
        legend_title.move_to(np.array([scale_x, scale_top + 0.4, 0]))
        self.add(legend_title)

        # Create vertical gradient bar (many horizontal rectangles)
        n_steps = 50  # Many steps for smooth gradient
        step_height = scale_height / n_steps

        for i in range(n_steps):
            # Charge goes from max (top) to min (bottom)
            charge = self.max_charge * (1 - i / (n_steps - 1))
            color = self.charge_to_color(charge)

            y_pos = scale_top - i * step_height - step_height / 2

            rect = Rectangle(
                width=scale_width,
                height=step_height,
                fill_color=color,
                fill_opacity=1.0,
                stroke_width=0
            )
            rect.move_to(np.array([scale_x, y_pos, 0]))
            self.add(rect)

        # Border around scale
        border = Rectangle(
            width=scale_width,
            height=scale_height,
            stroke_color=WHITE,
            stroke_width=2,
            fill_opacity=0
        )
        border.move_to(np.array([scale_x, (scale_top + scale_bottom) / 2, 0]))
        self.add(border)

        # Add charge labels on the right side of scale
        label_max = Text(f"{self.max_charge:.1f}", color=WHITE).scale(0.35)
        label_max.move_to(np.array([scale_x + scale_width/2 + 0.4, scale_top, 0]))
        self.add(label_max)

        label_min = Text(f"{self.min_charge:.1f}", color=WHITE).scale(0.35)
        label_min.move_to(np.array([scale_x + scale_width/2 + 0.4, scale_bottom, 0]))
        self.add(label_min)

        # Store scale parameters for slider positioning
        self.scale_x = scale_x
        self.scale_top = scale_top
        self.scale_bottom = scale_bottom
        self.scale_width = scale_width

    def charge_to_color(self, charge):
        """
        Convert charge value to color with extended gradient
        Blue (0) -> Cyan -> White -> Orange -> Red (1.5)
        """
        # Normalize to 0-1 range
        t = np.clip(charge / self.max_charge, 0, 1)

        if t < 0.25:
            # Blue to Cyan
            return interpolate_color(BLUE, "#00FFFF", t * 4)
        elif t < 0.5:
            # Cyan to White
            return interpolate_color("#00FFFF", WHITE, (t - 0.25) * 4)
        elif t < 0.75:
            # White to Orange
            return interpolate_color(WHITE, ORANGE, (t - 0.5) * 4)
        else:
            # Orange to Red
            return interpolate_color(ORANGE, RED, (t - 0.75) * 4)

    def create_charge_sliders(self):
        """Create slider indicators on the vertical charge scale"""
        # Left slider (simple FF - pointing right towards scale)
        arrow_size = 0.3

        # Create triangle pointing right (towards scale from left)
        self.slider_left = Polygon(
            np.array([-arrow_size, arrow_size/2, 0]),
            np.array([-arrow_size, -arrow_size/2, 0]),
            np.array([0, 0, 0]),
            fill_color=BLUE_C,
            fill_opacity=0.8,
            stroke_color=BLUE_C,
            stroke_width=3
        )

        # Position based on base_charge
        y_pos_left = self.charge_to_y_position(self.base_charge)
        self.slider_left.move_to(np.array([self.scale_x - self.scale_width/2 - arrow_size/2, y_pos_left, 0]))
        self.add(self.slider_left)

        # Right slider (polarizable FF - pointing left towards scale)
        self.slider_right = Polygon(
            np.array([arrow_size, arrow_size/2, 0]),
            np.array([arrow_size, -arrow_size/2, 0]),
            np.array([0, 0, 0]),
            fill_color=GREEN_C,
            fill_opacity=0.8,
            stroke_color=GREEN_C,
            stroke_width=3
        )

        # Position based on base_charge initially
        y_pos_right = self.charge_to_y_position(self.base_charge)
        self.slider_right.move_to(np.array([self.scale_x + self.scale_width/2 + arrow_size/2, y_pos_right, 0]))
        self.add(self.slider_right)

    def charge_to_y_position(self, charge):
        """Convert charge value to y-position on the vertical scale"""
        # Normalize charge to 0-1 range
        t = np.clip((charge - self.min_charge) / (self.max_charge - self.min_charge), 0, 1)

        # Interpolate between bottom and top
        y_pos = self.scale_bottom + t * (self.scale_top - self.scale_bottom)
        return y_pos

    def init_md_simulators(self):
        """Initialize MD simulators for both boxes"""
        np.random.seed(42)

        # Left simulator (simple FF)
        self.md_left = MDSimulator(
            n_atoms=self.n_environment_atoms + 1,
            box_size=self.box_size,
            epsilon=self.epsilon,
            sigma=self.sigma,
            dt=self.dt_md
        )
        self.md_left.initialize_positions(center_fixed=False)  # Allow central atom to move
        self.md_left.initialize_velocities(temperature=0.8, center_fixed=False)  # Lower temp for calmer motion

        # Right simulator (polarizable FF)
        np.random.seed(42)  # Same initial conditions
        self.md_right = MDSimulator(
            n_atoms=self.n_environment_atoms + 1,
            box_size=self.box_size,
            epsilon=self.epsilon,
            sigma=self.sigma,
            dt=self.dt_md
        )
        self.md_right.initialize_positions(center_fixed=False)  # Allow central atom to move
        self.md_right.initialize_velocities(temperature=0.8, center_fixed=False)  # Lower temp for calmer motion

    def init_atom_visuals(self):
        """Initialize visual representation of atoms"""
        # Left side atoms - atom of interest is now at index 0 and can move
        pos_left_central = self.center_left + self.md_left.positions[0]
        self.atom_left_central = self.create_atom_of_interest(
            pos_left_central,
            self.base_charge,
            self.visual_radius_central
        )
        self.add(self.atom_left_central)

        self.atoms_left_env = []
        for i in range(1, self.n_environment_atoms + 1):
            pos = self.center_left + self.md_left.positions[i]
            atom = self.create_environment_atom(pos, 0.3, self.visual_radius_env)
            self.atoms_left_env.append(atom)
            self.add(atom)

        # Right side atoms - atom of interest is now at index 0 and can move
        pos_right_central = self.center_right + self.md_right.positions[0]
        self.atom_right_central = self.create_atom_of_interest(
            pos_right_central,
            self.base_charge,
            self.visual_radius_central
        )
        self.add(self.atom_right_central)

        self.atoms_right_env = []
        for i in range(1, self.n_environment_atoms + 1):
            pos = self.center_right + self.md_right.positions[i]
            atom = self.create_environment_atom(pos, 0.3, self.visual_radius_env)
            self.atoms_right_env.append(atom)
            self.add(atom)

        # Create charge labels
        self.charge_label_left = DecimalNumber(
            self.base_charge,
            num_decimal_places=3,
            color=YELLOW
        ).scale(0.45)
        self.charge_label_left.move_to(self.center_left + DOWN * 2.9)

        self.charge_label_right = DecimalNumber(
            self.base_charge,
            num_decimal_places=3,
            color=YELLOW
        ).scale(0.45)
        self.charge_label_right.move_to(self.center_right + DOWN * 2.9)

        # Add "Partial charge:" prefix
        charge_prefix_left = Text(get_string("partial_charge"), color=WHITE).scale(0.35)
        charge_prefix_left.next_to(self.charge_label_left, LEFT, buff=0.1)

        charge_prefix_right = Text(get_string("partial_charge"), color=WHITE).scale(0.35)
        charge_prefix_right.next_to(self.charge_label_right, LEFT, buff=0.1)

        self.add(self.charge_label_left, self.charge_label_right)
        self.add(charge_prefix_left, charge_prefix_right)

        # Create temperature labels
        self.temp_label_left = DecimalNumber(
            0.8,
            num_decimal_places=2,
            color=ORANGE
        ).scale(0.4)
        self.temp_label_left.move_to(self.center_left + DOWN * 3.4)

        self.temp_label_right = DecimalNumber(
            0.8,
            num_decimal_places=2,
            color=ORANGE
        ).scale(0.4)
        self.temp_label_right.move_to(self.center_right + DOWN * 3.4)

        # Add "Temperature:" prefix
        temp_prefix_left = Text(get_string("temperature"), color=WHITE).scale(0.3)
        temp_prefix_left.next_to(self.temp_label_left, LEFT, buff=0.1)

        temp_prefix_right = Text(get_string("temperature"), color=WHITE).scale(0.3)
        temp_prefix_right.next_to(self.temp_label_right, LEFT, buff=0.1)

        self.add(self.temp_label_left, self.temp_label_right)
        self.add(temp_prefix_left, temp_prefix_right)

        # Add thermostat indicator
        thermostat_label = Text(get_string("thermostat"), color=ORANGE).scale(0.3)
        thermostat_label.move_to(DOWN * 3.8)
        self.add(thermostat_label)

        # Create charge sliders on the vertical scale
        self.create_charge_sliders()

    def create_atom_of_interest(self, position, charge, radius):
        """Create the central atom of interest with glow"""
        color = self.charge_to_color(charge)

        # Glow effect
        glow = Circle(
            radius=radius * 1.3,
            fill_color=color,
            fill_opacity=0.2,
            stroke_width=0
        )
        glow.move_to(position)

        # Main circle
        circle = Circle(
            radius=radius,
            fill_color=color,
            fill_opacity=0.9,
            stroke_color=YELLOW,
            stroke_width=3
        )
        circle.move_to(position)

        # Label
        label = Text("A", color=BLACK, weight=BOLD).scale(0.4)
        label.move_to(position)

        atom = VGroup(glow, circle, label)
        atom.charge = charge
        return atom

    def create_environment_atom(self, position, charge, radius):
        """Create an environment atom"""
        color = self.charge_to_color(charge)

        circle = Circle(
            radius=radius,
            fill_color=color,
            fill_opacity=0.85,
            stroke_color=WHITE,
            stroke_width=2
        )
        circle.move_to(position)

        atom = VGroup(circle)
        atom.charge = charge
        return atom

    def calculate_polarization_charge(self, md_sim):
        """
        Calculate polarization-induced charge using Gaussian decay
        q = q_base + alpha * sum_i exp(-beta * r_i^2)
        """
        center_pos = md_sim.positions[0]
        polarization = 0

        for i in range(1, md_sim.n_atoms):
            r_vec = md_sim.positions[i] - center_pos
            distance = np.linalg.norm(r_vec)

            # Gaussian-like decay for smoother, more sensitive response
            polarization += np.exp(-self.distance_decay * distance**2)

        new_charge = self.base_charge + self.polarization_strength * polarization
        return np.clip(new_charge, self.min_charge, self.max_charge)

    def update_visuals(self):
        """Update visual positions and colors"""
        # Left side - update positions (including central atom), charges stay constant
        # Update central atom position (index 0)
        new_pos_left_central = self.center_left + self.md_left.positions[0]
        self.atom_left_central.move_to(new_pos_left_central)

        # Update environment atoms
        for i, atom in enumerate(self.atoms_left_env):
            new_pos = self.center_left + self.md_left.positions[i + 1]
            atom.move_to(new_pos)

        # Right side - update positions (including central atom) and central atom charge
        # Update central atom position (index 0)
        new_pos_right_central = self.center_right + self.md_right.positions[0]
        self.atom_right_central.move_to(new_pos_right_central)

        # Update environment atoms
        for i, atom in enumerate(self.atoms_right_env):
            new_pos = self.center_right + self.md_right.positions[i + 1]
            atom.move_to(new_pos)

        # Update charge of central atom on right side
        new_charge = self.calculate_polarization_charge(self.md_right)
        new_color = self.charge_to_color(new_charge)

        self.atom_right_central[1].set_fill(new_color)  # Main circle
        self.atom_right_central[0].set_fill(new_color)  # Glow

        # Update glow intensity based on charge
        glow_opacity = 0.15 + 0.25 * (new_charge / self.max_charge)
        self.atom_right_central[0].set_opacity(glow_opacity)

        # Update charge label
        self.charge_label_right.set_value(new_charge)

        # Update temperature labels
        self.temp_label_left.set_value(self.md_left.current_temperature)
        self.temp_label_right.set_value(self.md_right.current_temperature)

        # Update slider positions on charge scale
        # Left slider stays at base_charge (constant)
        arrow_size = 0.3
        y_pos_left = self.charge_to_y_position(self.base_charge)
        self.slider_left.move_to(np.array([self.scale_x - self.scale_width/2 - arrow_size/2, y_pos_left, 0]))

        # Right slider follows dynamic charge
        y_pos_right = self.charge_to_y_position(new_charge)
        self.slider_right.move_to(np.array([self.scale_x + self.scale_width/2 + arrow_size/2, y_pos_right, 0]))

    def run_simulation(self):
        """Run the molecular dynamics simulation"""
        frame_dt = 1/self.fps  # Animation frame rate
        frames = int(self.total_time / frame_dt)

        for frame in range(frames):
            # Run multiple MD steps per frame (all atoms can move now)
            self.md_left.run_steps(self.steps_per_frame, center_fixed=False)
            self.md_right.run_steps(self.steps_per_frame, center_fixed=False)

            # Update visual representation
            self.update_visuals()

            self.wait(frame_dt)


if __name__ == "__main__":
    # Run with:
    # manimgl polarization_forcefield.py PolarizationForceField
    pass
