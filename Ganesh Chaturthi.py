import os
import cv2
import numpy as np
import random

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_IMAGE = os.path.join(script_dir, 'Ganesha.png')

CANVAS_W, CANVAS_H = 1920, 1080
FPS = 60
WINDOW_NAME = "Outline Rice Grain Assembly"

GRAIN_SPACING = 5
GRAIN_FLIGHT_FRAMES = 15
TOTAL_ASSEMBLY_SEC = 6.0
CROSSFADE_SEC = 1.0
HOLD_SEC = 3.0

def load_and_fit(path, w, h):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    ih, iw = img.shape[:2]
    scale = min(w / iw, h / ih)
    new_w, new_h = int(iw * scale), int(ih * scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    canvas = np.full((h, w, 3), 255, dtype=np.uint8)
    canvas[(h - new_h) // 2:(h - new_h) // 2 + new_h, (w - new_w) // 2:(w - new_w) // 2 + new_w] = resized
    return canvas

def draw_rice_grain(img, center, angle, color=(240, 245, 255), length=5, width=2):
    cv2.ellipse(img, center, (length, width), angle, 0, 360, color, -1, cv2.LINE_AA)

def main():
    try:
        base = load_and_fit(INPUT_IMAGE, CANVAS_W, CANVAS_H)
    except FileNotFoundError as e:
        print(e)
        return

    gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    _, outline_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    grains = []
    h, w = base.shape[:2]
    
    for y in range(0, h, GRAIN_SPACING):
        for x in range(0, w, GRAIN_SPACING):
            if outline_mask[y, x] == 0:
                continue
            
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top': start_pos = (random.randint(0, CANVAS_W), -40)
            elif edge == 'bottom': start_pos = (random.randint(0, CANVAS_W), CANVAS_H + 40)
            elif edge == 'left': start_pos = (-40, random.randint(0, CANVAS_H))
            else: start_pos = (CANVAS_W + 40, random.randint(0, CANVAS_H))

            grains.append({
                'start': start_pos,
                'target': (x, y),
                'start_angle': random.randint(0, 360),
                'target_angle': random.randint(0, 180),
                'color': (240, 245, 255)
            })

    random.shuffle(grains)
    
    total_assembly_frames = max(1, int(TOTAL_ASSEMBLY_SEC * FPS))
    total_grains = len(grains)
    
    for idx, grain in enumerate(grains):
        grain['start_frame'] = int((idx / total_grains) * (total_assembly_frames - GRAIN_FLIGHT_FRAMES))

    delay = max(1, int(1000 / FPS))
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    rice_canvas = np.zeros_like(base)

    target_final = np.zeros_like(base)
    target_final[outline_mask > 0] = (240, 245, 255)

    for current_frame in range(total_assembly_frames):
        frame = rice_canvas.copy()

        for grain in grains:
            st = grain['start_frame']
            et = st + GRAIN_FLIGHT_FRAMES

            if current_frame < st:
                continue
            elif current_frame >= et:
                if 'locked' not in grain:
                    draw_rice_grain(rice_canvas, grain['target'], grain['target_angle'], grain['color'])
                    grain['locked'] = True
            else:
                progress = (current_frame - st) / GRAIN_FLIGHT_FRAMES
                ease_t = 1 - (1 - progress) ** 2

                cx = int(grain['start'][0] + (grain['target'][0] - grain['start'][0]) * ease_t)
                cy = int(grain['start'][1] + (grain['target'][1] - grain['start'][1]) * ease_t)
                c_angle = grain['start_angle'] + (grain['target_angle'] - grain['start_angle']) * ease_t
                
                draw_rice_grain(frame, (cx, cy), c_angle, grain['color'])

        cv2.imshow(WINDOW_NAME, frame)
        if cv2.waitKey(delay) & 0xFF in (27, ord('q')):
            cv2.destroyAllWindows()
            return

    crossfade_frames = max(1, int(CROSSFADE_SEC * FPS))
    for f in range(crossfade_frames):
        t = (f + 1) / crossfade_frames
        blended = cv2.addWeighted(rice_canvas, 1 - t, target_final, t, 0)
        cv2.imshow(WINDOW_NAME, blended)
        if cv2.waitKey(delay) & 0xFF in (27, ord('q')):
            cv2.destroyAllWindows()
            return

    hold_frames = max(1, int(HOLD_SEC * FPS))
    for _ in range(hold_frames):
        cv2.imshow(WINDOW_NAME, target_final)
        if cv2.waitKey(delay) & 0xFF in (27, ord('q')):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
