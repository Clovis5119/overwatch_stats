import plotly.express as px
import pandas as pd


class OverwatchDraw:
    """Draw Overwatch stats, duh."""
    def __init__(self, dataset, stat_type):
        """Initialize!"""
        self.df = pd.DataFrame(dataset)
        self.stat_type = stat_type

    def sort_data_frame(self):
        """..."""
        self.df.sort_values(by=['Hero', 'Player'],
                            key=lambda x: x.str.lower(),
                            inplace=True)
        print(self.df)

    def bar_group(self):
        """TODO: Consider allowing user to do stacked bar graph."""

        fig = px.bar(self.df,
                     x='Player',
                     y=self.stat_type,
                     facet_col='Hero',
                     color='Player',
                     text='X',
                     title=f'Overwatch Stats Comparison - {self.stat_type}',
                     hover_name=self.stat_type,
                     hover_data={'Player': True,
                                 'Hero': False,
                                 'Color': False,
                                 'Games Played': True,
                                 'X': False,
                                 self.stat_type: False},
                     barmode='group',
                     facet_col_wrap=8,
                     )

        for data in fig.data:
            data['width'] = 0.9

        if self.stat_type == 'winPercentage':
            fig.update_yaxes(range=[25, 75])

        fig.show()
