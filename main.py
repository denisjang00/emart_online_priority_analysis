import pandas as pd
import argparse

# 데이터 수집
from data.raw.build_dataset import build_emart_dataset

# 분석 모듈
from src.data.loader import load_data
from src.data.preprocessing import preprocess
from src.features.feature_engineering import create_features
from src.models.train import train_model
from src.models.predict import predict
from src.evaluation.metrics import evaluate
from src.visualization.map import create_store_map
from src.utils.config import DATA_PATH, OUTPUT_PATH

def run_pipeline():
    """
    STEP 1: 데이터 수집

    - 크롤링
    - API 데이터 수집
    - CSV 생성
    """

    build_emart_dataset()

def run_analysis():
    """
    STEP 2: 분석 파이프라인

    흐름:
    1. 데이터 로드
    2. 전처리
    3. Feature 생성
    4. 모델 학습
    5. 평가
    6. 예측
    7. 우선순위 계산
    8. 결과 저장
    9. 시각화
    """

    # 1️. 데이터 로드
    df = load_data(DATA_PATH)

    # 2️. 전처리
    df = preprocess(df)

    # 3️. Feature Engineering
    df = create_features(df)

    # 4️. 모델 학습
    model, X_test, y_test, features = train_model(df)

    # 5️. 모델 성능 평가
    evaluate(model, X_test, y_test)

    # 6️. 전체 데이터 예측
    df = predict(model, df, features)

    # 7️. 우선순위 정렬
    df = df.sort_values(by='priority_score', ascending=False)

    # 7-1. ROI 기준 TOP 10 출력
    print("\n=== ROI 기준 TOP 10 ===")

    roi_top10 = df[['store_name', 'roi']].sort_values(
        by='roi', ascending=False
    ).head(10)

    for _, row in roi_top10.iterrows():
        print(f"{row['store_name']} | ROI: {row['roi']:.2f}")

    # 7-2. 투자 전략 분류
    priority_threshold = df['priority_score'].median()
    roi_threshold = df['roi'].median()

    def classify_strategy(row):
        if row['priority_score'] >= priority_threshold and row['roi'] >= roi_threshold:
            return "공격 투자"
        elif row['priority_score'] >= priority_threshold:
            return "성장 투자"
        elif row['roi'] >= roi_threshold:
            return "효율 투자"
        else:
            return "보류"

    df['strategy'] = df.apply(classify_strategy, axis=1)

    # 7-3. priority_score 기준 TOP 10 출력
    print("\n=== priority_score 기준 TOP 10 ===")
    top10 = df[['store_name', 'priority_score']].head(10)

    for i, row in top10.iterrows():
        print(f"{row['store_name']} | score: {row['priority_score']:.2f}")

    # 전략별 점포 수 출력
    print("\n=== 전략별 점포 수 ===")
    print(df['strategy'].value_counts())

    # 8️. 등급화 (A~E)
    df['grade'] = pd.qcut(
        df['priority_score'],
        5,
        labels=['E', 'D', 'C', 'B', 'A']
    )

    # 9️. 결과 저장
    df.to_csv(OUTPUT_PATH, index=False)

    print("분석 결과 저장 완료")

    # 10. 지도 시각화
    create_store_map(df)

def main():
    """
    실행 진입점

    사용법:
    - python main.py --pipeline  → 전체 실행
    - python main.py             → 분석만 실행
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline", action="store_true")
    args = parser.parse_args()

    # 데이터 수집 실행 여부
    if args.pipeline:
        run_pipeline()

    # 분석 실행
    run_analysis()

if __name__ == "__main__":
    main()