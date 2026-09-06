import sys
import base64
import requests
import time
from urllib.parse import unquote

def test_speed(url):
    try:
        start_time = time.time()
        # 仅请求头部，设置3秒超时，避免卡死
        response = requests.get(url, timeout=3, stream=True)
        if response.status_code == 200:
            return round((time.time() - start_time) * 1000) # 返回毫秒
    except:
        return 9999 # 失败返回极大值
    return 9999

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("未接收到数据")
        sys.exit(1)
        
    # 解析前端传来的 Base64 数据
    encoded_data = sys.argv[1]
    raw_text = base64.b64decode(encoded_data).decode('utf-8')
    
    lines = raw_text.strip().split('\n')
    valid_channels = []
    
    print("开始测速...")
    for line in lines:
        if ',' not in line:
            valid_channels.append(line) # 保留分类标题，如 "央视频道,#genre#"
            continue
            
        name, url = line.split(',', 1)
        speed = test_speed(url)
        
        if speed < 9999:
            valid_channels.append((name, url, speed))
            print(f"✅ {name} 速度: {speed}ms")
        else:
            print(f"❌ {name} 失效或超时")

    # 按速度排序（只针对有效频道，忽略分类标签）
    sorted_channels = []
    for item in valid_channels:
        if isinstance(item, str):
            sorted_channels.append(item)
        else:
            sorted_channels.append(item)
            
    # 将排序后的结果写入文件
    with open('result.txt', 'w', encoding='utf-8') as f:
        for item in sorted_channels:
            if isinstance(item, str):
                f.write(item + '\n')
            else:
                f.write(f"{item[0]},{item[1]}\n")
                
    print("测速完成，结果已保存至 result.txt")
