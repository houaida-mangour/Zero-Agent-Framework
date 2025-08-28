# tools/registry.py
from sub_agents.file_agents import (
    file_finder_intelligent,
    file_sorter_intelligent,
    duplicate_remover
)

TOOL_REGISTRY = {
    "file_finder": file_finder_intelligent,
    "file_sorter": file_sorter_intelligent,
    "duplicate_remover": duplicate_remover,
}