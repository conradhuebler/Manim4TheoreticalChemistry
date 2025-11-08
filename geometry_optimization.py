#!/usr/bin/env python3
"""
Geometry Optimization: Newton Method with Modifications
Shows Newton's method for finding energy minima on a complex potential surface
"""

from manimlib import *
import numpy as np
from scipy.optimize import minimize

LANGUAGE = "EN"

def get_string(key):
    """Get localized string"""
    strings = {
        "DE": {
            "title": "Geometrieoptimierung: Modifiziertes Newton-Verfahren",
            "position": "Position x",
            "energy": "Energie E",
            "iteration": "Iteration",
            "convergence": "Konvergiert!",
            "local_min": "Lokales Minimum",
            "global_min": "Globales Minimum",
            "maximum": "Maximum",
            "saddle": "Sattelpunkt",
            "scenario1": "Szenario 1: Konvergenz zum globalen Minimum",
            "scenario2": "Szenario 2: Trapped im lokalen Minimum",
            "scenario3": "Szenario 3: Start nahe Sattelpunkt",
            "summary_title": "Modifiziertes Newton-Verfahren:",
            "summary_newton": "• H > 0: Newton-Schritt x' = x - g/H",
            "summary_negative_h": "• H < 0: Gradient Descent (vermeidet Maxima)",
            "summary_zero_h": "• H ≈ 0: Gradient Descent (vermeidet Instabilität)",
            "summary_convergence": "• Konvergenz: |g| < ε",
        },
        "EN": {
            "title": "Geometry Optimization: Modified Newton Method",
            "position": "Position x",
            "energy": "Energy E",
            "iteration": "Iteration",
            "convergence": "Converged!",
            "local_min": "Local Minimum",
            "global_min": "Global Minimum",
            "maximum": "Maximum",
            "saddle": "Saddle Point",
            "scenario1": "Scenario 1: Convergence to Global Minimum",
            "scenario2": "Scenario 2: Trapped in Local Minimum",
            "scenario3": "Scenario 3: Starting Near Saddle Point",
            "summary_title": "Modified Newton Method:",
            "summary_newton": "• H > 0: Newton step x' = x - g/H",
            "summary_negative_h": "• H < 0: Gradient Descent (avoids maxima)",
            "summary_zero_h": "• H ≈ 0: Gradient Descent (avoids instability)",
            "summary_convergence": "• Convergence: |g| < ε",
        }
    }
    return strings[LANGUAGE].get(key, key)

class GeometryOptimizationImproved(Scene):
    """Geometry optimization with modified Newton method.

    GUI-compatible PARAMETERS structure for geometry optimization animation.
    """

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # ========================================================================
        # PES DOMAIN
        # ========================================================================
        "x_min": {
            "value": -3.0,
            "type": float,
            "unit": "-",
            "description": "Minimum x coordinate for PES domain",
            "min": -10.0,
            "max": 0.0
        },
        "x_max": {
            "value": 3.0,
            "type": float,
            "unit": "-",
            "description": "Maximum x coordinate for PES domain",
            "min": 0.0,
            "max": 10.0
        },

        # ========================================================================
        # CONVERGENCE CRITERIA
        # ========================================================================
        "convergence_threshold": {
            "value": 5e-4,
            "type": float,
            "unit": "-",
            "description": "Convergence threshold for gradient norm |g| < ε",
            "min": 1e-6,
            "max": 1e-2
        },
        "max_iterations": {
            "value": 20,
            "type": int,
            "unit": "iterations",
            "description": "Maximum number of optimization iterations",
            "min": 5,
            "max": 100
        },

        # ========================================================================
        # OPTIMIZATION ROBUSTNESS PARAMETERS
        # ========================================================================
        "max_step_size": {
            "value": 0.5,
            "type": float,
            "unit": "-",
            "description": "Trust region radius (maximum step size)",
            "min": 0.1,
            "max": 2.0
        },
        "lm_lambda": {
            "value": 1e-3,
            "type": float,
            "unit": "-",
            "description": "Levenberg-Marquardt damping parameter",
            "min": 1e-6,
            "max": 1.0
        },
        "backtrack_alpha": {
            "value": 0.3,
            "type": float,
            "unit": "-",
            "description": "Backtracking step reduction factor",
            "min": 0.1,
            "max": 0.9
        },
        "backtrack_c": {
            "value": 0.5,
            "type": float,
            "unit": "-",
            "description": "Armijo condition parameter for line search",
            "min": 0.01,
            "max": 0.99
        },
        "max_backtrack_iter": {
            "value": 10,
            "type": int,
            "unit": "iterations",
            "description": "Maximum backtracking line search iterations",
            "min": 1,
            "max": 50
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_parameters()

    def setup_parameters(self):
        """Extract parameters from central PARAMETERS dictionary"""
        # PES domain
        self.x_min = self.PARAMETERS["x_min"]["value"]
        self.x_max = self.PARAMETERS["x_max"]["value"]

        # Complex PES: sum of Gaussians (hardcoded, not user-configurable)
        # These define the specific shape of the potential energy surface
        self.pes_params = [
            {"A": -2.0, "x0": -1.5, "sigma": 0.3},   # Local minimum
            {"A": -3.0, "x0": 0.5, "sigma": 0.4},    # Global minimum
            {"A": -1.5, "x0": 1.8, "sigma": 0.2},    # Local minimum
            {"A": 1.0, "x0": -0.2, "sigma": 0.15},   # Barrier
            {"A": 0.8, "x0": 1.1, "sigma": 0.1},     # Barrier
        ]

        # Convergence criteria
        self.convergence_threshold = self.PARAMETERS["convergence_threshold"]["value"]
        self.max_iterations = self.PARAMETERS["max_iterations"]["value"]

        # Robustness parameters
        self.max_step_size = self.PARAMETERS["max_step_size"]["value"]
        self.lm_lambda = self.PARAMETERS["lm_lambda"]["value"]
        self.backtrack_alpha = self.PARAMETERS["backtrack_alpha"]["value"]
        self.backtrack_c = self.PARAMETERS["backtrack_c"]["value"]
        self.max_backtrack_iter = self.PARAMETERS["max_backtrack_iter"]["value"]

    def pes_function(self, x):
        """Potential energy surface"""
        E = 0.0
        for p in self.pes_params:
            E += p["A"] * np.exp(-((x - p["x0"]) / p["sigma"])**2)
        return E

    def pes_gradient(self, x):
        """First derivative dE/dx"""
        g = 0.0
        for p in self.pes_params:
            g += p["A"] * (-2 * (x - p["x0"]) / p["sigma"]**2) * \
                 np.exp(-((x - p["x0"]) / p["sigma"])**2)
        return g

    def pes_hessian(self, x):
        """Second derivative d²E/dx²"""
        H = 0.0
        for p in self.pes_params:
            exp_term = np.exp(-((x - p["x0"]) / p["sigma"])**2)
            H += p["A"] * ((-2 / p["sigma"]**2) +
                          (4 * (x - p["x0"])**2 / p["sigma"]**4)) * exp_term
        return H

    def find_critical_points(self):
        """
        Find all critical points (minima and maxima) using LOCAL scipy.optimize
        Returns: (minima, maxima) as lists of (x, E, H) tuples
        """
        minima = []
        maxima = []

        # Use dense grid of starting points for LOCAL optimization
        n_starts = 40
        start_points = np.linspace(self.x_min, self.x_max, n_starts)

        # Find minima using LOCAL optimization (each start converges to nearest minimum)
        for x0 in start_points:
            result = minimize(
                self.pes_function,
                x0=x0,
                method='L-BFGS-B',
                bounds=[(self.x_min, self.x_max)]
            )
            if result.success:
                x_crit = result.x[0]
                E_crit = result.fun
                H_crit = self.pes_hessian(x_crit)
                g_crit = self.pes_gradient(x_crit)

                # Verify it's actually a critical point and a minimum
                if abs(g_crit) < 1e-3 and H_crit > 0.01:
                    # Check if not a duplicate
                    is_duplicate = False
                    for existing_x, _, _ in minima:
                        if abs(x_crit - existing_x) < 0.1:
                            is_duplicate = True
                            break
                    if not is_duplicate:
                        minima.append((x_crit, E_crit, H_crit))

        # Find maxima by minimizing negative function with LOCAL optimization
        for x0 in start_points:
            result = minimize(
                lambda x: -self.pes_function(x[0]) if hasattr(x, '__iter__') else -self.pes_function(x),
                x0=[x0],
                method='L-BFGS-B',
                bounds=[(self.x_min, self.x_max)]
            )
            if result.success:
                x_crit = result.x[0]
                E_crit = self.pes_function(x_crit)
                H_crit = self.pes_hessian(x_crit)
                g_crit = self.pes_gradient(x_crit)

                # Verify it's actually a critical point and a maximum
                if abs(g_crit) < 1e-3 and H_crit < -0.01:
                    # Check if not a duplicate
                    is_duplicate = False
                    for existing_x, _, _ in maxima:
                        if abs(x_crit - existing_x) < 0.1:
                            is_duplicate = True
                            break
                    if not is_duplicate:
                        maxima.append((x_crit, E_crit, H_crit))

        # Sort by x position
        minima.sort(key=lambda t: t[0])
        maxima.sort(key=lambda t: t[0])

        return minima, maxima

    def construct(self):
        """Main animation"""
        self.setup_scene()
        self.wait(1)

        self.run_scenario(
            start_x=1,
            label=get_string("scenario1"),
            color=GREEN
        )
        self.wait(2)

        self.run_scenario(
            start_x=-2.0,
            label=get_string("scenario2"),
            color=ORANGE
        )
        self.wait(2)

        self.run_scenario(
            start_x=-0.25,
            label=get_string("scenario3"),
            color=RED
        )
        self.wait(2)

        self.show_summary()
        self.wait(3)

    def setup_scene(self):
        """Setup layout and PES plot"""
        # Title
        self.title = Text(get_string("title"), font_size=32)
        self.title.to_edge(UP, buff=0.2)
        self.play(FadeIn(self.title))

        # PES axes
        self.axes = Axes(
            x_range=(self.x_min, self.x_max, 1.0),
            y_range=(-3.5, 3.0, 1.0),
            height=5.0,
            width=10.0,
            axis_config={"stroke_color": GREY, "include_tip": True}
        ).move_to(ORIGIN + DOWN * 0.5)

        x_label = Text(get_string("position"), font_size=22)
        x_label.next_to(self.axes, DOWN, buff=0.3)

        y_label = Text(get_string("energy"), font_size=22)
        y_label.next_to(self.axes, LEFT, buff=0.3)

        self.play(
            ShowCreation(self.axes),
            FadeIn(x_label),
            FadeIn(y_label)
        )

        # PES curve
        x_vals = np.linspace(self.x_min, self.x_max, 300)
        pes_points = [
            self.axes.coords_to_point(x, np.clip(self.pes_function(x), -3.5, 3.0))
            for x in x_vals
        ]

        self.pes_curve = VMobject(color=BLUE, stroke_width=3)
        self.pes_curve.set_points_as_corners(pes_points)
        self.play(ShowCreation(self.pes_curve))

        # Label critical points
        self.label_critical_points()

        # Show labels for 10 seconds, then fade out to reduce clutter
        self.wait(10)
        self.play(FadeOut(self.critical_point_labels))
        self.wait(0.5)

    def label_critical_points(self):
        """Find and label minima (global/local) and maxima using scipy optimization"""
        # Use scipy to find precise critical points
        minima, maxima = self.find_critical_points()

        # Find global minimum (lowest energy among minima)
        global_min_idx = None
        if minima:
            global_min_idx = min(range(len(minima)), key=lambda i: minima[i][1])

        # Combine all critical points for intelligent positioning
        all_points = []
        for idx, (x_crit, E_crit, H_crit) in enumerate(minima):
            label_type = "global_min" if idx == global_min_idx else "local_min"
            color = BLUE if idx == global_min_idx else GREEN
            all_points.append((x_crit, E_crit, label_type, color))

        for x_crit, E_crit, H_crit in maxima:
            all_points.append((x_crit, E_crit, "maximum", RED))

        # Sort by x position for intelligent spacing
        all_points.sort(key=lambda p: p[0])

        # Create labels with intelligent positioning
        labels = []
        for i, (x_crit, E_crit, label_type, color) in enumerate(all_points):
            text = get_string(label_type)
            label = Text(text, font_size=18, color=color)

            # Intelligent offset calculation
            # Check distance to neighbors
            offset_y = 0.8  # Base offset

            # If has left neighbor and close
            if i > 0:
                x_prev = all_points[i-1][0]
                if abs(x_crit - x_prev) < 0.8:
                    # Alternate high/low
                    offset_y = 1.2 if i % 2 == 0 else 0.6

            # If has right neighbor and close
            if i < len(all_points) - 1:
                x_next = all_points[i+1][0]
                if abs(x_next - x_crit) < 0.8:
                    # Use higher offset for middle points
                    offset_y = max(offset_y, 1.0)

            # Maxima (higher energy) get pushed up more
            if label_type == "maximum":
                offset_y += 0.3

            label.move_to(self.axes.coords_to_point(x_crit, E_crit + offset_y))
            labels.append(label)

        # Store labels as instance variable for later fade-out
        if labels:
            self.critical_point_labels = VGroup(*labels)
            self.play(FadeIn(self.critical_point_labels))
        else:
            self.critical_point_labels = VGroup()  # Empty group if no labels

    def create_quadratic_approx(self, x0, color=YELLOW):
        """Create parabola approximating PES at x0"""
        E0 = self.pes_function(x0)
        g0 = self.pes_gradient(x0)
        H0 = self.pes_hessian(x0)

        def quad(x):
            return E0 + g0 * (x - x0) + 0.5 * H0 * (x - x0)**2

        # Local range
        x_range = 0.8
        x_local = np.linspace(
            max(x0 - x_range, self.x_min),
            min(x0 + x_range, self.x_max),
            100
        )

        quad_points = [
            self.axes.coords_to_point(x, np.clip(quad(x), -3.5, 3.0))
            for x in x_local
        ]

        parabola = VMobject(color=color, stroke_width=3, stroke_opacity=0.7)
        parabola.set_points_as_corners(quad_points)

        # Parabola minimum
        if abs(H0) > 1e-6:
            x_min = x0 - g0 / H0
            E_min = quad(x_min)
        else:
            x_min = x0
            E_min = E0

        return parabola, x_min, E_min, H0

    def modified_newton_step(self, x_current):
        """
        Robust Modified Newton Method with:
        - Levenberg-Marquardt damping for smooth transition
        - Trust region (max step size)
        - Backtracking line search
        - Safety checks for numerical stability
        """
        g = self.pes_gradient(x_current)
        H = self.pes_hessian(x_current)
        E_current = self.pes_function(x_current)

        # Safety check for NaN/Inf
        if not np.isfinite(g) or not np.isfinite(H):
            return x_current

        # Levenberg-Marquardt: smooth transition between Newton and gradient descent
        # When H is positive and large: behaves like Newton
        # When H is small or negative: behaves like gradient descent
        if H > 1e-6:
            # Positive Hessian: damped Newton step
            H_damped = H + self.lm_lambda
            step = -g / H_damped
        else:
            # Negative or near-zero Hessian: adaptive gradient descent
            # This avoids stepping toward maxima
            alpha = min(0.1, 1.0 / max(abs(g), 1.0))
            step = -alpha * g

        # Trust region: limit step size
        step_magnitude = abs(step)
        if step_magnitude > self.max_step_size:
            step = step * (self.max_step_size / step_magnitude)

        # Backtracking line search: ensure energy does not increase
        x_new = x_current + step
        x_new = np.clip(x_new, self.x_min, self.x_max)
        E_new = self.pes_function(x_new)

        backtrack_iter = 0
        # Simple condition: just ensure energy doesn't increase significantly
        # Allow small increases due to numerical errors
        while E_new > E_current + 1e-10 and backtrack_iter < self.max_backtrack_iter:
            # Reduce step size
            step *= self.backtrack_alpha
            x_new = x_current + step
            x_new = np.clip(x_new, self.x_min, self.x_max)
            E_new = self.pes_function(x_new)
            backtrack_iter += 1

            # If step becomes too small, stop backtracking
            if abs(step) < 1e-8:
                break

        return x_new

    def run_scenario(self, start_x, label, color):
        """Run one optimization scenario"""
        # Scenario label - centered below title
        scenario_label = Text(label, font_size=26, color=color)
        scenario_label.next_to(self.title, DOWN, buff=0.3)
        self.play(FadeIn(scenario_label))

        # Current position marker
        x_current = start_x
        E_current = self.pes_function(x_current)

        current_dot = Dot(radius=0.1, color=RED)
        current_dot.move_to(self.axes.coords_to_point(x_current, E_current))
        self.play(ShowCreation(current_dot))

        # Optimization loop
        iteration = 0
        converged = False

        while iteration < self.max_iterations and not converged:
            iteration += 1

            E_current = self.pes_function(x_current)
            g_current = self.pes_gradient(x_current)
            H_current = self.pes_hessian(x_current)

            # Create quadratic approximation
            parabola, x_min_parab, E_min_parab, H0 = self.create_quadratic_approx(x_current)

            # Show iteration info
            step_type = "Newton" if H_current > 1e-6 else "Gradient Descent"
            step_color_info = GREEN if H_current > 1e-6 else ORANGE

            info = VGroup(
                Text(f"{get_string('iteration')}: {iteration}", font_size=20),
                Text(f"x = {x_current:.3f}", font_size=20),
                Text(f"g = {g_current:.4f}", font_size=20),
                Text(f"H = {H_current:.3f}", font_size=20),
                Text(step_type, font_size=20, color=step_color_info)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            info.to_corner(UR, buff=0.3)

            self.play(FadeIn(info), run_time=0.3)
            self.play(ShowCreation(parabola), run_time=0.4)

            # Show parabola minimum
            parab_dot = Dot(radius=0.08, color=BLUE)
            parab_dot.move_to(self.axes.coords_to_point(x_min_parab, E_min_parab))
            self.play(ShowCreation(parab_dot), run_time=0.3)

            # Check convergence
            if abs(g_current) < self.convergence_threshold:
                converged = True

                # Create convergence texts
                conv_text = Text(get_string("convergence"), font_size=26, color=GREEN)
                grad_info = Text(f"|g| = {abs(g_current):.2e} < {self.convergence_threshold}",
                               font_size=18, color=GREEN)
                type_text = Text(
                    f"H = {H_current:.3f} > 0 → Minimum" if H_current > 0 else
                    f"H = {H_current:.3f} < 0 → Maximum!",
                    font_size=18,
                    color=GREEN if H_current > 0 else RED
                )

                # Group texts together
                conv_group = VGroup(conv_text, grad_info, type_text)
                conv_group.arrange(DOWN, buff=0.15, aligned_edge=LEFT)

                # Position above the current point
                conv_group.next_to(current_dot, UP, buff=0.5)

                # Create background rectangle (covers underlying content)
                conv_bg = BackgroundRectangle(
                    conv_group,
                    color=BLACK,
                    fill_opacity=0.9,
                    buff=0.3
                )

                # Create border
                border_color = GREEN if H_current > 0 else RED
                conv_border = SurroundingRectangle(
                    conv_group,
                    color=border_color,
                    stroke_width=3,
                    buff=0.3
                )

                # Animate box and texts
                self.play(FadeIn(conv_bg), FadeIn(conv_border))
                self.play(FadeIn(conv_group))
                self.wait(1.5)

                # Cleanup convergence info
                self.play(
                    FadeOut(conv_group),
                    FadeOut(conv_bg),
                    FadeOut(conv_border),
                    FadeOut(info),
                    FadeOut(parabola),
                    FadeOut(parab_dot)
                )
                break

            # Step arrow
            x_next = self.modified_newton_step(x_current)
            E_next = self.pes_function(x_next)

            arrow = Arrow(
                current_dot.get_center(),
                self.axes.coords_to_point(x_next, E_next),
                color=ORANGE,
                stroke_width=4
            )
            self.play(ShowCreation(arrow), run_time=0.4)
            self.wait(0.3)

            # Move to new position
            new_pos = self.axes.coords_to_point(x_next, E_next)
            self.play(current_dot.animate.move_to(new_pos), run_time=0.5)

            # Cleanup
            self.play(
                FadeOut(parabola),
                FadeOut(parab_dot),
                FadeOut(arrow),
                FadeOut(info),
                run_time=0.2
            )

            x_current = x_next
            self.wait(0.2)

        # Cleanup scenario
        self.wait(0.5)
        self.play(FadeOut(scenario_label), FadeOut(current_dot))

    def show_summary(self):
        """Show final summary of method"""
        summary = VGroup(
            Text(get_string("summary_title"), font_size=24, color=YELLOW),
            Text(get_string("summary_newton"), font_size=20, color=GREEN),
            Text(get_string("summary_negative_h"), font_size=20, color=ORANGE),
            Text(get_string("summary_zero_h"), font_size=20, color=ORANGE),
            Text(get_string("summary_convergence"), font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        summary.move_to(ORIGIN + DOWN * 3.0)

        #self.play(FadeIn(summary))
