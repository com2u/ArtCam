from PyQt6.QtWidgets import QWidget, QFormLayout

def create_time_abuse_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_time_smear = parent.create_slider(0, 100, 0)
    layout.addRow("Time Smear", parent.slider_time_smear)
    
    parent.slider_temp_echo = parent.create_slider(0, 30, 0)
    layout.addRow("Temporal Echo", parent.slider_temp_echo)
    
    parent.slider_time_slice = parent.create_slider(0, 1, 0)
    layout.addRow("Time Slice", parent.slider_time_slice)
    
    parent.slider_reverse_aging = parent.create_slider(0, 1, 0)
    layout.addRow("Reverse Aging", parent.slider_reverse_aging)
    
    parent.slider_freeze_cells = parent.create_slider(0, 100, 0)
    layout.addRow("Freeze Cells", parent.slider_freeze_cells)
    
    parent.slider_memory_burn = parent.create_slider(0, 100, 0)
    layout.addRow("Memory Burn", parent.slider_memory_burn)
    
    parent.slider_temp_feedback = parent.create_slider(0, 100, 0)
    layout.addRow("Temp Feedback", parent.slider_temp_feedback)
    
    parent.slider_time_jitter = parent.create_slider(0, 120, 0)
    layout.addRow("Time Jitter", parent.slider_time_jitter)
    
    parent.slider_slit_scan = parent.create_slider(0, 1, 0)
    layout.addRow("Slit-Scan", parent.slider_slit_scan)
    
    parent.slider_temp_quantize = parent.create_slider(0, 60, 0)
    layout.addRow("Temp Quantize", parent.slider_temp_quantize)
    
    return tab