import cv2
import numpy as np
import time

from .pipeline_filters import apply_pipeline
from .basic_filters import apply_edges, apply_sketch, apply_halftone, apply_geometry, apply_texture, apply_light, apply_looks
from .glitch_filters import apply_glitch, apply_optical
from .temporal_filters import apply_temporal, apply_temporal_abuse
from .destructive_filters import apply_destructive_color, apply_digital_violence
from .spatial_filters import apply_spatial_chaos
from .perception_filters import apply_perception_weirdness
from .hybrid_filters import apply_hybrids
from .minimalism_filters import apply_minimalism
from .performance_filters import apply_performance_art
from .gpu_filters import apply_gpu_accelerated

class ImageProcessor:
    def __init__(self):
        self.prev_frame = None
        self.motion_history = []
        self.start_time = time.time()
        
        # Filter settings
        self.settings = {
            "pipeline": "Area Scan",
            "invert": False,
            "contrast": 1.0,
            "saturation": 1.0,
            "color_depth": 8,
            "blur": 0,
            "pixelate": 1,
            "average": 0.0,
            
            # Edge/Outline
            "edge_mode": "None", # Canny, Sobel, Neon, Comic Ink
            "edge_thresh": 100,
            
            # Sketch
            "sketch_mode": "None", # Pencil, Charcoal, Stipple
            
            # Halftone
            "halftone_mode": "None", # Dots, Dithering, CMYK
            
            # Glitch
            "glitch_rgb_split": 0,
            "glitch_jitter": 0,
            "glitch_block_shift": 0,
            "vhs_noise": 0,
            
            # Optical
            "optical_mode": "None", # Kaleidoscope, Mirror, Swirl, Pinch/Bulge
            "optical_amount": 0,
            
            # Color Looks
            "look_mode": "None", # Duotone, Sepia, Cyberpunk
            "film_grain": 0,
            
            # Light & Depth
            "vignette": 0,
            "bloom": 0,
            
            # Temporal
            "motion_trail": 0,
            "ghosting": 0,
            "time_smear": 0,
            "temporal_echo": 0,
            "time_slice": 0,
            "reverse_aging": 0,
            "freeze_cells": 0,
            "memory_burn": 0,
            "temp_feedback": 0,
            "time_jitter": 0,
            "slit_scan": 0,
            "temp_quantize": 0,
            
            # Destructive Color
            "color_collapse": 0,
            "hue_shatter": 0,
            "bit_rot": 0,
            "palette_decay": 0,
            "solarize_hell": 0,
            "color_bleeding": 0,
            "chromatic_meltdown": 0,
            "hue_feedback": 0,
            "dead_channel": "None", # None, Red, Green, Blue
            
            # Glitch & Digital Violence
            "comp_artifacts": 0,
            "row_desync": 0,
            "packet_loss": 0,
            "res_thrashing": 0,
            "macroblock_shuffle": 0,
            "sync_loss": 0,
            "datamosh_still": 0,
            "buffer_overrun": 0,
            "corrupted_header": 0,
            
            # Spatial & Geometric Chaos
            "pixel_gravity": 0,
            "reality_tear": 0,
            "recursive_zoom": 0,
            "voronoi_dest": 0,
            "non_euclidean": 0,
            "pixel_erosion": 0,
            "fracture_glass": 0,
            "spatial_feedback": 0,
            "folding_space": 0,
            
            # Perception & Cognitive Weirdness
            "motion_hallucination": 0,
            "impossible_colors": 0,
            "edge_overload": 0,
            "depth_inversion": 0,
            "face_ghosting": 0,
            "pareidolia_booster": 0,
            "visual_tinnitus": 0,
            "afterimage_trap": 0,
            
            # Temporal + Spatial Hybrids
            "time_delayed_mirrors": 0,
            "motion_fossils": 0,
            "temp_blur_field": 0,
            "chrono_pixel_sort": 0,
            "frame_erosion": 0,
            "event_horizon": 0,
            "time_warp_vortex": 0,
            
            # Extreme Minimalism / Conceptual
            "single_pixel": 0,
            "average_reality": 0,
            "color_census": 0,
            "entropy_maximizer": 0,
            "camera_amnesia": 0,
            "reality_quantizer": 0,
            "noise_wins": 0,
            
            # Performance-Art / Statement
            "surveillance_degradation": 0,
            "attention_punisher": 0,
            "observer_effect": 0,
            "machine_fatigue": 0,
            "digital_death": 0,
            "resurrection_loop": 0,
            
            # GPU Accelerated (OpenCL)
            "gpu_blur": 0,
            "gpu_canny": 0,
            "gpu_bilateral": 0,
            "gpu_warp": 0,
            "gpu_punch": 0,
            "gpu_edge_glow": 0,
            "gpu_dream": 0,
            "gpu_posterize": 0,
            "gpu_chromatic": 0,
            "gpu_solarize": 0,
            "gpu_ghosting": 0,
            "gpu_color_cycle": 0,
            "gpu_block_glitch": 0,
            "gpu_radial_blur": 0,
            "gpu_infrared": 0,
            
            # Geometry
            "geometry_mode": "None", # Mosaic, ASCII
            
            # Texture
            "texture_mode": "None" # Canvas, Watercolor, Oil
        }

        # State for temporal filters
        self.time_buffer = []
        self.max_buffer_size = 120 # ~2 seconds at 60fps
        self.burn_in_buffer = None
        self.frozen_cells = None
        self.frozen_mask = None
        self.feedback_buffer = None
        self.smear_buffer = None
        self.quantized_frame = None
        self.frame_count = 0
        self.palette_mask = None
        self.hue_offset = 0
        self.gravity_buffer = None
        self.voronoi_points = None
        self.fracture_shards = None
        self.spatial_feedback_buffer = None
        self.fossil_buffer = None
        self.pixel_age_map = None
        self.event_horizon_mask = None
        self.average_reality_buffer = None
        self.amnesia_timer = time.time()
        self.session_start_time = time.time()
        self.death_buffer = None
        self.slit_scan_buffer = None
        self.slit_scan_pos = 0
        self.gpu_ghost_buffer = None
        self.gpu_hue_offset = 0

    def process(self, frame):
        # Pipeline
        frame = apply_pipeline(frame, self)
        
        # Temporal
        frame = apply_temporal(frame, self)
        
        # Temporal Abuse
        frame = apply_temporal_abuse(frame, self)
        
        # Destructive Color
        frame = apply_destructive_color(frame, self)
        
        # Digital Violence
        frame = apply_digital_violence(frame, self)
        
        # Spatial Chaos
        frame = apply_spatial_chaos(frame, self)
        
        # Perception Weirdness
        frame = apply_perception_weirdness(frame, self)
        
        # Hybrids
        frame = apply_hybrids(frame, self)
        
        # Minimalism
        frame = apply_minimalism(frame, self)
        
        # Performance Art
        frame = apply_performance_art(frame, self)
        
        # GPU Accelerated
        frame = apply_gpu_accelerated(frame, self)
        
        # Optical
        frame = apply_optical(frame, self)
        
        # Glitch
        frame = apply_glitch(frame, self)
        
        # Edges
        frame = apply_edges(frame, self)
        
        # Sketch
        frame = apply_sketch(frame, self)
        
        # Halftone
        frame = apply_halftone(frame, self)
        
        # Geometry
        frame = apply_geometry(frame, self)
        
        # Looks
        frame = apply_looks(frame, self)
        
        # Light
        frame = apply_light(frame, self)
        
        # Texture
        frame = apply_texture(frame, self)
        
        # Basic Filters (from before)
        if self.settings["invert"]:
            frame = cv2.bitwise_not(frame)
            
        if self.settings["contrast"] != 1.0 or self.settings["saturation"] != 1.0:
            hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS).astype(np.float32)
            hls[:, :, 1] *= self.settings["contrast"]
            hls[:, :, 2] *= self.settings["saturation"]
            hls = np.clip(hls, 0, 255).astype(np.uint8)
            frame = cv2.cvtColor(hls, cv2.COLOR_HLS2BGR)
            
        if self.settings["blur"] > 0:
            k = self.settings["blur"] * 2 + 1
            frame = cv2.GaussianBlur(frame, (k, k), 0)
            
        if self.settings["pixelate"] > 1:
            h, w = frame.shape[:2]
            p = self.settings["pixelate"]
            small = cv2.resize(frame, (max(1, w//p), max(1, h//p)), interpolation=cv2.INTER_LINEAR)
            frame = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

        self.prev_frame = frame.copy()
        return frame