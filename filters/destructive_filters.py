import cv2
import numpy as np
import time

def apply_destructive_color(frame, processor):
    processed = frame.copy()
    h, w = frame.shape[:2]
    
    # Color Channel Collapse
    if processor.settings["color_collapse"] > 0:
        b, g, r = cv2.split(processed.astype(np.float32))
        avg = (b + g + r) / 3.0
        alpha = processor.settings["color_collapse"] / 100.0
        b = cv2.addWeighted(b, 1.0 - alpha, avg, alpha, 0)
        g = cv2.addWeighted(g, 1.0 - alpha, avg, alpha, 0)
        r = cv2.addWeighted(r, 1.0 - alpha, avg, alpha, 0)
        processed = cv2.merge([b, g, r]).astype(np.uint8)
        
    # Hue Shatter
    if processor.settings["hue_shatter"] > 0:
        hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)
        h_chan, s, v = cv2.split(hsv)
        shards = processor.settings["hue_shatter"]
        h_chan = (h_chan // (180 // shards)) * (180 // shards)
        processed = cv2.cvtColor(cv2.merge([h_chan, s, v]), cv2.COLOR_HSV2BGR)
        
    # Bit-Rot Simulation
    if processor.settings["bit_rot"] > 0:
        noise = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
        mask = np.random.random((h, w, 3)) < (processor.settings["bit_rot"] / 1000.0)
        processed[mask] = processed[mask] ^ noise[mask]
        
    # Palette Decay
    if processor.settings["palette_decay"] > 0:
        div = max(1, 256 // (256 - processor.settings["palette_decay"] * 2))
        processed = (processed // div) * div
        
    # Solarization Hell
    if processor.settings["solarize_hell"] > 0:
        thresh = 255 - processor.settings["solarize_hell"] * 2
        gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
        processed[mask > 0] = 255 - processed[mask > 0]
        
    # Color Bleeding
    if processor.settings["color_bleeding"] > 0:
        kernel_size = processor.settings["color_bleeding"] // 5 * 2 + 1
        if kernel_size > 1:
            blurred = cv2.GaussianBlur(processed, (kernel_size, kernel_size), 0)
            edges = cv2.Canny(processed, 100, 200)
            edges_3ch = cv2.merge([edges]*3)
            processed = np.where(edges_3ch > 0, blurred, processed)
            
    # Chromatic Meltdown
    if processor.settings["chromatic_meltdown"] > 0:
        hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:,:,1] *= (1.0 + processor.settings["chromatic_meltdown"] / 10.0)
        hsv[:,:,1] = np.clip(hsv[:,:,1], 0, 255)
        processed = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
    # Hue Feedback Oscillator
    if processor.settings["hue_feedback"] > 0:
        processor.hue_offset = (processor.hue_offset + processor.settings["hue_feedback"]) % 180
        hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)
        h_chan, s, v = cv2.split(hsv)
        h_chan = (h_chan.astype(np.int16) + int(processor.hue_offset)) % 180
        processed = cv2.cvtColor(cv2.merge([h_chan.astype(np.uint8), s, v]), cv2.COLOR_HSV2BGR)
        
    # Dead Channel Emulation
    if processor.settings["dead_channel"] != "None":
        if processor.settings["dead_channel"] == "Red":
            processed[:,:,2] = 0
        elif processor.settings["dead_channel"] == "Green":
            processed[:,:,1] = 0
        elif processor.settings["dead_channel"] == "Blue":
            processed[:,:,0] = 0
            
    return processed

def apply_digital_violence(frame, processor):
    processed = frame.copy()
    h, w = frame.shape[:2]
    
    # Compression Artifact Storm
    if processor.settings["comp_artifacts"] > 0:
        q = max(1, 100 - processor.settings["comp_artifacts"])
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), q]
        _, encimg = cv2.imencode('.jpg', processed, encode_param)
        processed = cv2.imdecode(encimg, 1)
        
    # Row Desynchronization
    if processor.settings["row_desync"] > 0:
        for i in range(h):
            if np.random.random() < (processor.settings["row_desync"] / 100.0):
                shift = np.random.randint(-w//4, w//4)
                processed[i] = np.roll(processed[i], shift, axis=0)
                
    # Packet Loss Visualizer
    if processor.settings["packet_loss"] > 0:
        num_chunks = processor.settings["packet_loss"]
        for _ in range(num_chunks):
            ch = np.random.randint(10, 50)
            cw = np.random.randint(10, 50)
            cy = np.random.randint(0, h-ch)
            cx = np.random.randint(0, w-cw)
            if np.random.random() < 0.5:
                processed[cy:cy+ch, cx:cx+cw] = 0
            else:
                processed[cy:cy+ch, cx:cx+cw] = np.random.randint(0, 256, (ch, cw, 3))
                
    # Resolution Thrashing
    if processor.settings["res_thrashing"] > 0:
        factor = np.random.uniform(0.1, 1.0)
        small = cv2.resize(processed, (int(w*factor), int(h*factor)), interpolation=cv2.INTER_NEAREST)
        processed = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        
    # Macroblock Shuffle
    if processor.settings["macroblock_shuffle"] > 0:
        bs = 32
        blocks = []
        for y in range(0, h, bs):
            for x in range(0, w, bs):
                blocks.append(processed[y:y+bs, x:x+bs].copy())
        np.random.shuffle(blocks)
        i = 0
        for y in range(0, h, bs):
            for x in range(0, w, bs):
                if i < len(blocks):
                    bh, bw = blocks[i].shape[:2]
                    processed[y:y+bh, x:x+bw] = blocks[i]
                    i += 1
                    
    # Sync Loss
    if processor.settings["sync_loss"] > 0:
        offset = int(time.time() * 500) % h
        processed = np.roll(processed, offset, axis=0)
        if np.random.random() < 0.1:
            processed = np.roll(processed, np.random.randint(-20, 20), axis=1)
            
    # Data Moshing Stillness
    if processor.settings["datamosh_still"] > 0 and processor.prev_frame is not None:
        if processor.prev_frame.shape == frame.shape:
            mask = np.random.random((h, w)) < (processor.settings["datamosh_still"] / 100.0)
            processed[mask] = processor.prev_frame[mask]
            
    # Buffer Overrun Look
    if processor.settings["buffer_overrun"] > 0:
        shift = processor.settings["buffer_overrun"] * 10
        flat = processed.flatten()
        flat = np.roll(flat, shift)
        processed = flat.reshape((h, w, 3))
        
    # Corrupted Header Mode
    if processor.settings["corrupted_header"] > 0:
        matrix = np.random.uniform(0.5, 1.5, (3, 3))
        processed = cv2.transform(processed, matrix)
        
    return processed