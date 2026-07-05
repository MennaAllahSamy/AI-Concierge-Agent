"""Planner sub-agent — reads the user's calendar to answer scheduling questions."""

from google.adk.agents import LlmAgent
from concierge.security.confirmation_gate import confirmation_gate
from concierge.tools.calendar_client import list_events, find_free_slots
from concierge.tools.calendar_client import list_events, find_free_slots, create_calendar_event
planner_agent = LlmAgent(
    before_tool_callback=confirmation_gate,
    model="gemini-2.5-flash",
    name="planner",
    description=(
        "Reads the user's calendar to answer scheduling questions — "
        "what's coming up and when they are free. "
        "Called by the root Concierge agent when planning is needed."
    ),
   instruction=(
        "You are the Planner. You help the user with their schedule using "
        "these tools:\n"
        "- Use list_events when the user asks what is on their calendar or "
        "what is coming up.\n"
        "- Use find_free_slots when the user asks when they are free or "
        "available on a given date. Dates are YYYY-MM-DD.\n"
        "- Use create_calendar_event when the user asks to schedule or add an "
        "event. Provide summary, start, and end. When you call this tool you "
        "will receive an 'awaiting_confirmation' response — this is expected. "
        "When that happens, relay the confirmation message to the user, tell "
        "them the action needs their explicit approval, and STOP. Do NOT call "
        "the tool again in the same turn. Do not retry.\n\n"
        "Present results clearly and concisely. When showing free slots, list "
        "them as readable time ranges."
    ),
    tools=[list_events, find_free_slots, create_calendar_event],
)