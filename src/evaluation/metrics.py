import numpy as np

from sklearn.metrics import mean_squared_error, r2_score

def evaluate(model, X_test, y_test):

    # 예측 (log 상태)
    y_pred_log = model.predict(X_test)

    # 원래 스케일로 복원
    y_pred = np.expm1(y_pred_log)
    y_true = np.expm1(y_test)

    # RMSE: 예측 오차 크기
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)

    # R²: 설명력 (1에 가까울수록 좋음)
    r2 = r2_score(y_true, y_pred)

    print(f"RMSE: {rmse:.2f}")
    print(f"R2: {r2:.4f}")