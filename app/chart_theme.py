"""
Shared Plotly theming, factored out of views/analytics_dashboard.py so the
new feature-importance chart on the Attendance Predictor page doesn't
duplicate the same theme dict twice.
"""

BG = "#1b1e26"
GRID = "#2a2d36"
TEXT = "#f4f1ea"
TEXT_MUTED = "#8f8f88"

CATEGORY_COLORS = ["#e8a33d", "#2b6f6b", "#8f8f88", "#c97b3d", "#4a7c76", "#6b6b63", "#d8b26a"]
CONTINUOUS_SCALE = [[0, "#332615"], [0.5, "#8a5f1e"], [1, "#e8a33d"]]


def themed(fig, height=None):
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family="Inter, sans-serif", color=TEXT, size=12),
        title=dict(font=dict(family="Oswald, sans-serif", size=16, color=TEXT)),
        legend=dict(font=dict(color=TEXT_MUTED)),
        margin=dict(t=50, l=10, r=10, b=10),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, color=TEXT_MUTED)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, color=TEXT_MUTED)
    if height:
        fig.update_layout(height=height)
    return fig
