from locust import HttpUser, task, between

from utils.config_loader import load_config

# Load configuration values with error handling and adapt to config.yaml structure
config = load_config()
try:
    BASE_URL = config.get("base_url") or config.get("host")
    endpoints_list = config["endpoints"]
except KeyError as e:
    raise KeyError(f"Missing required config key: {e}")

ENDPOINTS = {
    # Use local json-server endpoints
    "user_list": "/users",           # GET /users
    "single_user": "/users/1",       # GET /users/1
    "resource_list": "/resources",   # GET /resources
    "single_resource": "/resources/2", # GET /resources/2
    "create_user": "/users"
}

class PerfGuardUser(HttpUser):
    wait_time = between(1, 3)  # Simulates user wait time between tasks



    def on_start(self):
        # No API key needed for local json-server
        self.common_headers = {
            "Content-Type": "application/json"
        }
        self.client.get("/", headers=self.common_headers, name="/")



    @task(2)
    def get_user_list(self):
        # GET /users
        self.client.get(ENDPOINTS['user_list'], headers=self.common_headers, name="/users")

    @task(1)
    def get_single_user(self):
        # GET /users/1
        self.client.get(ENDPOINTS["single_user"], headers=self.common_headers, name="/users/1")

    @task(1)
    def get_resource_list(self):
        # GET /resources
        self.client.get(ENDPOINTS['resource_list'], headers=self.common_headers, name="/resources")

    @task(1)
    def get_single_resource(self):
        # GET /resources/2
        self.client.get(ENDPOINTS["single_resource"], headers=self.common_headers, name="/resources/2")

    @task(1)
    def post_new_user(self):
        payload = {
            "name": "PerfGuard Bot",
            "job": "performance-tester"
        }
        # POST /users
        self.client.post(ENDPOINTS["create_user"], json=payload, headers=self.common_headers, name="/users")

    def on_stop(self):
        # Optional: Called when a simulated user stops
        pass

    # --- Additional Test Coverage: Error and Edge Cases ---

    @task(1)
    def get_nonexistent_user(self):
        # GET /users/9999 (should return 404)
        self.client.get("/users/9999", headers=self.common_headers, name="/users/9999", catch_response=True)

    @task(1)
    def get_nonexistent_resource(self):
        # GET /resources/9999 (should return 404)
        self.client.get("/resources/9999", headers=self.common_headers, name="/resources/9999", catch_response=True)

    @task(1)
    def post_invalid_user(self):
        # POST /users with invalid payload (should return 400)
        invalid_payload = {"invalid_field": "no name or job"}
        self.client.post("/users", json=invalid_payload, headers=self.common_headers, name="/users_invalid", catch_response=True)

    @task(1)
    def get_users_with_query(self):
        # GET /users?page=2 (edge: query param, should return 200 or 404 if not supported)
        self.client.get("/users?page=2", headers=self.common_headers, name="/users?page=2", catch_response=True)

    @task(1)
    def get_resources_with_query(self):
        # GET /resources?type=server (edge: query param, should return 200 or 404 if not supported)
        self.client.get("/resources?type=server", headers=self.common_headers, name="/resources?type=server", catch_response=True)
