# =========================================================
# 🧠 TOOL REGISTRY (Central place for all tools)
# =========================================================

from tools.calculator import calculate

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform basic math calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    }
]