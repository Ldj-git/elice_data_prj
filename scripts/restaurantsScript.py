import os
import pandas as pd
import numpy as np
import json
from pymongo import MongoClient, GEOSPHERE
from dotenv import load_dotenv

# 상위 폴더를 base directory로 설정
BASEDIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = BASEDIR[:BASEDIR.rfind('/')]

# .env 파일 경로 설정
load_dotenv(os.path.join(BASEDIR, 'back/.env'))

# michelinMuglang db에 연결
file = os.path.join(BASEDIR, "raw_data/michelin_my_maps.csv")
mongodb = os.getenv("MONGODB_URL")
client = MongoClient(mongodb)
db = client.michelinMuglang

data = pd.read_csv(file)
michelin = data.copy()

michelin.columns = ["name", "address", "location", "minPrice", "maxPrice", "currency",
       "cuisine", "longitude", "latitude", "phoneNumber", "url", "websiteUrl",
       "award"]

# cuisine을 String에서 Array로 변환 
michelin["cuisine"] = michelin["cuisine"].apply(lambda x:x.replace(", ", ",").split(","))

# 주소에서 국가 추출
michelin["country"] = michelin["address"].apply(lambda x:x[x.rfind(",")+2:])
michelin["country"] = michelin["country"].replace({'China Mainland':'China', 'Taipei & Taichung':'Taiwan'})

# string -> int로 형변환(결측값 포함) // ["minPrice", "maxPrice"]
michelin["minPrice"] = michelin["minPrice"].fillna(-1)
michelin["minPrice"] = michelin["minPrice"].apply(lambda x:str(x).strip().replace(",", ""))
michelin["minPrice"] = michelin["minPrice"].astype('Int32')
michelin["minPrice"] = michelin["minPrice"].replace(-1, np.nan)

michelin["maxPrice"] = michelin["maxPrice"].fillna(-1)
michelin["maxPrice"] = michelin["maxPrice"].apply(lambda x:str(x).strip().replace(",", ""))
michelin["maxPrice"] = michelin["maxPrice"].astype('Int32')
michelin["maxPrice"] = michelin["maxPrice"].replace(-1, np.nan)

# float64 -> string으로 형변환(결측값 포함) // phoneNumber
michelin["phoneNumber"] = michelin["phoneNumber"].fillna(-1)
michelin["phoneNumber"] = michelin["phoneNumber"].apply(lambda x:'+'+str(int(x)))
michelin["phoneNumber"] = michelin["phoneNumber"].replace("+-1", np.nan)

# longitude와 latitude로 coordinate(좌표) 생성
michelin["coordinate"] = michelin.apply(lambda row: [row["longitude"], row["latitude"]], axis=1)

dataJson = json.loads(michelin.to_json(orient="records"))

if "restaurants" in db.list_collection_names():
       db.restaurants.drop()
       print("collection has been dropped")

db.restaurants.insert_many(dataJson)
db.restaurants.create_index([("coordinate", GEOSPHERE)])