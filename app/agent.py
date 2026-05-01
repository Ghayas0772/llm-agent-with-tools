import json
import os

from app.services.azure_openai import client
from tools.registry import tools
from tools.calculator import calculate

# =====================================================
# 🧠 CONFIG
# =====================================================
MEMORY_FILE = "memory.json"
PROFILE_FILE = "profile.json"
MAX_MEMORY_MESSAGES = 12


# =====================================================
# 🧠 SAFE JSON LOADER
# =====================================================
def load_json(file_path, default):
    try:
        if not os.path.exists(file_path):
            return default

        with open(file_path, "r") as f:
            content = f.read().strip()

            if not content:
                return default

            return json.loads(content)

    except json.JSONDecodeError:
        return default


# =====================================================
# 🧠 MEMORY FUNCTIONS
# =====================================================
def load_memory():
    return load_json(MEMORY_FILE, [])


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def trim_memory(memory):
    return memory[-MAX_MEMORY_MESSAGES:]


# =====================================================
# 👤 PROFILE FUNCTIONS
# =====================================================
def load_user_profile():
    return load_json(PROFILE_FILE, {})


def save_user_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=2)


def extract_name(user_input):
    if "my name is" in user_input.lower():
        return user_input.split("is")[-1].strip()
    return None


# =====================================================
# 🤖 MAIN AGENT (CLEAN LEVEL 4 STABLE VERSION)
# =====================================================
def run_agent(user_input: str):

    # 🧠 Load state
    conversation_memory = load_memory()
    user_profile = load_user_profile()

    # 👤 Extract name
    name = extract_name(user_input)
    if name:
        user_profile["name"] = name
        save_user_profile(user_profile)

    # 🧠 Add user input
    conversation_memory.append({
        "role": "user",
        "content": user_input
    })

    # 💰 Trim memory
    trimmed_memory = trim_memory(conversation_memory)

    # 🧠 Build GPT context
    messages = [
        {
            "role": "system",
            "content": f"You are an AI assistant. User name is: {user_profile.get('name', 'unknown')}."
        }
    ] + trimmed_memory

    # 🤖 CALL GPT
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message


    # =====================================================
    # 🛠 TOOL EXECUTION
    # =====================================================
    if message.tool_calls:

        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name

        try:
            arguments = json.loads(tool_call.function.arguments)
        except:
            arguments = {}

        if function_name == "calculate":
            result = calculate(arguments.get("expression", "0"))

        elif function_name == "web_search":
            result = f"Search: {arguments.get('query', '')} (mock)"

        elif function_name == "read_file":
            try:
                with open(arguments.get("file_path", ""), "r") as f:
                    result = f.read()
            except Exception as e:
                result = str(e)

        # 🔁 SECOND GPT CALL
        second_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages + [
                message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            ]
        )

        final_answer = second_response.choices[0].message.content

        # 🧠 Save memory
        conversation_memory.append({
            "role": "assistant",
            "content": final_answer
        })

        conversation_memory = trim_memory(conversation_memory)
        save_memory(conversation_memory)

        return final_answer


    # =====================================================
    # 🧠 NO TOOL RESPONSE
    # =====================================================
    conversation_memory.append({
        "role": "assistant",
        "content": message.content
    })

    conversation_memory = trim_memory(conversation_memory)
    save_memory(conversation_memory)

    return message.content