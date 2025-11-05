#!/usr/bin/env python3
"""
Torsion Angle - Optimized 2D Visualization
Optimierte 2D-Darstellung des Torsionswinkels

Layout:
- Links oben: Große Newman-Projektion (Hauptfokus)
- Rechts oben: Schematische Moleküldarstellung
- Unten: Breite Energie-Kurve
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "EN"

STRINGS = {
    "DE": {
        "title": "Torsionswinkel in Ethan\nNewman-Projektion",
        "newman": "",
        "molecule": "Molekülmodell",
        "energy": "Rotationsbarriere",
        "dihedral_angle": "Diederwinkel φ (°)",
        "energy_label": "Energie (kcal/mol)",
        "staggered": "Gestaffelt\n(Minimum)",
        "eclipsed": "Verdeckt\n(Maximum)",
        "formula": r"V = \frac{V_0}{2}[1+\cos(3\phi)]",
        "front": "vorne",
        "back": "hinten",
    },
    "EN": {
        "title": "Torsion Angle in Ethan\nNewman Projection",
        "newman": "",
        "molecule": "Molecular Model",
        "energy": "Rotational Barrier",
        "dihedral_angle": "Dihedral Angle φ (°)",
        "energy_label": "Energy (kcal/mol)",
        "staggered": "Staggered\n(Minimum)",
        "eclipsed": "Eclipsed\n(Maximum)",
        "formula": r"V = \frac{V_0}{2}[1+\cos(3\phi)]",
        "front": "front",
        "back": "back",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class TorsionAngleOptimized(Scene):
    """Torsion angle animation with periodic potential V = V₀/2[1+cos(nφ-γ)]."""

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # Physical parameters
        "V0": {
            "value": 3.0,
            "type": float,
            "unit": "kcal/mol",
            "description": "Rotational barrier height for ethane torsion",
            "min": 0.0,
            "max": 10.0
        },
        "n": {
            "value": 3,
            "type": int,
            "unit": "-",
            "description": "Periodicity (3-fold for ethane)",
            "min": 1,
            "max": 6
        },
        "gamma": {
            "value": 0.0,
            "type": float,
            "unit": "rad",
            "description": "Phase shift for torsional potential",
            "min": 0.0,
            "max": 6.28
        },
        # Animation parameters
        "duration": {
            "value": 48.0,
            "type": float,
            "unit": "s",
            "description": "Total animation duration (3 full rotations)",
            "min": 10.0,
            "max": 120.0
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
        self.V0 = self.PARAMETERS["V0"]["value"]
        self.n = self.PARAMETERS["n"]["value"]
        self.gamma = self.PARAMETERS["gamma"]["value"]

        # Setup
        self.setup_layout()
        self.create_newman_projection()
        # self.create_molecule_schematic()  # Deaktiviert - sieht nicht gut aus
        self.create_energy_curve()

        # Animation
        self.animate_rotation()
        self.wait(2)

    def setup_layout(self):
        """Create title and layout guides"""
        title = Text(get_string("title"), color=YELLOW).scale(0.7)
        title.to_edge(UP, buff=0.2)
        self.add(title)

        # Panel positions - Newman centered at top
        self.newman_center = UP * 1.2
        self.energy_center = DOWN * 2.0

    def create_newman_projection(self):
        """Create large Newman projection (main focus)"""
        # Back carbon (C2) - circle
        radius = 1.0  # Even larger since we have more space
        back_circle = Circle(radius=radius, color=GREY_BROWN, stroke_width=5)
        back_circle.move_to(self.newman_center)

        # Front carbon (C3) - dot
        front_dot = Dot(self.newman_center, radius=0.15, color=GREY_BROWN)

        self.newman_group = VGroup(back_circle, front_dot)

        # Label
        newman_label = Text(get_string("newman"), color=GREEN_C).scale(0.45)
        newman_label.move_to(self.newman_center + UP * 2.2)
        self.add(newman_label)

        # Legend
        back_legend = VGroup(
            Line(LEFT * 0.3, RIGHT * 0.3, color=BLUE, stroke_width=5),
            Text(get_string("back"), color=WHITE).scale(0.3)
        ).arrange(RIGHT, buff=0.2)
        back_legend.move_to(self.newman_center + LEFT * 1.8 + DOWN * 2.0)

        front_legend = VGroup(
            Line(LEFT * 0.3, RIGHT * 0.3, color=RED, stroke_width=5),
            Text(get_string("front"), color=WHITE).scale(0.3)
        ).arrange(RIGHT, buff=0.2)
        front_legend.move_to(self.newman_center + RIGHT * 1.8 + DOWN * 2.0)

        self.add(back_legend, front_legend)

        # Angle display
        self.newman_angle = DecimalNumber(
            0, num_decimal_places=0, color=YELLOW, unit="°"
        ).scale(0.6)
        self.newman_angle.move_to(self.newman_center + DOWN * 1.85)

        # Initial bonds
        self.update_newman_projection(0)
        self.add(self.newman_group, self.newman_angle)

    def update_newman_projection(self, phi_degrees):
        """Update Newman projection"""
        # Remove old bonds
        if hasattr(self, 'newman_bonds'):
            for bond in self.newman_bonds:
                self.newman_group.remove(bond)

        self.newman_bonds = []

        # Back carbon bonds (C2, fixed at 0°, 120°, 240°)
        bond_length = 1.5  # Longer bonds for larger circle
        back_angles = [0, 120, 240]
        for angle in back_angles:
            angle_rad = np.radians(angle)
            end = self.newman_center + bond_length * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            line = Line(self.newman_center, end, color=BLUE, stroke_width=7)
            self.newman_bonds.append(line)
            self.newman_group.add(line)

            # H label
            h_label = Text("H", color=WHITE).scale(0.4)
            h_label.move_to(end + 0.35 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0]))
            self.newman_bonds.append(h_label)
            self.newman_group.add(h_label)

        # Front carbon bonds (C3, rotated by phi)
        front_angles = [phi_degrees, phi_degrees + 120, phi_degrees + 240]
        for angle in front_angles:
            angle_rad = np.radians(angle)
            end = self.newman_center + bond_length * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])

            # Half-line from center outward
            mid = self.newman_center + 0.25 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            line = Line(mid, end, color=RED, stroke_width=7)
            self.newman_bonds.append(line)
            self.newman_group.add(line)

            # H label
            h_label = Text("H", color=WHITE).scale(0.4)
            h_label.move_to(end + 0.35 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0]))
            self.newman_bonds.append(h_label)
            self.newman_group.add(h_label)

        # Update angle
        self.newman_angle.set_value(phi_degrees % 360)

    def create_molecule_schematic(self):
        """Create schematic molecule view"""
        # Title
        mol_label = Text(get_string("molecule"), color=BLUE_C).scale(0.45)
        mol_label.move_to(self.molecule_center + UP * 2.2)
        self.add(mol_label)

        # Four carbons in a line (schematic, not realistic geometry)
        self.C_circles = []
        spacing = 1.2
        for i in range(4):
            circle = Circle(radius=0.25, fill_color=GREY_BROWN, fill_opacity=1.0,
                          stroke_color=WHITE, stroke_width=2)
            label = Text(f"C{i+1}", color=WHITE).scale(0.25)
            atom = VGroup(circle, label)
            x_pos = self.molecule_center[0] + (i - 1.5) * spacing
            y_pos = self.molecule_center[1] + 0.5
            atom.move_to(np.array([x_pos, y_pos, 0]))
            self.C_circles.append(atom)
            self.add(atom)

        # Bonds
        self.mol_bonds = VGroup()

        # Angle display (create BEFORE calling update)
        self.mol_angle = DecimalNumber(
            0, num_decimal_places=0, color=YELLOW, unit="°"
        ).scale(0.5)
        self.mol_angle.move_to(self.molecule_center + DOWN * 1.0)

        # Initial update
        self.update_molecule_schematic(0)
        self.add(self.mol_bonds)
        self.add(self.mol_angle)

        # Rotation indicator
        start = self.molecule_center + UP * 0.5 + LEFT * 0.5
        end = self.molecule_center + UP * 0.5 + RIGHT * 0.5
        arrow_arc = CurvedArrow(start, end, color=YELLOW, stroke_width=3)
        arrow_label = Text("Rotation", color=YELLOW).scale(0.3)
        arrow_label.move_to(self.molecule_center + UP * 1.0)
        self.add(arrow_arc, arrow_label)

    def update_molecule_schematic(self, phi_degrees):
        """Update schematic molecule"""
        self.mol_bonds.submobjects.clear()

        # Simple representation: show rotation at C2-C3 bond
        positions = [c.get_center() for c in self.C_circles]

        # Bonds
        for i in range(3):
            color = YELLOW if i == 1 else WHITE
            width = 6 if i == 1 else 4
            bond = Line(positions[i], positions[i+1], stroke_width=width, color=color)
            self.mol_bonds.add(bond)

        # Show H atoms schematically on C2 and C3
        # C2 hydrogens (above, fixed)
        h2_pos1 = positions[1] + UP * 0.6 + LEFT * 0.3
        h2_pos2 = positions[1] + UP * 0.6 + RIGHT * 0.3
        for pos in [h2_pos1, h2_pos2]:
            h_circle = Circle(radius=0.12, fill_color=BLUE_D, fill_opacity=1.0,
                            stroke_color=BLUE, stroke_width=2)
            h_circle.move_to(pos)
            h_bond = Line(positions[1], pos, stroke_width=2, color=BLUE)
            self.mol_bonds.add(h_bond, h_circle)

        # C3 hydrogens (below, rotate with angle indicator)
        phi_rad = np.radians(phi_degrees)
        offset = 0.4 * np.sin(phi_rad)  # Simple 2D projection
        h3_pos1 = positions[2] + DOWN * 0.6 + LEFT * (0.3 + offset)
        h3_pos2 = positions[2] + DOWN * 0.6 + RIGHT * (0.3 - offset)
        for pos in [h3_pos1, h3_pos2]:
            h_circle = Circle(radius=0.12, fill_color=RED_D, fill_opacity=1.0,
                            stroke_color=RED, stroke_width=2)
            h_circle.move_to(pos)
            h_bond = Line(positions[2], pos, stroke_width=2, color=RED)
            self.mol_bonds.add(h_bond, h_circle)

        # Update angle
        self.mol_angle.set_value(phi_degrees % 360)

    def create_energy_curve(self):
        """Create wide energy diagram"""
        # Title
        energy_label = Text(get_string("energy"), color=GREEN_C).scale(0.45)
        energy_label.move_to(self.energy_center + UP * 1.05)
        self.add(energy_label)

        # Axes (wider)
        self.axes = Axes(
            x_range=[0, 360, 60],
            y_range=[0, 4, 1],
            width=10,
            height=2.2,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        self.axes.move_to(self.energy_center)

        # Labels
        x_label = Text(get_string("dihedral_angle"), color=WHITE).scale(0.35)
        x_label.next_to(self.axes.get_x_axis(), DOWN, buff=0.2)

        y_label = Text(get_string("energy_label"), color=WHITE).scale(0.35)
        y_label.next_to(self.axes.get_y_axis(), LEFT, buff=0.2)
        y_label.rotate(90 * DEGREES)

        self.add(self.axes, x_label, y_label)

        # Curve
        self.energy_graph = self.axes.get_graph(
            lambda phi: self.torsional_potential(phi),
            x_range=[0, 360],
            color=BLUE
        )
        self.add(self.energy_graph)

        # Mark minima and maxima
        for angle in [60, 180, 300]:
            point = self.axes.coords_to_point(angle, self.torsional_potential(angle))
            dot = Dot(point, color=GREEN, radius=0.06)
            self.add(dot)

        for angle in [0, 120, 240, 360]:
            point = self.axes.coords_to_point(angle, self.torsional_potential(angle))
            dot = Dot(point, color=RED, radius=0.06)
            self.add(dot)

        # Current position marker
        self.energy_dot = Dot(
            self.axes.coords_to_point(0, self.torsional_potential(0)),
            color=YELLOW, radius=0.1
        )
        self.add(self.energy_dot)

        # Labels (on the sides, next to dots)
        stag_label = Text(get_string("staggered"), color=GREEN).scale(0.3)
        stag_label.move_to(self.axes.coords_to_point(60, 0) + DOWN * 0.6)

        ecl_label = Text(get_string("eclipsed"), color=RED).scale(0.3)
        ecl_label.move_to(self.axes.coords_to_point(120, 4) + UP * 0.4)

        self.add(stag_label, ecl_label)

        # Formula
        formula = Tex(get_string("formula"), color=YELLOW).scale(0.5)
        formula.move_to(self.energy_center + RIGHT * 4 + UP * 1.3)
        self.add(formula)

    def torsional_potential(self, phi_degrees):
        """Calculate potential energy"""
        phi_rad = np.radians(phi_degrees)
        return (self.V0 / 2) * (1 + np.cos(self.n * phi_rad - self.gamma))

    def animate_rotation(self):
        """Animate full 360° rotation"""
        # Get animation parameters from central dictionary
        duration = self.PARAMETERS["duration"]["value"]
        fps = self.PARAMETERS["fps"]["value"]
        frames = int(duration * fps)

        for frame in range(frames):
            t = frame / fps
            phi_current = (1080 * t / duration) % 360

            # Update Newman projection
            self.update_newman_projection(phi_current)
            # self.update_molecule_schematic(phi_current)  # Deaktiviert

            # Update energy marker
            energy = self.torsional_potential(phi_current)
            point = self.axes.coords_to_point(phi_current, energy)
            self.energy_dot.move_to(point)

            # State label
            if frame % 15 == 0:
                if hasattr(self, 'state_label'):
                    self.remove(self.state_label)

                staggered = any(abs(phi_current - a) < 15 for a in [60, 180, 300])
                eclipsed = any(abs(phi_current - a) < 15 for a in [0, 120, 240, 360])

                if staggered or eclipsed:
                    state = get_string("staggered") if staggered else get_string("eclipsed")
                    color = GREEN if staggered else RED
                    self.state_label = Text(state, color=color).scale(0.5)
                    self.state_label.move_to(self.newman_center + RIGHT * 2.8 + UP * 0.5)
                    self.add(self.state_label)

            self.wait(1/fps)


if __name__ == "__main__":
    # Run with: manimgl torsion_angle_optimized.py TorsionAngleOptimized
    pass
