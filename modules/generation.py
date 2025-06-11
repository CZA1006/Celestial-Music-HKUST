import requests
import logging
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# 音乐生成API配置
MUSIC_API_CONFIG = {
    "base_url": "https://yue-inst.ngrok.app",
    "timeout": 120,  # 稍微增加超时时间，因为45秒音乐需要更长生成时间
    "max_retries": 2,
    "retry_delay": 3
}

def generate_music(instrument: str, mode: str, style: str = "cinematic, ethereal", model: str = "auto", duration: int = 45) -> Dict:
    """
    调用外部音乐生成API，生成指定长度的音乐
    
    Args:
        instrument: 乐器类型
        mode: 音乐调式  
        style: 音乐风格
        model: 生成模型
        duration: 音乐时长（秒）
    """
    # 构建包含时长的详细prompt
    prompt = f"{instrument}, {mode}, {style}, {duration} seconds duration, complete musical piece"
    
    payload = {
        "prompt": prompt,
        "model": model,
        "duration": duration,  # API参数中也指定时长
        "quality": "high",
        "style": style,
        "instrument": instrument,
        "mode": mode
    }
    
    logger.info(f"开始生成{duration}秒音乐: {payload}")
    
    # 尝试多次请求
    for attempt in range(MUSIC_API_CONFIG["max_retries"] + 1):
        try:
            logger.info(f"第{attempt + 1}次尝试调用音乐API (目标时长: {duration}秒)...")
            
            response = requests.post(
                f"{MUSIC_API_CONFIG['base_url']}/generate",
                json=payload,
                timeout=MUSIC_API_CONFIG["timeout"],
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "28-Xiu-Music-Generator/1.0"
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"音乐生成API调用成功: {result.get('task_id', 'N/A')}")
            
            return {
                "success": True,
                "download_url": result.get("download_url"),
                "pdf_download_url": result.get("pdf_download_url"),
                "task_id": result.get("task_id"),
                "prompt": prompt,
                "duration": duration,
                "status": result.get("status", "completed"),
                "generation_time": result.get("generation_time"),
                "api_response_time": f"{time.time():.2f}"
            }
            
        except requests.exceptions.Timeout as e:
            logger.warning(f"第{attempt + 1}次请求超时 (超时时间: {MUSIC_API_CONFIG['timeout']}秒): {e}")
            
            if attempt < MUSIC_API_CONFIG["max_retries"]:
                logger.info(f"等待{MUSIC_API_CONFIG['retry_delay']}秒后重试...")
                time.sleep(MUSIC_API_CONFIG["retry_delay"])
                continue
            else:
                logger.error(f"音乐生成API超时，已重试{MUSIC_API_CONFIG['max_retries']}次")
                return {
                    "success": False,
                    "error": f"音乐生成服务响应超时 (目标时长: {duration}秒)",
                    "error_type": "timeout",
                    "timeout_duration": MUSIC_API_CONFIG["timeout"],
                    "retry_attempts": attempt + 1,
                    "prompt": prompt,
                    "requested_duration": duration,
                    "suggestions": [
                        f"生成{duration}秒音乐可能需要更长时间",
                        "外部音乐服务可能暂时不可用",
                        "建议稍后重试或尝试较短的音乐长度"
                    ]
                }
                
        except requests.exceptions.ConnectionError as e:
            logger.error(f"连接音乐API失败: {e}")
            return {
                "success": False,
                "error": "无法连接到音乐生成服务",
                "error_type": "connection_error", 
                "prompt": prompt,
                "requested_duration": duration
            }
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"音乐API HTTP错误: {e}")
            return {
                "success": False,
                "error": f"音乐服务返回错误: {e}",
                "error_type": "http_error",
                "prompt": prompt,
                "requested_duration": duration
            }
            
        except Exception as e:
            logger.error(f"音乐生成过程中发生未知错误: {e}")
            return {
                "success": False,
                "error": f"未知错误: {str(e)}",
                "error_type": "unknown_error",
                "prompt": prompt,
                "requested_duration": duration
            }

def generate_music_with_custom_duration(instrument: str, mode: str, style: str = "cinematic, ethereal", duration: int = 45) -> Dict:
    """
    生成自定义时长的音乐
    """
    # 根据不同时长调整prompt
    if duration <= 30:
        duration_desc = "short"
    elif duration <= 60:
        duration_desc = "medium length"
    else:
        duration_desc = "extended"
    
    enhanced_style = f"{style}, {duration_desc} composition"
    
    return generate_music(instrument, mode, enhanced_style, duration=duration)
