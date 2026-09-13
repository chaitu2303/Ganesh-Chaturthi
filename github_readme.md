# White Rice Grain Animation (Ganesha Line Art Reveal)

An interactive Python animation project using OpenCV and NumPy that creates a visual particle-assembly effect. Thousands of individual white rice grains fly in sequentially from random off-screen positions to assemble into a dark line-art image of Lord Ganesha on a sleek black background, smoothly transitioning into a high-definition final reveal.

---

## 🌟 Visual Preview

* **Input Image:** `ganesha.png` (Black outline line-art image on white/transparent background)
* **Animation Flow:**
  1. **Background Setup:** Full HD Pitch Black Canvas ($1920 \times 1080$).
  2. **Sequential Assembly:** Thousands of individual 2D white rice grains fly in from off-screen borders.
  3. **Outline Masking:** Grains only lock onto the contours and line strokes of `ganesha.png`.
  4. **Final Sharp Transition:** Smooth crossfade from particle rice grains to a crisp high-contrast final outline display.

---

## 🛠️ Prerequisites & Requirements

Make sure you have Python 3.7+ installed along with the required libraries:

```bash
pip install opencv-python numpy
```

---

## 📁 Project Directory Structure

Ensure your project directory is structured as follows:

```text
├── ganesha.png          # Input image file (Ganesha outline)
├── particle_animation.py # Main Python animation script
└── README.md            # Documentation file
```

> **Note:** Place your image file (`ganesha.png`) in the same root directory as your script.

---

## 🚀 How to Run

Run the animation script via command line:

```bash
python particle_animation.py
```

### 🎮 Controls
* Press **`q`** or **`ESC`** anytime to exit the full-screen animation loop.

---

## ⚙️ Customization Parameters

You can easily adjust animation parameters inside `particle_animation.py` to customize the rendering:

| Parameter | Default Value | Description |
| :--- | :--- | :--- |
| `INPUT_IMAGE` | `'ganesha.png'` | Target image file path |
| `CANVAS_W`, `CANVAS_H` | `1920, 1080` | Output window resolution |
| `FPS` | `60` | Animation target frames per second |
| `GRAIN_SPACING` | `5` | Pixel step distance (Smaller = denser rice grains & sharper detail) |
| `GRAIN_FLIGHT_FRAMES` | `15` | Travel time per individual grain |
| `TOTAL_ASSEMBLY_SEC` | `6.0` | Total assembly sequence duration (seconds) |
| `CROSSFADE_SEC` | `1.0` | Duration of crossfade into sharp final artwork |

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).