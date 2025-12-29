from PyQt6.QtWidgets import QWidget, QFormLayout

def create_performance_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_surveillance_degradation = parent.create_slider(0, 1, 0)
    layout.addRow("Surveillance Deg", parent.slider_surveillance_degradation)
    
    parent.slider_attention_punisher = parent.create_slider(0, 1, 0)
    layout.addRow("Attention Punisher", parent.slider_attention_punisher)
    
    parent.slider_observer_effect = parent.create_slider(0, 1, 0)
    layout.addRow("Observer Effect", parent.slider_observer_effect)
    
    parent.slider_machine_fatigue = parent.create_slider(0, 1, 0)
    layout.addRow("Machine Fatigue", parent.slider_machine_fatigue)
    
    parent.slider_digital_death = parent.create_slider(0, 1, 0)
    layout.addRow("Digital Death", parent.slider_digital_death)
    
    parent.slider_resurrection_loop = parent.create_slider(0, 1, 0)
    layout.addRow("Resurrection Loop", parent.slider_resurrection_loop)
    
    return tab