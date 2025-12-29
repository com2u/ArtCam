from PyQt6.QtWidgets import QWidget, QFormLayout

def create_hybrids_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_time_delayed_mirrors = parent.create_slider(0, 1, 0)
    layout.addRow("Time-Delayed Mirrors", parent.slider_time_delayed_mirrors)
    
    parent.slider_motion_fossils = parent.create_slider(0, 1, 0)
    layout.addRow("Motion Fossils", parent.slider_motion_fossils)
    
    parent.slider_temp_blur_field = parent.create_slider(0, 1, 0)
    layout.addRow("Temporal Blur Field", parent.slider_temp_blur_field)
    
    parent.slider_chrono_pixel_sort = parent.create_slider(0, 1, 0)
    layout.addRow("Chrono-Pixel Sort", parent.slider_chrono_pixel_sort)
    
    parent.slider_frame_erosion = parent.create_slider(0, 100, 0)
    layout.addRow("Frame Erosion", parent.slider_frame_erosion)
    
    parent.slider_event_horizon = parent.create_slider(0, 1, 0)
    layout.addRow("Event Horizon", parent.slider_event_horizon)
    
    parent.slider_time_warp_vortex = parent.create_slider(0, 100, 0)
    layout.addRow("Time-Warp Vortex", parent.slider_time_warp_vortex)
    
    return tab