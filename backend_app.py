from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import os
import time  # 添加这个导入

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
    version="1.0.0"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("静态文件目录已挂载")

# 数据模型
class MusicRequest(BaseModel):
    date: Optional[str] = None
    lat: float = 22.3964
    lon: float = 114.1095
    style: str = "cinematic, ethereal"
    duration: Optional[int] = 45  # 添加时长参数

class CustomMusicRequest(BaseModel):
    date: Optional[str] = None
    lat: float = 22.3964
    lon: float = 114.1095
    style: str = "cinematic, ethereal"
    duration: int = 45

# 根路径
@app.get("/")
async def root():
    """根路径 - 返回前端页面或API信息"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    else:
        return {
            "message": "28星宿天体音乐生成器 API",
            "version": "1.0.0",
            "docs": "/docs",
            "endpoints": {
                "health": "/api/health",
                "mansion": "/api/mansion",
                "stars": "/api/stars/positions", 
                "moon": "/api/moon/position",
                "generate": "/api/generate_music",
                "generate_custom": "/api/generate_music_custom"
            }
        }

# 健康检查端点
@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    try:
        test_result = calc_mansion()
        
        return {
            "status": "healthy",
            "service": "28星宿音乐生成器",
            "version": "1.0.0",
            "modules": "loaded",
            "astronomy": "functional",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return {
            "status": "unhealthy",
            "service": "28星宿音乐生成器",
            "version": "1.0.0",
            "error": str(e),
            "timestamp": time.time()
        }

# API端点
@app.get("/api/mansion")
async def get_mansion_info(
    date: Optional[str] = Query(None, description="ISO格式时间字符串"),
    lat: float = Query(22.3964, description="纬度"),
    lon: float = Query(114.1095, description="经度")
):
    """获取月亮当前所在星宿信息"""
    try:
        logger.info(f"获取星宿信息: date={date}, lat={lat}, lon={lon}")
        
        result = calc_mansion(date, lat, lon)
        element = get_element(result['mansion'])
        instrument, mode = map_to_params(element)
        full_config = get_full_music_config(element)
        
        response = {
            "success": True,
            "mansion": result['mansion'],
            "element": element,
            "instrument": instrument,
            "mode": mode,
            "timestamp": result['timestamp'],
            "moon_ecliptic_lon": result.get('moon_ecliptic_lon', 0),
            "full_config": full_config
        }
        
        logger.info(f"星宿信息获取成功: {result['mansion']} -> {element}")
        return response
        
    except Exception as e:
        logger.error(f"获取星宿信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@app.get("/api/stars/positions")
async def get_star_positions(
    date: Optional[str] = Query(None, description="ISO格式时间字符串"),
    lat: float = Query(22.3964, description="纬度"),
    lon: float = Query(114.1095, description="经度")
):
    """获取28星宿所有恒星位置"""
    try:
        logger.info(f"获取星宿位置: date={date}, lat={lat}, lon={lon}")
        
        positions = get_all_mansions_positions(date, lat, lon)
        
        return {
            "success": True,
            "data": positions
        }
        
    except Exception as e:
        logger.error(f"获取星宿位置失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取星宿位置失败: {str(e)}")

@app.get("/api/moon/position")
async def get_moon_pos(
    date: Optional[str] = Query(None, description="ISO格式时间字符串"),
    lat: float = Query(22.3964, description="纬度"),
    lon: float = Query(114.1095, description="经度")
):
    """获取月亮详细位置信息"""
    try:
        logger.info(f"获取月亮位置: date={date}, lat={lat}, lon={lon}")
        
        position = get_moon_position(date, lat, lon)
        
        return {
            "success": True,
            "moon": position
        }
        
    except Exception as e:
        logger.error(f"获取月亮位置失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取月亮位置失败: {str(e)}")

@app.post("/api/generate_music")
async def generate_celestial_music(request: MusicRequest):
    """根据天文信息生成45秒音乐"""
    try:
        logger.info(f"收到音乐生成请求: {request}")
        start_time = time.time()
        
        # 获取天文信息
        mansion_info = calc_mansion(request.date, request.lat, request.lon)
        element = get_element(mansion_info['mansion'])
        instrument, mode = map_to_params(element)
        
        # 设置音乐时长
        duration = request.duration or 45
        
        # 获取完整配置（包含时长信息）
        full_config = get_full_music_config(element, duration)
        
        # 创建增强型prompt
        enhanced_prompt = f"{instrument}, {mode}, {request.style}, {duration} seconds duration, complete musical piece with clear beginning and ending"
        
        logger.info(f"生成增强型prompt: {enhanced_prompt}")
        
        # 记录天文计算耗时
        astronomy_time = time.time() - start_time
        logger.info(f"天文计算完成，耗时: {astronomy_time:.2f}秒")
        
        # 生成音乐
        music_start_time = time.time()
        music_result = generate_music(instrument, mode, request.style, duration=duration)
        music_generation_time = time.time() - music_start_time
        
        # 构建响应
        response = {
            "success": True,
            "astronomy": mansion_info,
            "parameters": {
                "element": element,
                "instrument": instrument,
                "mode": mode,
                "duration": duration,
                "enhanced_prompt": enhanced_prompt,
                "full_config": full_config
            },
            "music": music_result,
            "performance": {
                "astronomy_calculation_time": f"{astronomy_time:.2f}s",
                "music_generation_time": f"{music_generation_time:.2f}s",
                "total_time": f"{time.time() - start_time:.2f}s"
            }
        }
        
        # 根据音乐生成结果调整日志级别
        if music_result.get("success"):
            logger.info(f"{duration}秒音乐生成成功: {mansion_info['mansion']} -> {element}")
        else:
            logger.warning(f"{duration}秒音乐生成部分成功（参数生成成功，音频生成失败）: {mansion_info['mansion']} -> {element}")
            logger.warning(f"音乐生成失败原因: {music_result.get('error', 'Unknown')}")
        
        return response
        
    except Exception as e:
        logger.error(f"音乐生成服务失败: {e}")
        raise HTTPException(
            status_code=500, 
            detail={
                "error": f"服务内部错误: {str(e)}",
                "error_type": "service_error",
                "timestamp": time.time()
            }
        )

@app.post("/api/generate_music_custom")
async def generate_custom_duration_music(request: CustomMusicRequest):
    """生成自定义时长的音乐"""
    try:
        logger.info(f"收到自定义时长音乐生成请求: {request}")
        
        # 验证时长范围
        if request.duration < 10 or request.duration > 180:
            raise HTTPException(
                status_code=400,
                detail="音乐时长必须在10-180秒之间"
            )
        
        start_time = time.time()
        
        # 获取天文信息
        mansion_info = calc_mansion(request.date, request.lat, request.lon)
        element = get_element(mansion_info['mansion'])
        instrument, mode = map_to_params(element)
        
        # 获取完整配置
        full_config = get_full_music_config(element, request.duration)
        
        # 创建增强型prompt
        enhanced_prompt = f"{instrument}, {mode}, {request.style}, {request.duration} seconds duration, complete musical piece with clear structure"
        
        # 生成音乐
        music_result = generate_music(instrument, mode, request.style, duration=request.duration)
        
        response = {
            "success": True,
            "astronomy": mansion_info,
            "parameters": {
                "element": element,
                "instrument": instrument,
                "mode": mode,
                "duration": request.duration,
                "enhanced_prompt": enhanced_prompt,
                "full_config": full_config
            },
            "music": music_result,
            "performance": {
                "total_time": f"{time.time() - start_time:.2f}s"
            }
        }
        
        logger.info(f"{request.duration}秒自定义音乐生成完成: {mansion_info['mansion']} -> {element}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"自定义音乐生成失败: {e}")
        raise HTTPException(
            status_code=500, 
            detail={
                "error": str(e),
                "timestamp": time.time()
            }
        )

# 音乐服务状态检查
@app.get("/api/music/status")
async def check_music_service():
    """检查外部音乐服务状态"""
    try:
        from modules.generation import check_music_service_status
        status = check_music_service_status()
        return {
            "success": True,
            "music_service": status,
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": time.time()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
