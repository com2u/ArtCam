import cv2
import numpy as np
import time

def apply_hybrids(frame, processor):
    processed = frame.copy()
    h, w = frame.shape[:2]
    
    # Time-Delayed Mirrors
    if processor.settings["time_delayed_mirrors"] > 0:
        if len(processor.time_buffer) > 30:
            past = processor.time_buffer[-30]
            processed[:, :w//2] = past[:, :w//2]
            
    # Motion Fossils
    if processor.settings["motion_fossils"] > 0:
        if processor.fossil_buffer is None or processor.fossil_buffer.shape != frame.shape:
            processor.fossil_buffer = np.zeros_like(frame, dtype=np.float32)
        
        if processor.prev_frame is not None and processor.prev_frame.shape == frame.shape:
            diff = cv2.absdiff(frame, processor.prev_frame)
            _, mask = cv2.threshold(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY), 30, 255, cv2.THRESH_BINARY)
            mask_3ch = cv2.merge([mask]*3)
            processor.fossil_buffer[mask_3ch > 0] = frame[mask_3ch > 0].astype(np.float32)
        
        processed = cv2.addWeighted(processed, 0.7, processor.fossil_buffer.astype(np.uint8), 0.3, 0)
        
    # Temporal Blur Field
    if processor.settings["temp_blur_field"] > 0:
        if processor.pixel_age_map is None or processor.pixel_age_map.shape != (h, w):
            processor.pixel_age_map = np.zeros((h, w), dtype=np.float32)
        
        if processor.prev_frame is not None and processor.prev_frame.shape == frame.shape:
            diff = cv2.absdiff(frame, processor.prev_frame)
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            processor.pixel_age_map[gray_diff < 20] += 1
            processor.pixel_age_map[gray_diff >= 20] = 0
            
        # Apply variable blur (simplified)
        blurred = cv2.GaussianBlur(processed, (15, 15), 0)
        mask = np.clip(processor.pixel_age_map / 100.0, 0, 1)
        mask_3ch = cv2.merge([mask]*3)
        processed = (processed * (1 - mask_3ch) + blurred * mask_3ch).astype(np.uint8)
        
    # Chrono-Pixel Sorting
    if processor.settings["chrono_pixel_sort"] > 0:
        # Sort pixels in rows based on brightness if they are "old"
        if processor.pixel_age_map is not None:
            for i in range(h):
                if np.mean(processor.pixel_age_map[i]) > 50:
                    row = processed[i]
                    processed[i] = row[np.argsort(np.mean(row, axis=1))]
                    
    # Frame Erosion
    if processor.settings["frame_erosion"] > 0:
        if processor.pixel_age_map is not None:
            noise = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
            mask = processor.pixel_age_map > (100 - processor.settings["frame_erosion"])
            processed[mask] = noise[mask]
            
    # Event Horizon
    if processor.settings["event_horizon"] > 0:
        if processor.event_horizon_mask is None or processor.event_horizon_mask.shape != (h, w):
            processor.event_horizon_mask = np.zeros((h, w), dtype=np.uint8)
        
        line_pos = w // 2
        processor.event_horizon_mask[:, line_pos:] = 1
        if processor.prev_frame is not None and processor.prev_frame.shape == frame.shape:
            processed[processor.event_horizon_mask > 0] = processor.prev_frame[processor.event_horizon_mask > 0]
            
    # Time-Warp Vortex
    if processor.settings["time_warp_vortex"] > 0:
        flex_x = np.zeros((h, w), np.float32)
        flex_y = np.zeros((h, w), np.float32)
        center_x, center_y = w // 2, h // 2
        for y in range(h):
            for x in range(w):
                dx, dy = x - center_x, y - center_y
                dist = np.sqrt(dx**2 + dy**2)
                angle = np.arctan2(dy, dx) + dist / 100.0 * (processor.settings["time_warp_vortex"] / 10.0)
                flex_x[y, x] = center_x + dist * np.cos(angle)
                flex_y[y, x] = center_y + dist * np.sin(angle)
        
        # Use frames from buffer based on distance to center
        res = np.zeros_like(processed)
        remapped = cv2.remap(processed, flex_x, flex_y, cv2.INTER_LINEAR)
        for y in range(h):
            for x in range(w):
                dx, dy = x - center_x, y - center_y
                dist = np.sqrt(dx**2 + dy**2)
                idx = int(np.clip(dist / 10, 0, len(processor.time_buffer)-1))
                if len(processor.time_buffer) > 0:
                    res[y, x] = processor.time_buffer[-idx-1][int(flex_y[y, x])%h, int(flex_x[y, x])%w]
        processed = res
        
    return processed