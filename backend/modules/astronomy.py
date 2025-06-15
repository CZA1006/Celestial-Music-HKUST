from astropy.time import Time
from astropy.coordinates import get_body, EarthLocation, BarycentricTrueEcliptic, ICRS
import astropy.units as u
import pytz
import logging
import numpy as np

logger = logging.getLogger(__name__)

# 28星宿按传统顺序
MANSIONS = [
    "角", "亢", "氐", "房", "心", "尾", "箕",  # 东方青龙
    "斗", "牛", "女", "虚", "危", "室", "壁",  # 北方玄武
    "奎", "娄", "胃", "昴", "毕", "觜", "参",  # 西方白虎
    "井", "鬼", "柳", "星", "张", "翼", "轸"   # 南方朱雀
]

def get_moon_position(timestamp, latitude, longitude):
    """
    获取月亮位置信息
    """
    try:
        # 创建时间对象
        if isinstance(timestamp, (int, float)):
            time = Time(timestamp, format='unix')
        else:
            time = Time(timestamp)
        
        # 创建位置对象
        location = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg)
        
        # 获取月亮位置
        moon = get_body("moon", time, location)
        
        # 转换到黄道坐标系
        moon_ecliptic = moon.transform_to(BarycentricTrueEcliptic(equinox=time))
        
        result = {
            'ra': float(moon.ra.deg),
            'dec': float(moon.dec.deg),
            'ecliptic_longitude': float(moon_ecliptic.lon.deg),
            'ecliptic_latitude': float(moon_ecliptic.lat.deg),
            'distance': float(moon.distance.km),
            'timestamp': time.iso
        }
        
        logger.info(f"月亮位置计算成功: 黄经={result['ecliptic_longitude']:.2f}°")
        return result
        
    except Exception as e:
        logger.error(f"月亮位置计算失败: {str(e)}")
        # 返回默认值，避免程序崩溃
        return {
            'ra': 0.0,
            'dec': 0.0,
            'ecliptic_longitude': 0.0,
            'ecliptic_latitude': 0.0,
            'distance': 384400.0,
            'timestamp': str(timestamp),
            'error': str(e)
        }

def calc_mansion(ecliptic_longitude):
    """
    根据黄经计算星宿
    """
    try:
        # 确保黄经在0-360度范围内
        lon = float(ecliptic_longitude) % 360
        
        # 每个星宿约占12.857度 (360/28)
        mansion_degree = 360.0 / 28
        mansion_index = int(lon / mansion_degree)
        
        # 确保索引在有效范围内
        mansion_index = max(0, min(mansion_index, len(MANSIONS) - 1))
        
        return MANSIONS[mansion_index]
        
    except Exception as e:
        logger.error(f"星宿计算失败: {str(e)}")
        return "角"  # 返回默认星宿

def get_all_mansions_positions(timestamp):
    """
    获取所有星宿的位置信息
    """
    try:
        positions = {}
        for i, mansion in enumerate(MANSIONS):
            # 计算每个星宿的大致黄经位置
            ecliptic_lon = i * (360.0 / 28)
            positions[mansion] = {
                'ecliptic_longitude': ecliptic_lon,
                'index': i
            }
        return positions
    except Exception as e:
        logger.error(f"星宿位置计算失败: {str(e)}")
        return {}