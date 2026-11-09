"""Import researched 2027 Boise/Treasure Valley opportunities into Django Event.

Run from the project root AFTER making the Event date/deadline/fee nullable
and running migrations:
    python manage.py shell -c "exec(open('import_2027_events.py', encoding='utf-8').read())"

Idempotent: skips events with matching names, preserving your own edits/statuses.
Unknown dates, deadlines, and fees are NULL, never invented.
Research snapshot: 2026-11-09. Recheck organizer pages before applying.
"""
from datetime import date
from django.db import transaction
from dashboard.models import Event

EVENTS = [
    {
        'name': 'Food Truck Rally Goes to the Dogs (2027)',
        'location': 'Lloyd Square Park, Nampa, Idaho',
        'start': '2027-03-13', 'end': '2027-03-13', 'deadline': '2027-02-26',
        'details': '12:00-4:30 PM. Food-truck-focused fundraiser for Nampa dog parks. Published 2027 vendor deadline: February 26, 2027. Confirm separate food truck terms with organizer. The form lists a $150 standard vendor booth; do not assume that is a food-trailer charge. Contact Nampa Parks and Recreation: 208-468-5858.',
        'event_url': 'https://www.nampaparksandrecreation.org/193/Food-Truck-Rally-Goes-to-the-Dogs',
        'vendor_url': 'https://www.nampaparksandrecreation.org/FormCenter/Event-Sponsorships-10/Food-Truck-Rally-goes-to-the-Dogs-2027-158',
    },
    {
        'name': 'Treefort Foodfort / Street Eats (2027)',
        'location': 'Downtown Boise, Idaho (specific 2027 Foodfort site TBD)',
        'start': '2027-03-31', 'end': '2027-04-04', 'deadline': None,
        'details': 'Foodfort runs alongside Treefort Music Fest, March 31-April 4. Includes food programming and Street Eats. Food-trailer vendor application process and deadline have not been verified. Do not confuse this with Treefort Market: its Dec 10, 2026 applications are oriented to arts, crafts and market programming, not confirmed food-trailer placement.',
        'event_url': 'https://treefortmusicfest.com/fort/foodfort/',
        'vendor_url': 'https://treefortmusicfest.com/fort/foodfort/',
    },
    {
        'name': 'Boise Hempfest (2027)',
        'location': '700 S Capitol Blvd, Boise, Idaho',
        'start': '2027-04-17', 'end': '2027-04-18', 'deadline': None,
        'details': 'Saturday 10 AM-10 PM, Sunday 10 AM-8 PM. 2027 vendor application is posted. Applications accepted through event dates subject to remaining space. Applications/invoices paid after April 1 carry a 10% late fee; April 1 is a price threshold, NOT an application closing deadline. Contact admin@boisehempfest.org. Vendor fee varies; confirm with organizer.',
        'event_url': 'https://boisehempfest.org/event-info-1',
        'vendor_url': 'https://boisehempfest.org/vendors',
    },
    {
        'name': 'Green Acres Food Truck Park (2027 season)',
        'location': '767 S Pioneer St, Boise, Idaho',
        'start': None, 'end': None, 'deadline': None,
        'details': 'Recurring food-trailer opportunities; park says it reopens in April 2027. Specific first day, individual booking dates and deadline not announced. Food-truck vendor application is already available. Team@greenacresboise.com; 208-856-6157.',
        'event_url': 'https://www.greenacresboise.com/park-schedule',
        'vendor_url': 'https://www.greenacresboise.com/vendors',
    },
    {
        'name': 'Eagle Saturday Market (2027 season)',
        'location': 'Heritage Park, 185 E State St, Eagle, Idaho',
        'start': None, 'end': None, 'deadline': None,
        'details': 'Recurring Saturday market, traditionally May-September; exact 2027 opening and market dates not posted. Vendor applications open in February 2027. Food vendors require the applicable health permit and Idaho tax registration. Confirm whether a trailer can fit and whether the product/menu matches market criteria.',
        'event_url': 'https://www.cityofeagle.org/170/Eagle-Saturday-Market',
        'vendor_url': 'https://www.cityofeagle.org/1720/Vendor-Resource-Center',
    },
    {
        'name': 'Eagle Fun Days (2027)',
        'location': 'Downtown Eagle, Idaho',
        'start': None, 'end': None, 'deadline': None,
        'details': '2027 exact dates and food-vendor deadline have not been confirmed. A secondary listing shows June 2027 but specifically says dates are not updated from 2026; do NOT treat the 2026 dates as 2027 dates. City of Eagle special event applications generally open 3 months before each event.',
        'event_url': 'https://www.cityofeagle.org/430/Events',
        'vendor_url': 'https://www.cityofeagle.org/1720/Vendor-Resource-Center',
    },
    {
        'name': 'Meridian Dairy Days (2027)',
        'location': 'Storey Park, 215 E Franklin Rd, Meridian, Idaho',
        'start': None, 'end': None, 'deadline': None,
        'details': '2027 date/deadline not published in verified organizer information. FestivalNet says June 2027 but clearly marks dates not updated; historical 2026 food deadline was March 15, 2026, not a verified 2027 deadline. Contact the organizers for food-trailer applications.',
        'event_url': 'https://festivalnet.com/26759/Meridian-Idaho/Festivals/Meridian-Dairy-Days-Festival',
        'vendor_url': 'https://festivalnet.com/26759/Meridian-Idaho/Festivals/Meridian-Dairy-Days-Festival',
    },
    {
        'name': 'Boise Music Festival (2027)',
        'location': 'Expo Idaho, 5610 N Glenwood St, Garden City, Idaho',
        'start': '2027-06-26', 'end': '2027-06-26', 'deadline': None,
        'details': 'Saturday 10 AM-10 PM. Large music festival with many food concessions; vendor/sponsor inquiry form is open. No food-vendor application deadline or fees verified. Organizer says 40+ food vendors are provided. Apply early via the official interest form.',
        'event_url': 'https://boisemusicfestival.com/',
        'vendor_url': 'https://boisemusicfestival.com/become-a-vendor/',
    },
    {
        'name': 'Nampa Festival of the Arts (2027)',
        'location': 'Lakeview Park, Nampa, Idaho',
        'start': '2027-08-07', 'end': '2027-08-08', 'deadline': '2027-07-23',
        'details': 'Official Nampa Parks & Recreation 2027 form lists Aug 7-8 and a vendor deadline of July 23, 2027. Free family-friendly festival with 200+ booths, food, music and activities. Food-truck-specific eligibility and charges should be confirmed before applying; sponsor deadlines are different.',
        'event_url': 'https://www.nampaparksandrecreation.org/FormCenter/Event-Sponsorships-10/Nampa-Festival-of-the-Arts-2027-162',
        'vendor_url': 'https://www.nampaparksandrecreation.org/FormCenter/Event-Sponsorships-10/Nampa-Festival-of-the-Arts-2027-162',
    },
    {
        'name': 'Western Idaho Fair (2027)',
        'location': 'Expo Idaho, 5610 N Glenwood St, Garden City, Idaho',
        'start': '2027-08-13', 'end': '2027-08-29', 'deadline': None,
        'details': 'Expanded three-weekend fair, Aug 13-29, closed Mondays and Tuesdays. Official food-concessionaire applications for 2027 are not open yet; no deadline or fee posted. Apply through idahofair.com ONLY; organizer warns about fake vendor invoices. Do not confuse food concessionaires with commercial booth vendors.',
        'event_url': 'https://idahofair.com/news/western-idaho-fair-announces-expanded-schedule-beginning-2027/',
        'vendor_url': 'https://idahofair.com/concessionaires/',
    },
    {
        'name': 'Boise Soul Food Festival (2027)',
        'location': 'Julia Davis Park, Boise, Idaho',
        'start': '2027-08-14', 'end': '2027-08-14', 'deadline': None,
        'details': 'Saturday 11 AM-8 PM. Organizer confirms August 14, 2027. Food and beverage vendors featured; 2027 vendor applications are coming soon and no deadline published. Ask whether your specific menu qualifies.',
        'event_url': 'https://boisesoulfood.org/',
        'vendor_url': 'https://boisesoulfood.org/',
    },
    {
        'name': 'Spirit of Boise Balloon Classic (2027)',
        'location': 'Ann Morrison Park, Boise, Idaho',
        'start': '2027-09-01', 'end': '2027-09-05', 'deadline': None,
        'details': 'Sep 1-5, 2027. Main food/vendor opportunity is Friday Sep 3 Nite Glow; event organizer lists food, vendors and live music from 5 PM. Contact Mike.Owens@townsquaremedia.com using food-vendor sponsorship form. No closing deadline confirmed; balloon flights depend on weather.',
        'event_url': 'https://spiritofboise.com/schedule-of-events',
        'vendor_url': 'https://spiritofboise.com/become-a-sponsor',
    },
    {
        'name': 'Art in the Park - Boise (2027)',
        'location': 'Julia Davis Park, Boise, Idaho',
        'start': '2027-09-10', 'end': '2027-09-12', 'deadline': None,
        'details': 'Fri/Sat 10 AM-8 PM, Sun 10 AM-5 PM. Boise Art Museum says FOOD vendor applications typically start in March; 2027 closing deadline still TBD. Email organizer to join notification list. For budgeting only, 2026 fee schedule was $40 application, $250 booth/truck (or $150 cart), $75 city vendor fee, plus 25% of sales; THESE ARE NOT VERIFIED 2027 RATES.',
        'event_url': 'https://boiseartmuseum.org/art-in-the-park/',
        'vendor_url': 'https://boiseartmuseum.org/art-in-the-park/art-in-the-park-food-vendor-info-center/',
    },
    {
        'name': 'Hyde Park Street Fair (2027)',
        'location': 'Boise North End, Boise, Idaho',
        'start': None, 'end': None, 'deadline': None,
        'details': 'Large 3-day North End event with a food court and 200+ vendors. Official vendor page still displays 2026 dates (Sep 18-20), NOT 2027 dates. 2027 event dates, vendor deadline and fees TBD. For the new application cycle contact vendors@hydeparkstreetfair.org.',
        'event_url': 'https://www.northendboise.org/hpsfvendors',
        'vendor_url': 'https://www.northendboise.org/hpsfvendors',
    },
    {
        'name': 'Boise Pride Festival (2027)',
        'location': 'Boise, Idaho (2027 venue/location TBD)',
        'start': None, 'end': None, 'deadline': None,
        'details': 'Organizer confirms a 2027 festival and plans a 2027 food vendor application, but has not yet posted verified 2027 event dates, fees, or deadline. Check the official festival applications page for the food-vendor application.',
        'event_url': 'https://boisepridefest.org/festival-applications',
        'vendor_url': 'https://boisepridefest.org/festival-applications',
    },
    {
        'name': 'Potato Days - Boise (2027)',
        'location': 'Boise, Idaho (2027 venue TBD)',
        'start': None, 'end': None, 'deadline': None,
        'details': '2027 Boise event dates and vendor deadline not confirmed. Official site still shows Boise Oct 2-4 in 2026; DO NOT reuse these as 2027 dates. Organizer has a vendor page and has previously included food vendors. Verify Boise versus Meridian application and location.',
        'event_url': 'https://familypotatodays.com/',
        'vendor_url': 'https://familypotatodays.com/vendors/',
    },
]


def parse_date(value):
    return date.fromisoformat(value) if value else None


# This prevents the script from inserting invented placeholder dates or "$0" fees.
for field_name in ('event_date', 'application_deadline', 'application_fee'):
    if not Event._meta.get_field(field_name).null:
        raise RuntimeError(
            f'Event.{field_name} must allow NULL before importing 2027 events. '
            'Update dashboard/models.py, run makemigrations and migrate first.'
        )

created = 0
skipped = 0
with transaction.atomic():
    for info in EVENTS:
        if Event.objects.filter(name=info['name']).exists():
            print(f"SKIP: {info['name']} (already in database)")
            skipped += 1
            continue

        start = parse_date(info['start'])
        end = parse_date(info['end'])
        end_text = ('TBD' if end is None else end.isoformat())
        start_text = ('TBD' if start is None else start.isoformat())
        deadline_text = info['deadline'] or 'TBD / not verified'
        notes = (
            f"Event dates: {start_text} through {end_text}\n"
            f"2027 food-vendor deadline: {deadline_text}\n"
            f"2027 application fee: TBD / not verified\n"
            f"Vendor details: {info['details']}\n"
            f"Event website: {info['event_url']}\n"
            f"Vendor information: {info['vendor_url']}\n"
            'Research checked: 2026-11-09. Verify details with organizer before paying/applying.'
        )
        Event.objects.create(
            name=info['name'],
            location=info['location'],
            event_date=start,
            application_deadline=parse_date(info['deadline']),
            application_fee=None,
            notes=notes,
            # Defaults to Not Applied; importing does not mark an application submitted.
        )
        print(f"ADDED: {info['name']}")
        created += 1

print(f'Finished: {created} added, {skipped} already present, {len(EVENTS)} researched total.')