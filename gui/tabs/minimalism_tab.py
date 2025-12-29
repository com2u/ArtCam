from PyQt6.QtWidgets import QWidget, QFormLayout

def create_minimalism_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_single_pixel = parent.create_slider(0, 1, 0)
    layout.addRow("Single Pixel World", parent.slider_single_pixel)
    
    parent.slider_average_reality = parent.create_slider(0, 1, 0)
    layout.addRow("Average Reality", parent.slider_average_reality)
    
    parent.slider_color_census = parent.create_slider(0, 1, 0)
    layout.addRow("Color Census", parent.slider_color_census)
    
    parent.slider_entropy_maximizer = parent.create_slider(0, 1, 0)
    layout.addRow("Entropy Maximizer", parent.slider_entropy_maximizer)
    
    parent.slider_camera_amnesia = parent.create_slider(0, 60, 0)
    layout.addRow("Camera Amnesia", parent.slider_camera_amnesia)
    
    parent.slider_reality_quantizer = parent.create_slider(0, 1, 0)
    layout.addRow("Reality Quantizer", parent.slider_reality_quantizer)
    
    parent.slider_noise_wins = parent.create_slider(0, 1, 0)
    layout.addRow("Noise Wins", parent.slider_noise_wins)
    
    return tab