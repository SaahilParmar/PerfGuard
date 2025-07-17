from locust import HttpUser, task, between
from utils.config_loader import load_config

# Load configuration values
config = load_config()
BASE_URL = config["base_url"]
ENDPOINTS = config["endpoints"]

class PerfGuardUser(HttpUser):
    wait_time = between(1, 3)  # Simulates user wait time between tasks

    @task(2)
    def get_user_list(self):
        self.client.get(ENDPOINTS["user_list"], name="/users")

    @task(1)
    def get_single_user(self):
        self.client.get(f"{ENDPOINTS['single_user']}/2", name="/users/2")

    @task(1)
    def post_new_user(self):
        payload = {
            "name": "PerfGuard Bot",
            "job": "performance-tester"
        }
        self.client.post(ENDPOINTS["create_user"], json=payload, name="/users [POST]")

    def on_start(self):
        # Optional: Called when a simulated user starts
        self.client.get("/", name="/")

    def on_stop(self):
        # Optional: Called when a simulated user stops
        pass
