import numpy as np

def predict(model, df, features):

    df = df.copy()

    # 매출 예측
    df['predicted_sales'] = np.expm1(model.predict(df[features]))

    # 예측 대비 실제 매출 차이
    df['opportunity_gap'] = (
        df['predicted_sales'] - df['performance_excluding_tax23']
    )

    # 우선순위 점수
    df['priority_score'] = (
        df['opportunity_gap'] * np.log1p(df['population23'])
    )

    # 온라인 도입 시 매출 증가율 가정 (15%)
    ONLINE_LIFT = 1.15

    # 온라인 도입 시뮬레이션
    df['expected_after_online'] = df['predicted_sales'] * ONLINE_LIFT

    # 온라인 도입 비용 가정 (매출의 5%)
    ONLINE_COST_RATIO = 0.05

    df['estimated_cost'] = (
        df['predicted_sales'] * ONLINE_COST_RATIO
    )

    # ROI = (수익 증가) / 투자 비용
    df['roi'] = (
        df['expected_after_online'] - df['performance_excluding_tax23']
    ) / df['estimated_cost'].replace(0, 1)

    return df