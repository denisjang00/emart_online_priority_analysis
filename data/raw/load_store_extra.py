import pandas as pd

def load_store_extra(file_path):
    """
    점포별 추가 정보 (오픈일, 매출, 매장면적)
    """

    df = pd.read_excel(file_path)

    df = df.rename(columns={
        "점포": "store_name",
        "오픈일": "open_year",
        "세제외 실적": "sales_raw",
        "매장면적": "store_area_raw"
    })

    # 결측 제거
    df = df.dropna(subset=["open_year", "sales_raw", "store_area_raw"])

    # 타입 변환
    df["open_year"] = df["open_year"].astype(int)
    df["sales_raw"] = df["sales_raw"].astype(int)
    df["store_area_raw"] = df["store_area_raw"].astype(int)

    # 매출 단위 변환 (100만 → 억)
    df["performance_excluding_tax23"] = (df["sales_raw"] / 100).round().astype(int)

    # 매장 면적 처리
    def round_area(x):
        return round(x, -1) if int(str(x)[0]) > 4 else (x // 10) * 10

    df["store_area"] = df["store_area_raw"].apply(round_area)

    df = df[[
        "store_name",
        "open_year",
        "performance_excluding_tax23",
        "store_area"
    ]]

    print("엑셀 데이터 로드 완료")

    return df