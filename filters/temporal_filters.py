import cv2
import numpy as np
import time

def apply_temporal(frame, processor):
    if processor.settings["motion_trail"] > 0:
        processor.motion_history.append(frame.copy())
        if len(processor.motion_history) > processor.settings["motion_trail"]:
            processor.motion_history.pop(0)
        
        avg_frame = np.zeros_like(frame, dtype=np.float32)
        for f in processor.motion_history:
            avg_frame += f.astype(np.float32)
        avg_frame /= len(processor.motion_history)
        return avg_frame.astype(np.uint8)
    
    if processor.settings["ghosting"] > 0 and processor.prev_frame is not None:
        if processor.prev_frame.shape == frame.shape:
            diff = cv2.absdiff(frame, processor.prev_frame)
            return cv2.addWeighted(frame, 0.7, diff, 0.3, 0)
            
    return frame

def apply_temporal_abuse(frame, processor):
    h, w = frame.shape[:2]
    processed = frame.copy()
    
    # Update time buffer
    processor.time_buffer.append(frame.copy())
    if len(processor.time_buffer) > processor.max_buffer_size:
        processor.time_buffer.pop(0)
        
    # Time Smear
    if processor.settings["time_smear"] > 0:
        if processor.smear_buffer is None or processor.smear_buffer.shape != frame.shape:
            processor.smear_buffer = frame.astype(np.float32)
        alpha = 1.0 - (processor.settings["time_smear"] / 100.0)
        processor.smear_buffer = cv2.addWeighted(processor.smear_buffer, alpha, frame.astype(np.float32), 1.0 - alpha, 0)
        processed = processor.smear_buffer.astype(np.uint8)
        
    # Temporal Echo
    if processor.settings["temporal_echo"] > 0:
        echo_count = min(len(processor.time_buffer), processor.settings["temporal_echo"])
        if echo_count > 1:
            echo_frame = np.zeros_like(frame, dtype=np.float32)
            decay = 0.7
            weight_sum = 0
            for i in range(echo_count):
                w_i = decay ** i
                echo_frame += processor.time_buffer[-(i+1)].astype(np.float32) * w_i
                weight_sum += w_i
            processed = (echo_frame / weight_sum).astype(np.uint8)
            
    # Time Slice
    if processor.settings["time_slice"] > 0:
        slice_pos = (int(time.time() * 100) % w)
        if len(processor.time_buffer) > 30:
            past_frame = processor.time_buffer[-30]
            res = past_frame.copy()
            res[:, slice_pos:slice_pos+10] = frame[:, slice_pos:slice_pos+10]
            processed = res
            
    # Reverse Aging
    if processor.settings["reverse_aging"] > 0:
        if len(processor.time_buffer) > 60:
            for _ in range(5):
                ry = np.random.randint(0, h-50)
                rx = np.random.randint(0, w-50)
                age = np.random.randint(1, min(len(processor.time_buffer), 60))
                processed[ry:ry+50, rx:rx+50] = processor.time_buffer[-age][ry:ry+50, rx:rx+50]
                
    # Frame Freezing Cells
    if processor.settings["freeze_cells"] > 0:
        if processor.frozen_cells is None or processor.frozen_cells.shape != frame.shape:
            processor.frozen_cells = frame.copy()
            processor.frozen_mask = np.zeros((h, w), dtype=np.uint8)
        
        cell_size = 40
        for y in range(0, h, cell_size):
            for x in range(0, w, cell_size):
                if np.random.random() < (processor.settings["freeze_cells"] / 1000.0):
                    processor.frozen_mask[y:y+cell_size, x:x+cell_size] = 255
                    processor.frozen_cells[y:y+cell_size, x:x+cell_size] = frame[y:y+cell_size, x:x+cell_size]
                elif np.random.random() < 0.05: # Chance to unfreeze
                    processor.frozen_mask[y:y+cell_size, x:x+cell_size] = 0
        
        mask_3ch = cv2.merge([processor.frozen_mask]*3)
        processed = np.where(mask_3ch == 255, processor.frozen_cells, processed)
        
    # Memory Burn-In
    if processor.settings["memory_burn"] > 0:
        if processor.burn_in_buffer is None or processor.burn_in_buffer.shape != frame.shape:
            processor.burn_in_buffer = np.zeros_like(frame, dtype=np.float32)
        
        burn_rate = processor.settings["memory_burn"] / 1000.0
        processor.burn_in_buffer = cv2.addWeighted(processor.burn_in_buffer, 1.0, frame.astype(np.float32), burn_rate, 0)
        processed = cv2.addWeighted(processed, 1.0, np.clip(processor.burn_in_buffer, 0, 255).astype(np.uint8), 0.5, 0)
        
    # Temporal Feedback Loop
    if processor.settings["temp_feedback"] > 0:
        if processor.feedback_buffer is None or processor.feedback_buffer.shape != frame.shape:
            processor.feedback_buffer = frame.astype(np.float32)
        
        gain = 1.0 + (processor.settings["temp_feedback"] / 100.0)
        processor.feedback_buffer = cv2.addWeighted(processor.feedback_buffer, gain, frame.astype(np.float32), 0.1, 0)
        processor.feedback_buffer = np.clip(processor.feedback_buffer, 0, 255)
        processed = processor.feedback_buffer.astype(np.uint8)
        
    # Time Jitter
    if processor.settings["time_jitter"] > 0:
        if len(processor.time_buffer) > 10:
            jitter_range = min(len(processor.time_buffer), processor.settings["time_jitter"])
            idx = np.random.randint(1, jitter_range)
            processed = processor.time_buffer[-idx]
            
    # Slit-Scan Reality
    if processor.settings["slit_scan"] > 0:
        res = np.zeros_like(frame)
        for x in range(w):
            idx = int((x / w) * (len(processor.time_buffer) - 1))
            res[:, x] = processor.time_buffer[idx][:, x]
        processed = res
        
    # Temporal Quantization
    if processor.settings["temp_quantize"] > 0:
        processor.frame_count += 1
        q = max(1, 60 // processor.settings["temp_quantize"])
        if processor.frame_count % q == 0 or processor.quantized_frame is None:
            processor.quantized_frame = frame.copy()
        processed = processor.quantized_frame
        
    return processed