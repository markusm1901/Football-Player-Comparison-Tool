from PySide2 import QtCore, QtWidgets
from components.player_view import PlayersView
import pandas as pd 
from src import config

class PlayerSelection(QtWidgets.QWidget): 
    generate_requested_signal = QtCore.Signal(object)
    selected_player_signal = QtCore.Signal(int, pd.DataFrame)
    def __init__(self):
        super().__init__()
        self.player_view_1 = PlayersView(1)
        self.player_view_2 = PlayersView(2)
        self.players_data = [None, None]
        self.generate_chart_button = QtWidgets.QPushButton("GENERATE GRAPH")
        self.generate_chart_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.generate_chart_button.setFixedHeight(50) 
        self.generate_chart_button.setEnabled(False)
        
        self.player_view_1.player_selected_signal.connect(self.on_player_selected)
        self.player_view_2.player_selected_signal.connect(self.on_player_selected)
        self.generate_chart_button.clicked.connect(self.on_generate_clicked)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40) 
        self.layout.setSpacing(30)         
        self.inner_layout = QtWidgets.QHBoxLayout() 
        self.inner_layout.setSpacing(50)
        
        self.inner_layout.addWidget(self.player_view_1)
        self.inner_layout.addWidget(self.player_view_2)
        
        self.layout.addLayout(self.inner_layout)
        self.layout.addWidget(self.generate_chart_button, alignment=QtCore.Qt.AlignCenter)

    def on_player_selected(self, panel_id, df_player):
        if panel_id == 1:
            self.players_data[0] = df_player
        elif panel_id == 2:
            self.players_data[1] = df_player
        if self.players_data[0] is not None and self.players_data[1] is not None:
                    
                    pos1 = str(self.players_data[0]["position"].iloc[0]).strip().upper()
                    pos2 = str(self.players_data[1]["position"].iloc[0]).strip().upper()
                    idx1 = self.players_data[0].index[0]
                    self.players_data[0].loc[idx1, "position"] = pos1
                    idx2 = self.players_data[1].index[0]
                    self.players_data[1].loc[idx2, "position"] = pos2
                    is_compatible = False
                    for group in config.COMPATIBLE_GROUPS.keys():
                        if pos1 in group and pos2 in group:
                            is_compatible = True
                            break 
                    self.generate_chart_button.setEnabled(is_compatible)
    def on_generate_clicked(self):
        self.generate_requested_signal.emit(self.players_data)