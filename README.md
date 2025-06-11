# 28星宿天体音乐生成器 🌟🎵

[![GitHub stars](https://img.shields.io/github/stars/CZA1006/Celestial-Music-HKUST?style=social)](https://github.com/CZA1006/Celestial-Music-HKUST/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/CZA1006/Celestial-Music-HKUST?style=social)](https://github.com/CZA1006/Celestial-Music-HKUST/network)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-brightgreen.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com)

基于传统中国天文学和五行理论的智能音乐生成系统，将古代星宿知识与现代AI技术完美融合。

## 🌌 项目简介

**28星宿天体音乐生成器**是一个创新的跨学科项目，它：

- 🏛️ **传承古典文化**：基于中国传统28星宿天文学体系
- 🧠 **融合现代AI**：利用先进的音乐生成算法
- 🎭 **五行音乐理论**：根据星宿对应的五行属性生成独特音乐
- 🌍 **精确天文计算**：实时计算任意时间地点的月亮星宿位置
- 🎵 **个性化创作**：每个时刻都能生成独一无二的音乐作品

## ✨ 核心功能

### 🕰️ 历史时间选择
- **日晷式交互界面**：古典与现代结合的时间选择体验
- **历史时间支持**：可选择1950-2025年间任意时刻
- **精美视觉设计**：深空星域背景配合古铜质感UI

### 🌍 全球位置定位
- **3D地球交互**：可旋转的三维地球模型
- **精确坐标选择**：支持全球任意位置的经纬度选择
- **城市快速定位**：预设全球主要城市一键选择

### 🌟 28星宿星图可视化
- **完整星图展示**：真实的28星宿分布和连线
- **四象分类显示**：东青龙、南朱雀、西白虎、北玄武
- **实时天体追踪**：高亮显示月亮当前所在星宿
- **交互式控制**：旋转、缩放、标注显示等多种控制选项

### 🎼 智能音乐生成
- **五行音乐映射**：
  - 🌿 **木**：弦乐器、自然调式、流畅节奏
  - 🔥 **火**：铜管乐器、激烈调式、快速节拍
  - 🏔️ **土**：钢琴、稳定调式、扎实节奏
  - ⚡ **金**：钟声、清脆调式、明亮音色
  - 🌊 **水**：流动乐器、柔和调式、缓慢节拍
- **可定制参数**：时长、风格、乐器组合
- **高质量输出**：45秒完整音乐作品

## 🚀 技术栈

### 后端技术
- **FastAPI**: 高性能Python Web框架
- **Astropy**: 专业天文计算库
- **Pydantic**: 数据验证和序列化
- **PyTZ**: 时区处理

### 前端技术
- **Three.js**: 3D图形渲染
- **HTML5 Canvas**: 2D图形绘制
- **现代JavaScript**: ES6+语法
- **响应式设计**: 适配多种设备

### 核心算法
- **天文计算**: 精确的月亮位置计算
- **星宿定位**: 28星宿划分算法
- **五行映射**: 传统五行理论数字化
- **音乐生成**: AI驱动的音乐创作

## 📦 安装指南

### 环境要求
- Python 3.8+
- Node.js (可选，用于前端开发)

### 快速开始

1. **克隆项目**
```bash
git clone https://github.com/CZA1006/Celestial-Music-HKUST.git
cd Celestial-Music-HKUST
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **创建项目结构**
```bash
mkdir -p static modules
```

4. **配置文件**
将前端文件放入`static`目录：
```
static/
├── time-selector.html
├── location-selector.html
└── starmap.html
```

将后端模块放入`modules`目录：
```
modules/
├── __init__.py
├── astronomy.py
├── wuxing.py
├── mapping.py
└── generation.py
```

5. **启动服务**
```bash
uvicorn backend_app:app --reload
```

6. **访问应用**
打开浏览器访问 `http://localhost:8000`

## 📖 使用指南

### 第一步：选择时间 🕰️
1. 通过日晷式界面选择年份（1950-2025）
2. 旋转圆环选择月份和日期
3. 设置具体的小时
4. 确认时间选择

### 第二步：选择位置 🌍
1. 拖拽旋转3D地球找到目标位置
2. 点击地球表面选择精确坐标
3. 或使用快速城市选择功能
4. 确认地理位置

### 第三步：生成音乐 🎵
1. 查看实时计算的天文信息
2. 观察28星宿星图和月亮位置
3. 查看根据五行理论匹配的音乐参数
4. 点击生成音乐，享受独特的星宿音乐

## 🔬 科学原理

### 天文计算
- 使用Astropy库进行精确的天体位置计算
- 考虑地球自转、月球轨道等因素
- 支持任意历史时间和地理位置

### 传统文化
- **28星宿系统**：中国古代天文学的重要组成部分
- **四象理论**：东青龙、南朱雀、西白虎、北玄武
- **五行学说**：金木水火土的相生相克关系

### 音乐理论
- **调式映射**：不同五行对应不同音乐调式
- **乐器选择**：根据五行属性选择合适乐器
- **节奏设计**：五行特性影响音乐节奏和风格

## 📊 API文档

### 天文计算API
```http
POST /api/astronomy/calculate
Content-Type: application/json

{
  "time_data": {
    "year": 2025,
    "month": 6,
    "day": 11,
    "hour": 15
  },
  "location_data": {
    "latitude": 22.3193,
    "longitude": 114.1694,
    "address": "香港"
  }
}
```

### 音乐生成API
```http
POST /api/music/generate?instrument=Piano&mode=Major&duration=45
```

更多API详情请访问：`http://localhost:8000/docs`

## 🤝 贡献指南

我们欢迎各种形式的贡献！

### 如何贡献
1. Fork 这个项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

### 贡献领域
- 🐛 Bug修复和性能优化
- ✨ 新功能开发
- 📚 文档完善
- 🎨 UI/UX改进
- 🧪 测试覆盖
- 🌍 国际化支持

## 📝 开发路线图

### v2.0 (计划中)
- [ ] 更多星宿系统支持（西方星座）
- [ ] 音乐风格扩展（民族音乐、现代音乐）
- [ ] 移动端优化
- [ ] 用户系统和作品保存

### v3.0 (远期规划)
- [ ] 机器学习优化音乐生成
- [ ] 实时音乐演奏功能
- [ ] 社区分享平台
- [ ] VR/AR体验

## 🏆 致谢

### 技术支持
- [Astropy](https://www.astropy.org/) - 天文计算
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架
- [Three.js](https://threejs.org/) - 3D图形渲染

### 文化顾问
- 中国传统天文学研究团队
- 五行音乐理论专家
- 文化遗产保护组织

### 特别感谢
感谢所有为传统文化传承和现代技术融合做出贡献的开发者和研究者。

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源协议。

## 📞 联系我们

- **项目主页**: [GitHub](https://github.com/CZA1006/Celestial-Music-HKUST)
- **问题反馈**: [Issues](https://github.com/CZA1006/Celestial-Music-HKUST/issues)
- **讨论交流**: [Discussions](https://github.com/CZA1006/Celestial-Music-HKUST/discussions)

---

<div align="center">

**让古老的智慧奏响现代的乐章** 🌟

如果这个项目对您有帮助，请给我们一个 ⭐️ Star！

</div>