from PyQt6.QtWidgets import QWidget, QFormLayout

def create_perception_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_motion_hallucination = parent.create_slider(0, 1, 0)
    layout.addRow("Motion Hallucination", parent.slider_motion_hallucination)
    
    parent.slider_impossible_colors = parent.create_slider(0, 1, 0)
    layout.addRow("Impossible Colors", parent.slider_impossible_colors)
    
    parent.slider_edge_overload = parent.create_slider(0, 10, 0)
    layout.addRow("Edge Overload", parent.slider_edge_overload)
    
    parent.slider_depth_inversion = parent.create_slider(0, 1, 0)
    layout.addRow("Depth Inversion", parent.slider_depth_inversion)
    
    parent.slider_face_ghosting = parent.create_slider(0, 1, 0)
    layout.addRow("Face Ghosting", parent.slider_face_ghosting)
    
    parent.slider_pareidolia_booster = parent.create_slider(0, 1, 0)
    layout.addRow("Pareidolia Booster", parent.slider_pareidolia_booster)
    
    parent.slider_visual_tinnitus = parent.create_slider(0, 100, 0)
    layout.addRow("Visual Tinnitus", parent.slider_visual_tinnitus)
    
    parent.slider_afterimage_trap = parent.create_slider(0, 1, 0)
    layout.addRow("Afterimage Trap", parent.slider_afterimage_trap)
    
    return tab