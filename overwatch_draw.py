import plotly.graph_objects as go
from plotly.subplots import make_subplots


class OverwatchDraw:
    """Draw Overwatch stats, duh."""
    def __init__(self, main_program):
        """Initialize!"""
        self.heroes = main_program.heroes

    def draw_stats(self, dataset):
        """Prep the type of chart that will be drawn."""

        # Sets the maximum allowed columns in the chart.
        max_cols = 16

        # Draw subplots if there are many different heroes in the chart.
        if (num_heroes := len(self.hero_key)) > 3 and len(tags) > 2:
            rows = int(num_heroes / max_cols) + 1
            cols = int(num_heroes / rows) + 1
            fig = self._get_subplot_fig(dataset, rows, cols)
        else:
            fig = self._get_bargroup_fig(dataset)

        # Update general chart appearance.
        fig.update_layout(
            title=f"{self.user_hero} - {self.key3} (playtime under 3h excluded)",
        )

        # Set the unique scale and ticks for percent-based stats.
        if self.stat_type == 'percent':
            fig.update_yaxes(
                range=[0, 100],
                ticktext=['0%', '25%', '40%', '50%', '60%', '75%', '100%'],
                tickvals=[0, 25, 40, 50, 60, 75, 100],
            )

        # Display the chart and save a dynamic .html to file.
        fig.show()
        fig.write_html(f'charts/{self.key3}.html')

    def _get_bargroup_fig(self, dataset):
        """Draw bar graphs based on the provided dataset."""
        fig = go.Figure()

        for player in dataset:
            fig.add_trace(
                go.Bar(
                    x=list(dataset[player].keys()),
                    y=list(dataset[player].values()),
                    name=player.split('-')[0],
                    meta=player.split('-')[0],
                    hovertemplate=
                    "<b>%{meta}</b>: %{y:,.}<extra></extra>",
                )
            )

        my_layout = {
            'barmode': 'group',
            'bargroupgap': 0.02,
            'bargap': 0.25,
            'legend_title_text': 'Players: ',
            'xaxis': {'title': self.user_hero.title()},
            'yaxis': {'title': self.key3},
        }

        fig.update_layout(my_layout)
        return fig

    def _get_subplot_fig(self, dataset, rows, cols):
        """Description."""

        fig = make_subplots(rows=rows, cols=cols, shared_yaxes=True)

        # Create x-values.
        x_values = []
        [x_values.append(x.split('-')[0]) for x in dataset.keys()]

        row, col = 1, 1
        for h in self.hero_key:
            y_values = []
            [y_values.append(dataset[p].get(h, 0)) for p in dataset.keys()]

            fig.add_trace(
                go.Bar(
                    x=x_values,
                    y=y_values,
                    name=h.title(),
                    marker={
                        'color': self._get_hero_color(h),
                    },
                ),
                row=row,
                col=col,
            )

            fig.update_yaxes(scaleanchor='y')

            if rows > 1 and col == cols and row < rows:
                row += 1
                col = 1
            else:
                col += 1

        my_layout = {
            'legend_title_text': 'Heroes: ',
            'xaxis': {'title': self.user_hero.title()},
            'yaxis': {'title': self.key3},
        }

        fig.update_layout(my_layout)
        return fig