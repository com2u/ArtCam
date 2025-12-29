import cv2
import numpy as np

def apply_spatial_chaos(frame, processor):
    processed = frame.copy()
    h, w = frame.shape[:2]
    
    # Pixel Gravity
    if processor.settings["pixel_gravity"] > 0:
        if processor.gravity_buffer is None or processor.gravity_buffer.shape != frame.shape:
            processor.gravity_buffer = frame.copy()
        
        gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        for _ in range(processor.settings["pixel_gravity"]):
            y_indices, x_indices = np.where(gray > 128)
            if len(y_indices) > 0:
                for i in range(min(len(y_indices), 1000)):
                    idx = np.random.randint(0, len(y_indices))
                    y, x = y_indices[idx], x_indices[idx]
                    if y < h - 1:
                        processed[y+1, x] = processed[y, x]
    
    # Reality Tear
    if processor.settings["reality_tear"] > 0:
        for _ in range(processor.settings["reality_tear"]):
            y = np.random.randint(0, h)
            shift = np.random.randint(-50, 50)
            processed[y:] = np.roll(processed[y:], shift, axis=1)
            
    # Recursive Zoom Hole
    if processor.settings["recursive_zoom"] > 0:
        center = (w // 2, h // 2)
        scale = 1.0 + (processor.settings["recursive_zoom"] / 100.0)
        M = cv2.getRotationMatrix2D(center, 0, scale)
        zoomed = cv2.warpAffine(processed, M, (w, h))
        processed = cv2.addWeighted(processed, 0.5, zoomed, 0.5, 0)
        
    # Voronoi Destruction
    if processor.settings["voronoi_dest"] > 0:
        num_points = processor.settings["voronoi_dest"]
        points = np.column_stack((np.random.randint(0, w, num_points), np.random.randint(0, h, num_points)))
        res = np.zeros_like(processed)
        for y in range(0, h, 10):
            for x in range(0, w, 10):
                dists = np.sum((points - [x, y])**2, axis=1)
                closest = points[np.argmin(dists)]
                res[y:y+10, x:x+10] = processed[closest[1], closest[0]]
        processed = res
        
    # Non-Euclidean Mirror
    if processor.settings["non_euclidean"] > 0:
        flex_x = np.zeros((h, w), np.float32)
        flex_y = np.zeros((h, w), np.float32)
        for y in range(h):
            for x in range(w):
                flex_x[y, x] = x + np.sin(y / 10.0) * processor.settings["non_euclidean"]
                flex_y[y, x] = y + np.cos(x / 10.0) * processor.settings["non_euclidean"]
        processed = cv2.remap(processed, flex_x, flex_y, cv2.INTER_LINEAR)
        
    # Pixel Erosion
    if processor.settings["pixel_erosion"] > 0:
        kernel = np.ones((3, 3), np.uint8)
        processed = cv2.erode(processed, kernel, iterations=processor.settings["pixel_erosion"])
        
    # Fracture Glass
    if processor.settings["fracture_glass"] > 0:
        # Simple shard shift
        for _ in range(processor.settings["fracture_glass"]):
            x = np.random.randint(0, w-100)
            y = np.random.randint(0, h-100)
            dx = np.random.randint(-10, 10)
            dy = np.random.randint(-10, 10)
            shard = processed[y:y+100, x:x+100].copy()
            processed[np.clip(y+dy, 0, h-100):np.clip(y+dy+100, 0, h), np.clip(x+dx, 0, w-100):np.clip(x+dx+100, 0, w)] = shard
        
    # Spatial Feedback
    if processor.settings["spatial_feedback"] > 0:
        if processor.spatial_feedback_buffer is None or processor.spatial_feedback_buffer.shape != frame.shape:
            processor.spatial_feedback_buffer = processed.copy()
        roi_size = 100
        y1, x1 = np.random.randint(0, h-roi_size), np.random.randint(0, w-roi_size)
        y2, x2 = np.random.randint(0, h-roi_size), np.random.randint(0, w-roi_size)
        processor.spatial_feedback_buffer[y1:y1+roi_size, x1:x1+roi_size] = processed[y2:y2+roi_size, x2:x2+roi_size]
        processed = cv2.addWeighted(processed, 0.7, processor.spatial_feedback_buffer, 0.3, 0)
        
    # Folding Space
    if processor.settings["folding_space"] > 0:
        for _ in range(processor.settings["folding_space"]):
            processed = cv2.addWeighted(processed, 0.5, cv2.flip(processed, 1), 0.5, 0)
            
    return processed