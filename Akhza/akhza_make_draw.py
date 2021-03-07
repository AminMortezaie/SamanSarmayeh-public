import plotly.graph_objects as go
from akhza_analyze_class import Analyze


class MakeDraw:
    def __init__(self):
        self.analyze = Analyze()

    def make_draw(self, arr):
        pass

    def plotter(self, xArray, yArray, xLabel='x', yLabel='y', title='draw'):
        fig = go.Figure()
        # Create and style traces
        fig.add_trace(go.Scatter(x=xArray, y=yArray, name='name',
                                 line=dict(width=4)))
        fig.update_layout(title=title,
                          xaxis_title=xLabel,
                          yaxis_title=yLabel)
        fig.show()

    def plot_with_variety(self):
        self.plotter(self.analyze.find_variety()[
                     1], self.analyze.find_variety()[0], title=' YTM نمودار فراوانی دیتا بر حسب  ')


obj = MakeDraw()
obj.plot_with_variety()
