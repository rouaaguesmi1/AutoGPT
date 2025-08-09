# api/main.py (Version 5: Finalisée et Nettoyée)
import sys
import os
import datetime
from typing import Optional

# Ajoute le répertoire racine du projet au path pour permettre les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports des librairies externes
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fpdf import FPDF

# Imports de nos modules internes
# Note: On continue d'importer visualizer_node car il est utilisé en interne
from agents.agent_nodes import (
    planner_node,
    researcher_node,
    coder_node,
    writer_node,
    visualizer_node,
    data_extractor_node
)
from memory.chromadb_client import add_text_to_memory

# --- Initialisation de l'application FastAPI ---
app = FastAPI(title="AutoGPT++ Agent Platform")

# Monte le dossier 'static' pour servir les fichiers CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure le moteur de templates pour trouver les fichiers HTML
templates = Jinja2Templates(directory="templates")

# --- Modèles de Données Pydantic ---

class AgentRequest(BaseModel):
    """Définit la structure des données attendues de la part du frontend."""
    agent: str
    objective: str
    context: Optional[str] = None

# --- Fonctions Utilitaires ---

def save_result_and_update_memory(report_content: str, objective: str, agent_name: str):
    """
    1. Sauvegarde le rapport en Markdown et PDF dans le dossier /history.
    2. Ajoute le contenu du rapport à la mémoire RAG (ChromaDB) pour l'auto-amélioration.
    """
    if not os.path.exists("history"):
        os.makedirs("history")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_objective = "".join(x for x in objective[:30] if x.isalnum() or x in " _-").strip()
    filename_base = os.path.join("history", f"{timestamp}_{agent_name}_{safe_objective}")

    md_path = f"{filename_base}.md"
    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Rapport sauvegardé en Markdown : {md_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier Markdown : {e}")

    pdf_path = f"{filename_base}.pdf"
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        encoded_content = report_content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, encoded_content)
        pdf.output(pdf_path)
        print(f"Rapport sauvegardé en PDF : {pdf_path}")
    except Exception as e:
        print(f"Erreur lors de la création du fichier PDF : {e}")

    print(f"Mise à jour de la mémoire RAG avec le résultat de l'agent '{agent_name}'...")
    add_text_to_memory(
        report_content,
        {"source": "self_generated_report", "agent": agent_name, "objective": objective}
    )

# --- Endpoints de l'API ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Sert la page d'accueil principale (index.html)."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/execute_agent")
async def execute_agent_endpoint(request: AgentRequest):
    """
    Endpoint principal qui reçoit une requête et la dirige vers
    un agent simple ou un workflow d'agents complexe.
    """
    try:
        # --- CAS 1: Le workflow autonome Analyste-Visualiseur ---
        if request.agent == "analyst_visualizer":
            print(f"--- DÉMARRAGE DU WORKFLOW : Analyste-Visualiseur ---")

            # Étape 1: L'agent chercheur trouve l'information
            research_state = researcher_node({"objective": request.objective})
            
            # Vérifie si le chercheur a trouvé quelque chose
            if not research_state.get("research_summary"):
                raise HTTPException(status_code=404, detail="La recherche n'a retourné aucune information pertinente.")

            # Étape 2: L'agent extracteur transforme le texte en données
            extraction_state = data_extractor_node(research_state)

            # Vérifie si l'extracteur a trouvé des données
            extracted_data = extraction_state.get("research_summary")
            if not extracted_data:
                 raise HTTPException(status_code=500, detail="Échec de l'extraction des données. Le texte de recherche n'était peut-être pas adapté.")

            # Étape 3: L'agent visualiseur crée le graphique
            visualizer_state = visualizer_node({
                "objective": request.objective,
                "research_summary": extracted_data # Le visualiseur attend les données ici
            })

            # Étape 4: On combine les résultats pour un rapport final
            final_report = (
                f"# Rapport d'Analyse : {request.objective}\n\n"
                f"## Résumé de la Recherche\n\n"
                f"{research_state['research_summary']}\n\n"
                f"## Visualisation des Données\n\n"
                f"{visualizer_state['report']}"
            )

            save_result_and_update_memory(final_report, request.objective, request.agent)
            return JSONResponse(content={"output": final_report})

        # --- CAS 2: Les agents simples qui peuvent être appelés directement ---
        else:
            agent_functions = {
                "planner": planner_node,
                "researcher": researcher_node,
                "coder": coder_node,
                "writer": writer_node,
                # Le visualiseur a été retiré, il ne peut plus être appelé directement
            }
            agent_func = agent_functions.get(request.agent)

            if not agent_func:
                raise HTTPException(status_code=400, detail=f"Agent '{request.agent}' non valide ou non appelable directement.")

            initial_state = {
                "objective": request.objective,
                "research_summary": request.context or "", # Utilise le contexte s'il est fourni
            }

            print(f"--- DÉMARRAGE DE L'AGENT INDIVIDUEL : {request.agent.upper()} ---")
            result_state = agent_func(initial_state)
            print(f"--- AGENT {request.agent.upper()} TERMINÉ ---")

            output_key_map = {
                "planner": "plan",
                "researcher": "research_summary",
                "coder": "code",
                "writer": "report"
            }
            output = result_state.get(output_key_map.get(request.agent))

            if output is None:
                raise HTTPException(status_code=500, detail="L'agent n'a produit aucun résultat.")

            save_result_and_update_memory(output, request.objective, request.agent)
            return JSONResponse(content={"output": output})

    except Exception as e:
        # En cas d'erreur dans n'importe quelle branche, on log et on retourne une erreur 500
        print(f"ERREUR CRITIQUE dans l'endpoint pour l'agent '{request.agent}': {e}")
        # On retourne le message d'erreur au frontend pour le débogage
        raise HTTPException(status_code=500, detail=str(e))

# --- Démarrage du Serveur ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)