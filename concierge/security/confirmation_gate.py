# concierge/security/confirmation_gate.py

WRITE_TOOLS = {
    "create_calendar_event",
    "delete_calendar_event",
    "create_task",
    "save_task_priorities",
}


def confirmation_gate(tool, args, tool_context):
    if tool.name not in WRITE_TOOLS:
        return None

    approved = tool_context.state.get("user_approved_action")

    if approved is not True:
        return {
            "status": "awaiting_confirmation",
            "message": f"I'm about to run: {tool.name} with these details: {args}. "
                       f"I need your explicit approval before I continue.",
        }

    tool_context.state["user_approved_action"] = False
    return None