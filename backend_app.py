from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import os
import time
from datetime import datetime

# 导入自定义模块
try:
    from modules.astronomy import calc_mansion, get_all_mansions_positions, get_moon_position
    from modules.wuxing import get_element
    from modules.mapping import map_to_params, get_full_music_config
    from modules.generation import generate_music
except ImportError as e:
    print(f"模块导入错误: {e}")
    print("请确保modules目录下有所有必要的Python文件")
    exit(1)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="28星宿天体音乐生成器",
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

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

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

# ==================== 页面路由 ====================

@app.get("/")
async def time_selector():
    """第一步：时间选择页面"""
    return FileResponse('static/time-selector.html')

@app.get("/location")
async def location_selector():
    """第二步：位置选择页面"""
    return FileResponse('static/location-selector.html')

@app.get("/starmap")
async def starmap():
    """第三步：星图音乐页面"""
    return FileResponse('static/starmap.html')

# ==================== API接口 ====================

@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.1.0"
    }

@app.get("/api/mansion")
async def get_mansion_data(
    date: Optional[str] = Query(None, description="日期时间 (ISO格式)")
):
    """获取星宿数据 - 兼容原有前端调用"""
    try:
        # 从SessionStorage读取时间和位置数据
        time_data = None
        location_data = None
        
        # 解析时间
        if date:
            try:
                dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
                timestamp = dt.timestamp()
            except ValueError:
                dt = datetime.now()
                timestamp = dt.timestamp()
        else:
            dt = datetime.now()
            timestamp = dt.timestamp()
        
        # 默认位置（香港）- 如果没有从SessionStorage获取到位置
        latitude = 22.3193
        longitude = 114.1694
        
        logger.info(f"计算时间: {dt.isoformat()}, 位置: {latitude}, {longitude}")
        
        # 获取月亮位置
        moon_pos = get_moon_position(timestamp, latitude, longitude)
        logger.info(f"月亮位置数据: {moon_pos}")
        
        # 确保有ecliptic_longitude字段
        if 'ecliptic_longitude' not in moon_pos:
            if 'longitude' in moon_pos:
                moon_pos['ecliptic_longitude'] = moon_pos['longitude']
            else:
                raise ValueError("无法获取月亮黄经数据")
        
        # 计算星宿
        current_mansion = calc_mansion(moon_pos['ecliptic_longitude'])
        element = get_element(current_mansion)
        
        # 获取音乐配置
        music_config = get_full_music_config(current_mansion)
        
        # 构造响应数据 - 兼容原有前端
        response_data = {
            "success": True,
            "timestamp": dt.isoformat(),
            "mansion": current_mansion,
            "element": element,
            "moon_ecliptic_lon": moon_pos['ecliptic_longitude'],
            "instrument": music_config.get('instrument', 'Piano'),
            "mode": music_config.get('mode', 'Major'),
            "moon_position": moon_pos,
            "music_config": music_config
        }
        
        logger.info(f"返回数据: 月亮在{current_mansion}宿, 五行:{element}, 乐器:{music_config.get('instrument')}, 调式:{music_config.get('mode')}")
        return response_data
        
    except Exception as e:
        logger.error(f"天文计算失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"天文计算错误: {str(e)}")

@app.post("/api/astronomy/calculate")
async def calculate_astronomy(request: AstronomyRequest):
    """根据指定时间和位置计算天文数据"""
    try:
        # 转换时间
        dt = datetime(
            request.time_data.year,
            request.time_data.month,
            request.time_data.day,
            request.time_data.hour
        )
        timestamp = dt.timestamp()
        
        logger.info(f"计算历史时间: {dt.isoformat()}, 位置: {request.location_data.latitude}, {request.location_data.longitude}")
        
        # 获取月亮位置
        moon_pos = get_moon_position(
            timestamp, 
            request.location_data.latitude, 
            request.location_data.longitude
        )
        
        # 检查是否有错误
        if 'error' in moon_pos:
            raise ValueError(f"月亮位置计算失败: {moon_pos['error']}")
        
        # 确保有ecliptic_longitude字段
        if 'ecliptic_longitude' not in moon_pos:
            if 'longitude' in moon_pos:
                moon_pos['ecliptic_longitude'] = moon_pos['longitude']
            else:
                raise ValueError("无法获取月亮黄经数据")
        
        # 计算当前星宿
        current_mansion = calc_mansion(moon_pos['ecliptic_longitude'])
        element = get_element(current_mansion)
        
        # 获取所有星宿位置
        mansions_positions = get_all_mansions_positions(timestamp)
        
        # 生成音乐配置
        music_config = get_full_music_config(current_mansion)
        
        logger.info(f"计算成功: 月亮在 {current_mansion} 宿，黄经 {moon_pos['ecliptic_longitude']:.2f}°")
        
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
            "mansions_positions": mansions_positions,
            "music_config": music_config,
            # 兼容原有前端的字段
            "timestamp": dt.isoformat(),
            "mansion": current_mansion,
            "moon_ecliptic_lon": moon_pos['ecliptic_longitude'],
            "instrument": music_config.get('instrument', 'Piano'),
            "mode": music_config.get('mode', 'Major')
        }
        
    except Exception as e:
        logger.error(f"时间格式错误: {str(e)}")
        raise HTTPException(status_code=400, detail=f"天文计算失败: {str(e)}")
    
@app.get("/api/astronomy")
async def get_astronomy_data(
    year: int = Query(..., ge=1950, le=2025, description="年份(1950-2025)"),
    month: int = Query(..., ge=1, le=12, description="月份(1-12)"),
    day: int = Query(..., ge=1, le=31, description="日期(1-31)"),
    hour: int = Query(..., ge=0, le=23, description="小时(0-23)"),
    latitude: float = Query(..., ge=-90, le=90, description="纬度(-90到90)"),
    longitude: float = Query(..., ge=-180, le=180, description="经度(-180到180)")
):
    """通过GET参数获取天文数据"""
    try:
        request = AstronomyRequest(
            time_data=TimeSelection(year=year, month=month, day=day, hour=hour),
            location_data=LocationSelection(latitude=latitude, longitude=longitude)
        )
        return await calculate_astronomy(request)
    except Exception as e:
        logger.error(f"GET方式天文计算失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate_music")
async def generate_music_api(request: dict):
    """生成音乐接口 - 兼容原有前端调用"""
    try:
        logger.info(f"收到音乐生成请求: {request}")
        
        # 解析请求参数
        date_str = request.get('date')
        latitude = request.get('lat', 22.3193)
        longitude = request.get('lon', 114.1095)
        style = request.get('style', 'cinematic, ethereal')
        duration = request.get('duration', 45)
        
        # 首先计算天文数据
        if date_str:
            try:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                timestamp = dt.timestamp()
            except ValueError:
                dt = datetime.now()
                timestamp = dt.timestamp()
        else:
            dt = datetime.now()
            timestamp = dt.timestamp()
        
        # 获取天文数据
        moon_pos = get_moon_position(timestamp, latitude, longitude)
        if 'ecliptic_longitude' not in moon_pos:
            if 'longitude' in moon_pos:
                moon_pos['ecliptic_longitude'] = moon_pos['longitude']
            else:
                raise ValueError("无法获取月亮黄经数据")
        
        current_mansion = calc_mansion(moon_pos['ecliptic_longitude'])
        element = get_element(current_mansion)
        music_config = get_full_music_config(current_mansion)
        
        # 生成音乐
        music_result = generate_music(
            instrument=music_config.get('instrument', 'Piano'),
            mode=music_config.get('mode', 'Major'),
            style=style,
            duration=duration
        )
        
        # 构造响应数据
        response_data = {
            "success": True,
            "astronomy": {
                "mansion": current_mansion,
                "element": element,
                "moon_ecliptic_lon": moon_pos['ecliptic_longitude']
            },
            "parameters": {
                "element": element,
                "instrument": music_config.get('instrument', 'Piano'),
                "mode": music_config.get('mode', 'Major'),
                "duration": duration,
                "enhanced_prompt": f"{music_config.get('instrument', 'Piano')}, {music_config.get('mode', 'Major')}, {style}, {duration} seconds, inspired by {current_mansion} constellation and {element} element"
            },
            "music": music_result
        }
        
        logger.info(f"音乐生成完成: {current_mansion}宿, {element}元素")
        return response_data
        
    except Exception as e:
        logger.error(f"音乐生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"音乐生成错误: {str(e)}")

@app.post("/api/music/generate")
async def generate_music_query_api(
    instrument: str = Query(None, description="乐器类型"),
    mode: str = Query(None, description="音乐调式"), 
    style: str = Query(default="cinematic, ethereal", description="音乐风格"),
    duration: int = Query(default=45, ge=15, le=180, description="音乐时长(秒)")
):
    """通过查询参数生成音乐 - 兼容前端调用"""
    try:
        logger.info(f"收到查询参数音乐生成请求: instrument={instrument}, mode={mode}, style={style}, duration={duration}")
        
        # 使用当前时间和默认位置
        dt = datetime.now()
        timestamp = dt.timestamp()
        latitude = 22.3193
        longitude = 114.1095
        
        # 获取天文数据
        moon_pos = get_moon_position(timestamp, latitude, longitude)
        if 'ecliptic_longitude' not in moon_pos:
            if 'longitude' in moon_pos:
                moon_pos['ecliptic_longitude'] = moon_pos['longitude']
            else:
                raise ValueError("无法获取月亮黄经数据")
        
        current_mansion = calc_mansion(moon_pos['ecliptic_longitude'])
        element = get_element(current_mansion)
        music_config = get_full_music_config(current_mansion)
        
        # 使用参数优先级：前端传递 > 天文计算 > 默认值
        final_instrument = instrument if instrument and instrument != 'undefined' else music_config.get('instrument', 'Piano')
        final_mode = mode if mode and mode != 'undefined' else music_config.get('mode', 'Major')
        
        logger.info(f"最终音乐参数: instrument={final_instrument}, mode={final_mode}")
        
        # 生成音乐（使用最终确定的参数）
        music_result = generate_music(
            instrument=final_instrument,
            mode=final_mode,
            style=style,
            duration=duration
        )
        
        logger.info(f"音乐生成原始结果: {music_result}")
        
        # 处理音乐结果，确保返回正确的格式
        processed_music = music_result
        if isinstance(music_result, str) and music_result.isdigit():
            # 如果返回的是ID字符串，构造完整的音频信息
            processed_music = {
                "success": True,
                "id": music_result,
                "download_url": f"https://yue-inst.ngrok.app/download/{music_result}",  # 根据实际API调整
                "message": "音乐生成成功"
            }
        elif isinstance(music_result, dict):
            # 确保字典格式包含必要字段
            if 'success' not in music_result:
                processed_music['success'] = True
            if 'download_url' not in music_result and music_result.get('id'):
                processed_music['download_url'] = f"https://yue-inst.ngrok.app/download/{music_result['id']}"
        
        # 构造响应数据
        response_data = {
            "success": True,
            "astronomy": {
                "mansion": current_mansion,
                "element": element,
                "moon_ecliptic_lon": moon_pos['ecliptic_longitude']
            },
            "parameters": {
                "element": element,
                "instrument": final_instrument,
                "mode": final_mode,
                "duration": duration,
                "enhanced_prompt": f"{final_instrument}, {final_mode}, {style}, {duration} seconds, inspired by {current_mansion} constellation and {element} element"
            },
            "music": processed_music
        }
        
        logger.info(f"音乐生成完成: {current_mansion}宿, {element}元素, {final_instrument}, {final_mode}")
        return response_data
        
    except Exception as e:
        logger.error(f"查询参数音乐生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"音乐生成错误: {str(e)}")

@app.get("/api/mansions")
async def get_all_mansions():
    """获取所有28星宿的信息"""
    try:
        from modules.astronomy import MANSIONS
        from modules.wuxing import MANSION_ELEMENT_MAP
        
        mansions_info = []
        for mansion in MANSIONS:
            element = get_element(mansion)
            mansions_info.append({
                "name": mansion,
                "element": element,
                "element_en": MANSION_ELEMENT_MAP.get(mansion, "Wood")
            })
        
        return {
            "success": True,
            "mansions": mansions_info,
            "total": len(mansions_info)
        }
        
    except Exception as e:
        logger.error(f"获取星宿信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 错误处理 ====================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """404错误处理"""
    return JSONResponse(
        status_code=404,
        content={"error": "页面未找到", "status_code": 404}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """500错误处理"""
    logger.error(f"内部服务器错误: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "内部服务器错误", "status_code": 500}
    )

# ==================== 启动配置 ====================

if __name__ == "__main__":
    import uvicorn
    
    # 检查静态文件目录
    if not os.path.exists("static"):
        logger.warning("static目录不存在，创建中...")
        os.makedirs("static")
    
    logger.info("28星宿天体音乐生成器后端服务启动中...")
    logger.info("访问路径:")
    logger.info("  时间选择: http://localhost:8000/")
    logger.info("  位置选择: http://localhost:8000/location")
    logger.info("  星图音乐: http://localhost:8000/starmap")
    logger.info("  API文档:  http://localhost:8000/docs")
    
    uvicorn.run(
        "backend_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
