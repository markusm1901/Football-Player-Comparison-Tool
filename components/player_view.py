from PySide2 import QtCore, QtWidgets
from PySide2.QtGui import QStandardItemModel
from src import data_cleaner, config
class PlayersView(QtWidgets.QWidget): 
    player_selected_signal = QtCore.Signal(int, object)
    def __init__(self, id: int):
        super().__init__()
        self.id = id
        self.df_full = data_cleaner.get_data_csv(config.PLAYERS_DATA_PATH)
        self.cols = ['player_name','age','league','team','country','position']
        self.df_displayed = self.df_full[self.cols]
        self.selected_player = None

        self.name_filter = QtWidgets.QLineEdit()
        self.name_filter.setPlaceholderText("Player's name")
        self.league_filter = QtWidgets.QComboBox()
        self.league_filter.addItems(config.DISPLAY_LEAGUES)

        self.position_filter = QtWidgets.QComboBox()
        unique_positions = ['All (Position)'] + self.df_displayed['position'].drop_duplicates().tolist()
        remove_values = ["Defender","Midfielder","Forward", "Midfield"]
        unique_positions = [pos for pos in unique_positions if pos not in remove_values]
        self.position_filter.addItems(unique_positions)

        self.country_filter = QtWidgets.QComboBox()
        self.countries = ['All (Country)'] + self.df_displayed['country'].drop_duplicates().tolist()
        self.country_filter.addItems(self.countries)

        self.model = QStandardItemModel(len(self.df_displayed),len(self.cols))
        self.model.setHorizontalHeaderLabels(["Player","Age","League", "Team",'Country',"Position"])

        self.player_list = QtWidgets.QTableView()
        self.player_list.setModel(self.model)
        data_cleaner.fill_Qtableview(self.df_displayed,self.cols,config.DISPLAY_LEAGUES,self.model)
        self.player_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.player_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.player_list.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.player_list.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.player_list.verticalHeader().setVisible(False)
        self.player_list.setAlternatingRowColors(True)
        self.player_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.player_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.name_filter)
        self.layout.addWidget(self.league_filter)
        self.layout.addWidget(self.country_filter)
        self.layout.addWidget(self.position_filter)
        self.layout.addWidget(self.player_list)

        self.name_filter.textChanged.connect(self.apply_filters)
        self.league_filter.currentIndexChanged.connect(self.apply_filters)
        self.position_filter.currentIndexChanged.connect(self.apply_filters)
        self.country_filter.currentIndexChanged.connect(self.apply_filters)
        self.player_list.selectionModel().selectionChanged.connect(self.selected_row)
    def apply_filters(self, *args):
        df_current = self.df_displayed
        if self.name_filter.text() != "":
            df_current = df_current[df_current["player_name"].str.contains(self.name_filter.text(), case=False, na = False)]
        if self.position_filter.currentText() != "All (Position)":
            df_current = df_current[df_current["position"].str.contains(self.position_filter.currentText().split('-')[0].strip(), case=False, na=False)]
        if self.league_filter.currentText() != "All":
            df_current = df_current[df_current["league"].str.contains(self.league_filter.currentText())]
        if self.country_filter.currentText() != "All (Country)":
            df_current = df_current[df_current["country"].str.contains(self.country_filter.currentText())]

        data_cleaner.fill_Qtableview(df_current,self.cols,config.DISPLAY_LEAGUES,self.model)
    def selected_row(self, *args):
        if self.player_list.selectionModel().selectedRows()[0].row() is not None:
            player_row = self.player_list.selectionModel().selectedRows()[0].row()
            self.selected_player = self.df_full[self.df_full["player_name"] == self.model.item(player_row, 0).text()]
            self.player_selected_signal.emit(self.id, self.selected_player)
    