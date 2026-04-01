import pandas as pd
import urllib.request
import time

from bs4 import BeautifulSoup

BASE_URL = "https://store.emart.com"
LIST_URL = BASE_URL + "/branch/list.do"
DETAIL_URL = BASE_URL + "/branch/view.do?id="

def get_html(url):
    return urllib.request.urlopen(url)

def parse_store_list():
    """
    점포명 + store_id 수집
    """

    html = get_html(LIST_URL)
    soup = BeautifulSoup(html, "html.parser")

    store_names = []
    store_ids = []

    ul_tag = soup.find("ul", id="branchList")

    for li in ul_tag.find_all("li"):
        a_tag = li.find("a")

        if a_tag and "이마트" in a_tag.text:
            name = a_tag.text.strip().replace("이마트 ", "")
            store_id = li.find("input").get("data-store-id")

            store_names.append(name)
            store_ids.append(store_id)

    df = pd.DataFrame({
        "store_name": store_names,
        "store_id": store_ids
    })

    print(f"점포 리스트 수집 완료: {len(df)}개")

    return df

def get_parking_count(soup):
    li_elements = soup.find("div", class_="intro-wrap").find_all("li")

    for li in li_elements:
        strong = li.find("strong")
        if strong and strong.text.strip() == "주차시설":
            parking = li.find("p").text.strip()
            return int("".join(filter(str.isdigit, parking)))

    return None

def get_addresses(soup):
    branch_info = soup.find("div", class_="branch-info1")

    road = branch_info.find("dd", class_="data").text.strip()
    local = branch_info.find_all("dd", class_="data")[1].text.strip()

    return road, local

def enrich_store_detail(df):
    """
    점포별 상세 정보 수집
    """

    # 주차가능 수
    parking_counts = []

    # 도로명 주소
    road_addresses = []

    # 지번 주소
    local_addresses = []

    for store_id in df["store_id"]:
        url = DETAIL_URL + store_id
        html = get_html(url)
        time.sleep(0.3)
        soup = BeautifulSoup(html, "html.parser")

        parking_counts.append(get_parking_count(soup))

        road, local = get_addresses(soup)
        road_addresses.append(road)
        local_addresses.append(local)

    df["parking_count"] = parking_counts
    df["road_address"] = road_addresses
    df["local_address"] = local_addresses

    print("점포 상세 정보 수집 완료")

    return df

def extract_region(df):
    """
    주소 → 지역 추출
    """

    df["region"] = df["road_address"].apply(lambda x: x.split()[0])
    df["address"] = df["road_address"]

    return df

def crawl_emart():
    """
    전체 크롤링 파이프라인
    """

    df = parse_store_list()
    df = enrich_store_detail(df)
    df = extract_region(df)

    return df