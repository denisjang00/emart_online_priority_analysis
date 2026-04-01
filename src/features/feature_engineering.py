import numpy as np

def create_features(df):
    df = df.copy()
 
    """
    모델용 feature
    """
    
    # 경쟁 강도
    df['competition_index'] = (
        df['competitor_count'] + df['market_density']
    )
    df['competition_log'] = np.log1p(df['competition_index'])

    # 인구 / 면적 로그
    df['population_log'] = np.log1p(df['population23'])
    df['area_log'] = np.log1p(df['store_area'])

    # 가구당 인구 (상권 구조)
    df['household_size'] = (
        df['population23'] / df['household23'].replace(0, 1)
    )

    # 경쟁 대비 수요
    df['demand_competition_ratio'] = (
        df['population23'] / (df['competition_index'].replace(0, 1))
    )

    # 면적 대비 주차 (접근성)
    df['parking_per_area'] = (
        df['parking_count'] / df['store_area'].replace(0, 1)
    )

    """
    분석용 feature
    """

    # 인구 대비 매출 (상권 흡수력)
    df['sales_per_person'] = (
        df['performance_excluding_tax23'] / df['population23'].replace(0, 1)
    )

    # 경쟁 대비 매출 (경쟁 환경에서 성과)
    df['sales_per_competitor'] = (
        df['performance_excluding_tax23'] / df['competition_index'].replace(0, 1)
    )

    # 면적 대비 매출 (점포 효율성)
    df['store_efficiency'] = (
        df['performance_excluding_tax23'] / df['store_area'].replace(0, 1)
    )

    return df