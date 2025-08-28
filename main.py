# main.py
from orchestrator import orchestrator_agent
from engine import execute_plan

def main():
    # Pour l'instant, on demande la tâche dans la ligne de commande.
    user_task = input(" Quelle tâche souhaitez-vous accomplir ?\n> ")

    # Étape 1 : Le Cerveau planifie
    plan = orchestrator_agent(user_task)

    if plan:
        # Étape 2 : Le Moteur exécute le plan
        execute_plan(plan)
    else:
        print("Impossible de créer un plan. Arrêt.")

if __name__ == "__main__":
    main()