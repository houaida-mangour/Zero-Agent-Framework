# tools/agent_tools.py
import json
from config import client, AZURE_DEPLOYMENT_NAME

def parse_instruction_with_ai(instruction: str, function_schema: dict) -> dict:
    """
    Utilise l'IA pour parser une instruction naturelle en arguments de fonction basés sur un schéma.
    
    Args:
        instruction (str): L'instruction en langage naturel (ex: "find jpg files in Pictures")
        function_schema (dict): Un schéma JSON qui décrit la fonction et ses paramètres.
    
    Returns:
        dict: Un dictionnaire d'arguments pour la fonction.
    """
    
    # Construit le prompt système à partir du schéma de la fonction
    system_prompt = f"""
    Tu es un expert pour convertir des instructions en anglais en paramètres de fonction JSON.
    Tu DOIS outputter UNIQUEMENT un objet JSON valide qui correspond exactement à ce schéma :
    {json.dumps(function_schema, indent=2)}
    
    Analyse l'instruction de l'utilisateur et extrais les valeurs pertinentes pour chaque paramètre.
    """
    
    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": instruction}
            ],
            temperature=0.1
        )
        
        # Nettoie la réponse et extrait le JSON
        response_text = response.choices[0].message.content
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(response_text)
        
    except Exception as e:
        print(f"❌ Erreur lors du parsing de l'instruction: {e}")
        return {}