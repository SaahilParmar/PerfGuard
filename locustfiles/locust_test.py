from locust import HttpUser, task, between

from utils.config_loader import load_config

# Load configuration values with error handling and adapt to config.yaml structure
config = load_config()
try:
    BASE_URL = config.get("base_url") or config.get("host")
    endpoints_list = config["endpoints"]
except KeyError as e:
    raise KeyError(f"Missing required config key: {e}")

# Convert endpoints list to a dict for easy access by name
ENDPOINTS = {
    "user_list": next((ep["path"] for ep in endpoints_list if ep["method"] == "GET" and "/users" in ep["path"]), "/api/v1/users"),
    "single_user": next((ep["path"] for ep in endpoints_list if ep["method"] == "DELETE" and "/users/2" in ep["path"]), "/api/v1/users/2"),
    "create_user": next((ep["path"] for ep in endpoints_list if ep["method"] == "POST" and "/users" in ep["path"]), "/api/v1/users"),
}

class PerfGuardUser(HttpUser):
    wait_time = between(1, 3)  # Simulates user wait time between tasks

    @task(2)
    def get_user_list(self):
        self.client.get(ENDPOINTS["user_list"], name="/users")

    @task(1)
    def get_single_user(self):
        self.client.get(ENDPOINTS["single_user"], name="/users/2")

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
