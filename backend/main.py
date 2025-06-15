from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import os
from datetime import datetime

# 导入自定义模块
try:
    from modules.astronomy import calc_mansion, get_all_mansions_positions, get_moon_position
    from modules.wuxing import get_element
    from modules.mapping import get_full_music_config
    from modules.generation import generate_music
except ImportError as e:
    print(f"模块导入错误: {e}")
    exit(1)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="28星宿天体音乐生成器 API",
    description="基于传统中国天文学和五行理论的音乐生成系统",
    version="2.1.0"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 部署后改为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class TimeSelection(BaseModel):
    year: int
    month: int
    day: int
    hour: int

class LocationSelection(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None

class AstronomyRequest(BaseModel):
    time_data: TimeSelection
    location_data: LocationSelection

# API路由
@app.get("/")
async def root():
    return {
        "message": "28星宿天体音乐生成器 API",
        "version": "2.1.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/astronomy/calculate")
async def calculate_astronomy(request: AstronomyRequest):
    try:
        dt = datetime(
            request.time_data.year,
            request.time_data.month,
            request.time_data.day,
            request.time_data.hour
        )
        timestamp = dt.timestamp()
        
        moon_pos = get_moon_position(
            timestamp, 
            request.location_data.latitude, 
            request.location_data.longitude
        )
        
        if 'ecliptic_longitude' not in moon_pos:
            if 'longitude' in moon_pos:
                moon_pos['ecliptic_longitude'] = moon_pos['longitude']
            else:
                raise ValueError("无法获取月亮黄经数据")
        
        current_mansion = calc_mansion(moon_pos['ecliptic_longitude'])
        element = get_element(current_mansion)
        music_config = get_full_music_config(current_mansion)
        
        return {
            "success": True,
            "request_time": dt.isoformat(),
            "location": {
                "latitude": request.location_data.latitude,
                "longitude": request.location_data.longitude,
                "address": request.location_data.address
            },
            "moon_position": moon_pos,
            "current_mansion": current_mansion,
            "element": element,
            "ecliptic_longitude": moon_pos['ecliptic_longitude'],
            "music_config": music_config,
            "timestamp": dt.isoformat(),
            "mansion": current_mansion,
            "moon_ecliptic_lon": moon_pos['ecliptic_longitude'],
            "instrument": music_config.get('instrument', 'Piano'),
            "mode": music_config.get('mode', 'Major')
        }
        
    except Exception as e:
        logger.error(f"天文计算失败: {str(e)}")
        raise HTTPException(status_code=400, detail=f"天文计算失败: {str(e)}")

@app.post("/api/music/generate")
async def generate_music_api(
    instrument: str = Query(..., description="乐器类型"),
    mode: str = Query(..., description="音乐调式"), 
    style: str = Query(default="cinematic, ethereal", description="音乐风格"),
    duration: int = Query(default=45, description="音乐时长")
):
    try:
        dt = datetime.now()
        timestamp = dt.timestamp()
        
        moon_pos = get_moon_position(timestamp, 22.3193, 114.1694)
        if 'ecliptic_longitude' not in moon_pos:
            moon_pos['ecliptic_longitude'] = moon_pos.get('longitude', 0)
        
        current_mansion = calc_mansion(moon_pos['ecliptic_longitude'])
        element = get_element(current_mansion)
        
        music_result = generate_music(
            instrument=instrument,
            mode=mode,
            style=style,
            duration=duration
        )
        
        return {
            "success": True,
            "astronomy": {
                "mansion": current_mansion,
                "element": element,
                "moon_ecliptic_lon": moon_pos['ecliptic_longitude']
            },
            "parameters": {
                "element": element,
                "instrument": instrument,
                "mode": mode,
                "duration": duration,
                "enhanced_prompt": f"{instrument}, {mode}, {style}, {duration} seconds"
            },
            "music": music_result
        }
        
    except Exception as e:
        logger.error(f"音乐生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"音乐生成错误: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
