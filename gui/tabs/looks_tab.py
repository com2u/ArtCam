from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox

def create_looks_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.look_combo = QComboBox()
    parent.look_combo.addItems(["None", "Sepia", "Cyberpunk", "Duotone"])
    parent.look_combo.currentTextChanged.connect(parent.update_settings)
    layout.addRow("Look", parent.look_combo)
    
    parent.slider_grain = parent.create_slider(0, 50, 0)
    layout.addRow("Film Grain", parent.slider_grain)
    
    parent.slider_vignette = parent.create_slider(0, 100, 0)
    layout.addRow("Vignette", parent.slider_vignette)
    
    parent.slider_bloom = parent.create_slider(0, 100, 0)
    layout.addRow("Bloom", parent.slider_bloom)
    
    return tab