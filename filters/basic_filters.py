import cv2
import numpy as np

def apply_edges(frame, processor):
    mode = processor.settings["edge_mode"]
    if mode == "None": return frame
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if mode == "Canny":
        edges = cv2.Canny(gray, processor.settings["edge_thresh"], processor.settings["edge_thresh"]*2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif mode == "Sobel":
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        mag = np.sqrt(sobelx**2 + sobely**2)
        mag = np.uint8(np.clip(mag, 0, 255))
        return cv2.cvtColor(mag, cv2.COLOR_GRAY2BGR)
    elif mode == "Neon":
        edges = cv2.Canny(gray, processor.settings["edge_thresh"], processor.settings["edge_thresh"]*2)
        edges = cv2.dilate(edges, None)
        neon = np.zeros_like(frame)
        neon[edges > 0] = [255, 0, 255] # Magenta neon
        return cv2.addWeighted(frame, 0.5, neon, 0.5, 0)
    elif mode == "Comic Ink":
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        return cv2.bitwise_and(color, color, mask=edges)
    return frame

def apply_sketch(frame, processor):
    mode = processor.settings["sketch_mode"]
    if mode == "None": return frame
    
    if mode == "Pencil":
        gray, sketch = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif mode == "Charcoal":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inverted = 255 - gray
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blurred, scale=256)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    return frame

def apply_halftone(frame, processor):
    mode = processor.settings["halftone_mode"]
    if mode == "None": return frame
    h, w = frame.shape[:2]
    
    if mode == "Dots":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = np.full((h, w, 3), 255, dtype=np.uint8)
        step = 10
        for y in range(0, h, step):
            for x in range(0, w, step):
                roi = gray[y:y+step, x:x+step]
                avg = np.mean(roi)
                radius = int((255 - avg) / 255 * (step / 2))
                if radius > 0:
                    cv2.circle(res, (x + step//2, y + step//2), radius, (0, 0, 0), -1)
        return res
    return frame

def apply_geometry(frame, processor):
    mode = processor.settings["geometry_mode"]
    if mode == "None": return frame
    h, w = frame.shape[:2]
    
    if mode == "Mosaic":
        p = 20
        res = frame.copy()
        for y in range(0, h, p):
            for x in range(0, w, p):
                color = np.mean(frame[y:y+p, x:x+p], axis=(0, 1))
                cv2.rectangle(res, (x, y), (x+p, y+p), color, -1)
                cv2.rectangle(res, (x, y), (x+p, y+p), (0, 0, 0), 1)
        return res
    elif mode == "ASCII":
        chars = "@%#*+=-:. "
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (w//10, h//10))
        res = np.zeros((h, w, 3), dtype=np.uint8)
        for y in range(small.shape[0]):
            for x in range(small.shape[1]):
                char = chars[int(small[y, x] / 256 * len(chars))]
                cv2.putText(res, char, (x*10, y*10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        return res
    return frame

def apply_texture(frame, processor):
    mode = processor.settings["texture_mode"]
    if mode == "None": return frame
    
    if mode == "Oil":
        return cv2.xphoto.oilPainting(frame, 7, 1) if hasattr(cv2, 'xphoto') else cv2.stylization(frame, sigma_s=60, sigma_r=0.07)
    elif mode == "Watercolor":
        return cv2.stylization(frame, sigma_s=60, sigma_r=0.45)
    return frame

def apply_light(frame, processor):
    processed = frame.copy()
    h, w = frame.shape[:2]
    
    if processor.settings["vignette"] > 0:
        kernel_x = cv2.getGaussianKernel(w, w/2)
        kernel_y = cv2.getGaussianKernel(h, h/2)
        kernel = kernel_y * kernel_x.T
        mask = kernel / kernel.max()
        vignette = np.copy(processed)
        for i in range(3):
            vignette[:,:,i] = vignette[:,:,i] * mask
        processed = cv2.addWeighted(processed, 1 - processor.settings["vignette"]/100, vignette, processor.settings["vignette"]/100, 0)
        
    if processor.settings["bloom"] > 0:
        mask = cv2.threshold(cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY), 200, 255, cv2.THRESH_BINARY)[1]
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        bloom = cv2.GaussianBlur(mask, (25, 25), 0)
        processed = cv2.addWeighted(processed, 1, bloom, processor.settings["bloom"]/100, 0)
        
    return processed

def apply_looks(frame, processor):
    mode = processor.settings["look_mode"]
    processed = frame.copy()
    
    if mode == "Sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        processed = cv2.transform(processed, kernel)
    elif mode == "Cyberpunk":
        hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:,:,1] *= 1.5
        processed = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        b, g, r = cv2.split(processed)
        r = cv2.add(r, 50)
        b = cv2.add(b, 30)
        processed = cv2.merge([b, g, r])
    elif mode == "Duotone":
        gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        processed = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        
    if processor.settings["film_grain"] > 0:
        noise = np.random.normal(0, processor.settings["film_grain"], frame.shape).astype(np.uint8)
        processed = cv2.add(processed, noise)
        
    return processed