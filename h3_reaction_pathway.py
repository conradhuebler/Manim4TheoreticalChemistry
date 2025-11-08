#!/usr/bin/env python3
"""
H₃ Reaction Pathway Animation
H + H₂ → [H₃]‡ → H₂ + H

Visualizes reaction coordinate with 2 minima and transition state.
Left: Reaction box with 3 H-atoms
Right: Energy profile along reaction coordinate
"""

from manimlib import *
import numpy as np

# Language setting - change to "EN" for English
LANGUAGE = "EN"

def get_string(key):
    """Get localized string"""
    strings = {
        "DE": {
            "title": "H₃ Reaktionspfad: H + H₂ → H₂ + H",
            "reaction_box": "Reaktionsbox",
            "energy_profile": "Energieprofil",
            "reactants": "Edukte: H + H₂",
            "transition_state": "Übergangszustand [H₃]‡",
            "products": "Produkte: H₂ + H",
            "reaction_coordinate": "Reaktionskoordinate",
            "energy_title": "Energie (eV)",
            "approaching": "Annäherung",
            "bond_breaking": "Bindungsbruch",
            "bond_forming": "Bindungsbildung",
            "separation": "Trennung",
            "morse_h12": "H¹-H² Bindung",
            "morse_h23": "H²-H³ Bindung",
            "h2_position": "H² Position (Å)",
            "force": "Kraft (eV/Å)",
            "force_zero": "F = 0",
            "reactant_label": "H¹-H² + H³",
            "ts_label": "[H₃]‡",
            "product_label": "H¹ + H²-H³",
            "reaction_complete": "Reaktion abgeschlossen:",
            "reaction_equation": "H¹-H² + H³ → H¹ + H²-H³",
            "saddle_point": "Sattelpunkt",
            "derivative_zero": "dE/dx = 0"
        },
        "EN": {
            "title": "H₃ Reaction Path: H + H₂ → H₂ + H",
            "reaction_box": "Reaction Box",
            "energy_profile": "Energy Profile",
            "reactants": "Reactants: H + H₂",
            "transition_state": "Transition State [H₃]‡",
            "products": "Products: H₂ + H",
            "reaction_coordinate": "Reaction Coordinate",
            "energy_title": "Energy (eV)",
            "approaching": "Approaching",
            "bond_breaking": "Bond Breaking",
            "bond_forming": "Bond Forming",
            "separation": "Separation",
            "morse_h12": "H¹-H² Bond",
            "morse_h23": "H²-H³ Bond",
            "h2_position": "H² Position (Å)",
            "force": "Force (eV/Å)",
            "force_zero": "F = 0",
            "reactant_label": "H¹-H² + H³",
            "ts_label": "[H₃]‡",
            "product_label": "H¹ + H²-H³",
            "reaction_complete": "Reaction complete:",
            "reaction_equation": "H¹-H² + H³ → H¹ + H²-H³",
            "saddle_point": "Saddle Point",
            "derivative_zero": "dE/dx = 0"
        }
    }
    return strings[LANGUAGE].get(key, key)

class H3ReactionPathway(Scene):
    """H₃ reaction pathway: H + H₂ → [H₃]‡ → H₂ + H

    GUI-compatible PARAMETERS structure for H₃ reaction pathway animation.
    """

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # ========================================================================
        # MORSE POTENTIAL PARAMETERS
        # ========================================================================
        "D_e": {
            "value": 4.478,
            "type": float,
            "unit": "eV",
            "description": "Morse potential well depth (H-H dissociation energy)",
            "min": 1.0,
            "max": 10.0
        },
        "r_e": {
            "value": 0.741,
            "type": float,
            "unit": "Å",
            "description": "H-H equilibrium bond distance",
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
        # ATOM PARAMETERS
        # ========================================================================
        "mass": {
            "value": 1.008,
            "type": float,
            "unit": "amu",
            "description": "Hydrogen atom mass",
            "min": 0.5,
            "max": 2.0
        },
        "temperature": {
            "value": 300,
            "type": int,
            "unit": "K",
            "description": "System temperature",
            "min": 100,
            "max": 1000
        },

        # ========================================================================
        # SIMULATION PARAMETERS
        # ========================================================================
        "dt": {
            "value": 0.05,
            "type": float,
            "unit": "fs",
            "description": "Time step for simulation",
            "min": 0.01,
            "max": 1.0
        },

        # ========================================================================
        # PHASE DURATION PARAMETERS
        # ========================================================================
        "phase2_steps": {
            "value": 60,
            "type": int,
            "unit": "steps",
            "description": "Phase 2 duration: H₂ approaching center",
            "min": 20,
            "max": 200
        },
        "phase2_wait": {
            "value": 0.08,
            "type": float,
            "unit": "s",
            "description": "Phase 2 animation frame wait time",
            "min": 0.01,
            "max": 0.5
        },
        "phase3_steps": {
            "value": 40,
            "type": int,
            "unit": "steps",
            "description": "Phase 3 duration: Transition state [H₃]‡",
            "min": 10,
            "max": 100
        },
        "phase3_wait": {
            "value": 0.1,
            "type": float,
            "unit": "s",
            "description": "Phase 3 animation frame wait time",
            "min": 0.01,
            "max": 0.5
        },
        "phase4_steps": {
            "value": 60,
            "type": int,
            "unit": "steps",
            "description": "Phase 4 duration: Bond breaking/forming",
            "min": 20,
            "max": 200
        },
        "phase4_wait": {
            "value": 0.08,
            "type": float,
            "unit": "s",
            "description": "Phase 4 animation frame wait time",
            "min": 0.01,
            "max": 0.5
        },

        # ========================================================================
        # ATOM POSITIONS (fixed positions for visualization)
        # ========================================================================
        "x_h1": {
            "value": -1.5,
            "type": float,
            "unit": "Å",
            "description": "H¹ fixed position (left)",
            "min": -3.0,
            "max": -0.5
        },
        "x_h3": {
            "value": 1.5,
            "type": float,
            "unit": "Å",
            "description": "H³ fixed position (right)",
            "min": 0.5,
            "max": 3.0
        },
        "x_h2_initial": {
            "value": -0.7,
            "type": float,
            "unit": "Å",
            "description": "H² initial position (starts near H¹)",
            "min": -1.5,
            "max": 0.0
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Physical parameters
        self.setup_parameters()

        # Data arrays (internal state, not parameters)
        self.reaction_coord_data = []
        self.energy_data = []
        self.r12_data = []  # H1-H2 distance
        self.r23_data = []  # H2-H3 distance

        # Time tracking (internal state)
        self.current_time = 0.0

    def setup_parameters(self):
        """Extract parameters from central PARAMETERS dictionary"""
        # Morse potential parameters
        self.D_e = self.PARAMETERS["D_e"]["value"]
        self.r_e = self.PARAMETERS["r_e"]["value"]
        self.alpha = self.PARAMETERS["alpha"]["value"]

        # Atom parameters
        self.mass = self.PARAMETERS["mass"]["value"]
        self.temperature = self.PARAMETERS["temperature"]["value"]

        # Simulation parameters
        self.dt = self.PARAMETERS["dt"]["value"]

        # Phase duration parameters
        self.phase2_steps = self.PARAMETERS["phase2_steps"]["value"]
        self.phase2_wait = self.PARAMETERS["phase2_wait"]["value"]
        self.phase3_steps = self.PARAMETERS["phase3_steps"]["value"]
        self.phase3_wait = self.PARAMETERS["phase3_wait"]["value"]
        self.phase4_steps = self.PARAMETERS["phase4_steps"]["value"]
        self.phase4_wait = self.PARAMETERS["phase4_wait"]["value"]

        # Atom positions
        self.x_h1 = self.PARAMETERS["x_h1"]["value"]
        self.x_h3 = self.PARAMETERS["x_h3"]["value"]
        self.x_h2 = self.PARAMETERS["x_h2_initial"]["value"]

    def construct(self):
        """Main animation sequence"""
        self.setup_layout()
        self.wait(1)

        self.phase_1_initial_state()
        self.wait(2)

        self.phase_2_approaching()
        self.wait(2)

        self.phase_3_transition_state()
        self.wait(2)

        self.phase_4_bond_breaking()
        self.wait(2)

        self.phase_5_products()
        self.wait(3)

    def setup_layout(self):
        """Setup 2-area layout: reaction box + energy profile"""
        # Title
        title = Text(get_string("title"), font_size=28)
        title.to_edge(UP, buff=0.15)
        self.play(Write(title))

        # Define areas - more horizontal separation
        self.reaction_center = LEFT * 3.8
        self.energy_center = RIGHT * 3.8

        # Setup reaction box
        self.setup_reaction_box()

        # Setup energy profile
        self.setup_energy_profile()

    def setup_reaction_box(self):
        """Setup reaction visualization area"""
        # Box boundary - smaller size
        box_width = 4.5
        box_height = 3.5

        self.reaction_box = Rectangle(
            width=box_width, height=box_height,
            stroke_color=WHITE, stroke_width=2, fill_opacity=0.05
        )
        self.reaction_box.move_to(self.reaction_center + DOWN * 0.3)

        # Box label
        box_label = Text(get_string("reaction_box"), font_size=20, color=YELLOW)
        box_label.next_to(self.reaction_box, UP, buff=0.15)

        self.play(ShowCreation(self.reaction_box), Write(box_label))

        # Create H-atoms
        self.create_h_atoms()

    def create_h_atoms(self):
        """Create 3 H-atom visualizations: H1 and H3 fixed, H2 mobile"""
        # H1 atom (left, FIXED)
        self.h1_nucleus = Circle(radius=0.12, color=RED, fill_opacity=0.8)
        self.h1_label = Text("H¹", font_size=30, color=WHITE)

        # H2 atom (mobile, starts near H1)
        self.h2_nucleus = Circle(radius=0.12, color=GREEN, fill_opacity=0.8)
        self.h2_label = Text("H²", font_size=30, color=WHITE)

        # H3 atom (right, FIXED)
        self.h3_nucleus = Circle(radius=0.12, color=BLUE, fill_opacity=0.8)
        self.h3_label = Text("H³", font_size=30, color=WHITE)

        # Set initial positions manually (use direct x-coordinates)
        scale = 0.8
        h1_pos = self.reaction_center + np.array([self.x_h1 * scale, 0, 0])
        h2_pos = self.reaction_center + np.array([self.x_h2 * scale, 0, 0])
        h3_pos = self.reaction_center + np.array([self.x_h3 * scale, 0, 0])

        self.h1_nucleus.move_to(h1_pos)
        self.h1_label.move_to(h1_pos + DOWN * 0.3)
        self.h2_nucleus.move_to(h2_pos)
        self.h2_label.move_to(h2_pos + DOWN * 0.3)
        self.h3_nucleus.move_to(h3_pos)
        self.h3_label.move_to(h3_pos + DOWN * 0.3)

        # Bonds (initially H1-H2 strong, H2-H3 weak)
        self.bond_h12 = Line(
            self.h1_nucleus.get_center(),
            self.h2_nucleus.get_center(),
            color=GREEN, stroke_width=4
        )

        self.bond_h23 = Line(
            self.h2_nucleus.get_center(),
            self.h3_nucleus.get_center(),
            color=ORANGE, stroke_width=1, stroke_opacity=0.3
        )

        # Add to scene
        self.add(self.bond_h12, self.bond_h23)

        # Show atoms
        self.play(
            ShowCreation(self.h1_nucleus), Write(self.h1_label),
            ShowCreation(self.h2_nucleus), Write(self.h2_label),
            ShowCreation(self.h3_nucleus), Write(self.h3_label),
            ShowCreation(self.bond_h12), ShowCreation(self.bond_h23)
        )

    def update_atom_positions(self):
        """Update positions: H1 and H3 fixed, only H2 moves"""
        scale = 0.8  # Visual scaling

        # Use direct x-coordinates (no LEFT/RIGHT confusion)
        h1_pos = self.reaction_center + np.array([self.x_h1 * scale, 0, 0])
        h2_pos = self.reaction_center + np.array([self.x_h2 * scale, 0, 0])
        h3_pos = self.reaction_center + np.array([self.x_h3 * scale, 0, 0])

        # Move atoms
        self.h1_nucleus.move_to(h1_pos)
        self.h1_label.move_to(h1_pos + DOWN * 0.3)

        self.h2_nucleus.move_to(h2_pos)
        self.h2_label.move_to(h2_pos + DOWN * 0.3)

        self.h3_nucleus.move_to(h3_pos)
        self.h3_label.move_to(h3_pos + DOWN * 0.3)

        # Update bonds if they exist
        if hasattr(self, 'bond_h12'):
            self.bond_h12.put_start_and_end_on(
                self.h1_nucleus.get_center(),
                self.h2_nucleus.get_center()
            )

        if hasattr(self, 'bond_h23'):
            self.bond_h23.put_start_and_end_on(
                self.h2_nucleus.get_center(),
                self.h3_nucleus.get_center()
            )

    def setup_energy_profile(self):
        """Setup dual plots: energy and force vs reaction coordinate"""
        # Energy plot (top)
        self.energy_axes = Axes(
            x_range=(-0.8, 0.8, 0.4),  # H2 position
            y_range=(0, 2, 0.5),  # Energy in eV (normalized)
            height=2.4,
            width=5.5,
            axis_config={
                "stroke_color": GREY,
                "stroke_width": 1,
                "include_tip": True,
            }
        )
        self.energy_axes.move_to(self.energy_center + UP * 1.5)

        # Force plot (bottom) - first derivative
        self.force_axes = Axes(
            x_range=(-0.8, 0.8, 0.4),  # H2 position (same as energy)
            y_range=(-3, 3, 1),  # Force in eV/Å
            height=2.4,
            width=5.5,
            axis_config={
                "stroke_color": GREY,
                "stroke_width": 1,
                "include_tip": True,
            }
        )
        self.force_axes.move_to(self.energy_center + DOWN * 1.5)

        # Labels
        energy_y_label = Text(get_string("energy_title"), font_size=24)
        energy_y_label.next_to(self.energy_axes, LEFT, buff=0.15)

        force_x_label = Text(get_string("h2_position"), font_size=24)
        force_x_label.next_to(self.force_axes, DOWN, buff=0.15)

        force_y_label = Text(get_string("force"), font_size=24)
        force_y_label.next_to(self.force_axes, LEFT, buff=0.15)

        # Zero line for force
        self.force_zero_line = Line(
            self.force_axes.coords_to_point(-0.8, 0),
            self.force_axes.coords_to_point(0.8, 0),
            color=WHITE, stroke_width=1, stroke_opacity=0.5
        )

        self.play(
            ShowCreation(self.energy_axes),
            ShowCreation(self.force_axes),
            ShowCreation(self.force_zero_line),
            Write(energy_y_label),
            Write(force_x_label),
            Write(force_y_label)
        )

        # Create both curves
        self.create_energy_and_force_curves()

        # Current position markers
        self.energy_dot = Dot(radius=0.08, color=RED)
        self.force_dot = Dot(radius=0.08, color=BLUE)
        self.update_both_dots()

        self.play(ShowCreation(self.energy_dot), ShowCreation(self.force_dot))

    def calculate_numerical_derivative(self, x_h2, dx=0.01):
        """Calculate numerical derivative dE/dx (force = -dE/dx)"""
        if x_h2 - dx < -0.8:
            # Forward difference at left boundary
            return -(self.calculate_total_energy(x_h2 + dx) - self.calculate_total_energy(x_h2)) / dx
        elif x_h2 + dx > 0.8:
            # Backward difference at right boundary
            return -(self.calculate_total_energy(x_h2) - self.calculate_total_energy(x_h2 - dx)) / dx
        else:
            # Central difference
            return -(self.calculate_total_energy(x_h2 + dx) - self.calculate_total_energy(x_h2 - dx)) / (2 * dx)

    def create_energy_and_force_curves(self):
        """Create both energy and force curves"""
        # X-axis: position of H2 from -0.8 to +0.8
        x_h2_values = np.linspace(-0.8, 0.8, 200)
        energy_values = []
        force_values = []

        for x_h2 in x_h2_values:
            energy = self.calculate_total_energy(x_h2)
            force = self.calculate_numerical_derivative(x_h2)
            energy_values.append(energy)
            force_values.append(force)

        # Normalize energies (shift minimum to zero)
        min_energy = min(energy_values)
        max_energy = max(energy_values)
        energy_values = [(E - min_energy) * 2.0 / (max_energy - min_energy) for E in energy_values]

        # Store for later use
        self.x_h2_values = x_h2_values
        self.energy_values = energy_values
        self.force_values = force_values
        self.min_energy_ref = min_energy
        self.max_energy_ref = max_energy

        # Create energy curve
        energy_points = [
            self.energy_axes.coords_to_point(x_h2, min(max(E, 0), 2))
            for x_h2, E in zip(x_h2_values, energy_values)
        ]

        self.energy_profile_curve = VMobject(color=BLUE, stroke_width=3)
        self.energy_profile_curve.set_points_as_corners(energy_points)

        # Create force curve
        force_points = [
            self.force_axes.coords_to_point(x_h2, min(max(F, -3), 3))
            for x_h2, F in zip(x_h2_values, force_values)
        ]

        self.force_curve = VMobject(color=GREEN, stroke_width=3)
        self.force_curve.set_points_as_corners(force_points)

        self.play(
            ShowCreation(self.energy_profile_curve),
            ShowCreation(self.force_curve)
        )

        # Find and label key points on energy plot
        min_idx_left = np.argmin(energy_values[:80])  # Left minimum
        min_idx_right = np.argmin(energy_values[120:]) + 120  # Right minimum

        # TS at exact symmetry point (not array lookup)
        ts_x_h2 = 0.0
        ts_energy_raw = self.calculate_total_energy(ts_x_h2)
        ts_energy_norm = (ts_energy_raw - self.min_energy_ref) * 2.0 / (self.max_energy_ref - self.min_energy_ref)

        reactant_label = Text(get_string("reactant_label"), font_size=20, color=GREEN)
        reactant_label.move_to(self.energy_axes.coords_to_point(x_h2_values[min_idx_left], energy_values[min_idx_left] + 0.35))

        ts_label = Text(get_string("ts_label"), font_size=20, color=ORANGE)
        ts_label.move_to(self.energy_axes.coords_to_point(ts_x_h2, ts_energy_norm + 0.3))

        product_label = Text(get_string("product_label"), font_size=20, color=GREEN)
        product_label.move_to(self.energy_axes.coords_to_point(x_h2_values[min_idx_right], energy_values[min_idx_right] + 0.35))

        # Add force equilibrium labels
        force_eq_label = Text(get_string("force_zero"), font_size=20, color=YELLOW)
        force_eq_label.move_to(self.force_axes.coords_to_point(0, -2.8))

        # Annotate saddle point on energy plot
        saddle_dot = Dot(
            self.energy_axes.coords_to_point(ts_x_h2, ts_energy_norm),
            color=ORANGE, radius=0.10
        )

        saddle_annotation = Text(get_string("saddle_point"), font_size=18, color=ORANGE)
        saddle_annotation.next_to(saddle_dot, RIGHT, buff=0.15)

        # Draw vertical dashed line connecting energy maximum to force zero crossing
        ts_x_pos = ts_x_h2
        connection_line = DashedLine(
            self.energy_axes.coords_to_point(ts_x_pos, 0),
            self.force_axes.coords_to_point(ts_x_pos, 0),
            color=ORANGE, stroke_width=2, dash_length=0.1
        )

        # Mark zero crossing on force plot
        force_zero_dot = Dot(
            self.force_axes.coords_to_point(ts_x_pos, 0),
            color=ORANGE, radius=0.10
        )

        derivative_label = Text(get_string("derivative_zero"), font_size=18, color=ORANGE)
        derivative_label.next_to(force_zero_dot, RIGHT, buff=0.15)

        # Store for animation updates
        self.saddle_dot = saddle_dot
        self.force_zero_dot = force_zero_dot
        self.connection_line = connection_line

        self.play(
            Write(reactant_label),
            Write(ts_label),
            Write(product_label),
            Write(force_eq_label)
        )

        # Add saddle point annotations
        self.play(
            ShowCreation(saddle_dot),
            Write(saddle_annotation),
            ShowCreation(connection_line),
            ShowCreation(force_zero_dot),
            Write(derivative_label)
        )

    def calculate_total_energy(self, x_h2):
        """Calculate total energy for given H2 position"""
        # Calculate distances
        r12 = abs(x_h2 - self.x_h1)  # H1-H2 distance
        r23 = abs(self.x_h3 - x_h2)  # H2-H3 distance
        r13 = abs(self.x_h3 - self.x_h1)  # H1-H3 distance (constant = 3.0)

        # Sum of three Morse potentials
        V12 = self.morse_potential(r12)
        V23 = self.morse_potential(r23)
        V13 = self.morse_potential(r13)

        return V12 + V23 + V13

    def morse_potential(self, r):
        """Standard Morse potential"""
        if r < 0.3:
            return 10.0  # Repulsive wall
        r = max(0.3, min(4.0, r))
        arg = -self.alpha * (r - self.r_e)
        if abs(arg) > 20:
            return 10.0 if arg < 0 else -self.D_e
        exp_term = np.exp(arg)
        return self.D_e * (1 - exp_term)**2 - self.D_e

    def get_current_energy(self):
        """Get current total energy for H2 position"""
        return self.calculate_total_energy(self.x_h2)

    def update_both_dots(self):
        """Update positions of both energy and force dots"""
        current_energy = self.get_current_energy()
        current_force = self.calculate_numerical_derivative(self.x_h2)

        # Normalize energy (same as curve)
        normalized_energy = (current_energy - self.min_energy_ref) * 2.0 / (self.max_energy_ref - self.min_energy_ref)
        display_energy = min(max(normalized_energy, 0), 2)

        # Clamp force for display
        display_force = min(max(current_force, -3), 3)

        # Update energy dot
        energy_dot_pos = self.energy_axes.coords_to_point(self.x_h2, display_energy)
        self.energy_dot.move_to(energy_dot_pos)

        # Update force dot
        force_dot_pos = self.force_axes.coords_to_point(self.x_h2, display_force)
        self.force_dot.move_to(force_dot_pos)

    def update_energy_dot(self):
        """Legacy function - redirects to update_both_dots"""
        self.update_both_dots()

    def phase_1_initial_state(self):
        """Phase 1: Initial state - H2 near H1"""
        phase_label = Text(get_string("reactant_label"), font_size=26, color=YELLOW)
        phase_label.move_to(self.reaction_center + UP * 2.3)
        self.play(Write(phase_label))
        self.current_phase_label = phase_label

        # H2 starts at x = -0.7 (near H1)
        self.x_h2 = -0.7
        self.update_atom_positions()
        self.update_energy_dot()

        # Store initial data
        self.reaction_coord_data.append(self.x_h2)
        self.energy_data.append(self.get_current_energy())

        self.wait(1)

    def phase_2_approaching(self):
        """Phase 2: H2 moves toward center"""
        phase_label = Text(get_string("approaching"), font_size=26, color=YELLOW)
        phase_label.move_to(self.reaction_center + UP * 2.3)
        self.play(Transform(self.current_phase_label, phase_label))

        # Move H2 from -0.7 to -0.1 (approaching center)
        for step in range(self.phase2_steps):
            progress = step / 60
            self.x_h2 = -0.7 + 0.6 * progress

            # Update bond strengths based on distances
            r12 = abs(self.x_h2 - self.x_h1)
            r23 = abs(self.x_h3 - self.x_h2)

            # H1-H2 bond weakens, H2-H3 bond strengthens
            h12_strength = max(0.2, 1.0 - progress)
            h23_strength = min(1.0, 0.3 + progress * 0.7)

            self.bond_h12.set_stroke(width=4 * h12_strength)
            self.bond_h23.set_stroke(width=4 * h23_strength, opacity=h23_strength)

            # Update visualization
            self.update_atom_positions()
            self.update_energy_dot()

            # Store data
            self.reaction_coord_data.append(self.x_h2)
            self.energy_data.append(self.get_current_energy())

            if step % 5 == 0:
                self.wait(self.phase2_wait)

    def phase_3_transition_state(self):
        """Phase 3: Transition state [H3]‡"""
        phase_label = Text(get_string("ts_label"), font_size=26, color=ORANGE)
        phase_label.move_to(self.reaction_center + UP * 2.3)
        self.play(Transform(self.current_phase_label, phase_label))

        # Move H2 from -0.1 to +0.1 (through transition state)
        for step in range(self.phase3_steps):
            progress = step / 40
            self.x_h2 = -0.1 + 0.1 * progress

            # At transition state: both bonds equally weak
            bond_strength = 0.5  # Both bonds equally weak

            self.bond_h12.set_stroke(width=4 * bond_strength, opacity=bond_strength)
            self.bond_h23.set_stroke(width=4 * bond_strength, opacity=bond_strength)

            # Update visualization
            self.update_atom_positions()
            self.update_energy_dot()

            # Store data
            self.reaction_coord_data.append(self.x_h2)
            self.energy_data.append(self.get_current_energy())

            if step % 3 == 0:
                self.wait(self.phase3_wait)

        # Pause at transition state
        self.wait(1)

    def phase_4_bond_breaking(self):
        """Phase 4: H1-H2 bond breaks, H2-H3 bond forms"""
        phase_label = Text(get_string("bond_forming"), font_size=26, color=GREEN)
        phase_label.move_to(self.reaction_center + UP * 2.3)
        self.play(Transform(self.current_phase_label, phase_label))

        # Move H2 from +0.1 to +0.7 (toward H3)
        for step in range(self.phase4_steps):
            progress = step / 60
            self.x_h2 = 0.1 + 0.6 * progress

            # H1-H2 bond weakens, H2-H3 bond strengthens
            h12_strength = max(0.1, 0.5 - progress * 0.4)
            h23_strength = min(1.0, 0.5 + progress * 0.5)

            self.bond_h12.set_stroke(width=4 * h12_strength, opacity=h12_strength)
            self.bond_h23.set_stroke(width=4 * h23_strength, opacity=h23_strength)

            # Update visualization
            self.update_atom_positions()
            self.update_energy_dot()

            # Store data
            self.reaction_coord_data.append(self.x_h2)
            self.energy_data.append(self.get_current_energy())

            if step % 5 == 0:
                self.wait(self.phase4_wait)

    def phase_5_products(self):
        """Phase 5: Final products H1 + H2-H3"""
        phase_label = Text(get_string("product_label"), font_size=26, color=GREEN)
        phase_label.move_to(self.reaction_center + UP * 2.3)
        self.play(Transform(self.current_phase_label, phase_label))

        # Final positioning and bond adjustment
        self.x_h2 = 0.7  # Final position near H3

        # Final bond states: H1-H2 very weak, H2-H3 strong
        self.bond_h12.set_stroke(width=0.5, opacity=0.1)
        self.bond_h23.set_stroke(width=4, opacity=1.0)

        self.update_atom_positions()
        self.update_energy_dot()

        # Store final data
        self.reaction_coord_data.append(self.x_h2)
        self.energy_data.append(self.get_current_energy())

        self.wait(1)

        # Summary
        summary = VGroup(
            Text(get_string("reaction_complete"), font_size=24, color=YELLOW),
            Text(get_string("reaction_equation"), font_size=24, color=WHITE)
        ).arrange(DOWN, buff=0.15)
        summary.move_to(self.reaction_center + DOWN * 2.5)
        self.play(Write(summary))

# Scene class for ManimGL
class H3ReactionPathway(H3ReactionPathway):
    pass