# Best Practices für die Verwendung von ManimGL

Dieses Dokument fasst bewährte Praktiken und häufige Muster für die Erstellung von Animationen mit `manimlib` (ManimGL) zusammen. Die Regeln basieren auf der Analyse erfolgreicher Skripte im Projekt.

## 1. Grundlegende Struktur einer Szene

Jede Animation muss in einer Klasse enthalten sein, die von `Scene` erbt. Die Hauptlogik der Animation befindet sich in der `construct`-Methode.

```python
from manimlib import *

class MyAnimationScene(Scene):
    def construct(self):
        # 1. Objekte erstellen (MObjects)
        circle = Circle()
        text = Text("Hallo, Manim!")

        # 2. Objekte zur Szene hinzufügen
        self.add(circle)

        # 3. Animationen abspielen
        self.play(Write(text))

        # 4. Eine Weile warten
        self.wait(2)
```

**Wichtige Befehle:**
- `self.add(mobject)`: Fügt ein Objekt sofort und ohne Animation zur Szene hinzu.
- `self.play(animation, ...)`: Spielt eine oder mehrere Animationen ab (z.B. `Write`, `FadeIn`, `ShowCreation`).
- `self.wait(duration)`: Pausiert die Animation für eine bestimmte Dauer in Sekunden.

**Ausführen einer Szene:**
Führen Sie das Skript über die Kommandozeile aus. Der Name der Klasse ist wichtig.
```bash
manimgl my_script.py MyAnimationScene
```

## 2. Animation durch Schleifen (Loop-Based Animation)

Für dynamische Simulationen (z.B. Moleküldynamik, Monte Carlo) ist eine `for`-Schleife der bevorzugte Ansatz. Dies ist einfacher und direkter als die Verwendung von `add_updater`.

**Schlüsselkonzept:** Aktualisieren Sie die Eigenschaften von MObjects innerhalb der Schleife und rufen Sie dann `self.wait(dt)` auf, um die Szene neu zu zeichnen.

```python
# Aus bond_stretching.py
class BondStretching(Scene):
    def construct(self):
        # ... Setup ...
        self.create_molecule()
        self.create_potential_curve()

        # Animationsschleife
        duration = 8.0
        fps = 30
        frames = int(duration * fps)

        for frame in range(frames):
            t = frame / fps
            
            # 1. Berechne den aktuellen Zustand
            r_current = self.r0 + self.amplitude * np.sin(2 * np.pi * self.frequency * t)

            # 2. Aktualisiere die MObjects (KEINE .animate-Syntax hier!)
            self.update_molecule_positions(r_current)
            
            energy = self.harmonic_potential(r_current)
            point_on_curve = self.axes.coords_to_point(r_current, energy)
            self.current_dot.move_to(point_on_curve)

            # 3. Warte für einen Frame, um die Änderungen sichtbar zu machen
            self.wait(1/fps)
```

## 3. Erstellen von 3D-Animationen (`ThreeDScene`)

Für 3D-Animationen müssen spezielle Klassen und Methoden verwendet werden.

### a. `ThreeDScene` als Basisklasse
Ihre Szenen-Klasse muss von `ThreeDScene` erben.

```python
from manimlib import *

class My3DScene(ThreeDScene):
    def construct(self):
        # ... 3D-Logik hier ...
```

### b. Kamerasteuerung
Die Kamera wird anders gesteuert als in älteren Manim-Versionen.

- **Korrekte Methode:** `self.camera.frame.set_euler_angles(theta=..., phi=...)`
- **Falsche Methode:** `self.set_camera_orientation(...)` führt zu einem `AttributeError`.

```python
# Korrektes Setup der Kamera aus torsion_angle_3d.py
class TorsionAngle3D(ThreeDScene):
    def setup_camera(self):
        """Setup 3D camera view"""
        self.camera.frame.set_euler_angles(theta=-45*DEGREES, phi=70*DEGREES)
```

### c. Mischen von 3D-Objekten und 2D-Overlays (HUD)
Ein häufiger Anwendungsfall ist die Anzeige von 3D-Objekten, die rotieren, während 2D-Elemente (Text, Graphen) statisch im Vordergrund bleiben.

- **3D-Objekte:** Erstellen Sie `Sphere`, `Cube` oder positionieren Sie 2D-Objekte mit 3D-Vektoren (z.B., `Sphere().move_to([1, 2, 3])`).
- **2D-Overlays:** Erstellen Sie normale 2D-Objekte (`Text`, `Axes`, `VGroup`).
- **WICHTIG:** Rufen Sie die Methode `.fix_in_frame()` für jedes 2D-Overlay-Objekt auf.

```python
# Beispiel aus torsion_angle_3d.py
class TorsionAngle3D(ThreeDScene):
    def construct(self):
        # ...
        # 2D-Titel als Overlay
        title = Text("Torsionswinkel").scale(0.6)
        title.to_edge(UP)
        title.fix_in_frame() # <-- Dieser Aufruf ist entscheidend!
        self.add(title)

        # 3D-Objekt
        sphere = Sphere(radius=1)
        self.add(sphere)

        # Kamera-Rotation
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
```

### d. `Group` vs. `VGroup` in 3D
In 3D-Szenen ist es **zwingend erforderlich**, `Group` anstelle von `VGroup` zu verwenden, um 3D-Objekte (wie `Sphere`) oder eine Mischung aus 3D- und 2D-Objekten zu gruppieren. `VGroup` ist nur für 2D-vektorbasierte Objekte (`VMobject`) gedacht und führt sonst zu einer `Exception`.

## 4. Bewährte Praktiken (Best Practices)

### a. Strukturierung komplexer Szenen
Teilen Sie die `construct`-Methode in logische private Methoden auf. Dies verbessert die Lesbarkeit und Wartbarkeit erheblich.

```python
# Gutes Beispiel aus forcefield_visualization.py
class ForceFieldVisualization(Scene):
    def construct(self):
        self.setup_forcefield_parameters()
        self.setup_layout()
        self.create_molecular_system()
        self.run_forcefield_demonstration()
```

### b. Umgang mit Text und Formeln
- **Normaler Text:** Verwenden Sie `Text("Mein Text")`.
- **Mathematische Formeln (LaTeX):** Verwenden Sie `Tex(r"\frac{a}{b}")`.
  - **Wichtig:** Benutzen Sie immer Raw-Strings (`r"..."`), um Probleme mit Backslashes zu vermeiden.
  - `manimgl` erfordert eine funktionierende LaTeX-Installation.

### c. Datenvisualisierung mit `Axes`
- Erstellen Sie Achsen mit `Axes(...)`.
- **Wichtig:** Konvertieren Sie immer Datenkoordinaten in Bildschirmkoordinaten mit `self.axes.coords_to_point(x_val, y_val)`.
- Zum Plotten von Funktionen verwenden Sie `self.axes.get_graph(my_function, x_range=[...])`.

### d. Performance bei vielen Objekten
Wenn Sie Tausende von Objekten (z.B. Punkte in einer Monte-Carlo-Simulation) erstellen, begrenzen Sie die Anzahl der gleichzeitig angezeigten Objekte, um die Performance zu erhalten.

```python
# Gutes Beispiel aus monte_carlo_pi.py
self.displayed_points = []
self.max_displayed_points = 500

# In der Animationsschleife:
visual_point = Dot(...)
self.displayed_points.append(visual_point)

if len(self.displayed_points) > self.max_displayed_points:
    old_point = self.displayed_points.pop(0)
    self.remove(old_point) # Entfernt das älteste Objekt aus der Szene

self.add(visual_point)
```

### e. Internationalisierung (i18n)
Für mehrsprachige Animationen ist die Verwendung eines `STRINGS`-Dictionary ein robustes Muster.

```python
# Muster aus Ihren Skripten
LANGUAGE = "DE"  # oder "EN"

STRINGS = {
    "DE": {"title": "Mein Titel"},
    "EN": {"title": "My Title"}
}

def get_string(key):
    return STRINGS[LANGUAGE][key]

# Verwendung:
title = Text(get_string("title"))
```

## 5. Häufige Fehler und deren Vermeidung

1.  **Fehler: Objekt erscheint nicht.**
    - **Ursache:** Das MObject wurde erstellt, aber nie mit `self.add(mobject)` oder `self.play(Animation(mobject))` zur Szene hinzugefügt.
    - **Lösung:** Stellen Sie sicher, dass jedes Objekt, das sichtbar sein soll, hinzugefügt wird.

2.  **Fehler: Animationen werden nicht abgespielt; alles erscheint sofort am Ende.**
    - **Ursache:** Eigenschaften von Objekten wurden in einer Schleife geändert, aber `self.wait(dt)` wurde innerhalb der Schleife vergessen. Ohne `wait` oder `play` führt Manim den Code sofort aus und zeigt nur das Endergebnis.
    - **Lösung:** Fügen Sie am Ende jeder Iteration einer Animationsschleife `self.wait(dt)` hinzu.

3.  **Fehler: `AttributeError: 'NoneType' object has no attribute 'copy'` beim Animieren.**
    - **Ursache:** Falsche Verwendung von `self.play()`. `my_object.move_to(X)` gibt `None` zurück.
    - **Falsch:** `self.play(my_object.move_to(X))`
    - **Richtig:** `self.play(my_object.animate.move_to(X))`
    - **Hinweis:** In den gezeigten Skripten wird die `.animate`-Syntax selten benötigt, da die Animation durch die Schleife und `self.wait()` gesteuert wird. Sie ist hauptsächlich für einfache, einmalige Übergänge nützlich.

4.  **Fehler: Animation wird extrem langsam oder stürzt ab.**
    - **Ursache:** Tausende von MObjects werden zur Szene hinzugefügt, ohne alte zu entfernen.
    - **Lösung:** Implementieren Sie eine Begrenzung für angezeigte Objekte, wie in Punkt 4.d beschrieben.

5.  **Fehler: `AttributeError: 'MyScene' object has no attribute 'my_label'`**
    - **Ursache:** Falsche Initialisierungsreihenfolge. Eine Update-Methode greift auf ein `self`-Attribut zu, das noch nicht erstellt wurde.
    - **Beispiel-Problem:**
      ```python
      # FALSCH
      def create_molecule(self):
          # ...
          self.update_molecule(0) # FEHLER: self.angle_label existiert hier noch nicht
          # ...
          self.angle_label = DecimalNumber(0)
          self.add(self.angle_label)

      def update_molecule(self, angle):
          self.angle_label.set_value(angle) # <-- Führt zu AttributeError
      ```
    - **Lösung:** Stellen Sie sicher, dass alle MObjects, die von Update-Methoden benötigt werden, **vor** dem ersten Aufruf dieser Methoden initialisiert werden.
      ```python
      # RICHTIG
      def create_molecule(self):
          # ...
          # Label ZUERST erstellen
          self.angle_label = DecimalNumber(0)
          self.add(self.angle_label)
          # ...
          # DANN die Update-Methode aufrufen
          self.update_molecule(0)

      def update_molecule(self, angle):
          self.angle_label.set_value(angle)
      ```

6.  **Fehler: `Exception: Only VMobjects can be passed into VGroup`**
    - **Ursache:** Es wurde versucht, ein nicht-vektorisiertes Objekt (wie ein 3D-`Sphere`) in eine `VGroup` einzufügen.
    - **Falsch:** `my_group = VGroup(Sphere(), Circle())`
    - **Lösung:** Verwenden Sie die generische `Group`-Klasse, wenn Sie 3D-Objekte oder eine Mischung verschiedener Objekttypen gruppieren.
    - **Richtig:** `my_group = Group(Sphere(), Circle())`
