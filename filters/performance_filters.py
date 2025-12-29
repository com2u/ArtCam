import cv2
import numpy as np
import time

def apply_performance_art(frame, processor):
    processed = frame.copy()
    h, w = frame.shape[:2]
    
    # Surveillance Degradation
    if processor.settings["surveillance_degradation"] > 0:
        elapsed = time.time() - processor.session_start_time
        blur_amt = int(min(50, elapsed / 5.0)) * 2 + 1
        if blur_amt > 1:
            processed = cv2.GaussianBlur(processed, (blur_amt, blur_amt), 0)
            
    # Attention Punisher
    if processor.settings["attention_punisher"] > 0 and processor.prev_frame is not None:
        if processor.prev_frame.shape == frame.shape:
            diff = cv2.absdiff(frame, processor.prev_frame)
            motion = np.mean(diff)
            if motion < 10:
                processed = cv2.GaussianBlur(processed, (21, 21), 0)
                
    # Observer Effect
    if processor.settings["observer_effect"] > 0 and processor.prev_frame is not None:
        if processor.prev_frame.shape == frame.shape:
            diff = cv2.absdiff(frame, processor.prev_frame)
            _, mask = cv2.threshold(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY), 20, 255, cv2.THRESH_BINARY)
            mask_3ch = cv2.merge([mask]*3)
            noise = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
            processed = np.where(mask_3ch > 0, noise, processed)
            
    # Machine Fatigue
    if processor.settings["machine_fatigue"] > 0:
        elapsed = time.time() - processor.session_start_time
        noise_amt = min(100, elapsed / 2.0)
        noise = np.random.normal(0, noise_amt, frame.shape).astype(np.uint8)
        processed = cv2.add(processed, noise)
        
    # Digital Death
    if processor.settings["digital_death"] > 0:
        elapsed = time.time() - processor.session_start_time
        if elapsed > 120: # Dies after 2 minutes
            processed[:] = np.random.randint(0, 2, (h, w, 3), dtype=np.uint8) * 255
        
    # Resurrection Loop
    if processor.settings["resurrection_loop"] > 0:
        cycle = int(time.time() - processor.session_start_time) % 30
        if cycle > 25: # Collapse
            processed = cv2.resize(processed, (1, 1))
            processed = cv2.resize(processed, (w, h), interpolation=cv2.INTER_NEAREST)
        elif cycle < 5: # Reset/Resurrect
            pass # Normal
            
    return processed