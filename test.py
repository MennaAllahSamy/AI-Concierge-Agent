from concierge.security.confirmation_gate import confirmation_gate

class FakeTool:
    def __init__(self, name): self.name = name

class FakeContext:
    def __init__(self): self.state = {}

# 1. Write tool, no approval → should print the awaiting_confirmation dict
print(confirmation_gate(FakeTool("create_calendar_event"), {"title": "Sync"}, FakeContext()))

# 2. Read tool → should print None
print(confirmation_gate(FakeTool("list_calendar_events"), {}, FakeContext()))

# 3. Write tool WITH approval → should print None
ctx = FakeContext()
ctx.state["user_approved_action"] = True
print(confirmation_gate(FakeTool("create_calendar_event"), {"title": "Sync"}, ctx))