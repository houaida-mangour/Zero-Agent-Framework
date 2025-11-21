# test_intelligent.py
import sys
sys.path.append('C:\\Users\\houai\\OneDrive\\Documents\\zero-agent-framework')
from tools.agent_tools import parse_instruction_with_ai

FILE_FINDER_SCHEMA = {
    "type": "object",
    "properties": {
        "directory": {"type": "string", "description": "The directory path to search in"},
        "extensions": {
            "type": "array", 
            "items": {"type": "string"},
            "description": "List of file extensions to look for"
        }
    },
    "required": ["directory"]
}

instruction = "Find all PDF and Word documents in my Downloads folder"
result = parse_instruction_with_ai(instruction, FILE_FINDER_SCHEMA)

print("Instruction:", instruction)
print("Parsed result:", result)