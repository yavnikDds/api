api
│── myapi_project/   → Main Django project folder (contains global settings)
│   ├── __init__.py   → Marks this directory as a Python package
│   ├── settings.py   → Configuration settings for the project
│   ├── urls.py       → Main URL router for the project
│
│── users/           → Django app handling user-related functionality (authentication, profiles, etc.)
│   ├── migrations/   → Tracks database schema changes
│   ├── __init__.py   → Marks this directory as a Python package
│   ├── admin.py      → Registers models in Django Admin
│   ├── models.py     → Defines database models (User model, etc.)
│   ├── serializers.py→ Converts models to JSON and handles validation
│   ├── urls.py       → URL routing for user-related endpoints
│   ├── views.py      → API logic (e.g., registration, login)
│
│── venv/            → Virtual environment (isolates dependencies)
│── .gitignore       → Specifies files to exclude from version control (e.g., `venv`, `__pycache__`)
