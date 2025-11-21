import sys
sys.path.append('C:\\Users\\houai\\OneDrive\\Documents\\zero-agent-framework')
from engine import execute_plan

test_plan = [
    {
        "step": 1,
        "agent": "file_finder",
        "input": "Find all text files and Python scripts in my test_files directory"  # 👈 Instruction naturelle !
    },
    {
        "step": 2, 
        "agent": "file_sorter",
        "input": "Organize these files by their file type extension"  # 👈 Instruction naturelle !
    }
]

execute_plan(test_plan)