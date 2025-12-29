import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QCheckBox, 
                            QSlider, QGroupBox, QFormLayout,
                            QTabWidget, QScrollArea)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

from camera_manager import CameraManager, VirtualCameraManager
from filters import ImageProcessor

from .tabs.basic_tab import create_basic_tab
from .tabs.edge_tab import create_edge_tab
from .tabs.glitch_tab import create_glitch_tab
from .tabs.looks_tab import create_looks_tab
from .tabs.temporal_tab import create_temporal_tab
from .tabs.time_abuse_tab import create_time_abuse_tab
from .tabs.destructive_tab import create_destructive_tab
from .tabs.digital_violence_tab import create_digital_violence_tab
from .tabs.spatial_tab import create_spatial_tab
from .tabs.perception_tab import create_perception_tab
from .tabs.hybrids_tab import create_hybrids_tab
from .tabs.minimalism_tab import create_minimalism_tab
from .tabs.performance_tab import create_performance_tab
from .tabs.gpu_tab import create_gpu_tab

class ArtCamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ArtCam Pro")
        self.camera_manager = CameraManager()
        self.virtual_cam = VirtualCameraManager()
        self.processor = ImageProcessor()
        
        self.init_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left side: Controls (Scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        controls_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll, 1)

        # Camera & Pipeline
        cam_group = QGroupBox("Source & Pipeline")
        cam_layout = QFormLayout()
        self.cam_combo = QComboBox()
        cameras = self.camera_manager.list_cameras()
        for i in cameras:
            self.cam_combo.addItem(f"Camera {i}", i)
        self.cam_combo.currentIndexChanged.connect(self.change_camera)
        cam_layout.addRow("Camera", self.cam_combo)

        self.pipe_combo = QComboBox()
        self.pipe_combo.addItems(["Area Scan", "Vertical Split", "Horizontal Split",
                                  "Quad Mirror", "Radial Mirror", "Recursive Grid",
                                  "Time-Shifted Split", "RGB Channel Split",
                                  "Infinite Tunnel", "Checkerboard Mirror",
                                  "Kaleidoscope 8-way", "Scanline Interlace",
                                  "Glitch Grid", "Vertical Slit Scan",
                                  "Horizontal Slit Scan"])
        self.pipe_combo.currentTextChanged.connect(self.set_pipeline)
        cam_layout.addRow("Pipeline", self.pipe_combo)
        
        self.check_vcam = QCheckBox("Enable Virtual Camera")
        self.check_vcam.stateChanged.connect(self.toggle_vcam)
        cam_layout.addRow(self.check_vcam)
        
        cam_group.setLayout(cam_layout)
        controls_layout.addWidget(cam_group)

        # Tabs for Filters
        self.tabs = QTabWidget()
        controls_layout.addWidget(self.tabs)

        # Add tabs
        self.tabs.addTab(create_basic_tab(self), "Basic")
        self.tabs.addTab(create_edge_tab(self), "Edge/Sketch")
        self.tabs.addTab(create_glitch_tab(self), "Glitch/Opt")
        self.tabs.addTab(create_looks_tab(self), "Looks")
        self.tabs.addTab(create_temporal_tab(self), "Temp/Geom/Tex")
        self.tabs.addTab(create_time_abuse_tab(self), "Time Abuse")
        self.tabs.addTab(create_destructive_tab(self), "Dest Color")
        self.tabs.addTab(create_digital_violence_tab(self), "Digi Violence")
        self.tabs.addTab(create_spatial_tab(self), "Spatial Chaos")
        self.tabs.addTab(create_perception_tab(self), "Perception")
        self.tabs.addTab(create_hybrids_tab(self), "Hybrids")
        self.tabs.addTab(create_minimalism_tab(self), "Minimalism")
        self.tabs.addTab(create_performance_tab(self), "Perf Art")
        self.tabs.addTab(create_gpu_tab(self), "GPU Accel")

        # Right side: Image Display
        self.image_label = QLabel("No Camera Feed")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setStyleSheet("background-color: black; color: white;")
        main_layout.addWidget(self.image_label, 3)

        if cameras:
            self.change_camera(0)

    def create_slider(self, min_val, max_val, start_val):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(start_val)
        slider.valueChanged.connect(self.update_settings)
        return slider

    def change_camera(self, index):
        cam_id = self.cam_combo.currentData()
        if cam_id is not None:
            self.camera_manager.open_camera(cam_id)

    def set_pipeline(self, name):
        self.processor.settings["pipeline"] = name

    def toggle_vcam(self, state):
        if state == Qt.CheckState.Checked.value:
            # Try to start with current frame size
            frame = self.camera_manager.get_frame()
            h, w = frame.shape[:2]
            if not self.virtual_cam.start(w, h):
                self.check_vcam.setChecked(False)
        else:
            self.virtual_cam.stop()

    def update_settings(self):
        s = self.processor.settings
        s["invert"] = self.check_invert.isChecked()
        s["contrast"] = self.slider_contrast.value() / 10.0
        s["saturation"] = self.slider_saturation.value() / 10.0
        s["color_depth"] = self.slider_depth.value()
        
        s["edge_mode"] = self.edge_combo.currentText()
        s["edge_thresh"] = self.slider_edge_thresh.value()
        s["sketch_mode"] = self.sketch_combo.currentText()
        
        s["glitch_rgb_split"] = self.slider_rgb_split.value()
        s["glitch_jitter"] = self.slider_jitter.value()
        s["glitch_block_shift"] = self.slider_block.value()
        s["vhs_noise"] = self.slider_vhs.value()
        
        s["optical_mode"] = self.opt_combo.currentText()
        s["optical_amount"] = self.slider_opt_amt.value()
        
        s["look_mode"] = self.look_combo.currentText()
        s["film_grain"] = self.slider_grain.value()
        s["vignette"] = self.slider_vignette.value()
        s["bloom"] = self.slider_bloom.value()
        
        s["motion_trail"] = self.slider_trail.value()
        s["ghosting"] = self.slider_ghost.value()
        s["halftone_mode"] = self.halftone_combo.currentText()
        s["geometry_mode"] = self.geom_combo.currentText()
        s["texture_mode"] = self.texture_combo.currentText()
        
        s["time_smear"] = self.slider_time_smear.value()
        s["temporal_echo"] = self.slider_temp_echo.value()
        s["time_slice"] = self.slider_time_slice.value()
        s["reverse_aging"] = self.slider_reverse_aging.value()
        s["freeze_cells"] = self.slider_freeze_cells.value()
        s["memory_burn"] = self.slider_memory_burn.value()
        s["temp_feedback"] = self.slider_temp_feedback.value()
        s["time_jitter"] = self.slider_time_jitter.value()
        s["slit_scan"] = self.slider_slit_scan.value()
        s["temp_quantize"] = self.slider_temp_quantize.value()
        
        s["color_collapse"] = self.slider_color_collapse.value()
        s["hue_shatter"] = self.slider_hue_shatter.value()
        s["bit_rot"] = self.slider_bit_rot.value()
        s["palette_decay"] = self.slider_palette_decay.value()
        s["solarize_hell"] = self.slider_solarize_hell.value()
        s["color_bleeding"] = self.slider_color_bleeding.value()
        s["chromatic_meltdown"] = self.slider_chromatic_meltdown.value()
        s["hue_feedback"] = self.slider_hue_feedback.value()
        s["dead_channel"] = self.dead_channel_combo.currentText()
        
        s["comp_artifacts"] = self.slider_comp_artifacts.value()
        s["row_desync"] = self.slider_row_desync.value()
        s["packet_loss"] = self.slider_packet_loss.value()
        s["res_thrashing"] = self.slider_res_thrashing.value()
        s["macroblock_shuffle"] = self.slider_macroblock_shuffle.value()
        s["sync_loss"] = self.slider_sync_loss.value()
        s["datamosh_still"] = self.slider_datamosh_still.value()
        s["buffer_overrun"] = self.slider_buffer_overrun.value()
        s["corrupted_header"] = self.slider_corrupted_header.value()
        
        s["pixel_gravity"] = self.slider_pixel_gravity.value()
        s["reality_tear"] = self.slider_reality_tear.value()
        s["recursive_zoom"] = self.slider_recursive_zoom.value()
        s["voronoi_dest"] = self.slider_voronoi_dest.value()
        s["non_euclidean"] = self.slider_non_euclidean.value()
        s["pixel_erosion"] = self.slider_pixel_erosion.value()
        s["fracture_glass"] = self.slider_fracture_glass.value()
        s["spatial_feedback"] = self.slider_spatial_feedback.value()
        s["folding_space"] = self.slider_folding_space.value()
        
        s["motion_hallucination"] = self.slider_motion_hallucination.value()
        s["impossible_colors"] = self.slider_impossible_colors.value()
        s["edge_overload"] = self.slider_edge_overload.value()
        s["depth_inversion"] = self.slider_depth_inversion.value()
        s["face_ghosting"] = self.slider_face_ghosting.value()
        s["pareidolia_booster"] = self.slider_pareidolia_booster.value()
        s["visual_tinnitus"] = self.slider_visual_tinnitus.value()
        s["afterimage_trap"] = self.slider_afterimage_trap.value()
        
        s["time_delayed_mirrors"] = self.slider_time_delayed_mirrors.value()
        s["motion_fossils"] = self.slider_motion_fossils.value()
        s["temp_blur_field"] = self.slider_temp_blur_field.value()
        s["chrono_pixel_sort"] = self.slider_chrono_pixel_sort.value()
        s["frame_erosion"] = self.slider_frame_erosion.value()
        s["event_horizon"] = self.slider_event_horizon.value()
        s["time_warp_vortex"] = self.slider_time_warp_vortex.value()
        
        s["single_pixel"] = self.slider_single_pixel.value()
        s["average_reality"] = self.slider_average_reality.value()
        s["color_census"] = self.slider_color_census.value()
        s["entropy_maximizer"] = self.slider_entropy_maximizer.value()
        s["camera_amnesia"] = self.slider_camera_amnesia.value()
        s["reality_quantizer"] = self.slider_reality_quantizer.value()
        s["noise_wins"] = self.slider_noise_wins.value()
        
        s["surveillance_degradation"] = self.slider_surveillance_degradation.value()
        s["attention_punisher"] = self.slider_attention_punisher.value()
        s["observer_effect"] = self.slider_observer_effect.value()
        s["machine_fatigue"] = self.slider_machine_fatigue.value()
        s["digital_death"] = self.slider_digital_death.value()
        s["resurrection_loop"] = self.slider_resurrection_loop.value()
        
        s["gpu_blur"] = self.slider_gpu_blur.value()
        s["gpu_canny"] = self.slider_gpu_canny.value()
        s["gpu_bilateral"] = self.slider_gpu_bilateral.value()
        s["gpu_warp"] = self.slider_gpu_warp.value()
        s["gpu_punch"] = self.slider_gpu_punch.value()
        s["gpu_edge_glow"] = self.slider_gpu_edge_glow.value()
        s["gpu_dream"] = self.slider_gpu_dream.value()
        s["gpu_posterize"] = self.slider_gpu_posterize.value()
        s["gpu_chromatic"] = self.slider_gpu_chromatic.value()
        s["gpu_solarize"] = self.slider_gpu_solarize.value()
        s["gpu_ghosting"] = self.slider_gpu_ghosting.value()
        s["gpu_color_cycle"] = self.slider_gpu_color_cycle.value()
        s["gpu_block_glitch"] = self.slider_gpu_block_glitch.value()
        s["gpu_radial_blur"] = self.slider_gpu_radial_blur.value()
        s["gpu_infrared"] = self.slider_gpu_infrared.value()

    def update_frame(self):
        frame = self.camera_manager.get_frame()
        if frame is not None:
            processed = self.processor.process(frame)
            self.display_image(processed)
            if self.check_vcam.isChecked():
                self.virtual_cam.send_frame(processed)

    def display_image(self, img):
        qformat = QImage.Format.Format_RGB888
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        bytes_per_line = ch * w
        qimg = QImage(img.data, w, h, bytes_per_line, qformat)
        self.image_label.setPixmap(QPixmap.fromImage(qimg).scaled(
            self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def closeEvent(self, event):
        self.camera_manager.release()
        self.virtual_cam.stop()
        super().closeEvent(event)