from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox

def create_temporal_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_trail = parent.create_slider(0, 10, 0)
    layout.addRow("Motion Trail", parent.slider_trail)
    
    parent.slider_ghost = parent.create_slider(0, 1, 0)
    layout.addRow("Ghosting", parent.slider_ghost)
    
    parent.halftone_combo = QComboBox()
    parent.halftone_combo.addItems(["None", "Dots"])
    parent.halftone_combo.currentTextChanged.connect(parent.update_settings)
    layout.addRow("Halftone", parent.halftone_combo)
    
    parent.geom_combo = QComboBox()
    parent.geom_combo.addItems(["None", "Mosaic", "ASCII"])
    parent.geom_combo.currentTextChanged.connect(parent.update_settings)
    layout.addRow("Geometry", parent.geom_combo)
    
    parent.texture_combo = QComboBox()
    parent.texture_combo.addItems(["None", "Oil", "Watercolor"])
    parent.texture_combo.currentTextChanged.connect(parent.update_settings)
    layout.addRow("Texture", parent.texture_combo)
    
    return tab