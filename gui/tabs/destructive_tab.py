from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox

def create_destructive_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_color_collapse = parent.create_slider(0, 100, 0)
    layout.addRow("Color Collapse", parent.slider_color_collapse)
    
    parent.slider_hue_shatter = parent.create_slider(0, 36, 0)
    layout.addRow("Hue Shatter", parent.slider_hue_shatter)
    
    parent.slider_bit_rot = parent.create_slider(0, 100, 0)
    layout.addRow("Bit-Rot", parent.slider_bit_rot)
    
    parent.slider_palette_decay = parent.create_slider(0, 100, 0)
    layout.addRow("Palette Decay", parent.slider_palette_decay)
    
    parent.slider_solarize_hell = parent.create_slider(0, 100, 0)
    layout.addRow("Solarize Hell", parent.slider_solarize_hell)
    
    parent.slider_color_bleeding = parent.create_slider(0, 100, 0)
    layout.addRow("Color Bleeding", parent.slider_color_bleeding)
    
    parent.slider_chromatic_meltdown = parent.create_slider(0, 100, 0)
    layout.addRow("Chromatic Meltdown", parent.slider_chromatic_meltdown)
    
    parent.slider_hue_feedback = parent.create_slider(0, 100, 0)
    layout.addRow("Hue Feedback", parent.slider_hue_feedback)
    
    parent.dead_channel_combo = QComboBox()
    parent.dead_channel_combo.addItems(["None", "Red", "Green", "Blue"])
    parent.dead_channel_combo.currentTextChanged.connect(parent.update_settings)
    layout.addRow("Dead Channel", parent.dead_channel_combo)
    
    return tab