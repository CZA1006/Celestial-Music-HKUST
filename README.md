# 🌌 天文音乐生成系统 (Celestial Music Generator)

基于中国传统二十八星宿和五行理论的智能音乐生成系统，将天象数据转化为独特的音乐作品。

## ✨ 项目特色

- 🏺 **古典界面设计** - 青铜环时间选择器，古代天文仪器风格
- 🌙 **二十八星宿系统** - 完整的传统中国天文学支持
- 🎵 **智能音乐生成** - 基于五行理论的专业音乐创作
- 🌍 **精确天文计算** - 基于真实天体数据的高精度计算
- 📱 **跨平台支持** - 响应式设计，支持电脑、平板、手机

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 现代浏览器 (Chrome 80+, Firefox 75+, Safari 13+)

### 安装步骤

1. **克隆项目**
```bash
git clone <your-repository-url>
cd CELESTIAL-MUSIC-HKUST
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行后端服务**
```bash
python backend_app.py
```

4. **访问系统**

   打开浏览器访问：`http://localhost:8000/static/index.html`

## 📁 项目结构

```
CELESTIAL-MUSIC-HKUST/
├── modules/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── astronomy.py      # 天文计算模块
│   ├── generation.py     # 音乐生成模块
│   ├── mapping.py        # 音乐参数映射
│   └── wuxing.py         # 五行映射系统
├── static/
│   └── index.html        # 前端界面
├── backend_app.py        # FastAPI主应用
├── requirements.txt      # 依赖包列表
└── README.md            # 项目说明文档
```

## 🎯 功能模块

### 天文计算 (astronomy.py)
- 精确的月亮黄经计算
- 二十八星宿位置判定
- 基于Astropy的专业天文算法
- 支持任意时间和地点的天象计算

### 五行映射 (wuxing.py)
- 传统四象七宿分配
- 东方青龙七宿 → 木
- 南方朱雀七宿 → 火
- 西方白虎七宿 → 金
- 北方玄武七宿 → 水

### 音乐生成 (generation.py)
- 调用外部音乐生成API (`https://yue-inst.ngrok.app`)
- 支持45秒完整音乐作品
- 智能重试机制和错误处理
- 多种音乐风格支持

### 参数映射 (mapping.py)
- 五行到音乐参数的专业转换
- 乐器选择：弦乐、管乐、打击乐等
- 调式映射：多里安、弗里吉亚等教会调式
- 节拍和情绪的智能匹配

## 🔧 API接口

### 计算天文数据
```http
POST /api/calculate
Content-Type: application/json

{
    "datetime": "2024-01-15T20:30:00",
    "latitude": 22.3964,
    "longitude": 114.1095
}
```

**返回示例：**
```json
{
    "mansion": "角",
    "element": "Wood",
    "moon_ecliptic_lon": 127.45,
    "timestamp": "2024-01-15T20:30:00"
}
```

### 生成音乐
```http
POST /api/generate-music
Content-Type: application/json

{
    "mansion": "角",
    "element": "Wood",
    "duration": 45,
    "style": "cinematic, ethereal"
}
```

### 获取所有星宿信息
```http
GET /api/mansions
```

### 健康检查
```http
GET /api/health
```

## 🎨 使用指南

### 1. 时间选择
- 使用古典青铜环界面选择时间
- 四层嵌套环：年、月、日、时辰
- 支持拖拽滑动和点击选择
- 显示传统天干地支和现代时间

### 2. 位置选择
- 点击3D地球模型选择观测位置
- 支持拖拽旋转查看不同区域
- 精确获取经纬度坐标
- 显示主要城市标记

### 3. 星图查看
- 基于选定时间和位置的真实星空
- 完整的二十八星宿标注和连线
- 四象颜色区分（青龙、朱雀、白虎、玄武）
- 月亮位置实时高亮显示
- 星等系统显示恒星亮度

### 4. 音乐生成
- 自动计算月亮在二十八星宿中的位置
- 基于五行理论生成音乐参数
- 构建专业音乐提示词
- 调用API生成45秒完整音乐作品
- 支持在线播放和下载

## ⚙️ 配置说明

### 主要配置参数

```python
# backend_app.py 中的配置
MUSIC_API_URL = "https://yue-inst.ngrok.app"
DEFAULT_LATITUDE = 22.3964   # 香港
DEFAULT_LONGITUDE = 114.1095
SERVER_PORT = 8000
CORS_ORIGINS = ["*"]
```

### 音乐生成参数

```python
# generation.py 中的配置
MUSIC_API_CONFIG = {
    "base_url": "https://yue-inst.ngrok.app",
    "timeout": 120,
    "max_retries": 2,
    "retry_delay": 3
}
```

## 🔍 故障排除

### 常见问题解决

**1. 端口被占用**
```bash
# 查看端口占用
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# 或修改backend_app.py中的端口号
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**2. 依赖安装失败**
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用conda
conda install --file requirements.txt
```

**3. 音乐生成超时或失败**
- 检查网络连接状态
- 确认 `https://yue-inst.ngrok.app` 服务可用
- 查看控制台错误日志
- 尝试减少音乐时长 (duration)

**4. 天文计算错误**
```python
# 检查时间格式 (必须是ISO 8601格式)
"2024-01-15T20:30:00"  # 正确
"2024/01/15 20:30:00"  # 错误

# 检查经纬度范围
latitude: -90 到 90
longitude: -180 到 180
```

**5. 前端页面无法访问**
- 确认后端服务已启动
- 检查防火墙设置
- 尝试访问 `http://127.0.0.1:8000/static/index.html`

## 🌟 技术栈

### 后端技术
- **FastAPI** - 现代Python Web框架
- **Astropy** - 专业天文计算库
- **Requests** - HTTP客户端
- **Uvicorn** - ASGI服务器
- **Pydantic** - 数据验证和序列化

### 前端技术
- **HTML5/CSS3** - 现代Web标准
- **JavaScript ES6+** - 原生JavaScript
- **Three.js** - 3D渲染引擎
- **WebGL** - 硬件加速渲染

### 核心算法
- **月亮位置计算** - 基于JPL DE405星历表
- **坐标系转换** - 赤道坐标系到黄道坐标系
- **五行映射** - 传统中国天文学理论
- **音乐参数生成** - 基于教会调式理论

## 📊 系统架构

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   用户界面   │ -> │   FastAPI后端    │ -> │   天文计算模块   │
│  (Web前端)  │    │  (API路由)      │    │  (astronomy.py) │
└─────────────┘    └──────────────────┘    └─────────────────┘
                            │                        │
                            v                        v
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   音乐输出   │ <- │   音乐生成API    │ <- │   五行映射模块   │
│  (45秒音频)  │    │ (外部ngrok服务)  │    │  (wuxing.py)   │
└─────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔄 数据流程

1. **用户输入** → 时间 + 地理位置
2. **天文计算** → 月亮黄经位置
3. **星宿判定** → 确定二十八星宿
4. **五行映射** → 星宿转换为五行元素
5. **参数生成** → 五行转换为音乐参数
6. **提示词构建** → 生成音乐创作指令
7. **API调用** → 请求音乐生成服务
8. **音乐输出** → 返回音频文件

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- 遵循 PEP 8 Python代码规范
- 添加适当的注释和文档字符串
- 编写单元测试
- 更新相关文档

## 📈 性能优化

### 计算缓存
- 天文计算结果缓存 (1小时)
- 音乐参数映射缓存
- 静态资源CDN加速

### 并发处理
- 异步API调用
- 多线程天文计算
- 连接池管理

## 🔒 安全考虑

- API请求频率限制
- 输入参数验证
- 错误信息脱敏
- CORS跨域配置

## 📜 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- 项目维护者：[您的姓名]
- 邮箱：[您的邮箱]
- 项目地址：[项目GitHub链接]

## 🙏 致谢

- 感谢中国传统天文学的古代智慧
- 感谢 Astropy 天文计算库的开发团队
- 感谢 FastAPI 框架的优秀设计
- 感谢所有贡献者和测试用户
- 特别感谢香港科技大学的学术支持

## 📚 参考资料

- [中国古代二十八星宿](https://zh.wikipedia.org/wiki/二十八宿)
- [五行学说](https://zh.wikipedia.org/wiki/五行)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Astropy 天文计算](https://www.astropy.org/)
- [Three.js 3D库](https://threejs.org/)

---

*让古代天文智慧与现代音乐技术完美融合，创造独特的艺术体验* ✨

## 🌟 更新日志

### v1.0.0 (2024-01-15)
- ✅ 实现基础天文计算功能
- ✅ 完成二十八星宿映射系统
- ✅ 集成音乐生成API
- ✅ 构建青铜环用户界面
- ✅ 添加3D地球位置选择
- ✅ 实现星图可视化显示

### 计划中的功能
- 🔄 音乐风格自定义
- 🔄 历史音乐作品保存
- 🔄 社交分享功能
- 🔄 多语言界面支持
- 🔄 移动端原生应用

## 📋 Requirements.txt

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
astropy==5.3.4
requests==2.31.0
pydantic==2.5.0
python-multipart==0.0.6
pytz==2023.3
```

## 🛠️ 开发环境设置

### VS Code 推荐插件
- Python
- Python Docstring Generator
- GitLens
- Prettier
- Live Server

### 开发服务器
```bash
# 开发模式启动（自动重载）
uvicorn backend_app:app --reload --host 0.0.0.0 --port 8000

# 生产模式启动
gunicorn backend_app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker 部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "backend_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 测试

### 运行测试
```bash
# 安装测试依赖
pip install pytest pytest-asyncio httpx

# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_astronomy.py

# 生成测试覆盖率报告
pytest --cov=modules tests/
```

### 测试示例
```python
# tests/test_astronomy.py
import pytest
from modules.astronomy import calc_mansion

def test_calc_mansion():
    result = calc_mansion("2024-01-15T20:30:00", 22.3964, 114.1095)
    assert result["mansion"] in ["角", "亢", "氐", "房", "心", "尾", "箕"]
    assert result["element"] in ["Wood", "Fire", "Earth", "Metal", "Water"]
```
