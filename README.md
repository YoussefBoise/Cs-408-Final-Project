# Food Trailer Management System

## Overview

This project is a full-stack Food Trailer Management System developed for CS 408. It is designed to help food trailer owners manage their menu, inventory, events, sales, and expenses.

The project is being developed across seven checkpoints. Checkpoint 1 focuses on the Django application setup, PostgreSQL database, Bootstrap layout, automated testing, and AWS EC2 deployment.

## Technology Stack

- Backend: Python and Django
- Database: PostgreSQL
- Frontend: Django Templates, HTML, and Bootstrap
- Web Server: Gunicorn and Nginx
- Hosting: AWS EC2 (Ubuntu Linux)
- Testing: Django's built-in testing framework

## Requirements

- Python 3.12 or newer
- Git
- Python virtual environment support
- PostgreSQL for configured database deployments

## Installation and Local Startup

1. Clone the repository:

```bash
git clone https://github.com/YoussefBoise/Cs-408-Final-Project.git
cd Cs-408-Final-Project
```

2. Start the application:

```bash
./start.sh
```

On Windows Git Bash, you can alternatively run:

```bash
bash start.sh
```

The script creates a Python virtual environment if needed, installs dependencies from `requirements.txt`, applies database migrations, and starts Django.

Open the application at:

http://127.0.0.1:8000/

When no `.env` file is configured, the application uses SQLite for standalone development and grading.

## PostgreSQL Configuration

For PostgreSQL, create a `.env` file in the project root using `.env.example` as a template.

Configure these environment variables:

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`

The application uses PostgreSQL when database configuration is provided.

The `.env` file is excluded from Git to protect passwords and other credentials. Do not commit private keys or secret values.

## Automated Testing

Run the automated tests:

```bash
python manage.py test
```

Checkpoint 1 includes seven automated tests covering basic page loading and the five initial database models.

## AWS EC2 Deployment

The application is deployed to an Ubuntu EC2 instance using Gunicorn, Nginx, and systemd.

Live application:

http://34.221.130.61/

The deployment files are located in the `deploy/` directory:

- `setup-ec2.sh` installs and configures the required server software, Nginx, and systemd service.
- `foodtrailer.service` runs Gunicorn automatically when the server starts.
- `deploy.sh` runs tests, transfers application code, installs dependencies, applies migrations, collects static files, and restarts the application.

The EC2 instance must have PostgreSQL configured and a production `.env` file at `/home/ubuntu/foodtrailer/.env`.

### Initial EC2 Setup

After copying the `deploy/` directory to the Ubuntu server, run:

```bash
sudo bash deploy/setup-ec2.sh
```

### Deploy Updates

From the local project directory, run:

```bash
bash deploy/deploy.sh -h 34.221.130.61 -i RSA.pem
```

Replace the IP address and key path if using a different EC2 instance.

### Check Application Service

On EC2:

```bash
sudo systemctl status foodtrailer.service
```

The service is configured to start automatically when Ubuntu boots and restart if the application crashes.

## Checkpoint 1 Progress

Completed:

- Django project and GitHub repository
- PostgreSQL database configuration
- Five Django database models
- Shared Bootstrap navigation and layout
- Dashboard landing page
- Seven passing automated tests
- Local startup script
- AWS EC2 deployment scripts
- Running application on EC2
- Automatic application startup after reboot

## Future Development

Later checkpoints will add menu and inventory management, event tracking, sales and expenses, revenue and profit calculations, and dashboard search functionality.