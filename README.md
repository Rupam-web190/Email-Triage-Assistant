# Email Triage Assistant

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/Rupam-web190/Email-Triage-Assistant)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Rupam-web190/Email-Triage-Assistant/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

A production-ready, full-stack email triage assistant designed to process 50+ email threads simultaneously. Leveraging the proprietary **ScaleDown** compression algorithm, it reduces email content by up to 85% while maintaining context, enabling rapid decision-making through a modern, responsive social-media-style interface.

---

## ⚡ Quick Start (Run in 60 Seconds)

Get the application running locally in under a minute.

1.  **Clone & Install**
    ```bash
    git clone https://github.com/Rupam-web190/Email-Triage-Assistant.git
    cd Email-Triage-Assistant
    pip install -r backend/requirements.txt
    ```

2.  **Launch**
    *Terminal 1 (Backend, optimized on Windows):*
    ```bash
    scripts\start_server.bat
    ```
    *Alternative (cross-platform dev server):*
    ```bash
    python backend/app.py
    ```
    *Terminal 2 (Frontend):*
    ```bash
    python -m http.server 8000 --directory frontend
    ```

3.  **Explore**
    Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📚 Table of Contents
- [Features](#-features)
- [Installation & Configuration](#-installation--configuration)
- [Usage Guide](#-usage-guide)
- [Architecture](#-architecture)
- [Contributing](#-contributing)
- [Maintainers](#-maintainers)
- [License](#-license)

---

## ✨ Features

-   **ScaleDown Engine**: Compresses email threads by 85% for faster reading.
-   **Smart Triage**: Auto-categorizes emails (Urgent, Action, Newsletter) using a 5-point priority algorithm.
-   **Infinite Scroll Feed**: Social-media style interface for seamless browsing of large inboxes.
-   **Security First**: Built-in sanitization for EML files to prevent XSS attacks.
-   **Analytics Dashboard**: Track time saved and processing metrics.
-   **Dark/Light Mode**: Adaptive UI for any environment.

---

## 🛠 Installation & Configuration

<details>
<summary><strong>Click to expand detailed installation steps</strong></summary>

### Prerequisites
-   Python 3.8 or higher
-   Git

### Step-by-Step Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Rupam-web190/Email-Triage-Assistant.git
    cd Email-Triage-Assistant
    ```

2.  **Create Virtual Environment (Recommended)**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
    > **Tip:** If you see "Script is not signed" error on Windows, run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.

3.  **Install Dependencies**
    ```bash
    pip install -r backend/requirements.txt
    ```
    *Expected Output:* `Successfully installed flask flask-cors ...`

4.  **Verify Installation**
    Run the tests to ensure everything is set up correctly:
    ```bash
    python -m unittest discover tests
    ```
    *Expected Output:* `OK`

</details>

---

## 🚀 Usage Guide

<details>
<summary><strong>Mode 1: The Feed (Infinite Scroll)</strong></summary>

The default view presents your emails as a continuous social feed.
-   **Scroll** down to automatically load older threads.
-   **Interact** with emails: Like, Comment, or Archive directly from the card.
-   **Priority Indicators**: Look for Red (Urgent) or Yellow (Warning) badges.

</details>

<details>
<summary><strong>Mode 2: File Upload</strong></summary>

Manually process `.eml` files from your local machine.
1.  Click the **Upload** button in the sidebar.
2.  Select an `.eml` file (Max 10MB).
3.  The email is analyzed, sanitized, and added to your feed immediately.

> **Troubleshooting:** If upload fails, ensure the file extension is strictly `.eml` and the file is not corrupted. Check the backend console for specific error logs.

</details>

<details>
<summary><strong>Mode 3: Batch Processing</strong></summary>

Simulate processing 50+ threads at once.
1.  Navigate to **Batch Process** in the sidebar.
2.  Click **Start Batch**.
3.  Review the summary report of processed items and time saved.

</details>

---

## 🏗 Architecture

The project follows a modular full-stack architecture.

```text
Email-Triage-Assistant/
├── backend/                  # Flask REST API
│   ├── app.py                # Application Entry Point
│   ├── triage_engine.py      # Core Logic (ScaleDown & Priority)
│   ├── gmail_parser.py       # Data Ingestion
│   └── ...                   # Specialized Modules (Analytics, Replier)
├── frontend/                 # Vanilla JS SPA
│   ├── index.html            # Main Layout
│   ├── script.js             # Frontend Logic (API Calls, DOM)
│   └── style.css             # Responsive Design System
├── scripts/                  # Operational scripts
│   ├── start_server.bat      # Production-like server startup (Waitress)
│   └── demo_scenarios.py     # End-to-end demo runner
├── tests/                    # Unit Tests
└── test_cases/               # Sample Data (.eml files)
```

---

## Demo

### Triage Demo
[▶️ Watch Demo Video](demo/triage_demo.mp4)


## 🤝 Contributing

We welcome contributions! Please follow the **GitHub Flow**:

1.  **Fork** the repository.
2.  **Create a Branch** for your feature (`git checkout -b feature/AmazingFeature`).
3.  **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4.  **Push** to the branch (`git push origin feature/AmazingFeature`).
5.  **Open a Pull Request**.

### Guidelines
-   **Issues**: Check [Issues](https://github.com/Rupam-web190/Email-Triage-Assistant/issues) for available tasks.
-   **Code Style**: Ensure your code passes the existing unit tests (`python -m unittest discover tests`).

---

## 👥 Maintainers

| Name | Role | GitHub |
|------|------|--------|
| **Rupam Majumdar** | Lead Developer | [@Rupam-web190](https://github.com/Rupam-web190) |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
