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

    # --- Even More Edge/Error/Method Coverage ---

    @task(1)
    def put_update_user(self):
        # PUT /users/1 (should update user or return 404 if not supported)
        payload = {"name": "Updated Name", "job": "updated-job"}
        self.client.put("/users/1", json=payload, headers=self.common_headers, name="/users/1 [PUT]", catch_response=True)

    @task(1)
    def patch_update_user(self):
        # PATCH /users/1 (should partially update user or return 404 if not supported)
        payload = {"job": "patched-job"}
        self.client.patch("/users/1", json=payload, headers=self.common_headers, name="/users/1 [PATCH]", catch_response=True)

    @task(1)
    def delete_user(self):
        # DELETE /users/1 (should delete user or return 404 if not supported)
        self.client.delete("/users/1", headers=self.common_headers, name="/users/1 [DELETE]", catch_response=True)

    @task(1)
    def put_nonexistent_user(self):
        # PUT /users/9999 (should return 404)
        payload = {"name": "Ghost", "job": "none"}
        self.client.put("/users/9999", json=payload, headers=self.common_headers, name="/users/9999 [PUT]", catch_response=True)

    @task(1)
    def delete_nonexistent_user(self):
        # DELETE /users/9999 (should return 404)
        self.client.delete("/users/9999", headers=self.common_headers, name="/users/9999 [DELETE]", catch_response=True)

    @task(1)
    def post_to_resource_list(self):
        # POST /resources (invalid method, should return 404 or 405)
        payload = {"name": "Invalid Resource"}
        self.client.post("/resources", json=payload, headers=self.common_headers, name="/resources [POST]", catch_response=True)

    @task(1)
    def get_on_post_only(self):
        # GET /users with POST-only logic (should return 200 or 405)
        # Already covered by get_user_list, but can add POST-only endpoint if available
        pass

    @task(1)
    def malformed_json_post(self):
        # POST /users with malformed JSON (should return 400)
        malformed_json = '{"name": "Bad JSON", "job": "broken"'  # missing closing }
        self.client.post("/users", data=malformed_json, headers=self.common_headers, name="/users_malformed", catch_response=True)

    @task(1)
    def missing_content_type_header(self):
        # POST /users with missing Content-Type header (should return 400)
        payload = {"name": "No Header", "job": "none"}
        self.client.post("/users", json=payload, name="/users_no_header", catch_response=True)

    @task(1)
    def large_payload_post(self):
        # POST /users with a very large payload (should return 413 or 400 if not supported)
        large_payload = {"name": "A" * 10000, "job": "B" * 10000}
        self.client.post("/users", json=large_payload, headers=self.common_headers, name="/users_large_payload", catch_response=True)
