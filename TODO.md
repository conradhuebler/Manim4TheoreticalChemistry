# TODO: Parameter-Struktur gemäß claude.md Vorschrift

## Übersicht

**Vorschrift aus claude.md (Zeilen 99-309):**
Alle Animationsparameter MÜSSEN in einem zentralen `PARAMETERS`-Dictionary auf Klassenebene definiert werden, damit ein GUI-Tool (PyQt6) die Parameter dynamisch auslesen und Eingabefelder generieren kann.

**Erforderliches Format:**
```python
class MyAnimation(Scene):
    PARAMETERS = {
        "parameter_name": {
            "value": <default_value>,
            "type": <float|int|str|bool>,
            "unit": "<physikalische Einheit>",
            "description": "<Beschreibung>",
            "min": <min_wert>,  # optional
            "max": <max_wert>   # optional
        }
    }
```

## Status der Skriptdateien

**Legende:**
- ❌ = Nicht konform (kein PARAMETERS-Dictionary vorhanden)
- ⚠️ = Teilweise konform (PARAMETERS vorhanden, aber unvollständig)
- ✅ = Vollständig konform (PARAMETERS im korrekten Format)

### Forcefield Animation Series

| Datei | Status | Parameter-Definition | Anmerkungen |
|-------|--------|---------------------|-------------|
| `bond_stretching.py` | ✅ | Class-level `PARAMETERS` dictionary | 7 Parameter: k, r0, amplitude, frequency, scale_factor, duration, fps |
| `angle_bending.py` | ✅ | Class-level `PARAMETERS` dictionary | 7 Parameter: k_angle, theta0_deg, amplitude_deg, frequency, bond_length, duration, fps |
| `torsion_angle_optimized.py` | ✅ | Class-level `PARAMETERS` dictionary | 5 Parameter: V0, n, gamma, duration, fps |
| `nonbonded_interactions.py` | ✅ | Class-level `PARAMETERS` dictionary | 7 Parameter: epsilon, sigma, k_coulomb, r_start, r_end, duration, fps |
| `nh3_inversion.py` | ✅ | Class-level `PARAMETERS` dictionary | 5 Parameter: V0, a, h_radius, z_nitrogen_initial, dt (ThreeDScene) |

### Molecular Dynamics & Quantum

| Datei | Status | Parameter-Definition | Anmerkungen |
|-------|--------|---------------------|-------------|
| `h2_md_full_refactored.py` | ❌ | Zu prüfen | - |
| `h3_reaction_pathway.py` | ❌ | Zu prüfen | - |
| `geometry_optimization.py` | ❌ | Zu prüfen | - |
| `quantum_dynamics_manim.py` | ❌ | Zu prüfen | - |
| `quantum_nonlocality.py` | ❌ | Zu prüfen | - |
| `variational_method.py` | ❌ | Zu prüfen | - |

### Monte Carlo & Sampling

| Datei | Status | Parameter-Definition | Anmerkungen |
|-------|--------|---------------------|-------------|
| `monte_carlo_pi.py` | ✅ | Class-level `PARAMETERS` dictionary | 6 Parameter: total_samples, batch_size, animation_speed, max_displayed_points, square_size, circle_radius |
| `metropolis_animation.py` | ✅ | Class-level `PARAMETERS` dictionaries | 2 Szenen: MetropolisBasic (T, R), MetropolisTemperatures (R) |
| `polymer_monte_carlo.py` | ❌ | Zu prüfen | - |
| `polymer_sampling_comparison.py` | ❌ | Zu prüfen | - |

### Specialized Topics

| Datei | Status | Parameter-Definition | Anmerkungen |
|-------|--------|---------------------|-------------|
| `metadynamics_visualization.py` | ❌ | Zu prüfen | - |
| `pca_molecular_dynamics.py` | ❌ | Zu prüfen | - |
| `particle_interactions_combinatorics.py` | ❌ | Zu prüfen | - |
| `polarization_forcefield.py` | ❌ | Zu prüfen | - |

## Zusammenfassung

- **Gesamt:** 19 Dateien
- **Konform (✅):** 7 Dateien (36.8%)
- **Teilweise konform (⚠️):** 0 Dateien (0%)
- **Nicht konform (❌):** 12 Dateien (63.2%)

**🎉 Forcefield Animation Series: 5/5 KOMPLETT!**
**📊 Monte Carlo & Sampling: 2/4**

## Nächste Schritte

1. **Priorität 1: Forcefield Animation Series** (5 Dateien)
   - Diese Dateien sind gut dokumentiert und haben klare Parameter
   - Empfohlene Reihenfolge:
     1. `bond_stretching.py` - Einfachste Parameter-Struktur
     2. `angle_bending.py`
     3. `torsion_angle_optimized.py`
     4. `nonbonded_interactions.py` - Hat mehrere Phasen
     5. `nh3_inversion.py` - Verwendet ThreeDScene

2. **Priorität 2: Monte Carlo & Sampling** (4 Dateien)

3. **Priorität 3: Molecular Dynamics & Quantum** (6 Dateien)

4. **Priorität 4: Specialized Topics** (4 Dateien)

## Beispiel-Refactoring: bond_stretching.py

### Aktuell (Zeilen 56-64):
```python
class BondStretching(Scene):
    def construct(self):
        # Bond parameters (typical C-C single bond)
        self.k = 300.0  # kcal/(mol·Å²) - force constant
        self.r0 = 1.54  # Å - equilibrium bond length

        # Animation parameters
        self.amplitude = 0.4  # Å - oscillation amplitude
        self.frequency = 1.0  # Hz
        self.scale_factor = 2.0  # Scale for visualization
```

### Nach Refactoring (gemäß Vorschrift):
```python
class BondStretching(Scene):
    """Bond stretching animation with harmonic potential."""

    PARAMETERS = {
        # Physical parameters
        "k": {
            "value": 300.0,
            "type": float,
            "unit": "kcal/(mol·Å²)",
            "description": "Force constant for harmonic potential",
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
            "description": "Oscillation amplitude",
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
            "description": "Frames per second",
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

        # Rest of implementation...
```

## Vorteile der Umstellung

1. **GUI-Kompatibilität:** PyQt6-Tool kann automatisch Eingabefelder generieren
2. **Selbst-Dokumentation:** Parameter sind mit Beschreibungen und Einheiten versehen
3. **Validierung:** Min/Max-Werte ermöglichen automatische Eingabe-Validierung
4. **Auffindbarkeit:** Alle Parameter an einem zentralen Ort
5. **Type Safety:** Explizite Typ-Information verhindert Fehler

## Hinweise

- Die Animationen funktionieren aktuell korrekt, sind aber nicht GUI-kompatibel
- Das Refactoring ändert nichts an der Funktionalität, nur an der Struktur
- Jede Datei kann einzeln umgestellt werden (keine Abhängigkeiten)
- Nach dem Refactoring müssen die Animationen getestet werden

---

## Changelog

### 2025-11-05 - metropolis_animation.py refactored ✅

**Änderungen:**
- ✅ Zentrales `PARAMETERS`-Dictionary für beide Szenen hinzugefügt
- ✅ **MetropolisBasic:** 2 Parameter (T, R) vollständig strukturiert
- ✅ **MetropolisTemperatures:** 1 Parameter (R) strukturiert
- ✅ Alle Parameter mit value, type, unit, description, min, max versehen
- ✅ `construct()` Methoden aktualisiert: Parameter werden aus PARAMETERS extrahiert
- ✅ Alle R-Referenzen von global zu self.R konvertiert
- ✅ Syntax validiert: Keine Python-Fehler
- ✅ Struktur validiert: GUI-kompatibel für beide Szenen

**Besonderheiten:**
- **2 Szenen in einer Datei:** MetropolisBasic und MetropolisTemperatures
- Metropolis-Algorithmus: P(accept) = exp(-ΔE/RT)
- Temperaturvergleich mit mehreren Kurven
- T_values und colors_temp aus Modul-Level (könnte später konfigurierbar gemacht werden)

**Status:** Vollständig konform mit claude.md Vorschrift (Zeilen 99-309)

**📊 Monte Carlo & Sampling: 2/4**

### 2025-11-05 - monte_carlo_pi.py refactored ✅

**Änderungen:**
- ✅ Zentrales `PARAMETERS`-Dictionary auf Klassenebene hinzugefügt
- ✅ 6 Parameter vollständig strukturiert (total_samples, batch_size, animation_speed, max_displayed_points, square_size, circle_radius)
- ✅ Alle Parameter mit value, type, unit, description, min, max versehen
- ✅ `setup_monte_carlo_parameters()` Methode aktualisiert: Parameter werden aus PARAMETERS extrahiert
- ✅ Syntax validiert: Keine Python-Fehler
- ✅ Struktur validiert: GUI-kompatibel

**Besonderheiten:**
- Monte Carlo π-Berechnung durch Zufallspunkte
- 4-Quadranten Layout: Simulation + π-Tracking + Convergence
- Performance-Optimierung durch max_displayed_points
- Batch processing für Animation

**Status:** Vollständig konform mit claude.md Vorschrift (Zeilen 99-309)

**📊 Monte Carlo & Sampling: 1/4 gestartet**

### 2025-11-05 - nh3_inversion.py refactored ✅

**Änderungen:**
- ✅ Zentrales `PARAMETERS`-Dictionary auf Klassenebene hinzugefügt
- ✅ 5 Parameter vollständig strukturiert (V0, a, h_radius, z_nitrogen_initial, dt)
- ✅ Alle Parameter mit value, type, unit, description, min, max versehen
- ✅ `__init__()` Methode aktualisiert: Parameter werden aus PARAMETERS extrahiert
- ✅ `inversion_potential()` Methode aktualisiert: V0 und a aus PARAMETERS
- ✅ Syntax validiert: Keine Python-Fehler
- ✅ Struktur validiert: GUI-kompatibel

**Besonderheiten:**
- ThreeDScene mit __init__ statt construct() für Parameter-Extraktion
- Double-well potential für NH₃ Inversion
- 3D-Molekül + 2D-Energy-Overlay (fix_in_frame)
- h_positions wird dynamisch aus h_radius berechnet

**Status:** Vollständig konform mit claude.md Vorschrift (Zeilen 99-309)

**🎉 FORCEFIELD ANIMATION SERIES KOMPLETT! (5/5)**

### 2025-11-05 - nonbonded_interactions.py refactored ✅

**Änderungen:**
- ✅ Zentrales `PARAMETERS`-Dictionary auf Klassenebene hinzugefügt
- ✅ 7 Parameter vollständig strukturiert (epsilon, sigma, k_coulomb, r_start, r_end, duration, fps)
- ✅ Alle Parameter mit value, type, unit, description, min, max versehen
- ✅ `construct()` Methode aktualisiert: Parameter werden aus PARAMETERS extrahiert
- ✅ `animate_approach()` Methode aktualisiert: duration und fps aus PARAMETERS
- ✅ Syntax validiert: Keine Python-Fehler
- ✅ Struktur validiert: GUI-kompatibel

**Besonderheiten:**
- Kombiniert Lennard-Jones und Coulomb Potential
- 3 Phasen: Neutrale Atome, +/-, +/+
- r_min wird aus sigma berechnet (kein Input-Parameter)

**Status:** Vollständig konform mit claude.md Vorschrift (Zeilen 99-309)

### 2025-11-05 - torsion_angle_optimized.py refactored ✅

**Änderungen:**
- ✅ Zentrales `PARAMETERS`-Dictionary auf Klassenebene hinzugefügt
- ✅ 5 Parameter vollständig strukturiert (V0, n, gamma, duration, fps)
- ✅ Alle Parameter mit value, type, unit, description, min, max versehen
- ✅ `construct()` Methode aktualisiert: Parameter werden aus PARAMETERS extrahiert
- ✅ `animate_rotation()` Methode aktualisiert: duration und fps aus PARAMETERS
- ✅ Syntax validiert: Keine Python-Fehler
- ✅ Struktur validiert: GUI-kompatibel

**Status:** Vollständig konform mit claude.md Vorschrift (Zeilen 99-309)

### 2025-11-05 - angle_bending.py refactored ✅

**Änderungen:**
- ✅ Zentrales `PARAMETERS`-Dictionary auf Klassenebene hinzugefügt
- ✅ 7 Parameter vollständig strukturiert (k_angle, theta0_deg, amplitude_deg, frequency, bond_length, duration, fps)
- ✅ Alle Parameter mit value, type, unit, description, min, max versehen
- ✅ `construct()` Methode aktualisiert: Parameter werden aus PARAMETERS extrahiert
- ✅ `animate_bending()` Methode aktualisiert: duration und fps aus PARAMETERS
- ✅ Syntax validiert: Keine Python-Fehler
- ✅ Struktur validiert: GUI-kompatibel

**Status:** Vollständig konform mit claude.md Vorschrift (Zeilen 99-309)

### 2025-11-05 - bond_stretching.py refactored ✅

**Änderungen:**
- ✅ Zentrales `PARAMETERS`-Dictionary auf Klassenebene hinzugefügt
- ✅ 7 Parameter vollständig strukturiert (k, r0, amplitude, frequency, scale_factor, duration, fps)
- ✅ Alle Parameter mit value, type, unit, description, min, max versehen
- ✅ `construct()` Methode aktualisiert: Parameter werden aus PARAMETERS extrahiert
- ✅ `animate_stretching()` Methode aktualisiert: duration und fps aus PARAMETERS
- ✅ Bug fix: `self.wait(1/30)` → `self.wait(1/fps)` für Konsistenz
- ✅ Syntax validiert: Keine Python-Fehler
- ✅ Struktur validiert: GUI-kompatibel

**Status:** Vollständig konform mit claude.md Vorschrift (Zeilen 99-309)

---

**Stand:** 2025-11-05
**Analysiert von:** Claude Code
**Basierend auf:** claude.md Zeilen 93-309 (Architecture Requirements: GUI Tool Compatibility)
