from manimlib import *
import numpy as np
from scipy.integrate import quad
import os

# Ensure directories exist
os.makedirs("./videos", exist_ok=True)
os.makedirs("./images", exist_ok=True)

# Multilingual support
LANGUAGE = "DE"  # Set to "EN" for English or "DE" for German

STRINGS = {
    "DE": {
        "var_title": "Variationsmethode für den Harmonischen Oszillator",
        "var_principle": "Variationsprinzip:",
        "var_principle_eq": "E[\\psi] \\geq E_0",
        "var_exact_energy": "Exakte Energie:",
        "var_trial_functions": "Test-Wellenfunktionen",
        "var_energy_comparison": "Energie-Vergleich",
        "var_optimization": "Optimierung von α",
        "var_current_energy": "Aktuelle Energie:",
        "potential": "Potential",
        "wavefunction": "Wellenfunktion",
        "energy": "Energie",
    },
    "EN": {
        "var_title": "Variational Method for the Harmonic Oscillator",
        "var_principle": "Variational Principle:",
        "var_principle_eq": "E[\\psi] \\geq E_0",
        "var_exact_energy": "Exact Energy:",
        "var_trial_functions": "Trial Wavefunctions",
        "var_energy_comparison": "Energy Comparison",
        "var_optimization": "Optimization of α",
        "var_current_energy": "Current Energy:",
        "potential": "Potential",
        "wavefunction": "Wavefunction",
        "energy": "Energy",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE][key]


# ========================================
# Mathematical Helper Functions
# ========================================

# Physical constants (atomic units: ℏ = m = ω = 1) - will be moved to PARAMETERS
# Temporary module-level for compatibility with functions
HBAR = 1.0
MASS = 1.0
OMEGA = 1.0

def harmonic_potential(x):
    """Harmonic oscillator potential: V(x) = (1/2) * m * ω² * x²"""
    return 0.5 * MASS * OMEGA**2 * x**2

def exact_energy(n):
    """Exact energy eigenvalues for harmonic oscillator"""
    return HBAR * OMEGA * (n + 0.5)


# ========================================
# Trial Wavefunctions
# ========================================

def trial_gaussian(x, alpha):
    """Gaussian trial wavefunction: ψ(x) = (α/π)^(1/4) * exp(-α*x²/2)"""
    normalization = (alpha / np.pi)**(0.25)
    return normalization * np.exp(-alpha * x**2 / 2)

def trial_x2_gaussian(x):
    """Trial: x² * exp(-x²)"""
    norm = np.sqrt(2 / (3 * np.sqrt(np.pi)))
    return norm * x**2 * np.exp(-x**2)

def trial_polynomial_smooth(x, a=2.0):
    """Trial with smooth cutoff: avoids kinks at boundaries

    Uses exp(-1/(1-r²)) cutoff which is C^∞ (infinitely differentiable).
    This avoids numerical problems with finite differences at sharp edges.
    """
    r = x / a

    def smooth_cutoff(r_val):
        abs_r = np.abs(r_val)
        result = np.where(
            abs_r < 0.99,
            np.exp(-1.0 / (1.0 - abs_r**2)),
            0.0
        )
        return result

    psi = smooth_cutoff(r) * (1 - np.where(np.abs(r) < 1, r**2, 1))**2
    norm_sq, _ = quad(lambda y: (smooth_cutoff(y/a) * (1 - np.where(np.abs(y/a) < 1, (y/a)**2, 1))**2)**2, -a*1.5, a*1.5, limit=100)
    return psi / np.sqrt(norm_sq)

def trial_x4_gaussian(x):
    """Trial: x⁴ * exp(-x²)"""
    norm = np.sqrt(8 / (15 * np.sqrt(np.pi)))
    return norm * x**4 * np.exp(-x**2)


# ========================================
# Energy Calculations
# ========================================

def kinetic_energy_integral(psi_func, x_range=(-40, 40)):
    """Calculate ⟨ψ|T|ψ⟩ where T = -(ℏ²/2m) d²/dx²

    Uses 5-point stencil for improved accuracy (O(h⁴) vs O(h²))
    """
    def integrand(x):
        h = 1e-4
        psi = psi_func(x)
        psi_2h = psi_func(x + 2*h)
        psi_h = psi_func(x + h)
        psi_minus_h = psi_func(x - h)
        psi_minus_2h = psi_func(x - 2*h)

        d2psi_dx2 = (-psi_2h + 16*psi_h - 30*psi + 16*psi_minus_h - psi_minus_2h) / (12*h**2)
        return -HBAR**2 / (2 * MASS) * psi * d2psi_dx2

    result, _ = quad(integrand, x_range[0], x_range[1], limit=100)
    return result

def potential_energy_integral(psi_func, V_func, x_range=(-40, 40)):
    """Calculate ⟨ψ|V|ψ⟩"""
    def integrand(x):
        psi = psi_func(x)
        return V_func(x) * psi**2

    result, _ = quad(integrand, x_range[0], x_range[1], limit=100)
    return result

def expectation_energy(psi_func, V_func=harmonic_potential, x_range=(-40, 40)):
    """Calculate E[ψ] = ⟨ψ|H|ψ⟩ / ⟨ψ|ψ⟩

    Explicitly normalizes to ensure Variational Principle is satisfied.
    """
    norm_sq, _ = quad(lambda x: psi_func(x)**2, x_range[0], x_range[1], limit=100)
    T = kinetic_energy_integral(psi_func, x_range)
    V = potential_energy_integral(psi_func, V_func, x_range)
    E = (T + V) / norm_sq
    return E


# ========================================
# Color mapping for energy
# ========================================

def energy_to_color(E, E0=0.5, threshold=0.2):
    """Map energy to color: green (near E0) → yellow → red (far from E0)"""
    deviation = abs(E - E0)
    if deviation < threshold * 0.2:
        return GREEN
    elif deviation < threshold * 0.5:
        return interpolate_color(GREEN, YELLOW, (deviation / threshold - 0.2) / 0.3)
    elif deviation < threshold:
        return interpolate_color(YELLOW, ORANGE, (deviation / threshold - 0.5) / 0.5)
    else:
        return RED


# ========================================
# Scene: Variational Method
# ========================================

class VariationalMethod(Scene):
    """Variational method for harmonic oscillator.

    GUI-compatible PARAMETERS structure for variational method animation.
    """

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # ========================================================================
        # PHYSICAL CONSTANTS (atomic units)
        # ========================================================================
        "hbar": {
            "value": 1.0,
            "type": float,
            "unit": "a.u.",
            "description": "Reduced Planck constant (atomic units)",
            "min": 0.1,
            "max": 10.0
        },
        "mass": {
            "value": 1.0,
            "type": float,
            "unit": "a.u.",
            "description": "Particle mass (atomic units)",
            "min": 0.1,
            "max": 10.0
        },
        "omega": {
            "value": 1.0,
            "type": float,
            "unit": "a.u.",
            "description": "Angular frequency for harmonic oscillator",
            "min": 0.1,
            "max": 10.0
        },

        # ========================================================================
        # VISUALIZATION PARAMETERS
        # ========================================================================
        "x_range_min": {
            "value": -4.0,
            "type": float,
            "unit": "-",
            "description": "Minimum x for wavefunction plot",
            "min": -10.0,
            "max": 0.0
        },
        "x_range_max": {
            "value": 4.0,
            "type": float,
            "unit": "-",
            "description": "Maximum x for wavefunction plot",
            "min": 0.0,
            "max": 10.0
        },
        "n_points": {
            "value": 300,
            "type": int,
            "unit": "points",
            "description": "Number of points for wavefunction discretization",
            "min": 50,
            "max": 1000
        }
    }

    def construct(self):
        self.setup_parameters()
        self.phase_1_introduction()
        self.phase_2_trial_functions()
        self.phase_3_optimization()
        self.wait(3)

    def setup_parameters(self):
        """Extract parameters from central PARAMETERS dictionary"""
        # Update global constants (needed for module-level functions)
        global HBAR, MASS, OMEGA
        HBAR = self.PARAMETERS["hbar"]["value"]
        MASS = self.PARAMETERS["mass"]["value"]
        OMEGA = self.PARAMETERS["omega"]["value"]

        # Calculate exact ground state energy
        self.E0 = exact_energy(0)  # Ground state energy = ℏω/2

        # Visualization parameters
        x_min = self.PARAMETERS["x_range_min"]["value"]
        x_max = self.PARAMETERS["x_range_max"]["value"]
        n_pts = self.PARAMETERS["n_points"]["value"]
        self.x_range = np.linspace(x_min, x_max, n_pts)

        # Layout positions (internal, not parameters)
        self.wavefunction_center = LEFT * 3.5
        self.energy_chart_center = RIGHT * 3.5 + UP * 1.0
        self.energy_plot_center = RIGHT * 3.5 + DOWN * 1.8

    def phase_1_introduction(self):
        """Phase 1: Introduction to variational principle"""
        # Title
        title = Text(get_string("var_title"), font_size=24)
        title.to_edge(UP, buff=0.15)
        self.play(Write(title))
        self.title = title

        # Variational principle
        principle_text = Text(get_string("var_principle"), font_size=18, color=YELLOW)
        principle_text.move_to(UP * 2.5)

        principle_eq = Tex(r"E[\psi] = \frac{\langle \psi | H | \psi \rangle}{\langle \psi | \psi \rangle} \geq E_0", font_size=36)
        principle_eq.next_to(principle_text, DOWN, buff=0.3)

        self.play(Write(principle_text), Write(principle_eq))
        self.wait(2)

        # Show exact energy
        exact_text = Text(get_string("var_exact_energy"), font_size=16, color=GREEN)
        exact_text.move_to(UP * 1.0)
        exact_value = Tex(f"E_0 = {self.E0:.3f}", font_size=28, color=GREEN)
        exact_value.next_to(exact_text, RIGHT, buff=0.3)

        self.play(Write(exact_text), Write(exact_value))
        self.wait(2)

        # Fade out intro
        self.play(FadeOut(principle_text), FadeOut(principle_eq),
                  FadeOut(exact_text), FadeOut(exact_value))

    def phase_2_trial_functions(self):
        """Phase 2: Show 6 trial wavefunctions and their energies"""
        # Setup visualization areas
        self.setup_wavefunction_plot()
        self.setup_energy_chart()

        # Define trial functions
        trial_data = [
            ("Gauß α=0.5", lambda x: trial_gaussian(x, 0.5)),
            ("Gauß α=1.0", lambda x: trial_gaussian(x, 1.0)),
            ("Gauß α=2.0", lambda x: trial_gaussian(x, 2.0)),
            ("x² exp(-x²)", trial_x2_gaussian),
            ("Glatt Poly", lambda x: trial_polynomial_smooth(x, 2.0)),
            ("x⁴ exp(-x²)", trial_x4_gaussian),
        ]

        self.trial_energies = []

        for i, (name, psi_func) in enumerate(trial_data):
            # Calculate energy numerically
            E = expectation_energy(psi_func)
            self.trial_energies.append((name, E))

            # DEBUG: Print detailed information
            print(f"\n=== Trial function: {name} ===")
            norm_sq, _ = quad(lambda x: psi_func(x)**2, -40, 40, limit=100)
            print(f"Normalization ⟨ψ|ψ⟩ = {norm_sq:.6f}")

            T = kinetic_energy_integral(psi_func, (-40, 40))
            V = potential_energy_integral(psi_func, harmonic_potential, (-40, 40))
            print(f"Kinetic T = {T/norm_sq:.6f}")
            print(f"Potential V = {V/norm_sq:.6f}")
            print(f"Total E = {E:.6f}")
            print(f"ΔE = {E - self.E0:.6f}")

            # Verify variational principle
            if E < self.E0 - 1e-4:
                print(f"⚠️  WARNING: Variational principle violated!")
            else:
                print(f"✓ Variational principle satisfied")

            # Color based on energy
            color = energy_to_color(E, self.E0, threshold=1.0)

            # Show wavefunction
            self.show_trial_wavefunction(name, psi_func, color)

            # Add to energy chart
            self.add_energy_bar(i, name, E, color)

            self.wait(1.5)

            # Fade out wavefunction (keep chart)
            if i < len(trial_data) - 1:
                self.play(FadeOut(self.current_wf_plot), FadeOut(self.current_wf_label))

        self.wait(2)

    def setup_wavefunction_plot(self):
        """Setup axes for wavefunction visualization"""
        self.wf_axes = Axes(
            x_range=(-4, 4, 1),
            y_range=(-1.5, 1.5, 0.5),
            width=6,
            height=4,
            axis_config={"stroke_color": GREY, "stroke_width": 2},
        )
        self.wf_axes.move_to(self.wavefunction_center)

        x_label = Text("x", font_size=16)
        x_label.next_to(self.wf_axes, RIGHT, buff=0.1).shift(DOWN * 2)
        psi_label = Text("ψ(x)", font_size=16)
        psi_label.next_to(self.wf_axes, UP, buff=0.1).shift(LEFT * 3)

        # Plot potential
        potential_curve = self.wf_axes.get_graph(
            lambda x: harmonic_potential(x) * 0.2,
            x_range=(-4, 4),
            color=BLUE_D,
            stroke_width=2,
        )
        potential_label = Text(get_string("potential"), font_size=12, color=BLUE_D)
        potential_label.next_to(self.wf_axes.coords_to_point(3, 0.8), RIGHT, buff=0.1)

        self.play(
            ShowCreation(self.wf_axes),
            Write(x_label),
            Write(psi_label),
            ShowCreation(potential_curve),
            Write(potential_label)
        )

        self.wf_labels = VGroup(x_label, psi_label, potential_label)
        self.potential_curve = potential_curve

    def show_trial_wavefunction(self, name, psi_func, color):
        """Display a trial wavefunction"""
        x_vals = self.x_range
        psi_vals = np.array([psi_func(x) for x in x_vals])

        points = [self.wf_axes.coords_to_point(x, psi) for x, psi in zip(x_vals, psi_vals)]
        wf_curve = VMobject(color=color, stroke_width=4)
        wf_curve.set_points_as_corners(points)

        label = Text(name, font_size=14, color=color)
        label.move_to(self.wavefunction_center + UP * 2.5)

        self.play(ShowCreation(wf_curve), Write(label), run_time=1.0)

        self.current_wf_plot = wf_curve
        self.current_wf_label = label

    def setup_energy_chart(self):
        """Setup bar chart for energy comparison"""
        chart_title = Text(get_string("var_energy_comparison"), font_size=16, color=ORANGE)
        chart_title.move_to(self.energy_chart_center + UP * 2.2)
        self.play(Write(chart_title))

        # Reference line for E0
        ref_line_start = self.energy_chart_center + LEFT * 2.5
        ref_line_end = self.energy_chart_center + RIGHT * 2.5
        self.E0_ref_line = DashedLine(ref_line_start, ref_line_end, color=GREEN, stroke_width=2)

        E0_label = Text(f"E₀={self.E0:.2f}", font_size=12, color=GREEN)
        E0_label.next_to(self.E0_ref_line, LEFT, buff=0.1)

        self.play(ShowCreation(self.E0_ref_line), Write(E0_label))

        self.chart_title = chart_title
        self.E0_label = E0_label
        self.energy_bars = []
        self.bar_width = 0.3
        self.bar_spacing = 0.4

    def add_energy_bar(self, index, name, E, color):
        """Add a bar to the energy chart"""
        x_pos = self.energy_chart_center[0] - 2.0 + index * self.bar_spacing
        base_y = self.E0_ref_line.get_center()[1]

        height = (E - self.E0) * 1.5

        bar = Rectangle(
            width=self.bar_width,
            height=abs(height),
            fill_color=color,
            fill_opacity=0.7,
            stroke_color=color,
            stroke_width=2,
        )
        bar.move_to([x_pos, base_y + height/2, 0])

        value_label = Text(f"{E:.2f}", font_size=10, color=color)
        value_label.next_to(bar, UP, buff=0.05)

        self.play(FadeIn(bar), Write(value_label), run_time=0.8)

        self.energy_bars.append((bar, value_label))

    def phase_3_optimization(self):
        """Phase 3: Continuous optimization of α with live displays"""
        # Clear previous content
        self.play(
            FadeOut(self.current_wf_plot),
            FadeOut(self.current_wf_label),
            *[FadeOut(bar) for bar, label in self.energy_bars],
            *[FadeOut(label) for bar, label in self.energy_bars],
            FadeOut(self.chart_title),
            FadeOut(self.E0_label),
            FadeOut(self.E0_ref_line)
        )

        # Setup E(α) plot
        self.setup_energy_plot()

        # Optimization label
        opt_label = Text(get_string("var_optimization"), font_size=18, color=YELLOW)
        opt_label.move_to(self.energy_plot_center + UP * 2.5)
        self.play(Write(opt_label))

        # Wavefunction formula display
        formula_text = Tex(r"\psi(x) = \left(\frac{\alpha}{\pi}\right)^{1/4} e^{-\alpha x^2/2}", font_size=24)
        formula_text.move_to(self.wavefunction_center + UP * 2.5)
        self.play(Write(formula_text))

        # Alpha value display
        alpha_display = DecimalNumber(0.3, num_decimal_places=2, font_size=28, color=YELLOW)
        alpha_text = Tex(r"\alpha = ", font_size=28)
        alpha_group = VGroup(alpha_text, alpha_display).arrange(RIGHT, buff=0.1)
        alpha_group.move_to(self.wavefunction_center + UP * 1.8)
        self.play(Write(alpha_group))

        # Energy displays
        E_display = DecimalNumber(0, num_decimal_places=4, font_size=32, color=GREEN)
        E_text = Tex(r"E(\alpha) = ", font_size=24)
        E_group = VGroup(E_text, E_display).arrange(RIGHT, buff=0.1)
        E_group.move_to(self.wavefunction_center + DOWN * 2.2)

        delta_E_display = DecimalNumber(0, num_decimal_places=4, font_size=24, color=ORANGE)
        delta_E_text = Tex(r"\Delta E = ", font_size=20)
        delta_E_group = VGroup(delta_E_text, delta_E_display).arrange(RIGHT, buff=0.1)
        delta_E_group.move_to(self.wavefunction_center + DOWN * 2.8)

        self.play(Write(E_group), Write(delta_E_group))

        # α-Slider
        slider_center = self.wavefunction_center + DOWN * 3.5
        slider_length = 4.0
        slider_line = Line(
            slider_center + LEFT * slider_length/2,
            slider_center + RIGHT * slider_length/2,
            color=GREY,
            stroke_width=3
        )
        self.play(ShowCreation(slider_line))

        slider_label_min = Tex(r"0.3", font_size=14)
        slider_label_min.next_to(slider_line.get_start(), DOWN, buff=0.1)
        slider_label_max = Tex(r"3.0", font_size=14)
        slider_label_max.next_to(slider_line.get_end(), DOWN, buff=0.1)
        self.play(Write(slider_label_min), Write(slider_label_max))

        # Optimal alpha marker
        alpha_opt = 1.0
        opt_x = slider_center[0] + ((alpha_opt - 0.3) / (3.0 - 0.3) - 0.5) * slider_length
        opt_marker = Line(
            [opt_x, slider_center[1] - 0.2, 0],
            [opt_x, slider_center[1] + 0.2, 0],
            color=GREEN,
            stroke_width=4
        )
        opt_label_slider = Text("Min", font_size=10, color=GREEN)
        opt_label_slider.next_to(opt_marker, UP, buff=0.05)
        self.play(ShowCreation(opt_marker), Write(opt_label_slider))

        # Current alpha slider dot
        alpha_init = 0.3
        slider_dot = Dot(slider_line.get_start(), color=YELLOW, radius=0.1)
        self.play(FadeIn(slider_dot))

        # Create initial wavefunction and energy plot dot
        psi_init = lambda x: trial_gaussian(x, alpha_init)
        x_vals = self.x_range
        psi_vals = np.array([psi_init(x) for x in x_vals])
        points = [self.wf_axes.coords_to_point(x, psi) for x, psi in zip(x_vals, psi_vals)]
        wf_curve = VMobject(color=YELLOW, stroke_width=4)
        wf_curve.set_points_as_corners(points)

        E_init = expectation_energy(psi_init)
        plot_point = self.energy_axes.coords_to_point(alpha_init, E_init)
        energy_dot = Dot(plot_point, color=YELLOW, radius=0.08)

        self.play(ShowCreation(wf_curve), FadeIn(energy_dot))

        # Initialize displays
        alpha_display.set_value(alpha_init)
        E_display.set_value(E_init)
        delta_E_display.set_value(E_init - self.E0)

        # Animation loop: vary α from 0.3 to 3.0
        duration = 10.0
        fps = 30
        frames = int(duration * fps)

        alpha_values = np.linspace(0.3, 3.0, frames)

        for frame, alpha in enumerate(alpha_values):
            # Calculate new wavefunction
            psi_func = lambda x: trial_gaussian(x, alpha)
            psi_vals = np.array([psi_func(x) for x in x_vals])

            # Update wavefunction curve
            new_points = [self.wf_axes.coords_to_point(x, psi) for x, psi in zip(x_vals, psi_vals)]
            wf_curve.set_points_as_corners(new_points)

            # Calculate energy
            E = expectation_energy(psi_func)

            # Update energy plot dot position
            plot_point = self.energy_axes.coords_to_point(alpha, E)
            energy_dot.move_to(plot_point)

            # Update slider dot position
            slider_x = slider_center[0] + ((alpha - 0.3) / (3.0 - 0.3) - 0.5) * slider_length
            slider_dot.move_to([slider_x, slider_center[1], 0])

            # Update displays
            alpha_display.set_value(alpha)
            E_display.set_value(E)
            delta_E_display.set_value(E - self.E0)

            # Color based on proximity to E0
            color = energy_to_color(E, self.E0, threshold=1.0)
            wf_curve.set_color(color)
            energy_dot.set_color(color)
            slider_dot.set_color(color)
            alpha_display.set_color(color)
            E_display.set_color(color)

            self.wait(1/fps)

        self.wait(3)

    def setup_energy_plot(self):
        """Setup E(α) plot"""
        self.energy_axes = Axes(
            x_range=(0, 3, 0.5),
            y_range=(0.4, 1.5, 0.2),
            width=5,
            height=3.5,
            axis_config={"stroke_color": GREY, "stroke_width": 2},
        )
        self.energy_axes.move_to(self.energy_plot_center)

        alpha_label = Tex(r"\alpha", font_size=20)
        alpha_label.next_to(self.energy_axes, RIGHT, buff=0.1).shift(DOWN * 1.7)
        E_label = Text("E", font_size=16)
        E_label.next_to(self.energy_axes, UP, buff=0.1).shift(LEFT * 2.5)

        # Plot E(α) curve
        alpha_range = np.linspace(0.3, 3.0, 100)
        E_values = [expectation_energy(lambda x: trial_gaussian(x, a)) for a in alpha_range]

        energy_curve = VMobject(color=BLUE, stroke_width=3)
        curve_points = [self.energy_axes.coords_to_point(a, E) for a, E in zip(alpha_range, E_values)]
        energy_curve.set_points_as_corners(curve_points)

        # Mark minimum
        min_idx = np.argmin(E_values)
        min_alpha = alpha_range[min_idx]
        min_E = E_values[min_idx]
        min_dot = Dot(self.energy_axes.coords_to_point(min_alpha, min_E), color=GREEN, radius=0.1)
        min_label = Text("Min", font_size=12, color=GREEN)
        min_label.next_to(min_dot, UP, buff=0.1)

        # E0 reference line
        E0_line_points = [
            self.energy_axes.coords_to_point(0, self.E0),
            self.energy_axes.coords_to_point(3, self.E0)
        ]
        E0_line = DashedLine(*E0_line_points, color=GREEN, stroke_width=2)

        self.play(
            ShowCreation(self.energy_axes),
            Write(alpha_label),
            Write(E_label),
            ShowCreation(energy_curve),
            ShowCreation(E0_line),
            FadeIn(min_dot),
            Write(min_label)
        )

        self.energy_curve = energy_curve
