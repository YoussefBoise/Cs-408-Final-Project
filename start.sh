
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Starting Food Trailer Management System..."

if ! command -v python3 >/dev/null 2>&1 &&
   ! command -v python >/dev/null 2>&1; then
    echo "ERROR: Python is required."
    exit 1
fi

if [ ! -d ".venv" ]; then
    if command -v python3 >/dev/null 2>&1; then
        python3 -m venv .venv
    else
        python -m venv .venv
    fi
fi

if [ -f ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
elif [ -f ".venv/Scripts/python.exe" ]; then
    PYTHON=".venv/Scripts/python.exe"
else
    echo "ERROR: Python virtual environment is incomplete."
    exit 1
fi

"$PYTHON" -m pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "No .env found. Using standalone development configuration."
    export DJANGO_SECRET_KEY="$("$PYTHON" -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
    export DJANGO_DEBUG=True
    export DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
fi

"$PYTHON" manage.py migrate

echo "Open http://127.0.0.1:8000/"
"$PYTHON" manage.py runserver 0.0.0.0:8000
