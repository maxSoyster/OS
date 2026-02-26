# Max Soyster Heinz 
# Fast Fetch Code 

# pip install certifi
import requests, certifi
import threading
from datetime import datetime

URL = "https://picsum.photos/300"

printers = 5 
printer_pool = threading.Semaphore(printers)
lock = threading.Lock()

def log(status,i):
    with lock:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"image{i}.jpg"

        with open("logger.txt", "a") as f:
            f.write(f"{timestamp} | {URL} | {filename} | {status}\n")

def create_image(i):
    # CRITICAL SECTION
    with printer_pool:
        status = ""
        for v in range(1,3):
            try:
                response = requests.get(URL, verify = certifi.where(), timeout=3)
                with open(f"image{i}.jpg","wb") as f:
                    f.write(response.content)
                status += "SUCCESS"

                print(f"Downloaded: {i}/100")
                log(status,i)

                return

            except requests.exceptions.Timeout:
                status += "TIMEOUT"
                log(status,i)
            except Exception:
                status += "FAILURE"
                log(status,i)
        status = f"RETRY {i+1}"
            


threads = []
for i in range(1,101):
    t = threading.Thread(target=create_image, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All done!")