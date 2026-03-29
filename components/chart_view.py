from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets
import pandas as pd
from src import config
import plotly.graph_objects as go
class ChartView(QtWidgets.QWidget): 
    back_requested_signal = QtCore.Signal()
    def __init__(self):
        super().__init__()
        self.graph = QtWebEngineWidgets.QWebEngineView(self)
        self.player_1_data = None
        self.player_2_data = None
        self.back_btn = QtWidgets.QPushButton("Go back")
        self.back_btn.clicked.connect(self.back_requested_signal.emit)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.back_btn, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.graph)
    def set_chart_data(self, data):
        self.player_1_data = data[0]
        self.player_2_data = data[1]
        cols, scaled_player_1_values, scaled_player_2_values, real_player_1_values, real_player_2_values = self.setup_graph_data()
        self.draw_graph(cols, scaled_player_1_values, scaled_player_2_values, real_player_1_values, real_player_2_values)
    def setup_graph_data(self):
        metrics_to_plot = []
        pos1 = str(self.player_1_data["position"].iloc[0]).strip().upper()
        pos2 = str(self.player_2_data["position"].iloc[0]).strip().upper()
        for group, metrics in config.COMPATIBLE_GROUPS.items():
                if pos1 in group and pos2 in group:
                    metrics_to_plot = list(metrics)
                    break
        metrics_to_plot.remove("minutesPlayed")
        df_for_graph_player_1 = self.player_1_data[metrics_to_plot].copy()
        df_for_graph_player_2 = self.player_2_data[metrics_to_plot].copy()
        for metric in metrics_to_plot:
            if "Percentage" not in metric:
                df_for_graph_player_1[metric] = (float(self.player_1_data[metric]) / float(self.player_1_data["minutesPlayed"])) * 90
                df_for_graph_player_2[metric] = (float(self.player_2_data[metric]) / float(self.player_2_data["minutesPlayed"])) * 90 
        combined_df = pd.concat([df_for_graph_player_1, df_for_graph_player_2])
        max_values = combined_df.max()
        max_values = max_values.replace(0, 1)
        p1_scaled = (df_for_graph_player_1 / max_values) * 100
        p2_scaled = (df_for_graph_player_2 / max_values) * 100
        val_p1 = list(p1_scaled.iloc[0].values)
        val_p1.append(val_p1[0])
        val_p2 = list(p2_scaled.iloc[0].values)
        val_p2.append(val_p2[0])
        metrics_to_plot.append(metrics_to_plot[0])
        raw_p1 = list(df_for_graph_player_1.iloc[0].values)
        raw_p1.append(raw_p1[0])
        raw_p2 = list(df_for_graph_player_2.iloc[0].values)
        raw_p2.append(raw_p2[0])
        return metrics_to_plot, val_p1, val_p2, raw_p1, raw_p2
    def draw_graph(self, cols, scaled_player_1_values, scaled_player_2_values, real_player_1_values, real_player_2_values):
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scaled_player_1_values,
            theta=cols,
            fill='toself',
            name=str(self.player_1_data["player_name"].iloc[0]),
            hovertext=real_player_1_values,
            hoverinfo="text+name"
        ))
        fig.add_trace(go.Scatterpolar(
            r=scaled_player_2_values,
            theta=cols,
            fill='toself',
            name=str(self.player_2_data["player_name"].iloc[0]),
            hovertext=real_player_2_values,
            hoverinfo="text+name"
        ))
        fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 100],
            showticklabels=False
            )),
        showlegend=True
        )
        html_content = fig.to_html(
            include_plotlyjs="https://cdn.plot.ly/plotly-2.15.0.min.js", 
            full_html=True
        )
        self.graph.setHtml(html_content)