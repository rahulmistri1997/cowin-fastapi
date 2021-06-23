from datetime import datetime
import pathlib
from fastapi import FastAPI
import aiohttp
import json
import datetime
from fastapi_utils.tasks import repeat_every
from enum import Enum
from dotenv import load_dotenv
from pathlib import Path
from models import age_group
import os

## Loading ENV Variables
env_path = Path('.')/'.env'
load_dotenv(env_path)
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

app = FastAPI()
currentdata = None

@app.get("/")
async def indexhtml():
    return "Please go to /docs Url to learn about the API"

@app.get("/cowin/{pincode}/{dose}/{age}",description="Age should be 18 or 45 ! Dose should be 1 or 2")
async def index(pincode,dose,age):
    pincode = int(pincode)
    dose = int(dose)
    age = int(age)
    return await scan(pincode,dose,age)

async def scan(pincode=411014,dose=1,age=18):
    current_date = datetime.datetime.today().date()
    current_date = current_date.strftime("%d") + "-" + current_date.strftime("%m") + "-" + current_date.strftime("%Y")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={current_date}") as resp:
            centers = await resp.text()
            centers = json.loads(centers)
            outputlist = []
            for each in centers["centers"]:
                if each["sessions"][0][f"available_capacity_dose{dose}"] > 0 and each["fee_type"] == "Free" and each["sessions"][0]["min_age_limit"] == age:
                    outputlist.append(each)
                    outputlist.append("-----------------------------------------------------------------------------------")
            if outputlist:
                return outputlist
            return f"Not Available for Dose:{dose} / Age:{age}"

@app.on_event("startup")
@repeat_every(seconds=10)
async def looper():
    global currentdata ,telegram_token, telegram_chat_id
    data = await scan()
    url = "https://webhook.site/4a707569-4d1d-4e47-acf9-305b53839646"
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}&text={json.dumps(data)}" # You can have any webhook end-point over here.
    if not data.__contains__("Not"):
        try:
            if data != currentdata:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url=url,data=json.dumps(data)) as resp:
                        if resp.status == 200:
                            currentdata = data
        except Exception as e:
            print("exception ",e)
            
