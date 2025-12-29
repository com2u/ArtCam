from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox

def create_glitch_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_rgb_split = parent.create_slider(0, 20, 0)
    layout.addRow("RGB Split", parent.slider_rgb_split)
    
    parent.slider_jitter = parent.create_slider(0, 50, 0)
    layout.addRow("Jitter", parent.slider_jitter)
    
    parent.slider_block = parent.create_slider(0, 100, 0)
    layout.addRow("Block Shift", parent.slider_block)
    
    parent.slider_vhs = parent.create_slider(0, 100, 0)
    layout.addRow("VHS Noise", parent.slider_vhs)
    
    parent.opt_combo = QComboBox()
    parent.opt_combo.addItems(["None", "Kaleidoscope", "Swirl", "Mirror Tiles"])
    parent.opt_combo.currentTextChanged.connect(parent.update_settings)
    layout.addRow("Optical Mode", parent.opt_combo)
    
    parent.slider_opt_amt = parent.create_slider(0, 100, 0)
    layout.addRow("Amount", parent.slider_opt_amt)
    
    return tab