import requests
import os
import pandas as pd
import sys

#dt = sys.argv[1]

def req(load_dt="20120101", url_param={}):
    url = gen_url(load_dt, url_param)
    r = requests.get(url)
    code = r.status_code
    data = r.json()
    #print(data)
    return code, data

def gen_url(dt='20120101', url_param={}):
    base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    # key = "6d73ca55adb7b40c2b042c67db5f37eb"
    key = get_key()
    url = f"{base_url}?key={key}&targetDt={dt}"
    for k, v in url_param.items():
        #url = url + "&multiMovieYn=Y"
        url = url + f"&{k}={v}"

    return url

def get_key():
    """영화진흥위원회 가입 및 API 키생성 후 환경변수 선언 필요"""
    key = os.getenv('MOVIE_API_KEY')
    return key

def req2list(load_dt='20120101', url_param={}):
    _, data = req(load_dt, url_param)
    l = data['boxOfficeResult']['dailyBoxOfficeList']
    return l

def list2df(load_dt='20120101', url_param={}):
    l = req2list(load_dt, url_param)
    df = pd.DataFrame(l)
    return df

def save2df(load_dt='20120101', url_param={}):
    """airflow 호출 지점"""
    df = list2df(load_dt, url_param)
    df['load_dt'] = load_dt
    #df.to_parquet('~/tmp/test_parquet/', partition_cols=['load_dt'])
    return df

def echo(yaho):
    return yaho

def apply_type2df(load_dt="20120101", path="~/tmp/test_parquet"):
    df = pd.read_parquet(f'{path}/load_dt={load_dt}')
    num_cols = ['rnum', 'rank', 'rankInten', 'salesAmt', 'audiCnt', 'audiAcc', 'scrnCnt', 'showCnt', 'salesShare', 'salesInten', 'salesChange', 'audiInten', 'audiChange']

    #for c in num_cols:
        #df[c] = pd.to_numeric(df[c]) 
    
    df[num_cols] = df[num_cols].apply(pd.to_numeric)

    return df

