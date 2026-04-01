def preprocess(df):
    df = df.copy()

    # 좌표 없는 데이터 제거
    df = df[(df["latitude"] != 0) & (df["longitude"] != 0)]

    # 핵심 변수만 결측 제거
    df = df.dropna(subset=[
        "population23",
        "performance_excluding_tax23",
        "store_area"
    ])

    return df