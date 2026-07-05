from concierge.tools.calendar_client import list_events

for event in list_events():
    print(event["start"], "-", event["summary"])

from concierge.tools.calendar_client import find_free_slots

for slot in find_free_slots("2026-07-04"):
    print(slot["start"], "→", slot["end"])