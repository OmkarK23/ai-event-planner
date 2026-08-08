import plotly.express as px
import streamlit as st

# Plotly theme matched to the app's token system (styles.py) instead of the
# default plotly_dark rainbow palette, which clashed against the ink/amber design.
BG = "#1b1e26"
GRID = "#2a2d36"
TEXT = "#f4f1ea"
TEXT_MUTED = "#8f8f88"

# Amber/teal/gray family instead of plotly's default categorical rainbow, so
# charts read as part of the same system as the rest of the app.
CATEGORY_COLORS = ["#e8a33d", "#2b6f6b", "#8f8f88", "#c97b3d", "#4a7c76", "#6b6b63", "#d8b26a"]

CONTINUOUS_SCALE = [[0, "#332615"], [0.5, "#8a5f1e"], [1, "#e8a33d"]]


def _themed(fig):
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
    return fig


def render(df):
    st.header("Event analytics dashboard")

    st.subheader("Dashboard filters")

    colf1, colf2 = st.columns(2)

    with colf1:
        selected_event = st.selectbox(
            "Filter by event type", ["All"] + sorted(df["event_type"].unique().tolist())
        )

    with colf2:
        selected_promo = st.selectbox(
            "Filter by promotion", ["All"] + sorted(df["promotion_channel"].unique().tolist())
        )

    filtered_df = df.copy()

    if selected_event != "All":
        filtered_df = filtered_df[filtered_df["event_type"] == selected_event]

    if selected_promo != "All":
        filtered_df = filtered_df[filtered_df["promotion_channel"] == selected_promo]

    st.markdown("---")

    total_events = len(filtered_df)
    avg_attendance = int(filtered_df["actual_attendance"].mean())
    avg_budget = int(filtered_df["budget"].mean())
    avg_feedback = round(filtered_df["feedback_score"].mean(), 2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total events", total_events)
    col2.metric("Avg attendance", avg_attendance)
    col3.metric("Avg budget", f"${avg_budget}")
    col4.metric("Avg feedback", avg_feedback)

    st.markdown("---")

    st.subheader("Event insights")

    best_event = filtered_df.groupby("event_type")["actual_attendance"].mean().idxmax()
    best_promo = filtered_df.groupby("promotion_channel")["actual_attendance"].mean().idxmax()

    st.success(f"Highest average attendance comes from: **{best_event}** events.")
    st.info(f"Most effective promotion method: **{best_promo}**.")

    st.markdown("---")

    col5, col6 = st.columns(2)

    with col5:
        attendance_by_type = filtered_df.groupby("event_type")["actual_attendance"].mean().reset_index()
        fig1 = px.bar(
            attendance_by_type, x="event_type", y="actual_attendance",
            color="actual_attendance", color_continuous_scale=CONTINUOUS_SCALE,
            title="Average attendance by event type",
        )
        st.plotly_chart(_themed(fig1), use_container_width=True)

    with col6:
        promo = filtered_df.groupby("promotion_channel")["actual_attendance"].mean().reset_index()
        fig2 = px.pie(
            promo, names="promotion_channel", values="actual_attendance",
            hole=0.55, title="Promotion effectiveness",
            color_discrete_sequence=CATEGORY_COLORS,
        )
        fig2.update_traces(textfont=dict(color=TEXT))
        st.plotly_chart(_themed(fig2), use_container_width=True)

    col7, col8 = st.columns(2)

    with col7:
        fig3 = px.scatter(
            filtered_df, x="budget", y="actual_attendance", color="event_type",
            size="feedback_score", hover_data=["location", "promotion_channel"],
            title="Budget vs attendance", color_discrete_sequence=CATEGORY_COLORS,
        )
        st.plotly_chart(_themed(fig3), use_container_width=True)

    with col8:
        fig4 = px.histogram(
            filtered_df, x="actual_attendance", color="event_type",
            nbins=25, title="Attendance distribution",
            color_discrete_sequence=CATEGORY_COLORS,
        )
        st.plotly_chart(_themed(fig4), use_container_width=True)
