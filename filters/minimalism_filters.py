import cv2
import numpy as np
import time

def apply_minimalism(frame, processor):
    processed = frame.copy()
    h, w = frame.shape[:2]
    
    # Single Pixel World
    if processor.settings["single_pixel"] > 0:
        avg_color = np.mean(processed, axis=(0, 1))
        processed[:] = avg_color
        
    # Average Reality
    if processor.settings["average_reality"] > 0:
        if processor.average_reality_buffer is None or processor.average_reality_buffer.shape != frame.shape:
            processor.average_reality_buffer = frame.astype(np.float32)
        else:
            processor.average_reality_buffer = cv2.addWeighted(processor.average_reality_buffer, 0.99, frame.astype(np.float32), 0.01, 0)
        processed = processor.average_reality_buffer.astype(np.uint8)
        
    # Color Census
    if processor.settings["color_census"] > 0:
        pixels = processed.reshape(-1, 3)
        unique, counts = np.unique(pixels, axis=0, return_counts=True)
        most_common = unique[np.argmax(counts)]
        processed[:] = most_common
        
    # Entropy Maximizer
    if processor.settings["entropy_maximizer"] > 0:
        noise = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
        processed = cv2.addWeighted(processed, 0.9, noise, 0.1, 0)
        
    # Camera Amnesia
    if processor.settings["camera_amnesia"] > 0:
        if time.time() - processor.amnesia_timer > processor.settings["camera_amnesia"]:
            processed[:] = 0
            processor.amnesia_timer = time.time()
            
    # Reality Quantizer
    if processor.settings["reality_quantizer"] > 0:
        small = cv2.resize(processed, (16, 16), interpolation=cv2.INTER_NEAREST)
        processed = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        
    # Noise Wins
    if processor.settings["noise_wins"] > 0:
        noise = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
        alpha = min(1.0, (time.time() - processor.session_start_time) / 60.0)
        processed = cv2.addWeighted(processed, 1.0 - alpha, noise, alpha, 0)
        
    return processed