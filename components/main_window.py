from PySide2 import QtWidgets
from components.select_player_view import PlayerSelection
from components.chart_view import ChartView

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.resize(1400, 900)
        self.setWindowTitle("DataMB Clone - Football Analytics")
        self.widget_manager = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.widget_manager)
        self.select_player_view = PlayerSelection()
        self.chart_view = ChartView()
        self.widget_manager.addWidget(self.select_player_view)
        self.widget_manager.addWidget(self.chart_view)
        self.select_player_view.generate_requested_signal.connect(self.on_generate_chart_clicked)
        self.chart_view.back_requested_signal.connect(self.show_selection_page)
        
    def on_generate_chart_clicked(self):
        self.chart_view.set_chart_data(self.select_player_view.players_data)
        self.widget_manager.setCurrentIndex(1)
        
    def show_selection_page(self):
        self.widget_manager.setCurrentIndex(0)