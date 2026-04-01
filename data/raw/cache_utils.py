import pandas as pd
import os

def load_cache(path, key_col):
    """
    캐시 파일 로드
    """
    if not os.path.exists(path):
        return {}

    df = pd.read_csv(path)
    df = df.drop_duplicates(subset=[key_col], keep="last")

    return df.set_index(key_col).to_dict("index")

def save_cache(cache, path, key_col):
    """
    캐시 저장
    """
    df = pd.DataFrame.from_dict(cache, orient="index").reset_index()
    df = df.rename(columns={"index": key_col})

    os.makedirs(os.path.dirname(path), exist_ok=True)

    df.to_csv(path, index=False)