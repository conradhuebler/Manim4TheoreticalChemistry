<!--
author:   Computational Chemistry Course
email:
version:  1.0.0
language: de
narrator: Deutsch Female

comment:  LiaScript Template für bond_stretching.py - Harmonisches vs. Morse-Potential

@style
.lia-effect__circle {
  animation: none !important;
}
@end
-->

# Bond Stretching: Harmonisches vs. Morse-Potential

> **Lernziele:**
>
> - 🟢 Unterschied harmonisches vs. Morse-Potential verstehen
> - 🟢 Einfluss von Dissoziationsenergie D_e auf Bindungsstärke
> - 🟡 Quantitative Abweichung bei großen Amplituden analysieren
> - 🔴 Beziehung k = 2·D_e·alpha² herleiten

## 📚 Theorie

Das **harmonische Potential** ist die einfachste Näherung für Bindungsdehnungen:

$$V_{\text{harm}}(r) = \frac{1}{2} k (r - r_0)^2$$

Das **Morse-Potential** beschreibt realistischer die Anharmonizität und Dissoziation:

$$V_{\text{Morse}}(r) = D_e \left[1 - e^{-\alpha(r-r_e)}\right]^2 - D_e$$

**Parameter:**
- $D_e$ = Dissoziationsenergie (eV)
- $r_e$ = Gleichgewichtsbindungslänge (Å)
- $\alpha$ = Morse-Breitenparameter (Å⁻¹)
- $k$ = Harmonische Federkonstante (eV/Å²)

**Wichtige Beziehung:** $k = 2 D_e \alpha^2$

---

## 🎬 Interaktive Animation

### Parameter anpassen

Nutze die Slider, um die Animations-Parameter zu ändern:

**Dissoziationsenergie (D_e):**

<script input="range" value="4.478" output="D_e_val" min="2.0" max="8.0" step="0.1">@input</script>
D_e = <script>@input(`D_e_val`)</script> eV

**Morse-Breitenparameter (alpha):**

<script input="range" value="1.9" output="alpha_val" min="0.5" max="3.0" step="0.1">@input</script>
alpha = <script>@input(`alpha_val`)</script> Å⁻¹

**Oszillationsamplitude:**

<script input="range" value="0.3" output="amplitude_val" min="0.1" max="0.8" step="0.05">@input</script>
amplitude = <script>@input(`amplitude_val`)</script> Å

**Gleichgewichtsabstand (r_e):**

<script input="range" value="0.741" output="r_e_val" min="0.5" max="1.5" step="0.05">@input</script>
r_e = <script>@input(`r_e_val`)</script> Å

### Animation starten

```python
# Manim-Animation mit gewählten Parametern ausführen
# (In der praktischen Implementierung würde hier QManimPlayer aufgerufen)

from bond_stretching import BondStretching

# Parameter setzen
BondStretching.PARAMETERS["D_e"]["value"] = @input(`D_e_val`)
BondStretching.PARAMETERS["alpha"]["value"] = @input(`alpha_val`)
BondStretching.PARAMETERS["amplitude"]["value"] = @input(`amplitude_val`)
BondStretching.PARAMETERS["r_e"]["value"] = @input(`r_e_val`)

# Animation rendern
scene = BondStretching()
scene.render()
```

---

## ✏️ Übung 1: Wann versagt die harmonische Näherung? (🟢 Anfänger)

**Aufgabe:**
Variiere die Amplitude von 0.1 Å → 0.8 Å und beobachte die Abweichung zwischen Morse- und harmonischem Potential.

**Frage 1:** Bei welcher Amplitude wird der Fehler größer als 10%?

[[ ]] 0.1 Å
[[ ]] 0.2 Å
[[X]] 0.4 Å
[[ ]] 0.6 Å
[[ ]] 0.8 Å
***********************************************************************

**Erklärung:**

Bei kleinen Amplituden (< 0.2 Å) ist die harmonische Näherung sehr gut. Ab ca. 0.4 Å wird die Anharmonizität des Morse-Potentials signifikant:

- Das harmonische Potential ist **symmetrisch**
- Das Morse-Potential ist **asymmetrisch** (weicher bei Dehnung, härter bei Kompression)
- Bei großen Dehnungen nähert sich Morse der Dissoziation (V → 0), harmonisch wächst unbegrenzt

Der **relative Fehler** ist:

$$\epsilon = \frac{|V_{\text{harm}} - V_{\text{Morse}}|}{|V_{\text{Morse}}|} \times 100\%$$

Für H₂ (D_e = 4.478 eV, α = 1.9 Å⁻¹) gilt: ε > 10% ab A ≈ 0.4 Å

***********************************************************************

---

## ✏️ Übung 2: Starke vs. schwache Bindungen (🟡 Fortgeschritten)

**Aufgabe:**
Vergleiche H-H Bindung (D_e = 4.5 eV) mit hypothetischer He-He Bindung (D_e = 0.01 eV).

**Experimentiere:**
1. Setze D_e = 4.5 eV, alpha = 1.9 Å⁻¹ → Beobachte Schwingungsfrequenz
2. Setze D_e = 0.5 eV, alpha = 1.0 Å⁻¹ → Beobachte Schwingungsfrequenz

**Frage 2:** Wie ändert sich die Schwingungsfrequenz ω mit D_e?

[[ ]] ω ∝ D_e (linear)
[[X]] ω ∝ √D_e (Wurzel)
[[ ]] ω ∝ D_e² (quadratisch)
[[ ]] keine Abhängigkeit
***********************************************************************

**Erklärung:**

Die Schwingungsfrequenz nahe dem Minimum folgt aus der harmonischen Näherung:

$$\omega = \sqrt{\frac{k}{\mu}}$$

Mit der Beziehung $k = 2 D_e \alpha^2$ folgt:

$$\omega = \sqrt{\frac{2 D_e \alpha^2}{\mu}} \propto \sqrt{D_e}$$

**Physikalische Intuition:**
- Höhere Dissoziationsenergie → steileres Potential → stärkere Rückstellkraft → höhere Frequenz
- Aber: Der Effekt ist **sublinear** (Wurzel), nicht linear

**Beispiel:**
- D_e(H₂) = 4.5 eV → ω ≈ 4400 cm⁻¹
- D_e × 4 = 18 eV → ω × 2 = 8800 cm⁻¹ (nicht ×4!)

***********************************************************************

---

## ✏️ Übung 3: Der alpha-Parameter (🔴 Experte)

**Aufgabe:**
Zeige experimentell, dass $k = 2 D_e \alpha^2$ gilt.

**Hinweis:** Die harmonische Federkonstante k entspricht der zweiten Ableitung des Morse-Potentials bei r = r_e:

$$k = \left.\frac{d^2 V_{\text{Morse}}}{dr^2}\right|_{r=r_e}$$

**Frage 3:** Wenn D_e = 4.5 eV und α = 2.0 Å⁻¹, wie groß ist k?

[[36.0]]
[[?]] Tipp: k = 2 × D_e × alpha²
[[?]] Tipp: k = 2 × 4.5 × (2.0)² = ?
***********************************************************************

**Herleitung:**

Morse-Potential:
$$V(r) = D_e[1 - e^{-\alpha(r-r_e)}]^2 - D_e$$

Erste Ableitung (Kraft):
$$\frac{dV}{dr} = 2D_e[1-e^{-\alpha(r-r_e)}] \cdot \alpha e^{-\alpha(r-r_e)}$$

Bei $r = r_e$: $\frac{dV}{dr}\Big|_{r=r_e} = 0$ ✓ (Minimum)

Zweite Ableitung (Krümmung):
$$\frac{d^2V}{dr^2} = 2D_e \alpha^2 \left[e^{-\alpha(r-r_e)} - e^{-2\alpha(r-r_e)}\right]$$

Bei $r = r_e$:
$$k = \frac{d^2V}{dr^2}\Big|_{r=r_e} = 2D_e\alpha^2[1-1] + 2D_e\alpha^2 = 2D_e\alpha^2$$

**Numerisch:**
k = 2 × 4.5 eV × (2.0 Å⁻¹)² = 36.0 eV/Å²

***********************************************************************

---

## 📊 Zusammenfassung

Was Du gelernt hast:

- [[ ]] Das harmonische Potential ist bei allen Amplituden genau
- [[X]] Das Morse-Potential beschreibt Dissoziation realistisch
- [[X]] Die harmonische Näherung versagt bei großen Dehnungen
- [[X]] Die Schwingungsfrequenz wächst mit √D_e
- [[X]] Der alpha-Parameter bestimmt die "Breite" des Potentials
- [[X]] Es gilt: k = 2·D_e·alpha²

---

## 🔗 Weiterführende Themen

1. **Quantisierung:** Energieniveaus E_n = ℏω(n + 1/2) - ℏ²ω²x_e(n + 1/2)²
2. **Anharmonische Oszillator-Korrektur:** x_e = ℏω/(4D_e)
3. **Birge-Sponer Plot:** Experimentelle Bestimmung von D_e
4. **Dunham-Entwicklung:** Höhere Ordnungen der Anharmonizität

---

**Schwierigkeitsgrad:** 🟢 Anfänger bis 🔴 Experte

**Geschätzte Bearbeitungszeit:** 30-45 Minuten

**Voraussetzungen:** Grundlagen Molekülschwingungen, Taylor-Entwicklung
