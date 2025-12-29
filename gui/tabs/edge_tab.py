from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox

def create_edge_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.edge_combo = QComboBox()
    parent.edge_combo.addItems(["None", "Canny", "Sobel", "Neon", "Comic Ink"])
    parent.edge_combo.currentTextChanged.connect(parent.update_settings)
    layout.addRow("Edge Mode", parent.edge_combo)
    
    parent.slider_edge_thresh = parent.create_slider(10, 250, 100)
    layout.addRow("Threshold", parent.slider_edge_thresh)
    
    parent.sketch_combo = QComboBox()
    parent.sketch_combo.addItems(["None", "Pencil", "Charcoal"])
    parent.sketch_combo.currentTextChanged.connect(parent.update_settings)
    layout.addRow("Sketch Mode", parent.sketch_combo)
    
    return tab