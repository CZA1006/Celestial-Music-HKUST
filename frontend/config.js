// API配置
const CONFIG = {
    API_BASE: 'https://celestial-music-hkust-production.up.railway.app',
    
    // API端点
    ENDPOINTS: {
        ASTRONOMY_CALCULATE: '/api/astronomy/calculate',
        MUSIC_GENERATE: '/api/music/generate',
        HEALTH: '/api/health'
    }
};

// 导出配置
window.CONFIG = CONFIG;
