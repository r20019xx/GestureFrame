# GestureFrame

## Overview

**GestureFrame** is a Django‑based web interface that streams webcam frames to a PyTorch / YOLOv5 inference
service and overlays recognised sign‑language gestures in real time.

**Highlights**

- **Real‑time video capture** (HTML5 `<canvas>`)
- **Server‑side inference** with PyTorch + YOLOv5
- **REST API** via Django REST Framework
- **Docker‑first** workflow for local dev & production
- **CI/CD**: GitHub Actions → GHCR (or Docker Hub) → DigitalOcean App Platform

---

## Requirements

| Runtime | Version                            |
|---------|------------------------------------|
| Python  | = 3.11.10                          |
| Docker  | ≥ 20.10 (optional but recommended) |

- Python version pinned in **`runtime.txt`** for deployment platforms (e.g., `python-3.11.10`).
- Full dependencies listed in **`requirements.txt`** (e.g., `django==5.1.7`, `torch==2.6.0`, `torchvision==0.21.0`).

Use `pip install -r requirements.txt` after creating a virtual environment.

---

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/r20019xx/gesture-frame.git
cd GestureFrame

# 2. Initialize submodules
git submodule update --init --recursive

# 3. Virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configuration
cp .env.example .env            # Edit secrets, DB URL, etc.

# 6. Database & static files
python manage.py migrate
python manage.py collectstatic --noinput

# 7. Run development server
python manage.py runserver      # http://localhost:8000/
```

---

## Docker

```bash
docker build -t gesture-frame:latest .
docker run -d -p 8000:8000 --env-file .env gesture-frame:latest
```

Or with **Docker Compose**:

```bash
docker-compose up --build
```

---

## CI/CD

A single workflow file at `.github/workflows/docker-publish.yml` performs:

1. **Checkout** the repository
2. **Build & push** a multi‑arch Docker image to GHCR

---

## Project Layout

```
GestureFrame/
├── .github/
│   └── workflows/
│       └── docker-publish.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── .gitmodules
├── api/
├── backend_ml_model/
│   ├── yolov5/
│   ├── best.pt
│   └── main.py
├── dataset/
├── DjangoProject/
├── page/
├── submodule/
├── templates/
├── users/
├── db.sqlite3
├── Dockerfile
├── manage.py
├── README.md
├── requirements.txt
├── runtime.txt
└── docker-compose.yml  # optional
```

---

## Testing

### Unit Tests

Run all unit tests with:

```bash
python manage.py test
```

All tests are expected to pass.
> **Note:**  
> During the test run you may see output like:
> ```
> Simulated error
> ```
> This is intentional. Some tests use:
> ```python
> @patch(
>   'django.contrib.auth.models.User.objects.create_user',
>   side_effect=Exception("Simulated error")
> )
> ```
> to simulate a user‐creation failure and verify your error‐handling logic. Seeing “Simulated error” in the console *
*does not** indicate a test failure—it means the test successfully triggered and handled the simulated exception.

Unit test files are located in each app’s `tests.py` (for example, `api/tests.py` and `users/tests.py`).

### Acceptance Tests

Perform these steps in a web browser against the running application at `http://localhost:8000`:

1. **Register a new account**
    - Navigate to the **Register** page.
    - Fill in **Username**, **Email**, and **Password** fields.
    - Click **Sign Up**.
    - **Expected:** You are redirected to the **Login** page with a confirmation message.

2. **Log in**
    - Navigate to the **Login** page.
    - Enter your credentials and click **Log In**.
    - **Expected:** You are redirected to the **Home** page and see your username in the navbar.

3. **Start real‑time capture**
    - Click the **Live Capture** tab (or **title-tab** labeled “Live Capture”).
    - Click **Start Capture**.
    - **Expected:** The webcam feed appears, and detected gestures show up in the **Result** panel beside it.

4. **Upload a selfie for inference**
    - Switch to the **Upload Image** tab.
    - Click **Choose File**, select a selfie (`.jpg` or `.png`), and click **Upload**.
    - **Expected:** The image displays with gesture detection overlays.

5. **Feedback & comments**
    - Switch to the **Feedback** tab.
    - **Expected:** Logged‑in users see existing comments.
    - Enter a comment in the feedback form and click **Submit**.
    - **Expected:** Your comment appears in the list.

6. **Toggle dark mode**
    - Switch to the **Settings** tab.
    - Click **Change to Dark Mode**.
    - **Expected:** The site’s theme changes to dark colors.

7. **View profile information**
    - Click your **Username** in the navbar.
    - **Expected:** You are taken to your profile page showing your registration details.

8. **Log out**
    - Click **Log Out** in the navbar.
    - **Expected:** You are redirected to the **Login** page and no longer see your username in the navbar.
