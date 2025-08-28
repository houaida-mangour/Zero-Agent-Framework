# app.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

# Importe ton code existant
from orchestrator import orchestrator_agent
from engine import execute_plan

# Initialise l'application
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Affiche la page web avec le formulaire"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/run-task")
async def run_task(request: Request, task: str = Form(...)):
    """
    Reçoit une tâche du formulaire web et l'exécute.
    C'est EXACTEMENT le même code que main.py mais pour le web.
    """
    # Étape 1 : Planification (identique à avant)
    plan = orchestrator_agent(task)
    
    results = []
    if plan:
        # Étape 2 : Exécution (identique à avant)
        # On capture les prints pour les afficher sur la page web
        import contextlib
        from io import StringIO
        
        output = StringIO()
        with contextlib.redirect_stdout(output):
            execute_plan(plan)
        
        results = output.getvalue().split('\n')
    else:
        results = ["❌ Impossible de créer un plan."]
    
    # Affiche le résultat sur une nouvelle page
    return templates.TemplateResponse("result.html", {
        "request": request,
        "task": task,
        "plan": plan,
        "results": results
    })

# app.py (ajoute cette fonction)
@app.get("/status")
async def status_page(request: Request):
    """Page qui montre l'état du système"""
    import psutil
    import platform
    
    # Informations système
    system_info = {
        "système": platform.system(),
        "processeur": platform.processor(),
        "mémoire_utilisée": f"{psutil.virtual_memory().percent}%",
        "disque_utilisé": f"{psutil.disk_usage('/').percent}%"
    }
    
    return templates.TemplateResponse("status.html", {
        "request": request,
        "system_info": system_info
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)