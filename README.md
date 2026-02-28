# Rope Simulation

This project performs physics-based rope simulation using **Verlet integration**. Users can interactively move the rope, adjust gravity, and damping settings.

## Features

- **Verlet Integration**: Uses Verlet integration for realistic physics simulation.
- **Interactive Usage**: Drag and drop rope segments with the mouse.
- **Real-time Adjustments**: Adjust gravity, damping, segment count, and segment length in real-time.
- **Camera System**: Zoom in/out and pan (camera movement) features.
- **Interactive Interface**: Easy control with sliders and buttons.

## Technologies Used

| Technology | Version | Description |
|------------|---------|-------------|
| **Python** | `3.14` | Main programming language |
| **Pygame** | `2.6.1` | 2D graphics, game loop, and user interface |

### Project Structure

```
rope_sim/
├── src/
│   ├── main.py          # Main entry point and game loop
│   ├── requirements.txt # Dependencies (pygame==2.6.1)
│   ├── rope.py          # Rope class (Verlet integration)
│   ├── physics/
│   │   ├── __init__.py
│   │   ├── particle.py  # Particle (mass) class
│   │   └── constraint.py # Constraint (distance constraint) class
│   └── gui/
│       ├── __init__.py
│       └── gui.py       # User interface classes
└── venv/                # Python virtual environment
```

## Installation

1. **Clone the repository**
```bash
git clone <repourl>
cd rope_sim
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
cd src
pip install -r requirements.txt
```

## Running

```bash
cd src
python main.py
```

### Keyboard Controls

| Key | Function |
|-----|----------|
| `SPACE` | Start/Stop simulation |
| `R` | Reset rope |
| `ESC` | Exit |
| `+` / `Kp+` | Zoom in |
| `-` | Zoom out |
| `Drag` | Move rope segments |

### UI Controls

- **Reset Rope**: Reset rope to initial position
- **Gravity Slider**: Gravity force (0.1 - 2.5)
- **Damping Slider**: Damping coefficient (0.85 - 1.0)
- **Segments Slider**: Number of segments (2 - 5000)
- **Segment Length Slider**: Length of each segment (15 - 187)
- **Zoom +/-/Reset**: Camera zoom controls

## Technical Details

### Verlet Integration

The project uses Verlet integration for physics simulation:

```
v = (current_pos - old_pos) * damping
new_pos = current_pos + v + gravity * dt²
```

This method provides numerical stability and helps rope-like flexible structures appear realistic.

### System Components

1. **Particle**
   - Represents a mass
   - Stores position, velocity, and mass information
   - `is_fixed`: Is this a fixed point?
   - `is_being_dragged`: Is the user dragging it?

2. **Constraint**
   - Maintains distance between two particles
   - Controls flexibility with stiffness parameter
   - Iterative solving for stability

3. **Rope**
   - Combines particles and constraints
   - `update()`: Physics update
   - `draw()`: Screen drawing
   - `drag_particle()`: Mouse interaction

4. **Camera**
   - Zoom and pan operations
   - World coordinates ↔ Screen coordinates transformation

## Screenshots

The simulation screen includes:

- **Background**: Grid system
- **Rope**: White particles and gray segments
- **UI Panel**: Parameter controls in the top-right corner
- **Info Panel**: Real-time simulation statistics

---

**Note**: This is an educational physics simulation project written with the Pygame library.

**Vibe Coding Note**: This project was developed in approximately 2 hours of vibe coding.
````
