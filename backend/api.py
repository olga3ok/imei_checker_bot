from fastapi import FastAPI, HTTPException, Request
from .models import IMEIRequest
import aiohttp
import json
import os
from .utils import validate_imei
from dotenv import load_dotenv

load_dotenv()

IMEI_CHECK_API_URL: str = os.getenv('IMEI_CHECK_API_URL')
IMEI_CHECK_API_TOKEN: str = os.getenv('IMEI_CHECK_API_TOKEN')

app = FastAPI()


@app.post('/api/check-imei')
async def check_imei(request: Request, data: IMEIRequest) -> dict:
    """
    Проверка IMEI через внешний API
    """
    imei: str = data.imei
    token: str = IMEI_CHECK_API_TOKEN
    url: str = IMEI_CHECK_API_URL + "checks"

    if not validate_imei(imei):
        raise HTTPException(status_code=400, detail='Invalid IMEI format')

    headers: dict = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    body: str = json.dumps({
        "deviceId": imei,
        "serviceId": 12
    })

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, data=body) as response:
                if response.status == 201:
                    data = await response.json()
                    return data
                else:
                    raise HTTPException(status_code=response.status, detail=await response.text())
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=500, detail=f"Client error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
@app.get('/api/get-services')
async def get_services() -> dict:
    """
    Получение списка доступных сервисов через внешний API
    """
    token: str = IMEI_CHECK_API_TOKEN
    url: str = IMEI_CHECK_API_URL + "services"

    headers: dict = {
        'Authorization': 'Bearer ' + token,
        'Accept-Language': 'en',
        'Content-Type': 'application/json',
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise HTTPException(status_code=response.status, detail=await response.text())
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=500, detail=f"Client error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
