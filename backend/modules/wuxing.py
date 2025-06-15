MANSION_ELEMENT_MAP = {
    # 东方青龙七宿 - 木
    "角": "Wood", "亢": "Wood", "氐": "Wood", "房": "Wood",
    "心": "Wood", "尾": "Wood", "箕": "Wood",
    
    # 南方朱雀七宿 - 火  
    "井": "Fire", "鬼": "Fire", "柳": "Fire", "星": "Fire",
    "张": "Fire", "翼": "Fire", "轸": "Fire",
    
    # 西方白虎七宿 - 金
    "奎": "Metal", "娄": "Metal", "胃": "Metal", "昴": "Metal", 
    "毕": "Metal", "觜": "Metal", "参": "Metal",
    
    # 北方玄武七宿 - 水
    "斗": "Water", "牛": "Water", "女": "Water", "虚": "Water",
    "危": "Water", "室": "Water", "壁": "Water"
}

def get_element(mansion: str) -> str:
    return MANSION_ELEMENT_MAP.get(mansion, "Wood")
