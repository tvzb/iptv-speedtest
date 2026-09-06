import sys
import base64
import requests
import time

def test_speed(url):
    try:
        start_time = time.time()
        # 仅请求头部，设置3秒超时避免 Actions 运行超时
        response = requests.get(url, timeout=3, stream=True)
        if response.status_code == 200:
            return round((time.time() - start_time) * 1000) 
    except:
        pass
    return 9999 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("未接收到数据")
        sys.exit(1)
        
    encoded_data = sys.argv[1]
    raw_text = base64.b64decode(encoded_data).decode('utf-8')
    lines = raw_text.strip().split('\n')
    
    cctv_channels = []
    weishi_channels = []
    other_channels = []
    
    # 新增：用于记录已处理过的链接，实现去重
    seen_urls = set()
    
    print("开始测速、去重与频道分类...")
    for line in lines:
        line = line.strip()
        if not line or '#genre#' in line:
            continue
            
        if ',' in line:
            name, url = line.split(',', 1)
            
            # 新增：去重逻辑，如果URL已存在则直接跳过
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            speed = test_speed(url)
            
            if speed < 9999:
                print(f"✅ {name} 速度: {speed}ms")
                # 依据频道名称精准归类
                if 'CCTV' in name.upper() or '央视' in name:
                    cctv_channels.append((name, url, speed))
                elif '卫视' in name:
                    weishi_channels.append((name, url, speed))
                else:
                    other_channels.append((name, url, speed))
            else:
                print(f"❌ {name} 失效或超时，已删除")

    # 对有效频道按速度（speed）进行升序排列
    cctv_channels.sort(key=lambda x: x[2])
    weishi_channels.sort(key=lambda x: x[2])
    other_channels.sort(key=lambda x: x[2])
            
    # 写入最终的 IPTV 播放列表文件
    with open('iptv.txt', 'w', encoding='utf-8') as f:
        if cctv_channels:
            f.write("央视频道,#genre#\n")
            for name, url, speed in cctv_channels:
                f.write(f"{name},{url}\n")
                
        if weishi_channels:
            f.write("卫视频道,#genre#\n")
            for name, url, speed in weishi_channels:
                f.write(f"{name},{url}\n")
                
        if other_channels:
            f.write("其他频道,#genre#\n")
            for name, url, speed in other_channels:
                f.write(f"{name},{url}\n")
                
    print("生成完毕，已输出为标准格式的 iptv.txt")
