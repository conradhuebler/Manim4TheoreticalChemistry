#!/usr/bin/env python3
"""
NH₃ Inversion Animation - Born-Oppenheimer Approximation
Didactic visualization of NH3 inversion using classical mechanics

Visualizes the NH3 inversion in the Born-Oppenheimer approximation.
Left: 3D NH3 molecule with mobile N atom
Right: Double-well potential along inversion coordinate
"""

from manimlib import *
import numpy as np

# Language setting - change to "EN" for English
LANGUAGE = "EN"

def get_string(key):
    """Get localized string"""
    strings = {
        "DE": {
            "title": "NH₃ Inversion: Born-Oppenheimer Näherung",
            "molecule_view": "Molekülstruktur",
            "energy_profile": "Inversions-Potential",
            "pyramidal_up": "Pyramidal ↑",
            "pyramidal_down": "Pyramidal ↓",
            "planar_transition": "Planarer Übergangszustand",
            "inversion_coordinate": "Inversionskoordinate z",
            "energy_title": "Energie",
            "barrier_crossing": "Klassischer Übergang über Barriere",
            "oscillation": "Inversion-Oszillation",
            "n_above": "N oberhalb H₃-Ebene",
            "n_below": "N unterhalb H₃-Ebene",
            "approaching_barrier": "Annäherung an Barriere",
            "bo_dynamics": "",
        },
        "EN": {
            "title": "NH₃ Inversion: Born-Oppenheimer Approximation",
            "molecule_view": "Molecular Structure",
            "energy_profile": "Inversion Potential",
            "pyramidal_up": "Pyramidal ↑",
            "pyramidal_down": "Pyramidal ↓",
            "planar_transition": "Planar Transition State",
            "inversion_coordinate": "Inversion Coordinate z",
            "energy_title": "Energy",
            "barrier_crossing": "Classical Crossing over Barrier",
            "oscillation": "Inversion Oscillation",
            "n_above": "N above H₃ plane",
            "n_below": "N below H₃ plane",
            "approaching_barrier": "Approaching Barrier",
            "bo_dynamics": "",
        }
    }
    return strings[LANGUAGE].get(key, key)

class NH3Inversion(ThreeDScene):
    """NH3 inversion animation with double-well potential V = V₀(16(z/a)⁴-8(z/a)²+1)."""

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # Physical parameters
        "V0": {
            "value": 2.5,
            "type": float,
            "unit": "-",
            "description": "Barrier height for inversion potential (dimensionless)",
            "min": 0.5,
            "max": 10.0
        },
        "a": {
            "value": 0.4,
            "type": float,
            "unit": "Å",
            "description": "Well separation parameter (minima at ±a)",
            "min": 0.2,
            "max": 1.0
        },
        "h_radius": {
            "value": 0.8,
            "type": float,
            "unit": "Å",
            "description": "Distance from center to H atoms in triangular arrangement",
            "min": 0.5,
            "max": 1.5
        },
        # Animation parameters
        "z_nitrogen_initial": {
            "value": 0.4,
            "type": float,
            "unit": "Å",
            "description": "Initial N position above H plane",
            "min": 0.1,
            "max": 1.0
        },
        "dt": {
            "value": 0.02,
            "type": float,
            "unit": "s",
            "description": "Animation time step",
            "min": 0.01,
            "max": 0.1
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Extract physical parameters from central dictionary
        self.V0 = self.PARAMETERS["V0"]["value"]
        self.a = self.PARAMETERS["a"]["value"]
        self.h_radius = self.PARAMETERS["h_radius"]["value"]
        self.dt = self.PARAMETERS["dt"]["value"]
        self.z_nitrogen = self.PARAMETERS["z_nitrogen_initial"]["value"]

        # Setup NH3 molecular geometry
        self.setup_parameters()

        # Animation data
        self.time_data = []
        self.z_coord_data = []
        self.energy_data = []

        # Current state
        self.current_time = 0.0

    def setup_parameters(self):
        """Setup NH3 molecular geometry from h_radius parameter"""
        # H atoms in triangular arrangement (fixed)
        angle_offset = 2 * np.pi / 3  # 120° apart

        self.h_positions = []
        for i in range(3):
            angle = i * angle_offset
            x = self.h_radius * np.cos(angle)
            y = self.h_radius * np.sin(angle)
            self.h_positions.append([x, y, 0])  # H atoms in z=0 plane

    def setup_camera(self):
        """Setup 3D camera view for NH3 molecule"""
        # View from angle to see 3D structure clearly
        self.camera.frame.set_euler_angles(theta=-35*DEGREES, phi=70*DEGREES)
        # Zoom for good overview
        self.camera.frame.set_width(16)

    def construct(self):
        """Main animation sequence"""
        self.setup_camera()
        self.setup_layout()
        self.wait(1)

        self.phase_1_initial_state()
        self.wait(2)

        self.phase_2_approach_barrier()
        self.wait(2)

        self.phase_3_barrier_crossing()
        self.wait(2)

        self.phase_4_inverted_state()
        self.wait(2)

        self.phase_5_oscillation()
        self.wait(2)

    def setup_layout(self):
        """Setup layout with 3D molecule + 2D energy profile (fixed overlay)"""
        # Title (2D overlay - fixed in frame)
        title = Text(get_string("title"), font_size=28)
        title.to_edge(UP, buff=0.2)
        title.fix_in_frame()
        self.play(Write(title))

        # Define areas
        self.molecule_center = LEFT * 4.0
        self.energy_center = RIGHT * 4.0

        # Setup molecule visualization (3D)
        self.setup_molecule_view()

        # Setup energy profile (2D overlay)
        self.setup_energy_profile()

    def setup_molecule_view(self):
        """Setup 3D NH3 molecule visualization"""
        # Molecule view label (2D overlay - fixed)
        mol_label = Text(get_string("molecule_view"), font_size=22, color=YELLOW)
        mol_label.move_to(LEFT * 4.0 + UP * 3.5)
        mol_label.fix_in_frame()
        self.play(Write(mol_label))

        # Create 3D NH3 molecule (NOT fixed - rotates with camera)
        self.create_nh3_molecule_3d()

    def create_nh3_molecule_3d(self):
        """Create 3D NH3 molecule with Spheres (rotates with camera)"""
        # H atoms as 3D Spheres (fixed in triangular arrangement in z=0 plane)
        self.h_atoms = []
        self.h_labels = []

        for i, pos in enumerate(self.h_positions):
            # H atom as Sphere (3D object)
            h_atom = Sphere(radius=0.15, color=WHITE)
            h_atom.set_opacity(0.9)
            # Position in 3D space (offset from molecule_center)
            h_3d_pos = self.molecule_center + np.array([pos[0], pos[1], pos[2]]) * 0.8
            h_atom.move_to(h_3d_pos)
            self.h_atoms.append(h_atom)

            # H label (3D object - rotates with camera)
            h_label = Text("H", font_size=30, color=WHITE)
            h_label.move_to(h_3d_pos)
            self.h_labels.append(h_label)

        # N atom as Sphere (mobile, 3D object)
        self.n_atom = Sphere(radius=0.25, color=BLUE)
        self.n_atom.set_opacity(0.9)

        # N label (3D object - rotates with camera)
        self.n_label = Text("N", font_size=36, color=WHITE)

        # H₃ plane reference (2D overlay for guidance)
        self.h3_plane = Line(
            self.molecule_center + LEFT * 1.2,
            self.molecule_center + RIGHT * 1.2,
            color=GREY, stroke_width=1, stroke_opacity=0.3
        )
        self.h3_plane.fix_in_frame()

        # Initial N position
        self.update_molecule_3d_geometry()

        # N-H bonds (3D lines)
        self.nh_bonds = []
        for i in range(3):
            bond = Line(
                self.n_atom.get_center(),
                self.h_atoms[i].get_center(),
                color=GREEN, stroke_width=3
            )
            self.nh_bonds.append(bond)

        # Show molecule (use Group for 3D objects)
        self.mol_group = Group(*self.h_atoms, self.n_atom, *self.nh_bonds)
        self.play(
            *[ShowCreation(h) for h in self.h_atoms],
            *[Write(h_label) for h_label in self.h_labels],
            ShowCreation(self.n_atom), Write(self.n_label),
            ShowCreation(self.h3_plane),
            *[ShowCreation(bond) for bond in self.nh_bonds]
        )

    def update_molecule_3d_geometry(self):
        """Update 3D N position and all bonds based on current z_nitrogen"""
        # N atom position in 3D space (z_nitrogen is relative to H₃ plane)
        n_3d_pos = self.molecule_center + np.array([0, 0, self.z_nitrogen * 1.5])

        self.n_atom.move_to(n_3d_pos)
        # N label stays fixed in frame but moves with projected position
        self.n_label.move_to(n_3d_pos)

        # Update N-H bonds if they exist
        if hasattr(self, 'nh_bonds'):
            for i, bond in enumerate(self.nh_bonds):
                bond.put_start_and_end_on(
                    self.n_atom.get_center(),
                    self.h_atoms[i].get_center()
                )

    def setup_energy_profile(self):
        """Setup inversion potential energy surface (2D overlay - fixed)"""
        # Energy profile axes (2D overlay - fixed in frame)
        self.energy_axes = Axes(
            x_range=(-0.6, 0.6, 0.2),  # Inversion coordinate z
            y_range=(0, 30, 5),  # Energy in cm⁻¹
            height=6.0,
            width=6.0,
            axis_config={
                "stroke_color": GREY,
                "stroke_width": 1,
                "include_tip": True,
            }
        )
        self.energy_axes.move_to(self.energy_center)
        self.energy_axes.fix_in_frame()

        # Labels (2D overlays - fixed)
        energy_x_label = Text(get_string("inversion_coordinate"), font_size=24)
        energy_x_label.next_to(self.energy_axes, DOWN, buff=0.2)
        energy_x_label.fix_in_frame()

        energy_y_label = Text(get_string("energy_title"), font_size=24)
        energy_y_label.next_to(self.energy_axes, LEFT, buff=0.2)
        energy_y_label.fix_in_frame()

        self.play(
            ShowCreation(self.energy_axes),
            Write(energy_x_label),
            Write(energy_y_label)
        )

        # Create double-well potential curve
        self.create_inversion_potential()

        # Current position marker (2D overlay - fixed)
        self.energy_dot = Dot(radius=0.08, color=RED)
        self.energy_dot.fix_in_frame()
        self.update_energy_dot()

        self.play(ShowCreation(self.energy_dot))

    def inversion_potential(self, z):
        """NH3 inversion potential as function of N position"""
        # Didactic double-well potential: V(z) = V₀ * (16*(z/a)⁴ - 8*(z/a)² + 1)
        # This form guarantees symmetric minima at z = ±a and barrier at z = 0
        # V0 and a are now taken from PARAMETERS (set in __init__)

        # Normalized quartic double-well
        z_norm = z / self.a
        return self.V0 * (16 * z_norm**4 - 8 * z_norm**2 + 1)

    def create_inversion_potential(self):
        """Create the double-well inversion potential curve"""
        # Z-coordinate values (inversion coordinate)
        z_values = np.linspace(-0.6, 0.6, 200)
        potential_values = [self.inversion_potential(z) for z in z_values]

        # Create curve points
        potential_points = [
            self.energy_axes.coords_to_point(z, min(max(V, 0), 30))
            for z, V in zip(z_values, potential_values)
        ]

        self.potential_curve = VMobject(color=BLUE, stroke_width=3)
        self.potential_curve.set_points_as_corners(potential_points)
        self.potential_curve.fix_in_frame()  # 2D overlay

        self.play(ShowCreation(self.potential_curve))

        # Find and label key points
        min_idx_left = np.argmin(potential_values[:80])   # Left minimum
        min_idx_right = np.argmin(potential_values[120:]) + 120  # Right minimum
        max_idx = len(potential_values) // 2  # Barrier at z=0

        # Labels for minima and barrier (2D overlays - fixed)
        left_min_label = Text(get_string("pyramidal_up"), font_size=20, color=GREEN)
        left_min_label.move_to(self.energy_axes.coords_to_point(z_values[min_idx_left], potential_values[min_idx_left] + 5))
        left_min_label.fix_in_frame()

        barrier_label = Text(get_string("planar_transition"), font_size=20, color=ORANGE)
        barrier_label.move_to(self.energy_axes.coords_to_point(z_values[max_idx], potential_values[max_idx] + 6))
        barrier_label.fix_in_frame()

        right_min_label = Text(get_string("pyramidal_down"), font_size=20, color=GREEN)
        right_min_label.move_to(self.energy_axes.coords_to_point(z_values[min_idx_right], potential_values[min_idx_right] + 5))
        right_min_label.fix_in_frame()

        self.play(
            Write(left_min_label),
            Write(barrier_label),
            Write(right_min_label)
        )

    def update_energy_dot(self):
        """Update position of energy dot on potential curve"""
        current_energy = self.inversion_potential(self.z_nitrogen)

        # Clamp energy for display
        display_energy = min(max(current_energy, 0), 30)

        dot_pos = self.energy_axes.coords_to_point(self.z_nitrogen, display_energy)
        self.energy_dot.move_to(dot_pos)

    def phase_1_initial_state(self):
        """Phase 1: Initial pyramidal state (N above H₃ plane)"""
        phase_label = Text(
            f"{get_string('n_above')}",
            font_size=26, color=YELLOW
        )
        phase_label.move_to(self.molecule_center + UP * 2.8)
        phase_label.fix_in_frame()  # 2D overlay
        self.play(Write(phase_label))
        self.current_phase_label = phase_label

        # N starts at z = +0.4 Å (above H plane)
        self.z_nitrogen = 0.4
        self.update_molecule_3d_geometry()
        self.update_energy_dot()

        # Store initial data
        self.time_data.append(self.current_time)
        self.z_coord_data.append(self.z_nitrogen)
        self.energy_data.append(self.inversion_potential(self.z_nitrogen))

        self.wait(1)

    def phase_2_approach_barrier(self):
        """Phase 2: N approaches the H₃ plane"""
        phase_label = Text(
            f"{get_string('approaching_barrier')}",
            font_size=26, color=YELLOW
        )
        phase_label.move_to(self.molecule_center + UP * 2.8)
        phase_label.fix_in_frame()  # 2D overlay
        self.play(Transform(self.current_phase_label, phase_label))

        # Move N from z = +0.4 to z = +0.1
        for step in range(60):
            progress = step / 60
            self.z_nitrogen = 0.4 - 0.3 * progress

            # Update visualization
            self.update_molecule_3d_geometry()
            self.update_energy_dot()

            # Store data
            self.current_time += self.dt
            self.time_data.append(self.current_time)
            self.z_coord_data.append(self.z_nitrogen)
            self.energy_data.append(self.inversion_potential(self.z_nitrogen))

            if step % 5 == 0:
                self.wait(0.05)

    def phase_3_barrier_crossing(self):
        """Phase 3: Classical crossing over the barrier"""
        phase_label = Text(
            f"[{get_string('bo_dynamics')}] {get_string('barrier_crossing')}",
            font_size=26, color=ORANGE
        )
        phase_label.move_to(self.molecule_center + UP * 2.8)
        phase_label.fix_in_frame()  # 2D overlay
        self.play(Transform(self.current_phase_label, phase_label))

        # Classical transition through z = 0 (over the barrier, not through it)
        for step in range(40):
            progress = step / 40
            self.z_nitrogen = 0.1 - 0.2 * progress  # From +0.1 to -0.1

            # Update visualization
            self.update_molecule_3d_geometry()
            self.update_energy_dot()

            # Store data
            self.current_time += self.dt
            self.time_data.append(self.current_time)
            self.z_coord_data.append(self.z_nitrogen)
            self.energy_data.append(self.inversion_potential(self.z_nitrogen))

            if step % 3 == 0:
                self.wait(0.05)

    def phase_4_inverted_state(self):
        """Phase 4: Inverted pyramidal state (N below H₃ plane)"""
        phase_label = Text(
            f"{get_string('bo_dynamics')} {get_string('n_below')}",
            font_size=26, color=GREEN
        )
        phase_label.move_to(self.molecule_center + UP * 2.8)
        phase_label.fix_in_frame()  # 2D overlay
        self.play(Transform(self.current_phase_label, phase_label))

        # Move N from z = -0.1 to z = -0.4
        for step in range(60):
            progress = step / 60
            self.z_nitrogen = -0.1 - 0.3 * progress

            # Update visualization
            self.update_molecule_3d_geometry()
            self.update_energy_dot()

            # Store data
            self.current_time += self.dt
            self.time_data.append(self.current_time)
            self.z_coord_data.append(self.z_nitrogen)
            self.energy_data.append(self.inversion_potential(self.z_nitrogen))

            if step % 5 == 0:
                self.wait(0.05)

        # Pause at inverted state
        self.wait(1)

    def phase_5_oscillation(self):
        """Phase 5: Continuous inversion oscillation"""
        phase_label = Text(
            f"{get_string('oscillation')}",
            font_size=26, color=PURPLE
        )
        phase_label.move_to(self.molecule_center + UP * 2.8)
        phase_label.fix_in_frame()  # 2D overlay
        self.play(Transform(self.current_phase_label, phase_label))

        # Oscillate between z = -0.4 and z = +0.4 several times
        for cycle in range(3):
            # Return journey: -0.4 → +0.4
            for step in range(80):
                progress = step / 80
                self.z_nitrogen = -0.4 + 0.8 * progress

                # Update visualization
                self.update_molecule_3d_geometry()
                self.update_energy_dot()

                # Store data
                self.current_time += self.dt
                self.time_data.append(self.current_time)
                self.z_coord_data.append(self.z_nitrogen)
                self.energy_data.append(self.inversion_potential(self.z_nitrogen))

                if step % 4 == 0:
                    self.wait(0.03)

            # Forward journey: +0.4 → -0.4
            for step in range(80):
                progress = step / 80
                self.z_nitrogen = 0.4 - 0.8 * progress

                # Update visualization
                self.update_molecule_3d_geometry()
                self.update_energy_dot()

                # Store data
                self.current_time += self.dt
                self.time_data.append(self.current_time)
                self.z_coord_data.append(self.z_nitrogen)
                self.energy_data.append(self.inversion_potential(self.z_nitrogen))

                if step % 4 == 0:
                    self.wait(0.03)
