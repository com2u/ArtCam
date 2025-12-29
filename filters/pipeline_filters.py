import cv2
import numpy as np

def apply_pipeline(frame, processor):
    h, w = frame.shape[:2]
    pipeline = processor.settings["pipeline"]
    if pipeline == "Vertical Split":
        left = frame[:, :w//2]
        right = cv2.flip(left, 1)
        return np.hstack((left, right))
    elif pipeline == "Horizontal Split":
        top = frame[:h//2, :]
        bottom = cv2.flip(top, 0)
        return np.vstack((top, bottom))
    elif pipeline == "Quad Mirror":
        top_left = cv2.resize(frame, (w//2, h//2))
        top_right = cv2.flip(top_left, 1)
        bottom_left = cv2.flip(top_left, 0)
        bottom_right = cv2.flip(top_right, 0)
        top = np.hstack((top_left, top_right))
        bottom = np.hstack((bottom_left, bottom_right))
        return np.vstack((top, bottom))
    elif pipeline == "Radial Mirror":
        # Polar mirror effect
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, 180, 1.0)
        rotated = cv2.warpAffine(frame, M, (w, h))
        return cv2.addWeighted(frame, 0.5, rotated, 0.5, 0)
    elif pipeline == "Recursive Grid":
        res = np.zeros_like(frame)
        small = cv2.resize(frame, (w//2, h//2))
        res[:h//2, :w//2] = small
        res[:h//2, w//2:] = cv2.resize(small, (w//2, h//2))
        res[h//2:, :w//2] = cv2.resize(small, (w//2, h//2))
        res[h//2:, w//2:] = cv2.resize(small, (w//2, h//2))
        return res
    elif pipeline == "Time-Shifted Split":
        if len(processor.time_buffer) > 30:
            past = processor.time_buffer[-30]
            res = frame.copy()
            res[:, :w//2] = past[:, :w//2]
            return res
    elif pipeline == "RGB Channel Split":
        b, g, r = cv2.split(frame)
        b = cv2.flip(b, 1)
        g = cv2.flip(g, 0)
        # r is normal
        return cv2.merge([b, g, r])
    elif pipeline == "Infinite Tunnel":
        res = frame.copy()
        for i in range(1, 5):
            scale = 1.0 - (i * 0.2)
            M = cv2.getRotationMatrix2D((w//2, h//2), i * 10, scale)
            warped = cv2.warpAffine(frame, M, (w, h))
            res = cv2.addWeighted(res, 0.7, warped, 0.3, 0)
        return res
    elif pipeline == "Checkerboard Mirror":
        res = frame.copy()
        bs = 64
        for y in range(0, h, bs):
            for x in range(0, w, bs):
                if (x // bs + y // bs) % 2 == 1:
                    res[y:y+bs, x:x+bs] = cv2.flip(frame[y:y+bs, x:x+bs], 1)
        return res
    elif pipeline == "Kaleidoscope 8-way":
        # 8-way symmetry
        p1 = frame[:h//2, :w//2]
        p2 = cv2.flip(p1, 1)
        p3 = cv2.flip(p1, 0)
        p4 = cv2.flip(p2, 0)
        top = np.hstack((p1, p2))
        bottom = np.hstack((p3, p4))
        res = np.vstack((top, bottom))
        transposed = cv2.transpose(res)
        transposed = cv2.resize(transposed, (res.shape[1], res.shape[0]))
        res = cv2.addWeighted(res, 0.5, transposed, 0.5, 0)
        return cv2.resize(res, (w, h))
    elif pipeline == "Scanline Interlace":
        if len(processor.time_buffer) > 10:
            past = processor.time_buffer[-10]
            res = frame.copy()
            res[::2, :] = past[::2, :]
            return res
    elif pipeline == "Glitch Grid":
        res = frame.copy()
        bs = 40
        for y in range(0, h, bs):
            for x in range(0, w, bs):
                if np.random.random() < 0.1:
                    res[y:y+bs, x:x+bs] = np.roll(res[y:y+bs, x:x+bs], np.random.randint(-10, 10), axis=1)
        return res
    elif pipeline == "Vertical Slit Scan":
        if processor.slit_scan_buffer is None or processor.slit_scan_buffer.shape != frame.shape:
            processor.slit_scan_buffer = np.zeros_like(frame)
            processor.slit_scan_pos = 0
        
        center_col = frame[:, w//2]
        processor.slit_scan_buffer[:, processor.slit_scan_pos] = center_col
        processor.slit_scan_pos = (processor.slit_scan_pos + 1) % w
        return processor.slit_scan_buffer
    elif pipeline == "Horizontal Slit Scan":
        if processor.slit_scan_buffer is None or processor.slit_scan_buffer.shape != frame.shape:
            processor.slit_scan_buffer = np.zeros_like(frame)
            processor.slit_scan_pos = 0
        
        center_row = frame[h//2, :]
        processor.slit_scan_buffer[processor.slit_scan_pos, :] = center_row
        processor.slit_scan_pos = (processor.slit_scan_pos + 1) % h
        return processor.slit_scan_buffer
    return frame