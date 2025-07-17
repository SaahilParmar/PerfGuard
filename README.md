# 🚀 PerfGuard - Performance Testing Automation Framework

PerfGuard is a scalable and modular performance testing framework built using **Locust**, designed to automate load testing, analyze system behavior under stress, and generate insightful reports. It supports YAML-based configuration, CI/CD integration, and extensible user scenarios.

---

## 📁 Project Structure

perfguard/ ├── config/ │   └── config.yaml               # Load test configurations ├── locustfiles/ │   └── user_behavior.py          # Locust task definitions ├── utils/ │   └── config_loader.py          # YAML config loader ├── reports/ │   └── logs/                     # Execution logs and output ├── tests/ │   └── test_config_loader.py     # Unit tests ├── requirements.txt              # Project dependencies ├── README.md                     # Project documentation ├── troubleshooting_log.md        # Common errors and fixes └── .gitignore

---

## ⚙️ Features

- ✅ YAML-based config for test duration, users, spawn rate, host
- ✅ Modular structure for easy test case expansion
- ✅ Automated reports
- ✅ GitHub Actions CI/CD ready
- ✅ Clean and readable logs
- ✅ Easily extendable for APIs, web UIs, or socket services

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/perfguard.git
cd perfguard

2. Create a Virtual Environment

python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows

3. Install Dependencies

pip install -r requirements.txt


4. Update Config File

PerfGuard supports two configuration systems:

- `config/config.yaml`: Main configuration for Locust test runs (used by Python scripts).
- `config.env`: Used by the shell script (`run_performance_test.sh`) for environment variable-based runs.

**Recommended:** Use `config/config.yaml` for most workflows. Ensure the following structure:

```yaml
host: "https://example.com"
users: 10
spawn_rate: 2
run_time: "1m"
endpoints:
  - path: "/api/v1/users"
    method: "GET"
    weight: 3
  - path: "/api/v1/users"
    method: "POST"
    weight: 2
    payload:
      name: "John Doe"
      job: "Engineer"
  - path: "/api/v1/users/2"
    method: "DELETE"
    weight: 1
```

If you use `run_performance_test.sh`, edit `config.env` accordingly:

```env
TARGET_HOST=https://your-api.com
USERS=50
SPAWN_RATE=10
RUN_TIME=1m
```

**Note:** The Python Locust script expects `config/config.yaml` and will raise an error if required keys are missing. See Troubleshooting below for common issues.

----

🧪 Run Locust Tests

locust -f locustfiles/user_behavior.py --headless -u 10 -r 2 -t 1m --host https://example.com --csv=reports/logs/perf_results

> You can load values dynamically from config.yaml using config_loader.py




---

📈 Report Example (optional)

After test execution, you'll find:

reports/logs/perf_results_stats.csv
reports/logs/perf_results_failures.csv

You can convert to graphs or dashboards using tools like:

Excel

Pandas/Matplotlib

Allure (advanced)



---

✅ Run Unit Tests

pytest tests/test_config_loader.py


---

🧩 GitHub Actions CI/CD

This framework includes a CI pipeline (.github/workflows/locust.yml) that:

Installs dependencies

Validates YAML config

Runs unit tests

(Optional) Executes locust in headless mode



---


📚 Troubleshooting

**Config KeyError:**
If you see an error like `KeyError: 'base_url'` or `KeyError: 'endpoints'`, check that your `config/config.yaml` contains all required keys as shown above. The script now supports both `host` and `base_url` for flexibility.

More issues and solutions are documented in:
> troubleshooting_log.md




---

📌 Future Enhancements

[ ] Slack/Discord alert integration

[ ] Auto-trigger from Jenkins

[ ] Support for multiple environments

[ ] GraphQL & WebSocket performance testing



---

🛡️ License

This project is licensed under the MIT License.
© 2025 Saahil Parmar
