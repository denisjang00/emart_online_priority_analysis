import pandas as pd

from data.raw.crawl_emart import crawl_emart
from data.raw.load_store_extra import load_store_extra
from data.raw.geocoding import add_coordinates
from data.raw.kakao_api import add_competition
from data.raw.juso_api import add_road_code
from data.raw.population_api import add_population

def build_emart_dataset():

    # 1. 이마트 점포 크롤링
    df = crawl_emart()

    # 2. 내부 엑셀 데이터 (매출/면적)
    df_extra = load_store_extra("data/raw/store_extra.xlsx")
    
    # 3. 데이터 병합
    df = df.merge(df_extra, on="store_name", how="inner")

    # 4. 좌표 생성 (주소 → 위도/경도)
    df = add_coordinates(df)

    # 5. 도로명 코드 생성
    df = add_road_code(df)
    df = df.dropna(subset=["roadNmCd"])

    # 6. 인구 데이터
    df = add_population(df)

    # 7. 경쟁 점포
    df = add_competition(df)

    # 7. 최종 컬럼 정리
    df_final = df[[
        "store_name",
        "region",
        "open_year",
        "store_area",
        "parking_count",
        "competitor_count",
        "market_density",
        "performance_excluding_tax23",
        "population23",
        "household23",
        "longitude",
        "latitude"
    ]]

    # 8. 저장
    df_final.to_csv("data/processed/emart_final.csv", index=False)

    print("emart_final.csv 생성 완료")

    return df_final