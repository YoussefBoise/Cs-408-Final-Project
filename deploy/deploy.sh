
#!/usr/bin/env bash
set -euo pipefail

HOST=""
KEY=""

while getopts "h:i:" opt; do
    case "$opt" in
        h) HOST="$OPTARG" ;;
        i) KEY="$OPTARG" ;;
        *) exit 1 ;;
    esac
done

if [ -z "$HOST" ] || [ -z "$KEY" ]; then
    echo "Usage: ./deploy/deploy.sh -h PUBLIC_IP -i KEY_FILE"
    exit 1
fi

APP_DIR="/home/ubuntu/foodtrailer"
SERVER="ubuntu@$HOST"

cd "$(dirname "$0")/.."

echo "Running tests..."
python manage.py test

echo "Copying application to EC2..."

ssh -i "$KEY" "$SERVER" "mkdir -p $APP_DIR"

tar \
    --exclude=.git \
    --exclude=.venv \
    --exclude=.env \
    --exclude=db.sqlite3 \
    --exclude=RSA.pem \
    --exclude=__pycache__ \
    --exclude=staticfiles \
    -czf - . | ssh -i "$KEY" "$SERVER" \
    "tar -xzf - -C $APP_DIR"

echo "Installing dependencies and applying migrations..."

ssh -i "$KEY" "$SERVER" "
    set -e
    cd $APP_DIR
    if [ ! -d .venv ]; then
        python3 -m venv .venv
    fi
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python manage.py migrate
    .venv/bin/python manage.py collectstatic --noinput
    sudo systemctl restart foodtrailer.service
"

echo "Checking live website..."

curl --fail --show-error "http://$HOST/"

echo "Deployment completed."
