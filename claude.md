# Claude ManimGL Assistant - Kompakt und Präzise

**Hinweis: Diese Datei soll kompakt, klar und präzise bleiben. Detaillierte Dokumentation siehe README.md**

---

## ⚠️ MANDATORY: Lies diese Datei ZUERST!

**Bevor du IRGENDEINEN ManimGL-Code schreibst:**
1. ✅ Lies diese `claude.md` Datei vollständig
2. ✅ Bestätige intern, dass du die Syntax-Regeln kennst
3. ✅ Dann erst mit dem Coding beginnen

**Falls du Code schreibst ohne diese Datei gelesen zu haben:**
- ❌ STOPP sofort
- ❌ Korrigiere alle Fehler
- ❌ Entschuldige dich beim User

---

## ManimGL Syntax (Essential)

**Import:**
```python
from manimlib import *
import numpy as np
```

**Key Commands:**
- `ShowCreation()` NOT `Create()`
- `axes.get_graph()` NOT `axes.plot()`
- `axes.coords_to_point()` NOT `axes.c2p()`
- `--write_file` NOT `--write_to_movie`

**Reference Lines:**
- Use `Line(axes.coords_to_point(x1,y), axes.coords_to_point(x2,y))` NOT `axes.get_horizontal_line()`
- Use `axes.coords_to_point()` for all coordinate transformations

**LaTeX in Tex():**
- ❌ NEVER use Unicode characters in `Tex()` or `Text()` if used in math context: `"μ"`, `"r₀"`, `"θ"` → LaTeX Error!
- ❌ NEVER use Unicode in `Text()` that might be confused with LaTeX: `"Schwerpunkt μ"` → Error!
- ✅ ALWAYS use LaTeX syntax: `r"r_0"` or `r"\theta_0"` or `r"\mu"`
- ✅ Use raw strings (`r"..."`) for LaTeX formulas
- ✅ For Greek letters in text: Either use `Tex(r"...\mu...")` or avoid Unicode entirely
- Examples:
  - ❌ `Tex("V = ½k(r-r₀)²")`
  - ✅ `Tex(r"V = \frac{1}{2}k(r-r_0)^2")`
  - ❌ `Text("Schwerpunkt μ")`
  - ✅ `Text("Schwerpunkt")` or `Tex(r"\text{Schwerpunkt } \mu")`

**ParametricSurface Styling:**
- ❌ NO `set_style()` method exists!
- ❌ NO `set_fill()` method exists!
- ✅ Use `surface.set_color(COLOR)` and `surface.set_opacity(value)`
- Example:
  ```python
  surface = ParametricSurface(func, ...)
  surface.set_color(BLUE)
  surface.set_opacity(0.3)
  ```

**Animation Performance:**
- ❌ NEVER `remove()` and `add()` entire groups in animation loops
- ✅ Only remove/add objects that actually change (e.g., arcs, polygons)
- ✅ Use `put_start_and_end_on()` for lines, `move_to()` for atoms
- Bad: `self.remove(group); group = VGroup(...); self.add(group)` in loop
- Good: Only update positions of existing objects

## 4-Quadranten Layout Standard

- **Links**: Hauptvisualisierung (groß)
- **Rechts oben**: Energie vs Zeit
- **Rechts unten**: Parameter vs Zeit
- **Schriftgrößen**: 8-14px
- **Spacing**: `buff=0.2` minimum
- Reaktionsbox bzw, Molekülbox im linken Fenster - 2 Quadranten, Energie und Zeitracking in den rechten Diagrammen

## Kraftfeld Animationen (Neue Serie)

**5 modulare Animationen für Molekulardynamik-Kraftfelder:**
1. `bond_stretching.py` - Harmonisches Bindungspotential V = ½k(r-r₀)²
2. `angle_bending.py` - Winkelpotential V = ½k(θ-θ₀)²
3. `torsion_angle.py` - Torsionspotential V = V₀/2[1+cos(nφ)]
4. `inversion_motion.py` - Inversions-Doppelmulde (NH₃-Umbrella)
5. `nonbonded_interactions.py` - Lennard-Jones + Coulomb

**Design-Prinzipien:**
- 2-Panel Layout: Molekül links, Potentialkurve rechts
- ~20-30 Sekunden pro Animation
- Fokussiert auf einen Term
- Mehrsprachig (DE/EN)
- Marker auf Kurve zeigt aktuelle Position

## Quantenmechanik Animationen

### quantum_mechanics_separability.py
**Separabilität im 2-Teilchen-System** - zeigt wie ψ(x₁,x₂) = ψ₁(x₁)·ψ₂(x₂)
- 4 klare Schritte: 1D → Tisch-Metapher → 2D-Surface → Probability
- ThreeDScene mit fix_in_frame() für UI
- Keine verwirrenden Koordinaten-Transformationen!

### h2_born_oppenheimer.py
Einfache MD mit Morse-Potential, 4-Quadranten Layout

### h2_md_full.py
4-Phasen: Freie Atome → Wechselwirkung → Born-Oppenheimer → H₂-Bindung

## Ausführung

**Standard (aus Projektverzeichnis):**
```bash
# Aktiviere venv (falls nicht aktiv)
source venv/bin/activate  # oder: ~/maningl/venv/bin/activate

# Preview (interaktiv)
manimgl datei.py

# Video exportieren
manimgl datei.py SceneName --write_file
```

**Alternative (ohne venv aktivieren):**
```bash
PYTHONPATH="./venv/lib/python3.13/site-packages" ./venv/bin/python datei.py
```

**Mehrsprachig**: `LANGUAGE = "DE"/"EN"` am Dateianfang
