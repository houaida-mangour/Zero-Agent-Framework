# engine.py
from tools.registry import TOOL_REGISTRY

def execute_plan(plan: list):
    """
    Prend un plan (liste d'étapes) et l'exécute séquentiellement.
    Passe le résultat de l'étape précédente à l'étape suivante.
    """
    if not plan:
        print(" Le plan est vide. Rien à exécuter.")
        return

    print(" Démarrage de l'exécution du plan...")
    context = {}  

    for step in plan:
        step_num = step["step"]
        agent_name = step["agent"]
        agent_instruction = step["input"]

        print(f"\n--- [Étape {step_num}] Appel de l'agent '{agent_name}' ---")

        agent_function = TOOL_REGISTRY.get(agent_name)
        if agent_function is None:
            print(f" ERREUR : Agent '{agent_name}' inconnu. Arrêt du plan.")
            break

        if step_num > 1:
            previous_result = context.get(step_num - 1)
            try:
                result = agent_function(agent_instruction, previous_result)
            except TypeError:
                print(f" L'agent {agent_name} n'accepte pas le contexte, appel sans...")
                result = agent_function(agent_instruction)
        else:
            result = agent_function(agent_instruction)

        context[step_num] = result
        print(f" [Étape {step_num}] Terminée avec succès.")

    print("\n Exécution du plan terminée !")
    print(" Contexte final (résultats de chaque étape) :")
    for step_num, result in context.items():
        print(f"Étape {step_num}: {result}")