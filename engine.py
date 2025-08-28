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
    context = {}  # Stocke les résultats de chaque étape

    for step in plan:
        step_num = step["step"]
        agent_name = step["agent"]
        agent_instruction = step["input"]

        print(f"\n--- [Étape {step_num}] Appel de l'agent '{agent_name}' ---")

        # Trouve la fonction Python correspondant au nom de l'agent
        agent_function = TOOL_REGISTRY.get(agent_name)
        if agent_function is None:
            print(f" ERREUR : Agent '{agent_name}' inconnu. Arrêt du plan.")
            break

        # Prépare les arguments pour la fonction
        # Si ce n'est pas la première étape, on passe le résultat de l'étape précédente
        if step_num > 1:
            previous_result = context.get(step_num - 1)
            # Appelle la fonction avec l'instruction ET le résultat précédent
            try:
                result = agent_function(agent_instruction, previous_result)
            except TypeError:
                # Si la fonction n'accepte pas le second argument, on appelle sans
                print(f" L'agent {agent_name} n'accepte pas le contexte, appel sans...")
                result = agent_function(agent_instruction)
        else:
            # Première étape : on appelle juste avec l'instruction
            result = agent_function(agent_instruction)

        # Stocke le résultat de cette étape dans le contexte
        context[step_num] = result
        print(f" [Étape {step_num}] Terminée avec succès.")

    print("\n Exécution du plan terminée !")
    print(" Contexte final (résultats de chaque étape) :")
    for step_num, result in context.items():
        print(f"Étape {step_num}: {result}")