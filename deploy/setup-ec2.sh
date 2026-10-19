
#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/ubuntu/foodtrailer"
APP_USER="ubuntu"

if [ "$(id -u)" -ne 0 ]; then
    echo "Run this script with sudo."
    exit 1
fi

echo "Installing server dependencies..."

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 python3-venv python3-pip \
    postgresql postgresql-contrib libpq-dev \
    nginx git

echo "Preparing application directory..."

mkdir -p "$APP_DIR"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing systemd service..."

cp "$SCRIPT_DIR/foodtrailer.service" \
    /etc/systemd/system/foodtrailer.service

systemctl daemon-reload
systemctl enable foodtrailer.service

echo "Configuring Nginx..."

cat > /etc/nginx/sites-available/foodtrailer <<'EOF'
server {
    listen 80;
    server_name _;

    location /static/ {
        alias /home/ubuntu/foodtrailer/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sfn /etc/nginx/sites-available/foodtrailer \
    /etc/nginx/sites-enabled/foodtrailer

rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl enable nginx
systemctl restart nginx

echo "EC2 initial setup completed."
echo "Deploy the application code before starting foodtrailer.service."
