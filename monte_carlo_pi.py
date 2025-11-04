#!/usr/bin/env python3
"""
Monte Carlo π Calculation Visualization
Visualisierung der Monte-Carlo-Methode zur π-Berechnung

Demonstrates Monte Carlo method for calculating π using random point sampling
in a unit circle inscribed in a 2×2 square. Shows statistical convergence
and the power of random sampling methods.

Educational Features:
- Random point generation with visual animation
- Real-time π approximation tracking
- Convergence analysis and error visualization
- Color-coded points (green=inside circle, red=outside)
- Statistical accuracy demonstration
"""

from manimlib import *
import numpy as np
import os

# Ensure directories exist
os.makedirs("./videos", exist_ok=True)
os.makedirs("./images", exist_ok=True)

# Define missing colors and enhanced contrast colors
GRAY = "#808080"
BRIGHT_GREEN = "#00FF00"  # Vivid green for points inside circle
BRIGHT_RED = "#FF4444"    # Vivid red for points outside circle

# Multilingual support
LANGUAGE = "EN"  # Set to "EN" for English or "DE" for German

STRINGS = {
    "DE": {
        "title": "Monte-Carlo-Methode: π-Berechnung",
        "simulation_area": "Simulationsbereich",
        "pi_estimation": "π-Schätzung",
        "convergence_analysis": "Konvergenz-Analyse",
        "current_pi": "Aktueller π-Wert",
        "theoretical_pi": "Theoretischer π-Wert",
        "sample_count": "Stichprobengröße",
        "error": "Fehler",
        "points_inside": "Punkte im Kreis",
        "points_outside": "Punkte außerhalb",
        "total_points": "Gesamtpunkte",
        "accuracy": "Genauigkeit",
        "monte_carlo": "Monte Carlo Simulation",
        "unit_circle": "Einheitskreis",
        "square_boundary": "Quadrat-Grenze",
        "random_sampling": "Zufällige Stichproben",
        "statistical_convergence": "Statistische Konvergenz",
        "pi_approximation": "π-Annäherung",
        "error_reduction": "Fehlerreduktion",
        "iteration": "Iteration",
        "relative_error": "Relativer Fehler (%)",
        "step_by_step_demo": "Monte Carlo Verfahren - Schritt für Schritt",
        "points_in_circle": "Punkte im Kreis",
        "points_outside": "Punkte außerhalb",
        "random_generation": "Zufallszahl generieren...",
        "pi_calculation": "π-Berechnung:",
        "inside": "Innen",
        "outside": "Außen",
        "start_simulation": "Beginne automatische Simulation..."
    },
    "EN": {
        "title": "Monte Carlo Method: π Calculation",
        "simulation_area": "Simulation Area",
        "pi_estimation": "π Estimation",
        "convergence_analysis": "Convergence Analysis",
        "current_pi": "Current π Value",
        "theoretical_pi": "Theoretical π Value",
        "sample_count": "Sample Count",
        "error": "Error",
        "points_inside": "Points Inside",
        "points_outside": "Points Outside",
        "total_points": "Total Points",
        "accuracy": "Accuracy",
        "monte_carlo": "Monte Carlo Simulation",
        "unit_circle": "Unit Circle",
        "square_boundary": "Square Boundary",
        "random_sampling": "Random Sampling",
        "statistical_convergence": "Statistical Convergence",
        "pi_approximation": "π Approximation",
        "error_reduction": "Error Reduction",
        "iteration": "Iteration",
        "relative_error": "Relative Error (%)",
        "step_by_step_demo": "Monte Carlo Procedure - Step by Step",
        "points_in_circle": "Points in Circle",
        "points_outside": "Points Outside",
        "random_generation": "Generating random number...",
        "pi_calculation": "π Calculation:",
        "inside": "Inside",
        "outside": "Outside",
        "start_simulation": "Starting automatic simulation..."
    }
}

def get_string(key):
    return STRINGS[LANGUAGE][key]

class MonteCarloPI(Scene):
    def construct(self):
        # Initialize Monte Carlo parameters
        self.setup_monte_carlo_parameters()

        # Setup 4-quadrant layout
        self.setup_layout()

        # Create simulation area with square and circle
        self.create_simulation_area()

        # Show procedure demonstration first
        self.show_procedure_demonstration()

        # Transition to simulation
        self.transition_to_simulation()
        
        # Run Monte Carlo simulation
        self.run_monte_carlo_simulation()

        self.wait(2)

    def setup_monte_carlo_parameters(self):
        """Setup Monte Carlo simulation parameters"""

        # Mathematical constants
        self.pi_theoretical = np.pi
        self.square_size = 2.0  # 2×2 square from -1 to +1
        self.circle_radius = 1.0  # Unit circle

        # Simulation parameters
        self.total_samples = 5000  # Total points to generate
        self.batch_size = 10  # Points per animation frame
        self.animation_speed = 0.1  # Time between batches (seconds)

        # Current simulation state
        self.sample_count = 0
        self.points_inside_circle = 0
        self.current_pi_estimate = 0.0

        # Data storage for tracking
        self.sample_counts = []
        self.pi_estimates = []
        self.errors = []
        self.relative_errors = []

        # Visual elements storage
        self.displayed_points = []
        self.max_displayed_points = 500  # Limit for performance

    def setup_layout(self):
        """Setup 4-quadrant layout for simulation and analysis"""

        # Screen dimensions and layout
        self.screen_width = 14.0
        self.screen_height = 8.0

        # Define quadrants - charts stay on the right
        self.simulation_region = Rectangle(
            width=7.0, height=8.0,
            fill_opacity=0.05, fill_color=BLUE,
            stroke_color=WHITE, stroke_width=1
        ).move_to(LEFT * 3.5)

        # Position the pi tracking region at the top right (with safe vertical offset)
        self.pi_tracking_region = Rectangle(
            width=7.0, height=4.0,
            fill_opacity=0.05, fill_color=ORANGE,
            stroke_color=ORANGE, stroke_width=1
        ).move_to(RIGHT * 3.5 + UP * 2.0)  # Increased offset to 2.5 for safety

        # Position the convergence region at the bottom right (with safe vertical offset)
        self.convergence_region = Rectangle(
            width=7.0, height=4.0,
            fill_opacity=0.05, fill_color=BLUE,
            stroke_color=BLUE, stroke_width=1
        ).move_to(RIGHT * 3.5 + DOWN * 2.0)  # Increased offset to 2.5 for safety

        # Add simulation region label only (chart labels added later with charts)
        self.simulation_label = Text(
            get_string("simulation_area"), color=WHITE
        ).scale(0.6).move_to(self.simulation_region.get_top() + UP * 0.3)

        # Add title
        self.title = Text(
            get_string("title"), color=YELLOW
        ).scale(0.8).move_to(UP * 3.7)

        # Add all layout elements (region labels added later with charts)
        self.add(self.simulation_region, self.pi_tracking_region, self.convergence_region)
        #self.add(self.simulation_label, self.title)

    def create_simulation_area(self):
        """Create the 2×2 square with unit circle and quadrant lines"""

        # Create coordinate system for simulation area
        simulation_center = self.simulation_region.get_center()

        # Scale factor for visual representation (fit in left quadrant)
        self.sim_scale = 2.5  # Scale simulation coordinates for display

        # Create 2×2 square boundary
        self.square_boundary = Rectangle(
            width=self.square_size * self.sim_scale,
            height=self.square_size * self.sim_scale,
            stroke_color=WHITE,
            stroke_width=3,
            fill_opacity=0
        ).move_to(simulation_center)

        # Create unit circle
        self.unit_circle = Circle(
            radius=self.circle_radius * self.sim_scale,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_opacity=0
        ).move_to(simulation_center)

        # Create dashed quadrant lines
        # Vertical line (x = 0)
        vertical_line = DashedLine(
            simulation_center + UP * self.sim_scale,
            simulation_center + DOWN * self.sim_scale,
            stroke_color=GRAY,
            stroke_width=2,
            dash_length=0.1
        )

        # Horizontal line (y = 0)
        horizontal_line = DashedLine(
            simulation_center + LEFT * self.sim_scale,
            simulation_center + RIGHT * self.sim_scale,
            stroke_color=GRAY,
            stroke_width=2,
            dash_length=0.1
        )

        # Group simulation area elements
        self.simulation_visuals = VGroup(
            self.square_boundary, self.unit_circle, vertical_line, horizontal_line
        )

        # Add coordinate labels
        coord_labels = self.create_coordinate_labels(simulation_center)
        self.simulation_visuals.add(coord_labels)

        # Add to scene
        self.add(self.simulation_visuals)

    def create_coordinate_labels(self, center):
        """Create coordinate labels for the simulation area"""

        label_scale = 0.3
        offset = self.sim_scale * 0.9  # Reduced from 1.1 to avoid edge collision

        # Corner labels
        labels = VGroup(
            Text("(-1, 1)", color=WHITE).scale(label_scale).move_to(
                center + LEFT * offset + UP * offset
            ),
            Text("(1, 1)", color=WHITE).scale(label_scale).move_to(
                center + RIGHT * offset + UP * offset
            ),
            Text("(-1, -1)", color=WHITE).scale(label_scale).move_to(
                center + LEFT * offset + DOWN * offset
            ),
            Text("(1, -1)", color=WHITE).scale(label_scale).move_to(
                center + RIGHT * offset + DOWN * offset
            )
        )

        # Center label
        center_label = Text("(0, 0)", color=YELLOW).scale(label_scale).move_to(
            center + DOWN * 0.3 + RIGHT * 0.3
        )
        labels.add(center_label)

        return labels

    def create_charts(self):
        """Create and display charts when simulation starts"""

        # π tracking plot - now properly positioned in π-tracking-region
        self.pi_axes = Axes(
            x_range=[0, self.total_samples, 1000],  # Clean 1000-sample tick marks
            y_range=[0, 3.5, 1],  # Range around π with fine increments
            width=6,  # Full width of region
            height=2.5  # Full height of region
        ).move_to(self.pi_tracking_region.get_center())

        self.pi_axes.add_coordinate_labels()

        # Add theoretical π line
        pi_line_start = self.pi_axes.coords_to_point(0, self.pi_theoretical)
        pi_line_end = self.pi_axes.coords_to_point(self.total_samples, self.pi_theoretical)
        self.pi_reference_line = Line(
            pi_line_start, pi_line_end,
            stroke_color=RED, stroke_width=2
        )

        # Convergence plot - properly positioned in convergence-region
        self.error_axes = Axes(
            x_range=[0, self.total_samples, 1000],  # Clean 1000-sample tick marks
            y_range=[0, 6, 1],  # Range 0-6% with 1% increments for clean ticks
            width=6,
            height=2.5
        ).move_to(self.convergence_region.get_center())

        self.error_axes.add_coordinate_labels()

        # Add region labels and chart titles
        self.pi_tracking_label = Text(
            get_string("pi_estimation"), color=WHITE
        ).scale(0.6).move_to(self.pi_tracking_region.get_top() + UP)

        self.convergence_label = Text(
            get_string("convergence_analysis"), color=WHITE
        ).scale(0.6).move_to(self.convergence_region.get_top() + UP)

        pi_title = Text(get_string("pi_approximation"), color=YELLOW).scale(0.5).next_to(
            self.pi_axes, UP, buff=0.2)

        error_title = Text(get_string("relative_error"), color=ORANGE).scale(0.5).next_to(
            self.error_axes, UP, buff=0.2)

        # Add X-axis labels
        pi_x_label = Text(get_string("sample_count")).scale(0.3).next_to(
            self.pi_axes.get_x_axis(), DOWN, buff=0.1)

        error_x_label = Text(get_string("sample_count")).scale(0.3).next_to(
            self.error_axes.get_x_axis(), DOWN, buff=0.1)

        # Add plots and labels to scene
        self.add(
            #self.pi_tracking_label, self.convergence_label,
            self.pi_axes, self.pi_reference_line,
            self.error_axes,
            pi_title, error_title,
            pi_x_label, error_x_label
        )

        # Initialize empty graphs
        self.pi_graph = VMobject()
        self.error_graph = VMobject()

    def run_monte_carlo_simulation(self):
        """Run the Monte Carlo simulation with real-time visualization"""

        # Statistics display already created in demo phase - just continue using it

        # Run simulation in batches
        total_batches = self.total_samples // self.batch_size

        for batch in range(total_batches):
            # Generate batch of random points
            self.generate_point_batch()

            # Update π estimation
            self.update_pi_estimation()

            # Update visual displays
            self.update_statistics_display()
            self.update_tracking_plots()

            # Animation pause
            self.wait(self.animation_speed)

        # Final summary
        self.show_final_results()

    def generate_point_batch(self):
        """Generate a batch of random points and add to visualization"""

        simulation_center = self.simulation_region.get_center()

        for _ in range(self.batch_size):
            # Generate random point in [-1, 1] × [-1, 1]
            x = np.random.uniform(-1, 1)
            y = np.random.uniform(-1, 1)

            # Test if point is inside unit circle
            distance_squared = x**2 + y**2
            is_inside = distance_squared <= 1.0

            # Update counters
            self.sample_count += 1
            if is_inside:
                self.points_inside_circle += 1

            # Create visual point with enhanced colors and visibility
            point_color = BRIGHT_GREEN if is_inside else BRIGHT_RED
            visual_point = Dot(
                radius=0.025,  # Slightly larger for better visibility
                color=point_color,
                fill_opacity=0.9,  # More opaque for better contrast
                stroke_width=0  # No border for cleaner look
            ).move_to(simulation_center + np.array([x * self.sim_scale, y * self.sim_scale, 0]))

            # Add to displayed points (with performance limit)
            self.displayed_points.append(visual_point)
            if len(self.displayed_points) > self.max_displayed_points:
                old_point = self.displayed_points.pop(0)
                self.remove(old_point)

            # Add to scene
            self.add(visual_point)

    def update_pi_estimation(self):
        """Update the current π estimation"""

        if self.sample_count > 0:
            ratio = self.points_inside_circle / self.sample_count
            self.current_pi_estimate = 4.0 * ratio

            # Store data for tracking
            self.sample_counts.append(self.sample_count)
            self.pi_estimates.append(self.current_pi_estimate)

            # Calculate errors
            absolute_error = abs(self.current_pi_estimate - self.pi_theoretical)
            relative_error = (absolute_error / self.pi_theoretical) * 100

            self.errors.append(absolute_error)
            self.relative_errors.append(relative_error)

    def create_statistics_display(self):
        """Create real-time statistics display - horizontal layout"""

        # Position directly under the inner square within boundaries
        stats_position = self.square_boundary.get_bottom() + DOWN * 0.4

        # Create text elements
        self.stats_group = VGroup()

        # Current π estimate
        self.pi_estimate_text = Text("π ≈ 0.000", color=YELLOW).scale(0.4)

        # Sample count
        self.sample_count_text = Text("Samples: 0", color=WHITE).scale(0.3)

        # Points breakdown
        self.points_inside_text = Text("Inside: 0", color=BRIGHT_GREEN).scale(0.3)
        self.points_outside_text = Text("Outside: 0", color=BRIGHT_RED).scale(0.3)

        # Error
        self.error_text = Text("Error: 0.00%", color=ORANGE).scale(0.3)

        # Arrange horizontally
        self.stats_group.add(
            self.pi_estimate_text,
            self.sample_count_text,
            self.points_inside_text,
            self.points_outside_text,
            self.error_text
        )

        self.stats_group.arrange(RIGHT, aligned_edge=DOWN, buff=0.3)  # Horizontal arrangement
        self.stats_group.move_to(stats_position)

        self.add(self.stats_group)

    def update_statistics_display(self):
        """Update the real-time statistics display"""

        if self.sample_count > 0:
            # Update π estimate
            new_pi_text = Text(f"π ≈ {self.current_pi_estimate:.4f}", color=YELLOW).scale(0.4)
            new_pi_text.move_to(self.pi_estimate_text.get_center())
            self.remove(self.pi_estimate_text)
            self.pi_estimate_text = new_pi_text
            self.add(self.pi_estimate_text)

            # Update sample count
            new_sample_text = Text(f"Samples: {self.sample_count}", color=WHITE).scale(0.3)
            new_sample_text.move_to(self.sample_count_text.get_center())
            self.remove(self.sample_count_text)
            self.sample_count_text = new_sample_text
            self.add(self.sample_count_text)

            # Update points breakdown
            points_outside = self.sample_count - self.points_inside_circle

            new_inside_text = Text(f"Inside: {self.points_inside_circle}", color=BRIGHT_GREEN).scale(0.3)
            new_inside_text.move_to(self.points_inside_text.get_center())
            self.remove(self.points_inside_text)
            self.points_inside_text = new_inside_text
            self.add(self.points_inside_text)

            new_outside_text = Text(f"Outside: {points_outside}", color=BRIGHT_RED).scale(0.3)
            new_outside_text.move_to(self.points_outside_text.get_center())
            self.remove(self.points_outside_text)
            self.points_outside_text = new_outside_text
            self.add(self.points_outside_text)

            # Update error
            if len(self.relative_errors) > 0:
                current_error = self.relative_errors[-1]
                new_error_text = Text(f"Error: {current_error:.2f}%", color=ORANGE).scale(0.3)
                new_error_text.move_to(self.error_text.get_center())
                self.remove(self.error_text)
                self.error_text = new_error_text
                self.add(self.error_text)

    def update_tracking_plots(self):
        """Update π estimation and convergence plots"""

        if len(self.sample_counts) < 2:
            return

        # Only update if charts have been created (during simulation phase)
        if not hasattr(self, 'pi_axes') or not hasattr(self, 'error_axes'):
            return

        # Clear previous graphs
        self.remove(self.pi_graph, self.error_graph)

        # Create new π estimation graph (TOP CHART - shows current π values)
        if len(self.pi_estimates) > 1:
            pi_points = [
                self.pi_axes.coords_to_point(count, estimate)
                for count, estimate in zip(self.sample_counts, self.pi_estimates)
            ]
            self.pi_graph = VMobject()
            self.pi_graph.set_points_as_corners(pi_points)
            self.pi_graph.set_stroke(color=YELLOW, width=3)  # Yellow for π values

        # Create new error graph (BOTTOM CHART - shows relative errors)
        if len(self.relative_errors) > 1:
            error_points = [
                self.error_axes.coords_to_point(count, error)
                for count, error in zip(self.sample_counts, self.relative_errors)
            ]
            self.error_graph = VMobject()
            self.error_graph.set_points_as_corners(error_points)
            self.error_graph.set_stroke(color=ORANGE, width=3)  # Orange for error

        # Add updated graphs
        self.add(self.pi_graph, self.error_graph)

    def show_final_results(self):
        """Show final simulation results"""

        # Final π estimate
        final_pi = self.current_pi_estimate
        final_error = abs(final_pi - self.pi_theoretical)
        final_relative_error = (final_error / self.pi_theoretical) * 100

        # Create summary text
        summary_text = VGroup(
            Text(f"Final π estimate: {final_pi:.6f}", color=YELLOW).scale(0.5),
            Text(f"Theoretical π: {self.pi_theoretical:.6f}", color=WHITE).scale(0.5),
            Text(f"Absolute error: {final_error:.6f}", color=RED).scale(0.5),
            Text(f"Relative error: {final_relative_error:.4f}%", color=ORANGE).scale(0.5),
            Text(f"Total samples: {self.sample_count}", color=GREEN).scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        summary_text.move_to(UP * 1.5)

        # Add summary with highlight
        summary_box = Rectangle(
            width=summary_text.get_width() + 0.5,
            height=summary_text.get_height() + 0.3,
            stroke_color=YELLOW,
            fill_color=BLACK,
            fill_opacity=0.8
        ).move_to(summary_text.get_center())

        self.add(summary_box, summary_text)
        self.wait(3)

    def show_procedure_demonstration(self):
        """Demonstrate Monte Carlo procedure step-by-step with sample points"""

        # Add title for demonstration phase (more distance from main title)
        demo_title = Text(get_string("step_by_step_demo"), color=YELLOW).scale(0.6)
        demo_title.move_to(UP * 2.8)
        self.add(demo_title)
        self.wait(1)

        # Create stacks for inside/outside points
        self.create_point_stacks()

        # Create statistics display for demo phase
        self.create_statistics_display()

        # Demonstrate with 5 sample points
        demo_points = [
            (0.3, 0.4, True),   # Inside (0.25 ≤ 1)
            (-0.7, 0.6, True),  # Inside (0.85 ≤ 1) - CORRECTED
            (0.2, -0.8, True),  # Inside (0.68 ≤ 1)
            (0.9, 0.8, False),  # Outside (1.45 > 1)
            (-0.5, -0.3, True)  # Inside (0.34 ≤ 1)
        ]

        for i, (x, y, is_inside) in enumerate(demo_points):
            self.demonstrate_single_point(x, y, is_inside, i + 1)
            self.wait(2)

        # Show π calculation
        self.show_pi_calculation_demo(demo_points)
        self.wait(2)

        # Clean up demonstration
        self.cleanup_demonstration(demo_title)

    def create_point_stacks(self):
        """Create visual counter boxes in π-tracking region for demo"""

        # Position counters in π-tracking region (top right area)
        pi_region_center = self.pi_tracking_region.get_center()

        # Inside counter box (left side of π-region)
        inside_counter_pos = pi_region_center + LEFT * 1.5
        self.inside_counter_label = Text(get_string("points_in_circle"), color=BRIGHT_GREEN).scale(0.5)
        self.inside_counter_label.move_to(inside_counter_pos + UP * 0.5)

        # Outside counter box (right side of π-region)
        outside_counter_pos = pi_region_center + RIGHT * 1.5
        self.outside_counter_label = Text(get_string("points_outside"), color=BRIGHT_RED).scale(0.5)
        self.outside_counter_label.move_to(outside_counter_pos + UP * 0.5)

        # Counter display boxes
        self.inside_counter_box = Rectangle(
            width=1.5, height=0.8,
            stroke_color=BRIGHT_GREEN, fill_opacity=0.15, fill_color=BRIGHT_GREEN
        ).move_to(inside_counter_pos + 0.5 * DOWN)

        self.outside_counter_box = Rectangle(
            width=1.5, height=0.8,
            stroke_color=BRIGHT_RED, fill_opacity=0.15, fill_color=BRIGHT_RED
        ).move_to(outside_counter_pos+ 0.5 * DOWN)

        # Counter text displays
        self.inside_counter_text = Text("0", color=BRIGHT_GREEN).scale(1.0).move_to(inside_counter_pos+ 0.5 * DOWN)
        self.outside_counter_text = Text("0", color=BRIGHT_RED).scale(1.0).move_to(outside_counter_pos+ 0.5 * DOWN)

        self.add(self.inside_counter_label, self.outside_counter_label)
        self.add(self.inside_counter_box, self.outside_counter_box)
        self.add(self.inside_counter_text, self.outside_counter_text)

        # Initialize counters
        self.demo_inside_count = 0
        self.demo_outside_count = 0

    def demonstrate_single_point(self, x, y, is_inside, point_num):
        """Demonstrate the complete process for a single point"""

        simulation_center = self.simulation_region.get_center()

        # Step 1: Show dice/random generation
        self.show_random_generation(x, y, point_num)

        # Step 2: Create and place the point
        point_color = BRIGHT_GREEN if is_inside else BRIGHT_RED
        demo_point = Dot(
            radius=0.04, color=point_color,
            fill_opacity=0.9, stroke_width=2, stroke_color=WHITE
        ).move_to(simulation_center + np.array([x * self.sim_scale, y * self.sim_scale, 0]))

        self.add(demo_point)
        self.wait(0.5)

        # Step 3: Show coordinate display
        coord_text = Text(f"({x:.1f}, {y:.1f})", color=WHITE).scale(0.3)
        coord_text.next_to(demo_point, UP, buff=0.1)
        self.add(coord_text)
        self.wait(1)

        # Step 4: Show circle equation test
        self.show_circle_test(x, y, is_inside, demo_point)

        # Step 5: Update counters and keep point in circle
        self.update_demo_counters(is_inside)

        # Keep point in the simulation area
        self.wait(0.5)

        # Clean up temporary text
        self.remove(coord_text)

    def show_random_generation(self, x, y, point_num):
        """Show visual dice/random number generation in π-region"""

        # Position in π-region to avoid title collision
        pi_region_center = self.convergence_region.get_center()
        dice_position = pi_region_center + UP * 1.5

        # Create dice visual
        dice = Rectangle(width=0.6, height=0.6, stroke_color=WHITE, fill_color=GRAY, fill_opacity=0.8)
        dice.move_to(dice_position)

        dice_text = Text(f"#{point_num}", color=WHITE).scale(0.4).move_to(dice.get_center())

        # Show generation process
        generation_text = Text(get_string("random_generation"), color=YELLOW).scale(0.4)
        generation_text.next_to(dice, DOWN, buff=0.2)

        self.add(dice, dice_text, generation_text)
        self.wait(1)

        # Show resulting coordinates
        result_text = Text(f"→ ({x:.1f}, {y:.1f})", color=WHITE).scale(0.4)
        result_text.next_to(generation_text, DOWN, buff=0.2)
        self.add(result_text)
        self.wait(1)

        # Clean up
        self.remove(dice, dice_text, generation_text, result_text)

    def show_circle_test(self, x, y, is_inside, point):
        """Show the circle equation test visually in π-tracking region"""

        # Calculate distance squared
        distance_squared = x**2 + y**2

        # Position in π-tracking region for better layout
        pi_region_center = self.convergence_region.get_center()
        equation_position = pi_region_center + DOWN * 1.0

        # Show equation
        equation_text = Text(f"x² + y² = {x:.1f}² + {y:.1f}² = {distance_squared:.2f}",
                           color=WHITE).scale(0.45)
        equation_text.move_to(equation_position)

        # Show test result
        test_result = "≤ 1" if is_inside else "> 1"
        result_color = BRIGHT_GREEN if is_inside else BRIGHT_RED
        inside_outside = get_string("inside") if is_inside else get_string("outside")
        result_text = Text(f"{distance_squared:.2f} {test_result} → {inside_outside}",
                         color=result_color).scale(0.45)
        result_text.next_to(equation_text, DOWN, buff=0.3)

        self.add(equation_text, result_text)
        self.wait(1.5)

        # Highlight the point briefly
        highlight = Circle(radius=0.1, stroke_color=YELLOW, stroke_width=3)
        highlight.move_to(point.get_center())
        self.add(highlight)
        self.wait(0.5)
        self.remove(highlight)

        # Clean up
        self.remove(equation_text, result_text)

    def update_demo_counters(self, is_inside):
        """Update the counter displays instead of moving points"""

        if is_inside:
            self.demo_inside_count += 1
            # Update inside counter
            new_inside_text = Text(str(self.demo_inside_count), color=BRIGHT_GREEN).scale(0.8)
            new_inside_text.move_to(self.inside_counter_text.get_center())
            self.remove(self.inside_counter_text)
            self.inside_counter_text = new_inside_text
            self.add(self.inside_counter_text)
        else:
            self.demo_outside_count += 1
            # Update outside counter
            new_outside_text = Text(str(self.demo_outside_count), color=BRIGHT_RED).scale(0.8)
            new_outside_text.move_to(self.outside_counter_text.get_center())
            self.remove(self.outside_counter_text)
            self.outside_counter_text = new_outside_text
            self.add(self.outside_counter_text)

    def show_pi_calculation_demo(self, demo_points):
        """Show π calculation with the demonstration points in convergence region"""

        inside_count = sum(1 for _, _, is_inside in demo_points if is_inside)
        total_count = len(demo_points)
        pi_estimate = 4 * inside_count / total_count

        # Show calculation steps in convergence region
        calc_text = VGroup(
            Text(get_string("pi_calculation"), color=YELLOW).scale(0.5),
            Text(f"{get_string('points_inside')}: {inside_count}", color=BRIGHT_GREEN).scale(0.45),
            Text(f"{get_string('total_points')}: {total_count}", color=WHITE).scale(0.45),
            Text(f"π ≈ 4 × ({inside_count}/{total_count}) = {pi_estimate:.2f}", color=YELLOW).scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Position in convergence region for better organization
        convergence_center = self.convergence_region.get_center()
        calc_text.move_to(convergence_center)

        # Add calculation box
        calc_box = Rectangle(
            width=calc_text.get_width() + 0.3,
            height=calc_text.get_height() + 0.2,
            stroke_color=YELLOW, fill_color=BLACK, fill_opacity=0.8
        ).move_to(calc_text.get_center())

        self.add(calc_box, calc_text)
        self.wait(2)

        # Clean up calculation
        self.remove(calc_box, calc_text)

    def transition_to_simulation(self):
        """Clean transition from demo to simulation - remove demo elements and create charts"""

        # Show transition message
        transition_text = Text(get_string("start_simulation"), color=YELLOW).scale(0.6)
        transition_text.move_to(UP * 2.5)
        self.add(transition_text)
        self.wait(1)

        # Remove all demo elements
        self.remove(self.inside_counter_label, self.outside_counter_label)
        self.remove(self.inside_counter_box, self.outside_counter_box)
        self.remove(self.inside_counter_text, self.outside_counter_text)

        # Create and display charts for simulation
        self.create_charts()

        # Remove transition text
        self.remove(transition_text)
        self.wait(0.5)

    def cleanup_demonstration(self, demo_title):
        """Clean up demonstration elements and transition to simulation"""

        # Remove demo title
        self.remove(demo_title)

        # Perform clean transition to simulation
        self.transition_to_simulation()

if __name__ == "__main__":
    # For testing/preview - run with manimgl instead
    import subprocess
    import sys
    subprocess.run([
        sys.executable, "-m", "manimlib",
        __file__, "MonteCarloPI"
    ])