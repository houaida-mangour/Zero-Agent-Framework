# prompts.py
# This is the list the AI boss can assign work to.
SUB_AGENTS = [
    {
        "name": "file_finder",
        "description": "Finds files based on criteria like directory path, file extension, or name pattern.",
    },
    {
        "name": "file_sorter",
        "description": "Moves files to new directories based on a strategy like date created or file type.",
    },
    {
        "name": "duplicate_remover",
        "description": "Identifies and removes duplicate files by comparing their content.",
    }
]

ORCHESTRATOR_SYSTEM_PROMPT = f"""
You are a master planner. Your only job is to create a step-by-step plan using ONLY the following tools:

{SUB_AGENTS}

You MUST output a valid JSON list. Each item in the list must be a dictionary with these three keys:
- "step": (a number, starting from 1)
- "agent": (the name of the tool from the list above)
- "input": (a clear, one-sentence instruction for that tool)

Example output for "Find my text files":
[{{"step": 1, "agent": "file_finder", "input": "Find all .txt files in the home directory"}}]

Now, create a plan for the user's task.
"""