import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

def train_model(df):

    features = [
        'competition_log',
        'household_size',
        'parking_per_area',
        'demand_competition_ratio',
        'population_log',
        'area_log'
    ]

    X = df[features]
    y = np.log1p(df['performance_excluding_tax23'])

    # 학습/테스트 분리
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 모델 생성 및 학습
    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Feature 중요도
    importance = pd.Series(model.feature_importances_, index=features)

    print("\nFeature Importance:")
    print(importance.sort_values(ascending=False))

    return model, X_test, y_test, features