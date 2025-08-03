import requests
import os

# Dizi Ayarları
BASE_URL = "https://www.atv.com.tr/eskiya-dunyaya-hukumdar-olmaz/"
PROXY_PREFIX = "https://stream-extractor.koprulu.workers.dev/?url="
EXT = "&ext=mp4"
COVER_ART = "https://iaatv.tmgrup.com.tr/63e729/0/0/0/0/0/0?u=https://iatv.tmgrup.com.tr/2021/10/26/500x268/1635252493405.jpg"
CATEGORY = "EDHO"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
START_EPISODE = 1
END_EPISODE = 199

def get_last_episode():
    try:
        with open("last_episode.txt", "r") as f:
            return int(f.read().strip())
    except:
        return END_EPISODE

def check_episode(episode):
    try:
        test_url = f"{BASE_URL}{episode}-bolum/izle"
        headers = {"User-Agent": USER_AGENT}
        response = requests.head(f"{PROXY_PREFIX}{test_url}", headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False

def generate_m3u(end_episode):
    m3u_content = "#EXTM3U\n"
    
    for ep in range(START_EPISODE, end_episode + 1):
        stream_url = f"{PROXY_PREFIX}{BASE_URL}{ep}-bolum/izle{EXT}"
        m3u_content += f"""#EXTINF:-1 tvg-id="EDHO{ep}" tvg-name="Bölüm-{ep}" tvg-logo="{COVER_ART}" group-title="{CATEGORY}",EDHO Bölüm-{ep}
{stream_url}\n"""
    
    with open("edho.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    last_ep = get_last_episode()
    if check_episode(last_ep + 1):
        new_ep = last_ep + 1
        with open("last_episode.txt", "w") as f:
            f.write(str(new_ep))
        generate_m3u(new_ep)
    else:
        generate_m3u(last_ep)
