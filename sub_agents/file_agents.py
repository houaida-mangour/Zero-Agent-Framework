# sub_agents/file_agents.py
import os
import glob
import shutil
import hashlib
from typing import List, Dict, Any
import json
from tools.agent_tools import parse_instruction_with_ai

FILE_FINDER_SCHEMA = {
    "type": "object",
    "properties": {
        "directory": {
            "type": "string", 
            "description": "The directory path to search in"
        },
        "extensions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of file extensions to look for (e.g., ['.jpg', '.png'])"
        }
    },
    "required": ["directory"]
}

def file_finder_intelligent(instruction: str, previous_result: List[str] = None) -> List[str]:
    """
    Version intelligente du file_finder qui comprend les instructions naturelles.
    """
    print(f" [File Finder Intelligent] Instruction: '{instruction}'")
    
    parsed_args = parse_instruction_with_ai(instruction, FILE_FINDER_SCHEMA)
    
    if not parsed_args:
        print(" Impossible de comprendre l'instruction. Utilisation des valeurs par défaut.")
        parsed_args = {"directory": ".", "extensions": []}
    
    print(f" [File Finder Intelligent] Paramètres parsés: {parsed_args}")
    
    return file_finder(
        directory=parsed_args.get("directory", "."),
        extensions=parsed_args.get("extensions", [])
    )

def file_finder(directory: str, extensions: List[str] = None) -> List[str]:
    """
    Version originale - prend des paramètres structurés.
    """
    print(f" [File Finder] Searching in: '{directory}' for extensions: {extensions}")
    
    pattern = os.path.join(directory, "**", "*.*")
    
    found_files = []
    for file_path in glob.glob(pattern, recursive=True):
        if os.path.isfile(file_path):
            if not extensions or any(file_path.lower().endswith(ext.lower()) for ext in extensions):
                found_files.append(os.path.abspath(file_path))
    
    print(f" [File Finder] Found {len(found_files)} files.")
    return found_files

FILE_SORTER_SCHEMA = {
    "type": "object",
    "properties": {
        "strategy": {
            "type": "string", 
            "description": "Sorting strategy: 'by_extension', 'by_date', 'by_size'"
        }
    },
    "required": ["strategy"]
}

def file_sorter_intelligent(instruction: str, previous_result: List[str] = None) -> dict:
    """
    Version intelligente du file_sorter.
    """
    print(f" [File Sorter Intelligent] Instruction: '{instruction}'")
    
    parsed_args = parse_instruction_with_ai(instruction, FILE_SORTER_SCHEMA)
    
    if not parsed_args:
        print(" Impossible de comprendre l'instruction. Utilisation par défaut: 'by_extension'")
        parsed_args = {"strategy": "by_extension"}
    
    print(f" [File Sorter Intelligent] Paramètres parsés: {parsed_args}")
    
    if not previous_result:
        print(" Aucun fichier à trier. Veuillez d'abord exécuter file_finder.")
        return {"moved": [], "errors": ["No input files"]}
    
    return file_sorter(
        files=previous_result,
        strategy=parsed_args.get("strategy", "by_extension")
    )

def file_sorter(files: List[str], strategy: str) -> dict:
    """
    Version originale - trie les fichiers selon la stratégie.
    """
    print(f"[File Sorter] Sorting {len(files)} files by strategy: {strategy}")
    
    results = {"moved": [], "errors": []}
    
    for file_path in files:
        try:
            if not os.path.isfile(file_path):
                print(f" Warning: File not found {file_path}, skipping.")
                continue
            
            if strategy == "by_extension":
                _, extension = os.path.splitext(file_path)
                extension_folder = extension[1:] if extension else "no_extension"
                target_dir = os.path.join(os.path.dirname(file_path), extension_folder)
                
            else:
                print(f" Stratégie '{strategy}' non supportée. Utilisation 'by_extension'.")
                _, extension = os.path.splitext(file_path)
                extension_folder = extension[1:] if extension else "no_extension"
                target_dir = os.path.join(os.path.dirname(file_path), extension_folder)
            
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, os.path.basename(file_path))
            
            shutil.move(file_path, target_path)
            results["moved"].append(target_path)
            print(f" Mové {os.path.basename(file_path)} vers {os.path.basename(target_dir)}/")
            
        except Exception as e:
            error_msg = f"Échec du déplacement de {file_path}: {str(e)}"
            results["errors"].append(error_msg)
            print(f" {error_msg}")
    
    return results

def duplicate_remover(instruction: str, previous_result: List[str] = None) -> Dict[str, Any]:
    """
    Version originale - trouve les doublons (mode sans suppression).
    """
    print(f" [Duplicate Remover] Instruction: '{instruction}'")
    print(" [Duplicate Remover] Mode sans suppression activé.")
    
    if not previous_result:
        print(" Aucun fichier à vérifier. Veuillez d'abord exécuter file_finder.")
        return {"duplicates_found": 0, "files_to_delete": [], "message": "No input files"}
    
    print(f" [Duplicate Remover] Vérification de {len(previous_result)} fichiers.")
    
    hash_map = {}
    for file_path in previous_result:
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            if file_hash not in hash_map:
                hash_map[file_hash] = []
            hash_map[file_hash].append(file_path)
            
        except Exception as e:
            print(f" Impossible de lire le fichier {file_path}: {e}")
    
    duplicates = {hash: file_list for hash, file_list in hash_map.items() if len(file_list) > 1}
    
    print(f" [Duplicate Remover] {len(duplicates)} groupe(s) de doublons trouvé(s).")
    
    files_to_delete = []
    for file_list in duplicates.values():
        files_to_delete.extend(file_list[1:])  
    
    return {
        "duplicates_found": len(duplicates),
        "files_to_delete": files_to_delete,
        "message": "MODE SÉCURISÉ: Aucun fichier n'a été supprimé."
    }