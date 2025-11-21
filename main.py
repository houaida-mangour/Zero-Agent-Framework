# main.py
from orchestrator import orchestrator_agent
from engine import execute_plan

def main():
    user_task = input(" Quelle tâche souhaitez-vous accomplir ?\n> ")

    plan = orchestrator_agent(user_task)

    if plan:
        execute_plan(plan)
    else:
        print("Impossible de créer un plan. Arrêt.")

if __name__ == "__main__":
    main()