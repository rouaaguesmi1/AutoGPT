# agents/agent_nodes.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from memory.chromadb_client import get_retriever
from tools.web_search import get_web_search_tool
import matplotlib.pyplot as plt
import datetime
import os
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.chat_models import ChatOllama
# Initialize the local LLM
llm = ChatOllama(model="llama3", temperature=0)

def planner_node(state: dict):
    """
    Generates a step-by-step plan to address the user's objective.
    """
    print("---PLANNING---")
    objective = state['objective']
    
    prompt = ChatPromptTemplate.from_template(
        """You are an expert planner. Your job is to create a clear, concise, and actionable step-by-step plan 
        to achieve the following objective. Respond with nothing but the plan, formatted as a numbered list.

        Objective: {objective}
        """
    )
    
    chain = prompt | llm | StrOutputParser()
    plan = chain.invoke({"objective": objective})
    
    return {"plan": plan, "research_summary": ""}

def researcher_node(state: dict):
    """
    Conducts web and memory research based on the objective and plan.
    """
    print("---RESEARCHING---")
    objective = state['objective']
    plan = state['plan']
    
    # RAG retriever for memory search
    retriever = get_retriever()
    
    # Web search tool
    search_tool = get_web_search_tool()

    rag_docs = retriever.get_relevant_documents(objective)
    web_results = search_tool.run(objective)

    context = f"""
    Memory (Internal Knowledge):
    {rag_docs}

    Web Search Results (External Knowledge):
    {web_results}
    """
    
    prompt = ChatPromptTemplate.from_template(
        """You are a master researcher. Based on the provided internal knowledge and external web search results,
        synthesize a comprehensive summary that will help achieve the following objective. Focus only on the most relevant information.

        Objective: {objective}
        Plan: {plan}
        
        Context:
        {context}
        
        Provide a concise research summary:
        """
    )
    
    chain = prompt | llm | StrOutputParser()
    summary = chain.invoke({"objective": objective, "plan": plan, "context": context})

    return {"research_summary": summary}

def coder_node(state: dict):
    """
    Generates Python code based on the objective and research.
    """
    print("---CODING---")
    objective = state['objective']
    research_summary = state['research_summary']
    
    prompt = ChatPromptTemplate.from_template(
        """You are a world-class Python programmer. Based on the provided objective and research summary,
        write clean, efficient, and well-documented Python code to solve the problem.
        
        Objective: {objective}
        Research Summary: {research_summary}
        
        Respond with ONLY the Python code inside a single ```python ... ``` block.
        """
    )
    
    chain = prompt | llm | StrOutputParser()
    code = chain.invoke({"objective": objective, "research_summary": research_summary})

    # For simplicity, we are not executing/debugging code here, but this is where
    # you would add a call to a code execution tool.
    
    return {"code": code}

def writer_node(state: dict):
    """
    Generates a final Markdown report.
    """
    print("---WRITING REPORT---")
    objective = state['objective']
    plan = state['plan']
    research_summary = state['research_summary']
    code = state['code']
    
    prompt = ChatPromptTemplate.from_template(
        """You are a professional technical writer. Your task is to generate a comprehensive Markdown report
        based on the work done by the AI agents. The report should be well-structured and easy to read.

        Objective: {objective}
        
        ---
        
        ### Plan
        {plan}
        
        ---
        
        ### Research Summary
        {research_summary}
        
        ---
        
        ### Generated Code
        {code}
        
        ---
        
        ### Final Summary
        Provide a brief summary of the entire process and the final outcome.
        """
    )
    
    chain = prompt | llm | StrOutputParser()
    report = chain.invoke({
        "objective": objective,
        "plan": plan,
        "research_summary": research_summary,
        "code": code
    })
    
    return {"report": report}
def visualizer_node(state: dict):
    """
    Génère une visualisation (graphique) à partir de données structurées
    et la sauvegarde en tant qu'image.
    Retourne un lien Markdown vers l'image.
    """
    print("--- VISUALIZING DATA ---")
    
    # Pour ce noeud, nous attendons des données structurées dans le "contexte".
    # Par exemple : "Asie:4.6, Afrique:1.3, Europe:0.74"
    data_string = state.get("research_summary", "") # On réutilise ce champ pour les données
    objective = state.get("objective", "Graphique sans titre")

    # 1. Analyse des données d'entrée
    try:
        data_pairs = [pair.strip().split(':') for pair in data_string.split(',')]
        labels = [pair[0] for pair in data_pairs]
        values = [float(pair[1]) for pair in data_pairs]
    except Exception as e:
        return {"report": f"Erreur : Impossible d'analyser les données pour le graphique. Données reçues : {data_string}. Erreur : {e}"}

    # 2. Génération du graphique avec Matplotlib
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['#00aaff', '#00ffaa', '#ffaa00', '#ff5555'])
    ax.set_ylabel('Population (en milliards)')
    ax.set_title(objective)
    plt.xticks(rotation=15, ha="right") # Améliore la lisibilité des labels

    # 3. Sauvegarde du graphique dans le dossier /static
    static_dir = "static"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"chart_{timestamp}.png"
    image_path = os.path.join(static_dir, image_filename)
    
    plt.savefig(image_path, bbox_inches='tight') # bbox_inches='tight' pour éviter que les labels soient coupés
    plt.close(fig) # Libère la mémoire
    print(f"Graphique sauvegardé : {image_path}")

    # 4. Retourne le lien Markdown vers l'image
    markdown_link = f"![{objective}](/static/{image_filename})"
    
    # La "sortie" de cet agent est un rapport contenant le lien
    return {"report": markdown_link}
def data_extractor_node(state: dict):
    """
    Lit un texte brut, en extrait des données structurées pour un graphique,
    et nettoie la sortie pour assurer la robustesse.
    """
    print("--- EXTRACTING STRUCTURED DATA (IMPROVED) ---")
    
    text_to_parse = state.get("research_summary", "")
    if not text_to_parse:
        return {"report": "Erreur : Aucun texte fourni pour l'extraction de données."}

    # 1. NOUVEAU PROMPT "FEW-SHOT" : On lui montre un exemple parfait.
    # C'est beaucoup plus efficace qu'une simple description.
    prompt = ChatPromptTemplate.from_template(
        """
        Votre mission est d'agir comme un analyseur de données extrêmement précis. Vous devez extraire des paires label-valeur d'un texte et les formater SANS AUCUN TEXTE SUPPLÉMENTAIRE.

        --- EXEMPLE PARFAIT ---
        Texte d'entrée : "La population de l'Asie est de 4.6 milliards. L'Afrique compte 1.3 milliard d'habitants, et l'Europe environ 0.74 milliard."
        Votre sortie : Asie:4.6, Afrique:1.3, Europe:0.74
        --- FIN DE L'EXEMPLE ---

        Basé sur cet exemple, analysez le texte suivant. Ne donnez QUE la liste des données formatées. Ne dites pas "voici les données" ou quoi que ce soit d'autre.

        Texte à analyser :
        >>>
        {text_to_parse}
        >>>

        Données extraites :
        """
    )
    
    # On utilise un LLM avec une "température" de 0 pour qu'il soit le plus déterministe et factuel possible.
    llm = ChatOllama(model="llama3", temperature=0)
    chain = prompt | llm | StrOutputParser()
    extracted_data_raw = chain.invoke({"text_to_parse": text_to_parse})
    
    print(f"Sortie brute de l'extracteur LLM : '{extracted_data_raw}'")

    # 2. FILET DE SÉCURITÉ : On nettoie la sortie du LLM, au cas où il désobéirait.
    # On cherche la première occurrence d'un motif "mot:chiffre" et on prend tout ce qui suit.
    match = re.search(r'[\w\s]+:\s*\d+(\.\d+)?', extracted_data_raw)
    if match:
        # On extrait la chaîne à partir du début de la première correspondance trouvée
        cleaned_data = extracted_data_raw[match.start():].strip()
        print(f"Données nettoyées pour le visualiseur : '{cleaned_data}'")
        # On remplace le champ par les données nettoyées et prêtes à l'emploi
        return {"research_summary": cleaned_data}
    else:
        # Si aucun motif n'est trouvé, on signale une erreur claire
        print("ERREUR : L'extracteur n'a trouvé aucune donnée valide dans la sortie du LLM.")
        # On retourne un dictionnaire avec la sortie originale pour le débogage, mais aussi une erreur claire
        return {
            "report": f"Erreur critique : L'agent d'extraction n'a pas pu trouver de données formatées. Sortie brute reçue : '{extracted_data_raw}'",
            "research_summary": "" # On s'assure que le champ est vide pour que le visualiseur échoue proprement
        }
