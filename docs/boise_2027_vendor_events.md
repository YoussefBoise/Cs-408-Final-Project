# Boise and Treasure Valley 2027 food-trailer opportunities

This branch includes 16 researched events and vendor opportunities, a one-time importer, and support for unpublished (TBD) dates, application deadlines and fees.

## Load events locally

From the project root, after checking out the branch and setting up your Python environment:

```bash
python manage.py migrate
python manage.py check
python manage.py test
python manage.py shell -c "exec(open('import_2027_events.py', encoding='utf-8').read())"
python manage.py runserver
```

Visit http://127.0.0.1:8000/events/ and open individual events to see researched sources, dates and application notes.

The importer inserts new events as **Not Applied**, skips matching event names on rerun, and never invents unannounced dates or fees. Multi-day events use the first day for `event_date` and put the full range in Notes. The sources were checked on **November 9, 2026** and should be rechecked before you submit applications.

## Deploy to EC2

After merging this branch into `main` and pulling it locally:

```bash
bash deploy/deploy.sh -h 34.221.130.61 -i RSA.pem
```

Your deployment script applies migrations, **but it does not import new event records automatically**. On EC2, run:

```bash
ssh -i RSA.pem ubuntu@34.221.130.61
cd /home/ubuntu/foodtrailer
.venv/bin/python manage.py shell -c "exec(open('import_2027_events.py', encoding='utf-8').read())"
exit
```

Then verify http://34.221.130.61/events/ displays 16 newly added events (if not already imported).

The imported records are database content, not code. Both your local database and EC2 database need their own import. The `cp4` tag is unchanged.
