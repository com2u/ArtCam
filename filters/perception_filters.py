import cv2
import numpy as np
import time

def apply_perception_weirdness(frame, processor):
    processed = frame.copy()
    h, w = frame.shape[:2]
    
    # Motion Hallucination
    if processor.settings["motion_hallucination"] > 0:
        offset = int(time.time() * 10) % 20
        for i in range(0, h, 20):
            processed[i:i+10] = np.roll(processed[i:i+10], offset, axis=1)
            processed[i+10:i+20] = np.roll(processed[i+10:i+20], -offset, axis=1)
            
    # Impossible Colors
    if processor.settings["impossible_colors"] > 0:
        lab = cv2.cvtColor(processed, cv2.COLOR_BGR2LAB).astype(np.float32)
        lab[:,:,1] = 255 - lab[:,:,1] # Invert A channel
        lab[:,:,2] = 255 - lab[:,:,2] # Invert B channel
        processed = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        
    # Edge Overload
    if processor.settings["edge_overload"] > 0:
        for _ in range(processor.settings["edge_overload"]):
            edges = cv2.Canny(processed, 50, 150)
            edges_3ch = cv2.merge([edges]*3)
            processed = cv2.addWeighted(processed, 0.8, edges_3ch, 0.5, 0)
            
    # Depth Inversion
    if processor.settings["depth_inversion"] > 0:
        gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        inverted_gray = 255 - gray
        processed = cv2.applyColorMap(inverted_gray, cv2.COLORMAP_JET)
        
    # Face Ghosting
    if processor.settings["face_ghosting"] > 0:
        # Simple approximation: amplify skin-like tones
        hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 20, 70])
        upper = np.array([20, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        mask_3ch = cv2.merge([mask]*3)
        ghost = cv2.GaussianBlur(processed, (25, 25), 0)
        processed = np.where(mask_3ch > 0, cv2.addWeighted(processed, 0.5, ghost, 0.5, 0), processed)
        
    # Pareidolia Booster
    if processor.settings["pareidolia_booster"] > 0:
        # Enhance local contrast and sharpen
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        processed = cv2.filter2D(processed, -1, kernel)
        
    # Visual Tinnitus
    if processor.settings["visual_tinnitus"] > 0:
        gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        noise = np.random.randint(0, 256, (h, w), dtype=np.uint8)
        mask = (gray.astype(np.float32) / 255.0) * (processor.settings["visual_tinnitus"] / 100.0)
        mask_3ch = cv2.merge([mask]*3)
        noise_3ch = cv2.merge([noise]*3)
        processed = (processed * (1 - mask_3ch) + noise_3ch * mask_3ch).astype(np.uint8)
        
    # Afterimage Trap
    if processor.settings["afterimage_trap"] > 0 and processor.prev_frame is not None:
        if processor.prev_frame.shape == frame.shape:
            inverted_prev = 255 - processor.prev_frame
            processed = cv2.addWeighted(processed, 0.7, inverted_prev, 0.3, 0)
            
    return processed