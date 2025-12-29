import cv2
import numpy as np

def apply_glitch(frame, processor):
    processed = frame.copy()
    h, w = frame.shape[:2]
    
    # RGB Split
    shift = processor.settings["glitch_rgb_split"]
    if shift > 0:
        b, g, r = cv2.split(processed)
        b = np.roll(b, shift, axis=1)
        r = np.roll(r, -shift, axis=1)
        processed = cv2.merge([b, g, r])
        
    # Jitter
    jitter = processor.settings["glitch_jitter"]
    if jitter > 0:
        for i in range(h):
            if np.random.random() < 0.1:
                processed[i] = np.roll(processed[i], np.random.randint(-jitter, jitter), axis=0)
                
    # Block Shift
    block = processor.settings["glitch_block_shift"]
    if block > 0:
        for _ in range(5):
            by = np.random.randint(0, h-block)
            bx = np.random.randint(0, w-block)
            bh = np.random.randint(10, block+10)
            bw = np.random.randint(10, block+10)
            shift_x = np.random.randint(-block, block)
            processed[by:by+bh, bx:bx+bw] = np.roll(processed[by:by+bh, bx:bx+bw], shift_x, axis=1)
    
    # VHS Noise
    if processor.settings["vhs_noise"] > 0:
        noise = np.random.randint(0, 50, (h, w, 3), dtype=np.uint8)
        processed = cv2.addWeighted(processed, 0.9, noise, 0.1, 0)
        # Add some horizontal lines
        for _ in range(3):
            y = np.random.randint(0, h)
            processed[y:y+2, :] = processed[y:y+2, :] * 0.5 + 128
            
    return processed

def apply_optical(frame, processor):
    mode = processor.settings["optical_mode"]
    if mode == "None": return frame
    h, w = frame.shape[:2]
    
    if mode == "Kaleidoscope":
        # Simple 4-way mirror
        top_left = frame[:h//2, :w//2]
        top_right = cv2.flip(top_left, 1)
        bottom_left = cv2.flip(top_left, 0)
        bottom_right = cv2.flip(top_right, 0)
        top = np.hstack((top_left, top_right))
        bottom = np.hstack((bottom_left, bottom_right))
        return np.vstack((top, bottom))
    
    elif mode == "Swirl":
        flex_x = np.zeros((h, w), np.float32)
        flex_y = np.zeros((h, w), np.float32)
        center_x, center_y = w // 2, h // 2
        radius = min(w, h) // 2
        strength = processor.settings["optical_amount"] / 10.0
        
        for y in range(h):
            for x in range(w):
                dx, dy = x - center_x, y - center_y
                distance = np.sqrt(dx**2 + dy**2)
                if distance < radius:
                    angle = np.arctan2(dy, dx) + strength * (radius - distance) / radius
                    flex_x[y, x] = center_x + distance * np.cos(angle)
                    flex_y[y, x] = center_y + distance * np.sin(angle)
                else:
                    flex_x[y, x] = x
                    flex_y[y, x] = y
        return cv2.remap(frame, flex_x, flex_y, cv2.INTER_LINEAR)
    
    elif mode == "Mirror Tiles":
        tile_w, tile_h = w // 4, h // 4
        tile = frame[:tile_h, :tile_w]
        tile_flipped = cv2.flip(tile, 1)
        row = np.tile(np.hstack((tile, tile_flipped)), (1, 2))
        row_flipped = cv2.flip(row, 0)
        return np.tile(np.vstack((row, row_flipped)), (2, 1))[:h, :w]
        
    return frame