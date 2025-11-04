#!/usr/bin/env python3
"""
Principal Component Analysis (PCA) for Molecular Dynamics
Hauptkomponentenanalyse (PCA) für Molekulardynamik

Educational animation showing PCA as coordinate system rotation:
- Combined trajectory: Linear drift + perpendicular oscillation
  (Models protein motion: e.g., overall translation + domain rotation)
- Centering: Shift center of mass to origin
  (Standard in MD: remove overall translation)
- PCA: Find principal vibrational modes (eigenvectors of covariance matrix)
  (Identifies collective motions in proteins/molecules)
- Rotation: Transform to natural coordinates aligned with main motions
  (Like viewing protein from optimal angle)
- Dimensionality reduction: Keep only functionally important motions
  (Few PCs capture main biological function)
- Result: Separated independent motions (drift on PC1, oscillation on PC2)
  (E.g., PC1 = opening/closing, PC2 = side chain rotation)

Didactic approach for chemists/biologists:
1. Build trajectory with time color gradient (blue → red)
2. Center data (move center of mass to origin)
3. Covariance analysis: measure coupled motions
4. PCA decomposition: find principal vibrational modes
5. Coordinate rotation (split-screen: original vs. natural coordinates)
6. Show separation of independent motions
7. Dimensionality reduction: ignore unimportant fluctuations
8. Connect to real MD applications (protein folding, ligand binding)

Key insights for intuitive understanding:
- PCA = finding the "natural" coordinate system of molecular motion
- Like rotating a camera to see the motion most clearly
- Separates complex motion into independent components
- Few components often capture the main biological function
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "EN"  # Set to "EN" for English

STRINGS = {
    "DE": {
        "title": "PCA als Koordinatensystem-Drehung",
        "phase1_label": "Phase 1: Original-Trajektorie",
        "phase2_label": "Phase 2: Zentrierung",
        "phase3_label": "Phase 3: PCA-Zerlegung",
        "phase4_label": "Phase 4: Koordinaten-Drehung",
        "phase5_label": "Phase 5: Bewegungstrennung",
        "phase6_label": "Phase 6: Dimensionsreduktion",
        "phase7_label": "Phase 7: MD-Anwendung",
        "trajectory_desc": "2D-Trajektorie: Linear + Oszillation",
        "time_legend": "Zeit",
        "mean_position": "Schwerpunkt",
        "centering_formula": r"\tilde{X} = X - \mu",
        "centering_explanation": "Verschiebe Schwerpunkt auf Ursprung",
        "centered_data": "Zentrierte Daten",
        "covariance": "Kovarianz-Ellipse",
        "covariance_formula": r"C = \frac{1}{N}\tilde{X}^T\tilde{X}",
        "covariance_explanation": "Misst gekoppelte Bewegungen",
        "ellipse_explanation": "Form zeigt Hauptbewegungsrichtungen",
        "eigendecomp": r"C = V\Lambda V^T",
        "eigendecomp_explanation": "Finde Hauptschwingungsrichtungen",
        "pc1_label": "PC1 (Hauptbewegung)",
        "pc2_label": "PC2",
        "variance_explained": "Bewegungsenergie",
        "rotation_formula": r"Y = \tilde{X} \cdot V",
        "rotation_explanation": "Drehe zu natürlichen Koordinaten",
        "rotation_metaphor": "Wie Kamera optimal ausrichten",
        "original_system": "Original (x1, x2)",
        "rotated_system": "Gedreht (PC1, PC2)",
        "linear_motion": "Lineare Drift",
        "oscillation": "Oszillation",
        "separated": "Getrennt!",
        "dim_reduction": "Dimensionsreduktion",
        "dim_reduction_explanation": "Ignoriere unwichtige Bewegungen",
        "only_pc1": "Nur PC1",
        "only_pc2": "Nur PC2",
        "full_data": "Vollständig",
        "back_projection": r"\tilde{X}' = Y' \cdot V^T",
        "back_projection_explanation": "Zurück zum Originalraum",
        "keep_pc1": "Behalte nur PC1, setze PC2=0",
        "keep_pc2": "Behalte nur PC2, setze PC1=0",
        "approximation": "Näherung",
        "md_title": "PCA in Molekulardynamik",
        "md_text1": "Protein mit N Atomen → 3N Dimensionen",
        "md_text2": "PCA findet kollektive Bewegungen",
        "md_text3": "Beispiel: PC1 = Öffnen/Schließen",
        "md_text4": "Beispiel: PC2 = Domänenrotation",
        "md_text5": "Wenige PCs erfassen Hauptfunktion",
        "md_example_title": "Praktische Anwendungen:",
        "md_example1": "• Proteinfaltung analysieren",
        "md_example2": "• Ligandenbindung verstehen",
        "md_example3": "• Funktionelle Bewegungen identifizieren",
        "x1_axis": r"x_1",
        "x2_axis": r"x_2",
        "numbers_title": "PCA Parameter",
        "cov_before": "Kovarianzmatrix (vorher)",
        "cov_after": "Kovarianzmatrix (nachher)",
        "correlated": "Bewegungen gekoppelt!",
        "decorrelated": "Bewegungen entkoppelt!",
        "off_diagonal": "Kopplung",
        "key_insight": "Kernidee: PCA trennt unabhängige Bewegungen!",
    },
    "EN": {
        "title": "PCA as Coordinate System Rotation",
        "phase1_label": "Phase 1: Original Trajectory",
        "phase2_label": "Phase 2: Centering",
        "phase3_label": "Phase 3: PCA Decomposition",
        "phase4_label": "Phase 4: Coordinate Rotation",
        "phase5_label": "Phase 5: Motion Separation",
        "phase6_label": "Phase 6: Dimensionality Reduction",
        "phase7_label": "Phase 7: MD Application",
        "trajectory_desc": "2D Trajectory: Linear + Oscillation",
        "time_legend": "Time",
        "mean_position": "Center of Mass",
        "centering_formula": r"\tilde{X} = X - \mu",
        "centering_explanation": "Shift center of mass to origin",
        "centered_data": "Centered Data",
        "covariance": "Covariance Ellipse",
        "covariance_formula": r"C = \frac{1}{N}\tilde{X}^T\tilde{X}",
        "covariance_explanation": "Measures coupled motions",
        "ellipse_explanation": "Shape shows main motion directions",
        "eigendecomp": r"C = V\Lambda V^T",
        "eigendecomp_explanation": "Find principal vibrational modes",
        "pc1_label": "PC1 (Main Motion)",
        "pc2_label": "PC2",
        "variance_explained": "Motion Energy",
        "rotation_formula": r"Y = \tilde{X} \cdot V",
        "rotation_explanation": "Rotate to natural coordinates",
        "rotation_metaphor": "Like aligning camera optimally",
        "original_system": "Original (x1, x2)",
        "rotated_system": "Rotated (PC1, PC2)",
        "linear_motion": "Linear Drift",
        "oscillation": "Oscillation",
        "separated": "Separated!",
        "dim_reduction": "Dimensionality Reduction",
        "dim_reduction_explanation": "Ignore unimportant motions",
        "only_pc1": "Only PC1",
        "only_pc2": "Only PC2",
        "full_data": "Full Data",
        "back_projection": r"\tilde{X}' = Y' \cdot V^T",
        "back_projection_explanation": "Back to original space",
        "keep_pc1": "Keep only PC1, set PC2=0",
        "keep_pc2": "Keep only PC2, set PC1=0",
        "approximation": "Approximation",
        "md_title": "PCA in Molecular Dynamics",
        "md_text1": "Protein with N atoms → 3N dimensions",
        "md_text2": "PCA finds collective motions",
        "md_text3": "Example: PC1 = Opening/Closing",
        "md_text4": "Example: PC2 = Domain Rotation",
        "md_text5": "Few PCs capture main function",
        "md_example_title": "Practical Applications:",
        "md_example1": "• Analyze protein folding",
        "md_example2": "• Understand ligand binding",
        "md_example3": "• Identify functional motions",
        "x1_axis": r"x_1",
        "x2_axis": r"x_2",
        "numbers_title": "PCA Parameters",
        "cov_before": "Covariance Matrix (before)",
        "cov_after": "Covariance Matrix (after)",
        "correlated": "Motions coupled!",
        "decorrelated": "Motions decoupled!",
        "off_diagonal": "Coupling",
        "key_insight": "Key Insight: PCA separates independent motions!",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class PCAMolecularDynamics(Scene):
    def construct(self):
        # Setup parameters
        self.setup_parameters()

        # Title
        self.create_title()
        self.wait(1)

        # Phase 1: Build original trajectory
        self.phase1_trajectory()

        # Phase 2: Center the data
        self.phase2_centering()

        # Phase 3: Covariance analysis and PCA
        self.phase3_pca_decomposition()

        # Phase 4: Coordinate system rotation
        self.phase4_rotation()

        # Phase 5: Show separation in rotated system
        self.phase5_separation()

        # Phase 6: Dimensionality reduction
        self.phase6_dimensionality_reduction()

        # Phase 7: MD connection (DISABLED)
        # self.phase7_md_connection()

        self.wait(3)

    def setup_parameters(self):
        """Setup trajectory and PCA parameters"""
        # Time parameters
        self.t_max = 10.0
        self.n_points = 200
        self.t_values = np.linspace(0, self.t_max, self.n_points)

        # Trajectory: x(t) = t * [1, 1] + A * sin(ω*t) * [-1, 1]/√2
        self.drift_velocity = np.array([1.0, 1.0])
        self.amplitude = 1.5
        self.omega = 2 * np.pi * 0.8
        self.oscillation_dir = np.array([-1.0, 1.0]) / np.sqrt(2)

        # Generate trajectory
        self.generate_trajectory()

        # Perform PCA
        self.perform_pca()

        # Visualization scale
        self.viz_scale = 0.5  # Scale for displaying coordinates

    def generate_trajectory(self):
        """Generate 2D trajectory: linear drift + orthogonal oscillation

        Physical interpretation:
        - Linear drift: overall translation (e.g., protein center of mass movement)
        - Oscillation: periodic motion (e.g., breathing mode, domain oscillation)
        These are perpendicular = independent motions that PCA will separate
        """
        self.trajectory = []

        for t in self.t_values:
            linear_part = t * self.drift_velocity  # Constant velocity drift
            oscillation_part = self.amplitude * np.sin(self.omega * t) * self.oscillation_dir  # Perpendicular oscillation
            position = linear_part + oscillation_part
            self.trajectory.append(position)

        self.trajectory = np.array(self.trajectory)

    def perform_pca(self):
        """Perform PCA on trajectory data

        Physical meaning:
        - Center data: remove center of mass motion (standard in MD)
        - Covariance: measure how coordinates move together
        - Eigenvectors: principal vibrational modes (natural motion directions)
        - Eigenvalues: motion energy in each direction (variance)
        - Rotation: transform to coordinates aligned with natural motions
        """
        # Center the data (remove center of mass motion)
        self.mean_position = np.mean(self.trajectory, axis=0)
        self.centered_data = self.trajectory - self.mean_position

        # Covariance matrix (measures coupled motions)
        self.cov_matrix = np.cov(self.centered_data.T)

        # Eigenvalue decomposition (find principal modes)
        self.eigenvalues, self.eigenvectors = np.linalg.eig(self.cov_matrix)

        # Sort by eigenvalue (descending) = most important motions first
        idx = np.argsort(self.eigenvalues)[::-1]
        self.eigenvalues = self.eigenvalues[idx]
        self.eigenvectors = self.eigenvectors[:, idx]

        # Principal components (as column vectors) = principal vibrational modes
        self.pc1 = self.eigenvectors[:, 0]  # Main motion direction
        self.pc2 = self.eigenvectors[:, 1]  # Secondary motion direction

        # Rotation angle (how much to rotate coordinates)
        self.rotation_angle = np.arctan2(self.pc1[1], self.pc1[0])
        self.rotation_angle_deg = np.degrees(self.rotation_angle)

        # Transform to PC coordinates (natural coordinate system)
        self.rotated_trajectory = self.centered_data @ self.eigenvectors

        # Explained variance = motion energy distribution
        self.explained_variance = self.eigenvalues / np.sum(self.eigenvalues) * 100

    def create_title(self):
        """Create main title"""
        title = Text(get_string("title"), color=YELLOW).scale(0.8)
        title.to_edge(UP, buff=0.15)
        self.play(FadeIn(title))
        self.title = title

    def create_color_legend(self):
        """Create color scale legend for time"""
        # Create gradient bar
        n_segments = 20
        gradient_group = VGroup()

        bar_width = 1.5
        bar_height = 0.15
        segment_width = bar_width / n_segments

        for i in range(n_segments):
            ratio = i / (n_segments - 1)
            color = interpolate_color(BLUE, RED, ratio)
            segment = Rectangle(
                width=segment_width,
                height=bar_height,
                fill_color=color,
                fill_opacity=1.0,
                stroke_width=0
            )
            segment.move_to(RIGHT * (i - n_segments/2) * segment_width)
            gradient_group.add(segment)

        # Labels (larger for better readability)
        time_label = Text(get_string("time_legend"), color=WHITE).scale(0.35)
        t0_label = Text("t=0s", color=BLUE).scale(0.35)
        t_max_label = Text(f"t={self.t_max:.0f}s", color=RED).scale(0.35)

        # Arrange
        legend = VGroup(
            time_label,
            gradient_group,
            VGroup(t0_label, t_max_label).arrange(RIGHT, buff=bar_width - 0.3)
        ).arrange(DOWN, buff=0.15)

        # Position: right upper area, more centered horizontally
        legend.scale(1.1)
        legend.move_to(RIGHT * 3.8 + UP * 2.2)

        return legend

    def create_numbers_box(self):
        """Create box with concrete PCA numbers"""
        # Format numbers
        mean_str = f"mu = [{self.mean_position[0]:.1f}, {self.mean_position[1]:.1f}]"
        lambda1_str = f"lambda_1 = {self.eigenvalues[0]:.1f}"
        lambda2_str = f"lambda_2 = {self.eigenvalues[1]:.1f}"
        theta_str = f"theta = {self.rotation_angle_deg:.1f} deg"
        v1_str = f"v_1 = [{self.pc1[0]:.2f}, {self.pc1[1]:.2f}]"
        v2_str = f"v_2 = [{self.pc2[0]:.2f}, {self.pc2[1]:.2f}]"

        # Create text objects
        title = Text(get_string("numbers_title"), color=YELLOW).scale(0.3)
        lines = VGroup(
            Text(mean_str, color=WHITE).scale(0.25),
            Text(lambda1_str, color=YELLOW).scale(0.25),
            Text(lambda2_str, color=GREEN).scale(0.25),
            Text(theta_str, color=ORANGE).scale(0.25),
            Text(v1_str, color=YELLOW).scale(0.23),
            Text(v2_str, color=GREEN).scale(0.23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        box_content = VGroup(title, lines).arrange(DOWN, buff=0.15)

        # Background box
        background = Rectangle(
            width=box_content.get_width() + 0.3,
            height=box_content.get_height() + 0.2,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=1
        )
        background.move_to(box_content.get_center())

        box = VGroup(background, box_content)
        box.move_to(RIGHT * 5.2 + DOWN * 0.5)  # Moved down to avoid collision with formulas

        return box

    def create_covariance_matrix_display(self, matrix, title_text, highlight_offdiag=False):
        """Create visual display of covariance matrix"""
        # Matrix elements
        c00_str = f"{matrix[0, 0]:.1f}"
        c01_str = f"{matrix[0, 1]:.1f}"
        c10_str = f"{matrix[1, 0]:.1f}"
        c11_str = f"{matrix[1, 1]:.1f}"

        # Title
        title = Text(title_text, color=YELLOW).scale(0.35)

        # Matrix using Tex for proper formatting
        matrix_tex = Tex(
            r"C = \begin{bmatrix}" +
            c00_str + r" & " + c01_str + r" \\ " +
            c10_str + r" & " + c11_str +
            r"\end{bmatrix}",
            color=WHITE
        ).scale(0.6)

        # Highlight off-diagonal if needed
        if highlight_offdiag:
            if abs(matrix[0, 1]) < 0.1:
                # Decorrelated
                status_text = Text(get_string("decorrelated"), color=GREEN).scale(0.3)
                offdiag_text = Text(f"{get_string('off_diagonal')} ≈ 0", color=GREEN).scale(0.28)
            else:
                # Correlated
                status_text = Text(get_string("correlated"), color=RED).scale(0.3)
                offdiag_text = Text(f"{get_string('off_diagonal')} ≠ 0", color=RED).scale(0.28)
        else:
            status_text = None
            offdiag_text = None

        # Arrange
        if status_text:
            display = VGroup(
                title,
                matrix_tex,
                offdiag_text,
                status_text
            ).arrange(DOWN, buff=0.15)
        else:
            display = VGroup(
                title,
                matrix_tex
            ).arrange(DOWN, buff=0.15)

        # Background
        background = Rectangle(
            width=display.get_width() + 0.4,
            height=display.get_height() + 0.3,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_color=YELLOW if highlight_offdiag else WHITE,
            stroke_width=2 if highlight_offdiag else 1
        )
        background.move_to(display.get_center())

        result = VGroup(background, display)
        return result

    def phase1_trajectory(self):
        """Phase 1: Build original trajectory"""
        # Phase label
        phase_label = Text(get_string("phase1_label"), color=BLUE).scale(0.55)
        phase_label.next_to(self.title, DOWN, buff=0.2)
        self.play(FadeIn(phase_label))
        self.wait(0.5)

        # Create axes
        self.main_axes = Axes(
            x_range=[-2, 12, 2],
            y_range=[-2, 12, 2],
            width=5.5,
            height=5.5,
            axis_config={"include_tip": True}
        )
        self.main_axes.shift(LEFT * 2.5 + DOWN * 0.5)

        # Axis labels
        x1_label = Tex(get_string("x1_axis"), color=WHITE).scale(0.65)
        x1_label.next_to(self.main_axes.get_x_axis().get_end(), RIGHT, buff=0.2)

        x2_label = Tex(get_string("x2_axis"), color=WHITE).scale(0.65)
        x2_label.next_to(self.main_axes.get_y_axis().get_end(), UP, buff=0.2)

        self.play(
            ShowCreation(self.main_axes),
            FadeIn(x1_label),
            FadeIn(x2_label),
            run_time=1
        )

        # Description
        desc = Text(get_string("trajectory_desc"), color=WHITE).scale(0.45)
        desc.move_to(self.main_axes.get_bottom() + DOWN * 0.6)
        self.play(FadeIn(desc))

        # Color legend
        self.color_legend = self.create_color_legend()
        self.play(FadeIn(self.color_legend))

        # Build trajectory with color gradient
        points_3d = []
        for x1, x2 in self.trajectory:
            point = self.main_axes.coords_to_point(x1 * self.viz_scale, x2 * self.viz_scale)
            points_3d.append(point)

        self.trajectory_curve = VMobject()
        self.trajectory_curve.set_points_as_corners(points_3d)
        self.trajectory_curve.set_color_by_gradient(BLUE, RED)
        self.trajectory_curve.set_stroke(width=3)

        # Animate trajectory
        self.play(ShowCreation(self.trajectory_curve), run_time=3)

        # Start/end markers
        start_dot = Dot(points_3d[0], color=BLUE, radius=0.08)
        end_dot = Dot(points_3d[-1], color=RED, radius=0.08)

        self.play(FadeIn(start_dot), FadeIn(end_dot))
        self.wait(1)

        # Store objects
        self.phase1_objects = VGroup(
            self.main_axes, x1_label, x2_label,
            self.trajectory_curve, start_dot, end_dot, desc
        )

        self.play(FadeOut(phase_label))

    def phase2_centering(self):
        """Phase 2: Center the data (subtract mean)"""
        # Phase label
        phase_label = Text(get_string("phase2_label"), color=BLUE).scale(0.55)
        phase_label.next_to(self.title, DOWN, buff=0.2)
        self.play(FadeIn(phase_label))
        self.wait(0.5)

        # Show mean position
        mean_point = self.main_axes.coords_to_point(
            self.mean_position[0] * self.viz_scale,
            self.mean_position[1] * self.viz_scale
        )
        mean_dot = Dot(mean_point, color=GREEN, radius=0.1)
        mean_label = Text(get_string("mean_position"), color=GREEN).scale(0.48)
        mean_label.next_to(mean_dot, DOWN + LEFT, buff=0.25)

        self.play(FadeIn(mean_dot), FadeIn(mean_label))
        self.wait(1)

        # Show centering formula
        centering_formula = Tex(get_string("centering_formula"), color=YELLOW).scale(0.7)
        centering_formula.move_to(RIGHT * 4.5 + UP * 2.8)
        self.play(FadeIn(centering_formula))

        # Physical explanation
        centering_expl = Text(get_string("centering_explanation"), color=YELLOW).scale(0.4)
        centering_expl.next_to(centering_formula, DOWN, buff=0.15)
        self.play(FadeIn(centering_expl))

        # Show mean value
        mean_text = Text(f"mu = [{self.mean_position[0]:.1f}, {self.mean_position[1]:.1f}]",
                        color=GREEN).scale(0.42)
        mean_text.next_to(centering_expl, DOWN, buff=0.25)
        self.play(FadeIn(mean_text))
        self.wait(1)

        # Create centered trajectory curve
        centered_points = []
        for x1, x2 in self.centered_data:
            point = self.main_axes.coords_to_point(x1 * self.viz_scale, x2 * self.viz_scale)
            centered_points.append(point)

        centered_curve = VMobject()
        centered_curve.set_points_as_corners(centered_points)
        centered_curve.set_color_by_gradient(BLUE, RED)
        centered_curve.set_stroke(width=3)

        # Animate the shift
        self.play(
            Transform(self.trajectory_curve, centered_curve),
            FadeOut(mean_dot),
            FadeOut(mean_label),
            run_time=2
        )
        self.wait(1)

        # Label centered data
        centered_label = Text(get_string("centered_data"), color=WHITE).scale(0.45)
        centered_label.move_to(self.main_axes.get_bottom() + DOWN * 0.6)
        self.play(FadeIn(centered_label))
        self.wait(1)

        # Store for later
        self.centering_objects = VGroup(centering_formula, centering_expl, mean_text, centered_label)

        self.play(FadeOut(phase_label))

    def phase3_pca_decomposition(self):
        """Phase 3: Covariance and PCA decomposition"""
        # Phase label
        phase_label = Text(get_string("phase3_label"), color=BLUE).scale(0.55)
        phase_label.next_to(self.title, DOWN, buff=0.2)
        self.play(FadeIn(phase_label))
        self.wait(0.5)

        # Fade out centering objects to avoid collision with new formulas
        self.play(FadeOut(self.centering_objects))
        self.wait(0.3)

        # Covariance ellipse
        ellipse = self.create_covariance_ellipse()
        ellipse.set_stroke(ORANGE, width=2)
        ellipse.set_fill(ORANGE, opacity=0.15)

        cov_label = Text(get_string("covariance"), color=ORANGE).scale(0.42)
        cov_label.move_to(self.main_axes.get_top() + UP * 0.4)

        self.play(ShowCreation(ellipse), FadeIn(cov_label))

        # Ellipse explanation
        ellipse_expl = Text(get_string("ellipse_explanation"), color=ORANGE).scale(0.38)
        ellipse_expl.next_to(cov_label, DOWN, buff=0.12)
        self.play(FadeIn(ellipse_expl))
        self.wait(1.0)

        # Show PC axes
        origin = self.main_axes.coords_to_point(0, 0)

        # PC1
        scale1 = 2.5 * np.sqrt(self.eigenvalues[0]) * self.viz_scale
        pc1_end = origin + scale1 * np.array([np.cos(self.rotation_angle),
                                               np.sin(self.rotation_angle), 0])
        pc1_start = origin - scale1 * np.array([np.cos(self.rotation_angle),
                                                 np.sin(self.rotation_angle), 0])

        self.pc1_line = Line(pc1_start, pc1_end, stroke_width=4, color=YELLOW)
        pc1_label = Text(get_string("pc1_label"), color=YELLOW).scale(0.52)
        pc1_label.next_to(pc1_end, UP + RIGHT, buff=0.2)

        # PC2
        angle2 = self.rotation_angle + np.pi/2
        scale2 = 2.5 * np.sqrt(self.eigenvalues[1]) * self.viz_scale
        pc2_end = origin + scale2 * np.array([np.cos(angle2), np.sin(angle2), 0])
        pc2_start = origin - scale2 * np.array([np.cos(angle2), np.sin(angle2), 0])

        self.pc2_line = Line(pc2_start, pc2_end, stroke_width=4, color=GREEN)
        pc2_label = Text(get_string("pc2_label"), color=GREEN).scale(0.52)
        pc2_label.next_to(pc2_end, UP + LEFT, buff=0.25)  # Shortened to "PC2" so now fits on screen

        self.play(
            ShowCreation(self.pc1_line),
            FadeIn(pc1_label),
            run_time=1
        )
        self.play(
            ShowCreation(self.pc2_line),
            FadeIn(pc2_label),
            run_time=1
        )
        self.wait(0.8)

        # Show covariance matrix (before rotation) - prominently displayed
        cov_matrix_display = self.create_covariance_matrix_display(
            self.cov_matrix,
            get_string("cov_before"),
            highlight_offdiag=True
        )
        cov_matrix_display.move_to(RIGHT * 5.0 + UP * 0.8)  # More central position
        cov_matrix_display.scale(1.2)  # Make it larger and more prominent
        self.play(FadeIn(cov_matrix_display))
        self.wait(2.0)

        # Show numbers box
        #self.numbers_box = self.create_numbers_box()
        #self.play(FadeIn(self.numbers_box))
        #self.wait(1.5)

        # Store objects
        self.pca_objects = VGroup(
            ellipse, cov_label, ellipse_expl,
            self.pc1_line, pc1_label, self.pc2_line, pc2_label,
            cov_matrix_display
        )

        self.play(FadeOut(phase_label))

    def create_covariance_ellipse(self):
        """Create covariance ellipse"""
        scale = 2.0
        n_points = 100
        theta = np.linspace(0, 2*np.pi, n_points)

        # Standard circle
        circle_points = np.array([np.cos(theta), np.sin(theta)]).T

        # Scale by sqrt of eigenvalues
        scaled_points = circle_points * np.sqrt(self.eigenvalues) * scale * self.viz_scale

        # Rotate by eigenvectors
        rotated_points = scaled_points @ self.eigenvectors.T

        # Convert to scene coordinates
        points_3d = [self.main_axes.coords_to_point(p[0], p[1])
                    for p in rotated_points]

        ellipse = VMobject()
        ellipse.set_points_as_corners(points_3d + [points_3d[0]])

        return ellipse

    def phase4_rotation(self):
        """Phase 4: Coordinate system rotation (split-screen)"""
        # Phase label
        phase_label = Text(get_string("phase4_label"), color=BLUE).scale(0.55)
        phase_label.next_to(self.title, DOWN, buff=0.2)
        self.play(FadeIn(phase_label))
        self.wait(0.5)

        # Fade out some elements
        self.play(FadeOut(self.centering_objects), FadeOut(self.pca_objects))
        self.wait(0.3)

        # Create split screen labels (clean, no formulas)
        orig_label = Text(get_string("original_system"), color=BLUE_C).scale(0.55)
        orig_label.move_to(LEFT * 2.5 + UP * 3.0)

        rot_label = Text(get_string("rotated_system"), color=YELLOW).scale(0.55)
        rot_label.move_to(RIGHT * 4 + UP * 3.0)

        self.play(FadeIn(orig_label), FadeIn(rot_label))
        self.wait(0.5)

        # Create rotated coordinate system (right side)
        self.rotated_axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[-3, 3, 2],
            width=5.5,
            height=5.5,
            axis_config={"include_tip": True}
        )
        self.rotated_axes.shift(RIGHT * 4 + DOWN * 0.5)

        # Labels for rotated axes
        pc1_axis_label = Text(get_string("pc1_label"), color=YELLOW).scale(0.6)
        pc1_axis_label.next_to(self.rotated_axes.get_x_axis().get_end(), RIGHT, buff=0.3)

        pc2_axis_label = Text(get_string("pc2_label"), color=GREEN).scale(0.6)
        pc2_axis_label.next_to(self.rotated_axes.get_y_axis().get_end(), UP, buff=0.25)  # Now fits on screen since shortened to "PC2"

        self.play(
            ShowCreation(self.rotated_axes),
            FadeIn(pc1_axis_label),
            FadeIn(pc2_axis_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Create rotated trajectory
        rotated_points = []
        for y1, y2 in self.rotated_trajectory:
            point = self.rotated_axes.coords_to_point(y1 * self.viz_scale, y2 * self.viz_scale)
            rotated_points.append(point)

        rotated_curve = VMobject()
        rotated_curve.set_points_as_corners(rotated_points)
        rotated_curve.set_color_by_gradient(BLUE, RED)
        rotated_curve.set_stroke(width=3)

        # Animate appearance of rotated trajectory
        self.play(ShowCreation(rotated_curve), run_time=3)
        self.wait(1)

        # Store objects
        self.rotation_objects = VGroup(
            orig_label, rot_label,
            self.rotated_axes, pc1_axis_label, pc2_axis_label, rotated_curve
        )

        self.play(FadeOut(phase_label))

    def phase5_separation(self):
        """Phase 5: Demonstrate separation of motions"""
        # Phase label
        phase_label = Text(get_string("phase5_label"), color=BLUE).scale(0.55)
        phase_label.next_to(self.title, DOWN, buff=0.2)
        self.play(FadeIn(phase_label))
        self.wait(0.5)

        # Highlight the separation
        # Add annotations on rotated system
        linear_arrow = Arrow(
            self.rotated_axes.coords_to_point(-4, -1.8),
            self.rotated_axes.coords_to_point(4, -1.8),
            stroke_width=3,
            color=YELLOW,
            buff=0
        )
        linear_text = Text(get_string("linear_motion"), color=YELLOW).scale(0.45)
        linear_text.next_to(linear_arrow, DOWN, buff=0.15)

        self.play(
            ShowCreation(linear_arrow),
            FadeIn(linear_text)
        )
        self.wait(1)

        # Oscillation (vertical)
        osc_arrow = Arrow(
            self.rotated_axes.coords_to_point(4.5, -1.3),
            self.rotated_axes.coords_to_point(4.5, 1.3),
            stroke_width=3,
            color=GREEN,
            buff=0
        )
        osc_text = Text(get_string("oscillation"), color=GREEN).scale(0.45)
        osc_text.next_to(osc_arrow, RIGHT, buff=0.15)

        self.play(
            ShowCreation(osc_arrow),
            FadeIn(osc_text)
        )
        self.wait(1)

        # Show covariance matrix (after rotation) - THE KEY INSIGHT!
        cov_matrix_rotated = np.cov(self.rotated_trajectory.T)
        cov_matrix_display_after = self.create_covariance_matrix_display(
            cov_matrix_rotated,
            get_string("cov_after"),
            highlight_offdiag=True
        )
        cov_matrix_display_after.move_to(LEFT * 2.5 + DOWN * 2.8)
        self.play(FadeIn(cov_matrix_display_after))
        self.wait(1)

        # Key insight text (positioned lower to avoid overlap with phase_label)
        key_insight = Text(get_string("key_insight"), color=YELLOW).scale(0.6)
        key_insight.move_to(UP * 2.9)
        self.play(FadeIn(key_insight))
        self.wait(1.5)

        # "Separated!" label
        separated_text = Text(get_string("separated"), color=GREEN).scale(0.7)
        separated_text.move_to(RIGHT * 4 + DOWN * 2.9)
        self.play(FadeIn(separated_text))
        self.wait(1.5)

        # Store
        self.separation_objects = VGroup(
            linear_arrow, linear_text, osc_arrow, osc_text,
            cov_matrix_display_after, key_insight, separated_text
        )

        self.play(FadeOut(phase_label))

    def phase6_dimensionality_reduction(self):
        """Phase 6: Dimensionality reduction with back-projection"""
        # Phase label
        phase_label = Text(get_string("phase6_label"), color=BLUE).scale(0.55)
        phase_label.next_to(self.title, DOWN, buff=0.2)
        self.play(FadeIn(phase_label))
        self.wait(0.5)

        # Fade out previous phase
        self.play(
            FadeOut(self.phase1_objects),
            FadeOut(self.rotation_objects),
            FadeOut(self.separation_objects)
        )

        # Title
        dim_red_title = Text(get_string("dim_reduction"), color=YELLOW).scale(0.65)
        dim_red_title.move_to(UP * 3.2)
        self.play(FadeIn(dim_red_title))
        self.wait(0.5)

        # Create three panels: Full | Only PC1 | Only PC2
        # Panel 1: Full data (left)
        axes1 = Axes(
            x_range=[-2, 12, 4],
            y_range=[-2, 12, 4],
            width=3.5,
            height=3.5,
            axis_config={"include_tip": True}
        ).shift(LEFT * 4.5 + DOWN * 0.8)

        label1 = Text(get_string("full_data"), color=WHITE).scale(0.48)
        label1.next_to(axes1, UP, buff=0.25)

        # Full trajectory
        full_points = []
        for x1, x2 in self.centered_data:
            point = axes1.coords_to_point(x1 * self.viz_scale, x2 * self.viz_scale)
            full_points.append(point)

        full_curve = VMobject()
        full_curve.set_points_as_corners(full_points)
        full_curve.set_color_by_gradient(BLUE, RED)
        full_curve.set_stroke(width=2.5)

        # Panel 2: Only PC1 (center)
        axes2 = Axes(
            x_range=[-2, 12, 4],
            y_range=[-2, 12, 4],
            width=3.5,
            height=3.5,
            axis_config={"include_tip": True}
        ).shift(LEFT * 0.3 + DOWN * 0.8)

        label2 = Text(get_string("only_pc1"), color=YELLOW).scale(0.48)
        label2.next_to(axes2, UP, buff=0.25)

        # Back-project: keep only PC1
        pc1_only = self.rotated_trajectory.copy()
        pc1_only[:, 1] = 0  # Set PC2 to 0
        back_proj_pc1 = pc1_only @ self.eigenvectors.T

        pc1_points = []
        for x1, x2 in back_proj_pc1:
            point = axes2.coords_to_point(x1 * self.viz_scale, x2 * self.viz_scale)
            pc1_points.append(point)

        pc1_curve = VMobject()
        pc1_curve.set_points_as_corners(pc1_points)
        pc1_curve.set_color_by_gradient(BLUE, RED)
        pc1_curve.set_stroke(width=2.5)

        # Panel 3: Only PC2 (right)
        axes3 = Axes(
            x_range=[-2, 12, 4],
            y_range=[-2, 12, 4],
            width=3.5,
            height=3.5,
            axis_config={"include_tip": True}
        ).shift(RIGHT * 3.9 + DOWN * 0.8)

        label3 = Text(get_string("only_pc2"), color=GREEN).scale(0.48)
        label3.next_to(axes3, UP, buff=0.25)

        # Back-project: keep only PC2
        pc2_only = self.rotated_trajectory.copy()
        pc2_only[:, 0] = 0  # Set PC1 to 0
        back_proj_pc2 = pc2_only @ self.eigenvectors.T

        pc2_points = []
        for x1, x2 in back_proj_pc2:
            point = axes3.coords_to_point(x1 * self.viz_scale, x2 * self.viz_scale)
            pc2_points.append(point)

        pc2_curve = VMobject()
        pc2_curve.set_points_as_corners(pc2_points)
        pc2_curve.set_color_by_gradient(BLUE, RED)
        pc2_curve.set_stroke(width=2.5)

        # Show axes
        self.play(
            ShowCreation(axes1),
            ShowCreation(axes2),
            ShowCreation(axes3),
            FadeIn(label1),
            FadeIn(label2),
            FadeIn(label3),
            run_time=1.5
        )
        self.wait(0.5)

        # Show curves
        self.play(
            ShowCreation(full_curve),
            run_time=2
        )
        self.wait(0.5)

        # Explain PC1
        keep_pc1_text = Text(get_string("keep_pc1"), color=YELLOW).scale(0.38)
        keep_pc1_text.move_to(LEFT * 0.3 + DOWN * 2.9)
        var_pc1_text = Text(f"{self.explained_variance[0]:.0f}% {get_string('variance_explained')}",
                           color=YELLOW).scale(0.38)
        var_pc1_text.next_to(keep_pc1_text, DOWN, buff=0.12)

        self.play(
            FadeIn(keep_pc1_text),
            FadeIn(var_pc1_text)
        )
        self.play(ShowCreation(pc1_curve), run_time=2)
        self.wait(1)

        # Explain PC2
        keep_pc2_text = Text(get_string("keep_pc2"), color=GREEN).scale(0.38)
        keep_pc2_text.move_to(RIGHT * 3.9 + DOWN * 2.9)
        var_pc2_text = Text(f"{self.explained_variance[1]:.0f}% {get_string('variance_explained')}",
                           color=GREEN).scale(0.38)
        var_pc2_text.next_to(keep_pc2_text, DOWN, buff=0.12)

        self.play(
            FadeIn(keep_pc2_text),
            FadeIn(var_pc2_text)
        )
        self.play(ShowCreation(pc2_curve), run_time=2)
        self.wait(2)

        # Store
        self.dim_reduction_objects = VGroup(
            dim_red_title,
            axes1, axes2, axes3,
            label1, label2, label3,
            full_curve, pc1_curve, pc2_curve,
            keep_pc1_text, var_pc1_text,
            keep_pc2_text, var_pc2_text
        )

        self.play(FadeOut(phase_label))

    def phase7_md_connection(self):
        """Phase 7: Connect to MD applications"""
        # Phase label
        phase_label = Text(get_string("phase7_label"), color=BLUE).scale(0.55)
        phase_label.next_to(self.title, DOWN, buff=0.2)
        self.play(FadeIn(phase_label))
        self.wait(0.5)

        # Fade out everything
        self.play(
            FadeOut(self.dim_reduction_objects),
        #    FadeOut(self.numbers_box),
            FadeOut(self.color_legend)
        )

        # MD explanation
        md_title = Text(get_string("md_title"), color=YELLOW).scale(0.8)
        md_title.move_to(UP * 3)

        self.play(FadeIn(md_title))
        self.wait(0.5)

        # Main points about MD and PCA
        md_points = VGroup(
            Text(get_string("md_text1"), color=WHITE).scale(0.55),
            Text(get_string("md_text2"), color=BLUE_C).scale(0.55),
            Text(get_string("md_text3"), color=YELLOW).scale(0.55),
            Text(get_string("md_text4"), color=GREEN).scale(0.55),
            Text(get_string("md_text5"), color=WHITE).scale(0.55)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        #md_points.move_to(UP * 1.1)

        #for point in md_points:
        #    self.play(FadeIn(point), run_time=0.6)
        #    self.wait(0.4)

        #self.wait(1)

        # Practical applications section
        examples_title = Text(get_string("md_example_title"), color=ORANGE).scale(0.65)
        examples_title.move_to(DOWN * 0.9)

        examples = VGroup(
            Text(get_string("md_example1"), color=WHITE).scale(0.5),
            Text(get_string("md_example2"), color=WHITE).scale(0.5),
            Text(get_string("md_example3"), color=WHITE).scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        examples.next_to(examples_title, DOWN, buff=0.3)

        #self.play(FadeIn(examples_title))
        #self.wait(0.3)

        #for example in examples:
        #    self.play(FadeIn(example), run_time=0.5)
        #    self.wait(0.3)

        #self.wait(2.5)

        # Fade out
        self.play(
            FadeOut(phase_label),
            FadeOut(md_title),
            FadeOut(md_points),
            FadeOut(examples_title),
            FadeOut(examples),
            FadeOut(self.title)
        )


if __name__ == "__main__":
    # Run with: manimgl pca_molecular_dynamics.py PCAMolecularDynamics
    # Or export: manimgl pca_molecular_dynamics.py PCAMolecularDynamics --write_file
    pass
