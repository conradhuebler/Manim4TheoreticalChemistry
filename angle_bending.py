#!/usr/bin/env python3
"""
Angle Bending Potential Visualization
Visualisierung des harmonischen Winkelpotentials

Shows how bond angles behave with harmonic potential:
- Left: Three atoms (C-C-C) with variable angle
- Right: Angular harmonic potential V = 1/2 k(θ-θ₀)²

Animation demonstrates angle bending with real-time
energy tracking on the potential curve.
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "EN"  # Set to "EN" for English

STRINGS = {
    "DE": {
        "title": "Winkelverbiegung: Harmonisches Winkelpotential",
        "molecule_view": "Molekülmodell",
        "potential_curve": "Potentialenergie-Kurve",
        "bond_angle": "Bindungswinkel θ (°)",
        "energy": "Energie (kcal/mol)",
        "equilibrium": "Gleichgewicht (tetraedrisch)",
        "compressed": "Komprimiert",
        "expanded": "Geweitet",
        "force_constant": "Kraftkonstante k",
        "eq_angle": "Gleichgewichtswinkel θ₀",
        "current_angle": "Aktueller Winkel",
        "harmonic_formula": r"V = \frac{1}{2}k(\theta-\theta_0)^2",
        "tetrahedral": "109.5°",
    },
    "EN": {
        "title": "Angle Bending: Harmonic Angular Potential",
        "molecule_view": "Molecular Model",
        "potential_curve": "Potential Energy Curve",
        "bond_angle": "Bond Angle θ (°)",
        "energy": "Energy (kcal/mol)",
        "equilibrium": "Equilibrium (tetrahedral)",
        "compressed": "Compressed",
        "expanded": "Expanded",
        "force_constant": "Force Constant k",
        "eq_angle": "Equilibrium Angle θ₀",
        "current_angle": "Current Angle",
        "harmonic_formula": r"V = \frac{1}{2}k(\theta-\theta_0)^2",
        "tetrahedral": "109.5°",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class AngleBending(Scene):
    def construct(self):
        # Angle parameters (typical C-C-C angle)
        self.k_angle = 58.0  # kcal/(mol·rad²) - force constant
        self.theta0_deg = 109.5  # degrees - tetrahedral angle
        self.theta0_rad = np.radians(self.theta0_deg)

        # Animation parameters
        self.amplitude_deg = 25.0  # degrees - oscillation amplitude
        self.frequency = 0.5  # Hz
        self.bond_length = 1.5  # Å - for visualization

        # Setup layout
        self.setup_layout()

        # Create molecular view
        self.create_molecule()

        # Create potential curve
        self.create_potential_curve()

        # Run animation
        self.animate_bending()

        self.wait(2)

    def setup_layout(self):
        """Create two-panel layout"""
        # Title
        title = Text(get_string("title"), color=YELLOW).scale(0.65)
        title.to_edge(UP, buff=0.3)
        self.add(title)

        # Dividing line
        divider = Line(UP * 3.5 + LEFT * 0.1, DOWN * 3.5 + LEFT * 0.1,
                      stroke_width=2, color=WHITE)
        self.add(divider)

        # Panel labels
        mol_label = Text(get_string("molecule_view"), color=BLUE_C).scale(0.5)
        mol_label.move_to(LEFT * 3.5 + UP * 3.2)

        pot_label = Text(get_string("potential_curve"), color=GREEN_C).scale(0.5)
        pot_label.move_to(RIGHT * 3.5 + UP * 3.2)

        self.add(mol_label, pot_label)

    def create_molecule(self):
        """Create three-atom molecule (C-C-C) with variable angle"""
        # Center position
        self.mol_center = LEFT * 3.5 + DOWN * 0.5

        # Create three atoms
        self.atom_left = self.create_atom("C₁", GREY_BROWN, radius=0.35)
        self.atom_center = self.create_atom("C₂", GREY_BROWN, radius=0.35)
        self.atom_right = self.create_atom("C₃", GREY_BROWN, radius=0.35)

        # Create bonds
        self.bond_left = Line(LEFT, RIGHT, stroke_width=6, color=WHITE)
        self.bond_right = Line(LEFT, RIGHT, stroke_width=6, color=WHITE)

        # Create angle arc
        self.angle_arc = Arc(
            radius=0.8,
            start_angle=0,
            angle=PI/2,
            color=YELLOW,
            stroke_width=3
        )

        # Create angle label
        self.angle_label = DecimalNumber(
            self.theta0_deg, num_decimal_places=1, color=YELLOW, unit="°"
        ).scale(0.6)

        # Position at equilibrium
        self.update_molecule_positions(self.theta0_deg)

        # Add to scene
        self.molecule_group = VGroup(
            self.bond_left, self.bond_right,
            self.atom_left, self.atom_center, self.atom_right,
            self.angle_arc
        )
        self.add(self.molecule_group, self.angle_label)

        # Add equilibrium marker
        eq_text = Text(get_string("equilibrium"), color=GREEN).scale(0.4)
        eq_text.move_to(self.mol_center + DOWN * 2.5)
        self.eq_marker = eq_text
        self.add(self.eq_marker)

    def create_atom(self, label_text, color, radius=0.3):
        """Create an atom with label"""
        circle = Circle(radius=radius, fill_color=color, fill_opacity=1.0,
                       stroke_color=WHITE, stroke_width=2)
        label = Text(label_text, color=WHITE).scale(0.35)
        atom = VGroup(circle, label)
        return atom

    def update_molecule_positions(self, theta_degrees):
        """Update atom positions based on angle"""
        theta_rad = np.radians(theta_degrees)

        # Center atom stays at mol_center
        self.atom_center.move_to(self.mol_center)

        # Calculate positions for left and right atoms
        # Place them symmetrically around horizontal axis (pointing right)
        # angle_left - angle_right = theta_rad (the actual bond angle)

        # Left atom: above horizontal by theta_rad/2
        angle_left = theta_rad/2
        pos_left = self.mol_center + self.bond_length * np.array([
            np.cos(angle_left), np.sin(angle_left), 0
        ])
        self.atom_left.move_to(pos_left)

        # Right atom: below horizontal by theta_rad/2
        angle_right = -theta_rad/2
        pos_right = self.mol_center + self.bond_length * np.array([
            np.cos(angle_right), np.sin(angle_right), 0
        ])
        self.atom_right.move_to(pos_right)

        # Update bonds
        self.bond_left.put_start_and_end_on(self.mol_center, pos_left)
        self.bond_right.put_start_and_end_on(self.mol_center, pos_right)

        # Update angle arc
        self.remove(self.angle_arc)
        self.angle_arc = Arc(
            radius=0.8,
            start_angle=angle_right,
            angle=theta_rad,
            color=YELLOW,
            stroke_width=3
        ).move_arc_center_to(self.mol_center)
        self.add(self.angle_arc)

        # Update angle label
        self.angle_label.set_value(theta_degrees)
        # Position label inside the arc (at the midpoint angle = 0 for symmetric arrangement)
        label_angle = 0  # Midpoint between angle_left and angle_right
        label_pos = self.mol_center + 1.4 * np.array([
            np.cos(label_angle), np.sin(label_angle), 0
        ])
        self.angle_label.move_to(label_pos)

    def create_potential_curve(self):
        """Create harmonic angular potential energy curve"""
        # Create axes
        self.axes = Axes(
            x_range=[0, 160, 20],     # Angle in degrees
            y_range=[0, 40, 10],       # Energy in kcal/mol
            width=6,
            height=5,
            axis_config={"include_tip": True},
        )
        self.axes.move_to(RIGHT * 3.5 + DOWN * 0.3)

        get_x_axis = self.axes.get_x_axis()
        get_x_axis.add_numbers(font_size=20)

        get_y_axis = self.axes.get_y_axis()
        get_y_axis.add_numbers(font_size=20)
        # Axis labels
        x_label = Text(get_string("bond_angle"), color=WHITE).scale(0.35)
        x_label.next_to(self.axes.get_x_axis(), DOWN, buff=0.3)

        y_label = Text(get_string("energy"), color=WHITE).scale(0.35)
        y_label.next_to(self.axes.get_y_axis(), LEFT, buff=-0.75)
        y_label.rotate(90 * DEGREES)

        self.add(self.axes, x_label, y_label)

        # Plot harmonic angular potential
        self.potential_graph = self.axes.get_graph(
            lambda theta_deg: self.angular_potential(theta_deg),
            x_range=[60, 160],
            color=BLUE
        )
        self.add(self.potential_graph)

        # Mark equilibrium position
        eq_point = self.axes.coords_to_point(self.theta0_deg, 0)
        eq_dot = Dot(eq_point, color=GREEN, radius=0.08)
        eq_line = DashedLine(
            self.axes.coords_to_point(self.theta0_deg, 0),
            self.axes.coords_to_point(self.theta0_deg, 20),
            stroke_width=2,
            color=GREEN,
            dash_length=0.1
        )
        eq_label = Text(get_string("tetrahedral"), color=GREEN).scale(0.35)
        eq_label.next_to(eq_line, UP, buff=0.1)

        self.add(eq_line, eq_dot, eq_label)

        # Create moving dot to show current position
        self.current_dot = Dot(eq_point, color=RED, radius=0.1)
        self.add(self.current_dot)

        # Add formula
        formula = Tex(get_string("harmonic_formula"), color=YELLOW).scale(0.6)
        formula.move_to(self.axes.get_top() + UP * 0.2)
        self.add(formula)

        # Add parameter info
        params = VGroup(
            Tex(f"k = {self.k_angle:.0f}~\\text{{kcal/(mol·rad²)}}", color=WHITE).scale(0.4),
            Tex(f"\\theta_0 = {self.theta0_deg:.1f}°", color=WHITE).scale(0.4)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        params.move_to(self.axes.get_corner(UR) + LEFT * 1.5 + DOWN * 0.5)
        #self.add(params)

    def angular_potential(self, theta_degrees):
        """Calculate harmonic angular potential energy"""
        theta_rad = np.radians(theta_degrees)
        return 0.5 * self.k_angle * (theta_rad - self.theta0_rad)**2

    def animate_bending(self):
        """Animate angle bending with sinusoidal motion"""
        duration = 8.0  # seconds
        fps = 30
        frames = int(duration * fps)

        for frame in range(frames):
            t = frame / fps

            # Calculate current angle (sinusoidal oscillation)
            theta_current = self.theta0_deg + self.amplitude_deg * np.sin(
                2 * np.pi * self.frequency * t
            )

            # Update molecule
            self.update_molecule_positions(theta_current)

            # Update angle label display
            self.remove(self.angle_label)
            self.angle_label = DecimalNumber(
                theta_current, num_decimal_places=1, color=YELLOW
            ).scale(0.6)
            # Label at midpoint of symmetric arrangement (horizontal center)
            label_angle = 0
            label_pos = self.mol_center + 1.4 * np.array([
                np.cos(label_angle), np.sin(label_angle), 0
            ])
            self.angle_label.move_to(label_pos)
            self.add(self.angle_label)

            # Update dot on potential curve
            energy = self.angular_potential(theta_current)
            point = self.axes.coords_to_point(theta_current, energy)
            self.current_dot.move_to(point)

            # Update state labels
            if frame % 10 == 0:  # Update every 2 seconds
                if hasattr(self, 'state_label'):
                    self.remove(self.state_label)

                if theta_current < self.theta0_deg - 5:
                    state = get_string("compressed")
                    color = RED
                elif theta_current > self.theta0_deg + 5:
                    state = get_string("expanded")
                    color = ORANGE
                else:
                    state = get_string("equilibrium")
                    color = GREEN

                self.state_label = Text(state, color=color).scale(0.5)
                self.state_label.move_to(self.mol_center + DOWN * 3.0)
                self.add(self.state_label)

            self.wait(1/fps)


if __name__ == "__main__":
    # Run with: manimgl angle_bending.py AngleBending
    pass
