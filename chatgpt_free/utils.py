# Get the Model List
def getModels():
    return ["gpt-3.5-turbo", "gpt-4"]


# Check if Past Chat History has Correct Structure
def _filterPastChatHistory(history: list):
    valid_roles = {"assistant", "user"}
    last_role = None
    if type(history) is not list:
        return f"Error: History must be a List. Got {type(history)}"

    for item in history:
        role = item.get("role")
        content = item.get("content")

        if (not role) or (not content):
            return (
                "Error: 'role' or 'content' key is missing in one or more dictionaries."
            )

        if role not in valid_roles:
            return f"Error: Invalid role '{role}' found. Role must be one of 'assistant' or 'user'"

        if role == last_role:
            return f"Error: Two consecutive roles '{role}' found. Roles must alternate."

        last_role = role

    if last_role == "user":
        return history[:-1]

    return history
