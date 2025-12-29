from PyQt6.QtWidgets import QWidget, QFormLayout

def create_digital_violence_tab(parent):
    tab = QWidget()
    layout = QFormLayout(tab)
    
    parent.slider_comp_artifacts = parent.create_slider(0, 100, 0)
    layout.addRow("Comp Artifacts", parent.slider_comp_artifacts)
    
    parent.slider_row_desync = parent.create_slider(0, 100, 0)
    layout.addRow("Row Desync", parent.slider_row_desync)
    
    parent.slider_packet_loss = parent.create_slider(0, 100, 0)
    layout.addRow("Packet Loss", parent.slider_packet_loss)
    
    parent.slider_res_thrashing = parent.create_slider(0, 1, 0)
    layout.addRow("Res Thrashing", parent.slider_res_thrashing)
    
    parent.slider_macroblock_shuffle = parent.create_slider(0, 1, 0)
    layout.addRow("Macroblock Shuffle", parent.slider_macroblock_shuffle)
    
    parent.slider_sync_loss = parent.create_slider(0, 1, 0)
    layout.addRow("Sync Loss", parent.slider_sync_loss)
    
    parent.slider_datamosh_still = parent.create_slider(0, 100, 0)
    layout.addRow("Datamosh Still", parent.slider_datamosh_still)
    
    parent.slider_buffer_overrun = parent.create_slider(0, 100, 0)
    layout.addRow("Buffer Overrun", parent.slider_buffer_overrun)
    
    parent.slider_corrupted_header = parent.create_slider(0, 1, 0)
    layout.addRow("Corrupted Header", parent.slider_corrupted_header)
    
    return tab