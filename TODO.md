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
| `bond_stretching.py` | ❌ | `construct()` Methode, Zeilen 57-64 | Parameter: k, r0, amplitude, frequency, scale_factor |
| `angle_bending.py` | ❌ | `construct()` Methode, Zeilen 59-67 | Parameter: k_angle, theta0_deg, amplitude_deg, frequency, bond_length |
| `torsion_angle_optimized.py` | ❌ | `construct()` Methode, Zeilen 53-56 | Parameter: V0, n, gamma |
| `nh3_inversion.py` | ❌ | `setup_parameters()` Methode, Zeilen 72-83 | Parameter: h_radius, h_positions, dt, z_nitrogen |
| `nonbonded_interactions.py` | ❌ | `construct()` Methode, Zeilen 82-92 | Parameter: epsilon, sigma, k_coulomb, r_start, r_end |

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
| `monte_carlo_pi.py` | ❌ | Keine expliziten Parameter-Definitionen gefunden (erste 100 Zeilen) | - |
| `metropolis_animation.py` | ❌ | Zu prüfen | - |
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
- **Konform (✅):** 0 Dateien (0%)
- **Teilweise konform (⚠️):** 0 Dateien (0%)
- **Nicht konform (❌):** 19 Dateien (100%)

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

**Stand:** 2025-11-05
**Analysiert von:** Claude Code
**Basierend auf:** claude.md Zeilen 93-309 (Architecture Requirements: GUI Tool Compatibility)
