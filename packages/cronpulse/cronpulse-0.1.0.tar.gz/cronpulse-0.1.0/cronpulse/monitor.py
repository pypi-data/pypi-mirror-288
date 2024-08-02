# cronpulse/monitor.py
import requests
from urllib.parse import urlencode
from datetime import datetime
import asyncio

class Monitor:
    def __init__(self, job_key, base_url="https://cronpulse.live"):
        self.job_key = job_key
        self.base_url = base_url

    def ping(self, state, message=""):
        endpoint = None
        query_params = {}

        if state == "run":
            endpoint = f"/api/run/{self.job_key}"
        elif state == "complete":
            endpoint = f"/api/complete/{self.job_key}"
        elif state == "failed":
            endpoint = f"/api/complete/{self.job_key}"
            query_params['failed'] = message or True
        else:
            raise ValueError(f"Invalid state: {state}")

        return self.send_request(endpoint, query_params)

    def send_request(self, endpoint, query_params=None):
        if query_params is None:
            query_params = {}

        url = f"{self.base_url}{endpoint}"
        if query_params:
            url += f"?{urlencode(query_params)}"

        print(f"📡 Sending request to: {url}")

        response = requests.get(url)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📬 Response body: {response.text}")

        response.raise_for_status()
        return response.text

def wrap(job_key, job_function):
    monitor = Monitor(job_key)
    start_time = datetime.now()

    async def wrapped_function():
        try:
            monitor.ping("run")
            await job_function()
            monitor.ping("complete")
        except Exception as e:
            print(f"❌ Job failed: {e}")
            monitor.ping("failed", message=str(e))
        finally:
            end_time = datetime.now()
            print(f"Job execution time: {(end_time - start_time).total_seconds()} seconds")

    return wrapped_function
