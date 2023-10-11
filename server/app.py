from fastapi import FastAPI, APIRouter
import pymongo
from pathlib import Path
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()
router = APIRouter()

@app.get('/education/rank')
async def rank():
    myclient = pymongo.MongoClient("mongodb://43.202.26.130:27017/")
    mydb = myclient["admin"]
    mycol = mydb["koreanSAT"]
    
    packs = dict()
    for _ in range(1,6):
        pak = mycol.find_one({'pack': _}, {'_id': 0, 'name': 1})
        packs[f"pack{_}"] = pak["pack"]

    return packs

@app.get('/education/test')
async def test(cnt : int):
    myclient = pymongo.MongoClient("mongodb://43.202.26.130:27017/")
    mydb = myclient["admin"]
    mycol = mydb["koreanSAT"]
    
    pak = mycol.find({'pack': cnt}, {'_id': 0, 'pack': 0, 'answer' : 0 , "time": 0,})
    # print(list(pak))
    
    test = dict()
    cnt = 1
    for _ in list(pak):
        
        test[f"qassage{cnt}"] = _["qassage"]
        test[f"question{cnt}"] = _["question"]
        test[f"options{cnt}"] = _["options"]
        test[f"id{cnt}"] = _["id"]
        cnt += 1

    return test

@app.get('/education/answer')
async def test(id : str):
    myclient = pymongo.MongoClient("mongodb://43.202.26.130:27017/")
    mydb = myclient["admin"]
    mycol = mydb["koreanSAT"]
    
    pak = mycol.find_one({'id': id}, {'_id': 0, 'answer' : 1 })

    return pak

@app.get('/Campingstore/search')
async def imgPrint(name: str):
    myclient = pymongo.MongoClient("mongodb://43.202.26.130:27017/")
    mydb = myclient["admin"]
    mycol = mydb["koreanSAT"]
  
    titleimg = mycol.find({'name':{'$regex': name}}, {'_id': 0, 'name': 1 })

    name_lsit = []
    for _ in list(titleimg):
        print(_)
        print("**" * 50)
        name_lsit.append(_["name"])
    
    set_name = set(name_lsit)
    
    names = dict()
    cnt = 1
    for i in set_name[0:10]:
        names[f"name{cnt}"] = i
        cnt += 1
    
    return names
   
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
    print("server 3000 PORT OPEN")