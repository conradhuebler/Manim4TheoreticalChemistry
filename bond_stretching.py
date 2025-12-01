#!/usr/bin/env python3
"""
Bond Stretching Potential Visualization
Visualisierung des harmonischen Bindungspotentials

Shows how a chemical bond behaves like a spring:
- Left: Two atoms connected by a bond
- Right: Harmonic potential energy curve V = 1/2 k(r-r₀)²

Animation demonstrates stretching and compression with real-time
energy tracking on the potential curve.
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "EN"  # Set to "EN" for English

STRINGS = {
    "DE": {
        "title": "Bindungsstreckung: Harmonisches Potential",
        "molecule_view": "Molekülmodell",
        "potential_curve": "Potentialenergie-Kurve",
        "bond_length": "Bindungslänge r (Å)",
        "energy": "Energie (kcal/mol)",
        "equilibrium": "Gleichgewicht",
        "compressed": "Gestaucht",
        "stretched": "Gestreckt",
        "force_constant": "Kraftkonstante k",
        "eq_distance": "Gleichgewichtsabstand r₀",
        "current_energy": "Aktuelle Energie",
        "harmonic_formula": r"V = \frac{1}{2}k(r-r_0)^2",
    },
    "EN": {
        "title": "Bond Stretching: Harmonic Potential",
        "molecule_view": "Molecular Model",
        "potential_curve": "Potential Energy Curve",
        "bond_length": "Bond Length r (Å)",
        "energy": "Energy (kcal/mol)",
        "equilibrium": "Equilibrium",
        "compressed": "Compressed",
        "stretched": "Stretched",
        "force_constant": "Force Constant k",
        "eq_distance": "Equilibrium Distance r₀",
        "current_energy": "Current Energy",
        "harmonic_formula": r"V = \frac{1}{2}k(r-r_0)^2",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class BondStretching(Scene):
    """Bond stretching animation with harmonic potential V = 1/2 k(r-r₀)²."""

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # Physical parameters
        "k": {
            "value": 1000.0,
            "type": float,
            "unit": "kcal/(mol·Å²)",
            "description": "Force constant for harmonic potential (typical C-C single bond)",
            "min": 0.0,
            "max": 1000.0
        },
        "r0": {
            "value": 1.54,
            "type": float,
            "unit": "Å",
            "description": "Equilibrium bond length (C-C single bond)",
            "min": 0.5,
            "max": 3.0
        },
        # Animation parameters
        "amplitude": {
            "value": 0.4,
            "type": float,
            "unit": "Å",
            "description": "Oscillation amplitude for bond stretching",
            "min": 0.1,
            "max": 1.0
        },
        "frequency": {
            "value": 1.0,
            "type": float,
            "unit": "Hz",
            "description": "Oscillation frequency",
            "min": 0.1,
            "max": 5.0
        },
        "scale_factor": {
            "value": 2.0,
            "type": float,
            "unit": "-",
            "description": "Visual scaling factor for molecule display",
            "min": 0.5,
            "max": 5.0
        },
        "duration": {
            "value": 10.0,
            "type": float,
            "unit": "s",
            "description": "Total animation duration",
            "min": 1.0,
            "max": 60.0
        },
        "fps": {
            "value": 60,
            "type": int,
            "unit": "frames/s",
            "description": "Frames per second for animation",
            "min": 10,
            "max": 120
        }
    }

    def construct(self):
        # Extract parameters from central dictionary
        self.k = self.PARAMETERS["k"]["value"]
        self.r0 = self.PARAMETERS["r0"]["value"]
        self.amplitude = self.PARAMETERS["amplitude"]["value"]
        self.frequency = self.PARAMETERS["frequency"]["value"]
        self.scale_factor = self.PARAMETERS["scale_factor"]["value"]

        # Setup layout
        self.setup_layout()

        # Create molecular view
        self.create_molecule()

        # Create potential curve
        self.create_potential_curve()

        # Run animation
        self.animate_stretching()

        self.wait(2)

    def setup_layout(self):
        """Create two-panel layout"""
        # Title
        title = Text(get_string("title"), color=YELLOW).scale(0.7)
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
        """Create two-atom molecule visualization"""
        # Store initial center position
        self.mol_center = LEFT * 3.5 + DOWN * 0.5

        # Create atoms (C-C bond example)
        self.atom1 = self.create_atom("C₁", GREY_BROWN, radius=0.4)
        self.atom2 = self.create_atom("C₂", GREY_BROWN, radius=0.4)

        # Create bond (as a spring-like line)
        self.bond_line = Line(LEFT, RIGHT, stroke_width=8, color=WHITE)

        # Create distance label
        self.distance_label = DecimalNumber(
            self.r0, num_decimal_places=2, color=YELLOW
        ).scale(0.6)

        # Position everything at equilibrium
        self.update_molecule_positions(self.r0)

        # Add to scene
        self.molecule_group = VGroup(self.atom1, self.atom2, self.bond_line)
        self.add(self.molecule_group, self.distance_label)

        # Add equilibrium marker
        eq_text = Text(get_string("equilibrium"), color=GREEN).scale(0.4)
        eq_text.move_to(self.mol_center + DOWN * 2.0)
        eq_arrow = Arrow(eq_text.get_top(), self.mol_center + DOWN * 0.8,
                        stroke_width=2, color=GREEN)
        self.eq_marker = VGroup(eq_text, eq_arrow)
        self.add(self.eq_marker)

    def create_atom(self, label_text, color, radius=0.3):
        """Create an atom with label"""
        circle = Circle(radius=radius, fill_color=color, fill_opacity=1.0,
                       stroke_color=WHITE, stroke_width=2)
        label = Text(label_text, color=WHITE).scale(0.4)
        atom = VGroup(circle, label)
        return atom

    def update_molecule_positions(self, bond_length):
        """Update atom positions based on bond length"""
        scaled_length = bond_length * self.scale_factor

        # Position atoms symmetrically around center
        self.atom1.move_to(self.mol_center + LEFT * scaled_length / 2)
        self.atom2.move_to(self.mol_center + RIGHT * scaled_length / 2)

        # Update bond line
        self.bond_line.put_start_and_end_on(
            self.atom1.get_center(),
            self.atom2.get_center()
        )

        # Update distance label
        self.distance_label.set_value(bond_length)
        self.distance_label.move_to(self.mol_center + UP * 0.8)

    def create_potential_curve(self):
        """Create harmonic potential energy curve"""
        # Create axes
        self.axes = Axes(
            x_range=[0, 2.5, 0.5],  # Bond length in Å
            y_range=[0, 50, 10],       # Energy in kcal/mol
            width=6,
            height=5,
            axis_config={"include_tip": True},
        )
        self.axes.move_to(RIGHT * 3.5 + DOWN * 0.3)

        get_x_axis = self.axes.get_x_axis()
        get_x_axis.add_numbers(font_size=20, num_decimal_places=1)

        get_y_axis = self.axes.get_y_axis()
        get_y_axis.add_numbers(font_size=20)

        # Axis labels
        x_label = Text(get_string("bond_length"), color=WHITE).scale(0.35)
        x_label.next_to(self.axes.get_x_axis(), DOWN, buff=0.3)

        y_label = Text(get_string("energy"), color=WHITE).scale(0.35)
        y_label.next_to(self.axes.get_y_axis(), LEFT, buff=0.3)
        y_label.rotate(90 * DEGREES)

        self.add(self.axes, x_label, y_label)

        # Plot harmonic potential
        self.potential_graph = self.axes.get_graph(
            lambda r: self.harmonic_potential(r),
            x_range=[self.r0 - 0.5, self.r0 + 0.5],
            color=BLUE
        )
        self.add(self.potential_graph)

        # Mark equilibrium position
        eq_point = self.axes.coords_to_point(self.r0, 0)
        eq_dot = Dot(eq_point, color=GREEN, radius=0.08)
        eq_line = DashedLine(
            self.axes.coords_to_point(self.r0, 0),
            self.axes.coords_to_point(self.r0, 20),
            stroke_width=2,
            color=GREEN,
            dash_length=0.1
        )
        self.add(eq_line, eq_dot)

        # Create moving dot to show current position
        self.current_dot = Dot(eq_point, color=RED, radius=0.1)
        self.add(self.current_dot)

        # Add formula
        formula = Tex(get_string("harmonic_formula"), color=YELLOW).scale(0.6)
        formula.move_to(self.axes.get_top() + RIGHT + DOWN)
        self.add(formula)

        # Add parameter info
        params = VGroup(
          #  Tex(f"k = {self.k:.0f}~\\text{{kcal/(mol·Å²)}}", color=WHITE).scale(0.4),
            Tex(f"r_0 = {self.r0:.2f}~\\text{{Å}}", color=WHITE).scale(0.4)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        params.move_to(self.axes.get_corner(UR) + LEFT * 2.5 + DOWN *2)
        self.add(params)

    def harmonic_potential(self, r):
        """Calculate harmonic potential energy"""
        return 0.5 * self.k * (r - self.r0)**2

    def animate_stretching(self):
        """Animate bond stretching with sinusoidal motion"""
        # Get animation parameters from central dictionary
        duration = self.PARAMETERS["duration"]["value"]
        fps = self.PARAMETERS["fps"]["value"]
        frames = int(duration * fps)

        for frame in range(frames):
            t = frame / fps

            # Calculate current bond length (sinusoidal oscillation)
            r_current = self.r0 + self.amplitude * np.sin(2 * np.pi * self.frequency * t)

            # Update molecule
            self.update_molecule_positions(r_current)

            # Update dot on potential curve
            energy = self.harmonic_potential(r_current)
            point = self.axes.coords_to_point(r_current, energy)
            self.current_dot.move_to(point)

            # Update state labels
            if frame % 2 == 0:  # Update every 2 seconds
                if hasattr(self, 'state_label'):
                    self.remove(self.state_label)

                if r_current < self.r0 - 0.1:
                    state = get_string("compressed")
                    color = RED
                elif r_current > self.r0 + 0.1:
                    state = get_string("stretched")
                    color=ORANGE
                else:
                    state = get_string("equilibrium")
                    color = GREEN

                self.state_label = Text(state, color=color).scale(0.5)
                self.state_label.move_to(self.mol_center + DOWN * 2.8)
                self.add(self.state_label)

            self.wait(1/fps)


if __name__ == "__main__":
    # Run with: manimgl bond_stretching.py BondStretching
    pass
