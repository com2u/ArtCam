from PyQt6.QtWidgets import QWidget, QFormLayout

def create_gpu_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_gpu_blur = parent.create_slider(0, 50, 0)
    layout.addRow("GPU Blur", parent.slider_gpu_blur)
    
    parent.slider_gpu_canny = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Canny", parent.slider_gpu_canny)
    
    parent.slider_gpu_bilateral = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Bilateral", parent.slider_gpu_bilateral)
    
    parent.slider_gpu_warp = parent.create_slider(0, 100, 0)
    layout.addRow("GPU Warp Speed", parent.slider_gpu_warp)
    
    parent.slider_gpu_punch = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Color Punch", parent.slider_gpu_punch)
    
    parent.slider_gpu_edge_glow = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Edge Glow", parent.slider_gpu_edge_glow)
    
    parent.slider_gpu_dream = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Dream Vision", parent.slider_gpu_dream)
    
    parent.slider_gpu_posterize = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Posterize", parent.slider_gpu_posterize)
    
    parent.slider_gpu_chromatic = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Chromatic", parent.slider_gpu_chromatic)
    
    parent.slider_gpu_solarize = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Solarize", parent.slider_gpu_solarize)
    
    parent.slider_gpu_ghosting = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Ghosting", parent.slider_gpu_ghosting)
    
    parent.slider_gpu_color_cycle = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Color Cycle", parent.slider_gpu_color_cycle)
    
    parent.slider_gpu_block_glitch = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Block Glitch", parent.slider_gpu_block_glitch)
    
    parent.slider_gpu_radial_blur = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Radial Blur", parent.slider_gpu_radial_blur)
    
    parent.slider_gpu_infrared = parent.create_slider(0, 1, 0)
    layout.addRow("GPU Infrared", parent.slider_gpu_infrared)
    
    return tab