import requests
import os
import time

from dotenv import load_dotenv

load_dotenv()

JUSO_API_KEY = os.getenv("JUSO_API_KEY")

def get_roadNmCd(address):
    """
    주소 → 도로명 코드 변환 (JUSO API)

    반환:
    - roadNmCd (도로명 코드)
    """

    url = "https://business.juso.go.kr/addrlink/addrLinkApi.do"

    params = {
        "confmKey": JUSO_API_KEY,
        "currentPage": 1,
        "countPerPage": 1,
        "keyword": address,
        "resultType": "json"
    }

    try:
        res = requests.get(url, params=params, timeout=5)
        data = res.json()

        juso_list = data.get("results", {}).get("juso", [])

        if len(juso_list) > 0:
            return juso_list[0]["rnMgtSn"]  # 도로명 코드

    except Exception as e:
        print(f"JUSO API 오류: {e}")

    return None

def add_road_code(df):
    road_codes = []

    for addr in df["road_address"]:
        code = get_roadNmCd(addr)

        # API 과부하 방지
        time.sleep(0.1)

        road_codes.append(code)

    df["roadNmCd"] = road_codes

    return df