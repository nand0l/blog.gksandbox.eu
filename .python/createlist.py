import time
import os

base_url = "https://main.d3na2i9ef1o07g.amplifyapp.com/docs/exams/SAP-C02/"
file_path = os.path.join(os.path.dirname(__file__), f"urlList-{int(time.time())}.txt")

with open(file_path, "w") as f:
    f.write("\n".join(f"{base_url}{i}" for i in range(1, 501)))
    f.write("\n")
