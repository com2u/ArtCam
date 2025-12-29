from PyQt6.QtWidgets import QWidget, QFormLayout

def create_spatial_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_pixel_gravity = parent.create_slider(0, 100, 0)
    layout.addRow("Pixel Gravity", parent.slider_pixel_gravity)
    
    parent.slider_reality_tear = parent.create_slider(0, 100, 0)
    layout.addRow("Reality Tear", parent.slider_reality_tear)
    
    parent.slider_recursive_zoom = parent.create_slider(0, 100, 0)
    layout.addRow("Recursive Zoom", parent.slider_recursive_zoom)
    
    parent.slider_voronoi_dest = parent.create_slider(0, 100, 0)
    layout.addRow("Voronoi Dest", parent.slider_voronoi_dest)
    
    parent.slider_non_euclidean = parent.create_slider(0, 100, 0)
    layout.addRow("Non-Euclidean", parent.slider_non_euclidean)
    
    parent.slider_pixel_erosion = parent.create_slider(0, 10, 0)
    layout.addRow("Pixel Erosion", parent.slider_pixel_erosion)
    
    parent.slider_fracture_glass = parent.create_slider(0, 100, 0)
    layout.addRow("Fracture Glass", parent.slider_fracture_glass)
    
    parent.slider_spatial_feedback = parent.create_slider(0, 1, 0)
    layout.addRow("Spatial Feedback", parent.slider_spatial_feedback)
    
    parent.slider_folding_space = parent.create_slider(0, 10, 0)
    layout.addRow("Folding Space", parent.slider_folding_space)
    
    return tab