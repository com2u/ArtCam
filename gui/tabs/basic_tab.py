from PyQt6.QtWidgets import QWidget, QFormLayout, QCheckBox

def create_basic_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.check_invert = QCheckBox("Invert")
    parent.check_invert.stateChanged.connect(parent.update_settings)
    layout.addRow(parent.check_invert)
    
    parent.slider_contrast = parent.create_slider(5, 30, 10)
    layout.addRow("Contrast", parent.slider_contrast)
    
    parent.slider_saturation = parent.create_slider(0, 30, 10)
    layout.addRow("Saturation", parent.slider_saturation)
    
    parent.slider_depth = parent.create_slider(1, 8, 8)
    layout.addRow("Color Depth", parent.slider_depth)
    
    return tab