import plotly.express as px

def create_store_map(df):
    """
    점포별 우선순위 지도 시각화
    """
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="priority_score", # 색상 = 우선순위
        size="performance_excluding_tax23",
        hover_name="store_name",
        zoom=6,
        height=600
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        title="점포별 온라인 도입 우선순위"
    )

    fig.show()