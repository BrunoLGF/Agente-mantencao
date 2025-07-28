from core.agent import MaintenanceAgent

agent = MaintenanceAgent()

def process_user_message(user_number, message):
    return agent.handle_message(user_number, message)
