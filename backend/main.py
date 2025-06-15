from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import os
from datetime import datetime
import random

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 简化的星宿数据
MANSIONS = ["角", "亢", "氐", "房", "心", "尾", "箕", "斗", "牛", "女", "虚", "危", "室", "壁", "奎", "娄", "胃", "昴", "毕", "觜", "参", "井", "鬼", "柳", "星", "张", "翼", "轸"]
ELEMENTS = {"角": "Wood", "心": "Fire", "昴": "Metal", "斗": "Water", "井": "Fire"}

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
        "status": "running",
        "docs": "/docs"
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
        # 模拟天文计算
        dt = datetime(
            request.time_data.year,
            request.time_data.month,
            request.time_data.day,
            request.time_data.hour
        )
        
        # 简单的星宿计算（基于时间hash）
        mansion_index = (dt.day + dt.hour) % len(MANSIONS)
        current_mansion = MANSIONS[mansion_index]
        element = ELEMENTS.get(current_mansion, "Wood")
        ecliptic_lon = (dt.day * 12.5 + dt.hour * 15) % 360
        
        # 模拟音乐配置
        instruments = {"Wood": "Strings", "Fire": "Trumpet", "Metal": "Bells", "Water": "Flute", "Earth": "Piano"}
        modes = {"Wood": "Dorian", "Fire": "Phrygian", "Metal": "Lydian", "Water": "Aeolian", "Earth": "Ionian"}
        
        music_config = {
            "instrument": instruments.get(element, "Piano"),
            "mode": modes.get(element, "Major")
        }
        
        return {
            "success": True,
            "request_time": dt.isoformat(),
            "location": {
                "latitude": request.location_data.latitude,
                "longitude": request.location_data.longitude,
                "address": request.location_data.address
            },
            "current_mansion": current_mansion,
            "element": element,
            "ecliptic_longitude": ecliptic_lon,
            "music_config": music_config,
            "timestamp": dt.isoformat(),
            "mansion": current_mansion,
            "moon_ecliptic_lon": ecliptic_lon,
            "instrument": music_config["instrument"],
            "mode": music_config["mode"]
        }
        
    except Exception as e:
        logger.error(f"计算失败: {str(e)}")
        raise HTTPException(status_code=400, detail=f"计算失败: {str(e)}")

@app.post("/api/music/generate")
async def generate_music_api(
    instrument: str = Query(..., description="乐器类型"),
    mode: str = Query(..., description="音乐调式"), 
    style: str = Query(default="cinematic, ethereal", description="音乐风格"),
    duration: int = Query(default=45, description="音乐时长")
):
    try:
        # 模拟音乐生成
        current_mansion = random.choice(MANSIONS)
        element = ELEMENTS.get(current_mansion, "Wood")
        
        # 模拟音乐结果
        music_result = {
            "success": True,
            "id": f"music_{random.randint(1000000, 9999999)}",
            "message": "音乐生成成功（演示版本）"
        }
        
        return {
            "success": True,
            "astronomy": {
                "mansion": current_mansion,
                "element": element,
                "moon_ecliptic_lon": random.uniform(0, 360)
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
