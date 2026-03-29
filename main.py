from src import data_cleaner, data_scraper, config
from PySide2.QtWidgets import QApplication
from components.main_window import MainWindow
import asyncio
from qt_material import apply_stylesheet
import os
import sys
def main():
    if not os.path.exists(config.PLAYERS_DATA_PATH):
        df = asyncio.run(data_scraper.download_all_leagues_fast())    
        data_scraper.save_to_csv(df)
        df_players = data_cleaner.get_data_csv(config.PLAYERS_DATA_PATH)
        df = data_cleaner.repair(df_players)
        data_cleaner.change_positions(df)    
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    main_window = MainWindow()
    main_window.setWindowTitle("Player comparison")
    main_window.resize(1900,1000)
    main_window.show()
    sys.exit(app.exec_())


if __name__ =="__main__":
    main()