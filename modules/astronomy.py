from astropy.time import Time
from astropy.coordinates import get_moon, EarthLocation, BarycentricTrueEcliptic, SkyCoord, AltAz
import astropy.units as u
import pytz
import logging

logger = logging.getLogger(__name__)

# 28星宿按传统顺序
MANSIONS = [
    "角", "亢", "氐", "房", "心", "尾", "箕",  # 东方青龙
    "斗", "牛", "女", "虚", "危", "室", "壁",  # 北方玄武
    "奎", "娄", "胃", "昴", "毕", "觜", "参",  # 西方白虎
    "井", "鬼", "柳", "星", "张", "翼", "轸"   # 南方朱雀
]

# 星宿恒星数据
XIU_STARS = {
    "角": [
        {"name": "角宿一", "hip": 65474, "ra": 201.298, "dec": -11.161, "mag": 0.97},
        {"name": "角宿二", "hip": 63090, "ra": 213.915, "dec": -0.596, "mag": 3.38}
    ],
    "心": [
        {"name": "心宿一", "hip": 78820, "ra": 243.587, "dec": -28.216, "mag": 2.89},
        {"name": "心宿二", "hip": 80763, "ra": 247.352, "dec": -26.432, "mag": 0.96},
        {"name": "心宿三", "hip": 80112, "ra": 245.297, "dec": -25.592, "mag": 2.70}
    ],
    "昴": [
        {"name": "昴宿一", "hip": 17702, "ra": 56.871, "dec": 24.105, "mag": 5.65},
        {"name": "昴宿二", "hip": 17847, "ra": 57.290, "dec": 24.367, "mag": 4.30},
        {"name": "昴宿三", "hip": 17499, "ra": 56.217, "dec": 24.283, "mag": 4.18}
    ]
}

def calc_mansion(date: str = None, lat: float = 22.3964, lon: float = 114.1095):
    try:
        tz = pytz.timezone("Asia/Hong_Kong")
        
        if date:
            try:
                dt = Time(date).to_datetime()
                dt = tz.localize(dt)
            except:
                dt = tz.localize(Time.now().to_datetime())
        else:
            dt = tz.localize(Time.now().to_datetime())
        
        t = Time(dt)
        loc = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)
        moon = get_moon(t, loc)
        ecl = moon.transform_to(BarycentricTrueEcliptic())
        lon_deg = ecl.lon.degree
        
        mansion_width = 360.0 / 28
        mansion_index = int(lon_deg / mansion_width) % 28
        mansion = MANSIONS[mansion_index]
        
        return {
            "mansion": mansion,
            "mansion_index": mansion_index,
            "moon_ecliptic_lon": lon_deg,
            "timestamp": t.iso,
            "local_time": dt.isoformat()
        }
    except Exception as e:
        logger.error(f"计算失败: {e}")
        return {
            "mansion": "角",
            "mansion_index": 0,
            "moon_ecliptic_lon": 0.0,
            "timestamp": Time.now().iso,
            "error": str(e)
        }

def get_all_mansions_positions(date: str = None, lat: float = 22.3964, lon: float = 114.1095):
    try:
        tz = pytz.timezone("Asia/Hong_Kong")
        
        if date:
            try:
                dt = Time(date).to_datetime()
                dt = tz.localize(dt)
            except:
                dt = tz.localize(Time.now().to_datetime())
        else:
            dt = tz.localize(Time.now().to_datetime())
        
        t = Time(dt)
        loc = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)
        altaz_frame = AltAz(obstime=t, location=loc)
        
        all_positions = {}
        
        for mansion_name, stars in XIU_STARS.items():
            mansion_positions = []
            
            for star in stars:
                try:
                    coord = SkyCoord(ra=star["ra"]*u.deg, dec=star["dec"]*u.deg, frame='icrs')
                    altaz_coord = coord.transform_to(altaz_frame)
                    
                    star_info = {
                        "name": star["name"],
                        "hip": star.get("hip"),
                        "ra": star["ra"],
                        "dec": star["dec"],
                        "alt": altaz_coord.alt.degree,
                        "az": altaz_coord.az.degree,
                        "magnitude": star["mag"],
                        "visible": altaz_coord.alt.degree > 0
                    }
                    mansion_positions.append(star_info)
                except:
                    continue
            
            all_positions[mansion_name] = mansion_positions
        
        return {
            "timestamp": t.iso,
            "observer": {"lat": lat, "lon": lon},
            "mansions": all_positions
        }
    except Exception as e:
        return {"error": str(e), "mansions": {}}

def get_moon_position(date: str = None, lat: float = 22.3964, lon: float = 114.1095):
    try:
        tz = pytz.timezone("Asia/Hong_Kong")
        
        if date:
            try:
                dt = Time(date).to_datetime()
                dt = tz.localize(dt)
            except:
                dt = tz.localize(Time.now().to_datetime())
        else:
            dt = tz.localize(Time.now().to_datetime())
        
        t = Time(dt)
        loc = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)
        moon = get_moon(t, loc)
        altaz_frame = AltAz(obstime=t, location=loc)
        moon_altaz = moon.transform_to(altaz_frame)
        ecl = moon.transform_to(BarycentricTrueEcliptic())
        
        return {
            "ra": moon.ra.degree,
            "dec": moon.dec.degree,
            "alt": moon_altaz.alt.degree,
            "az": moon_altaz.az.degree,
            "ecliptic_lon": ecl.lon.degree,
            "ecliptic_lat": ecl.lat.degree,
            "visible": moon_altaz.alt.degree > 0,
            "timestamp": t.iso
        }
    except Exception as e:
        return {"error": str(e)}
