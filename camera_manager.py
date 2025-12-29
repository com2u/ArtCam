import cv2
import numpy as np
try:
    import pyvirtualcam
except ImportError:
    pyvirtualcam = None

class CameraManager:
    def __init__(self):
        self.cap = None

    @staticmethod
    def list_cameras(max_to_test=5):
        available_cameras = []
        for i in range(max_to_test):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras

    def open_camera(self, index):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(index)
        return self.cap.isOpened()

    def get_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        
        # Fallback: Generate a test pattern if no camera is available
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(test_frame, "No Camera Feed - Test Pattern", (50, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # Add some moving element to see filters like 'average'
        import time
        t = time.time()
        x = int(320 + 200 * np.cos(t))
        y = int(240 + 150 * np.sin(t))
        cv2.circle(test_frame, (x, y), 50, (0, 255, 0), -1)
        return test_frame

    def release(self):
        if self.cap is not None:
            self.cap.release()

class VirtualCameraManager:
    def __init__(self):
        self.cam = None
        self.width = 0
        self.height = 0

    def start(self, width, height, fps=30):
        if pyvirtualcam is None:
            print("pyvirtualcam not installed. Virtual camera disabled.")
            return False
        
        try:
            self.cam = pyvirtualcam.Camera(width=width, height=height, fps=fps)
            self.width = width
            self.height = height
            print(f"Virtual camera started: {self.cam.device}")
            return True
        except Exception as e:
            print(f"Failed to start virtual camera: {e}")
            return False

    def send_frame(self, frame):
        if self.cam is not None:
            # pyvirtualcam expects RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if frame_rgb.shape[1] != self.width or frame_rgb.shape[0] != self.height:
                frame_rgb = cv2.resize(frame_rgb, (self.width, self.height))
            self.cam.send(frame_rgb)
            self.cam.sleep_until_next_frame()

    def stop(self):
        if self.cam is not None:
            self.cam.close()
            self.cam = None
