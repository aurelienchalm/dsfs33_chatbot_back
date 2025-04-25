from langchain.agents import Tool
from duckduckgo_search import DDGS
import smtplib
from email.mime.text import MIMEText
import os
import re
import json
import requests
from datetime import datetime

HISTO_FILE = "historique_newsletters.json"

# === DuckDuckGo ===
def duck_search(query: str, max_results: int = 10, region="fr-fr", timelimit=None) -> str:
    with DDGS() as ddgs:
        results = ddgs.text(query, region=region, safesearch="moderate", timelimit=timelimit)
        if not results:
            return "Aucun résultat trouvé."
        return "\n".join([
            f"- {r['title']} ({r['href']}): {r['body']}" for r in results[:max_results]
        ])

# === Historique ===
def enregistrer_historique(sujet, liste_articles):
    historique = []
    if os.path.exists(HISTO_FILE):
        with open(HISTO_FILE, "r", encoding="utf-8") as f:
            historique = json.load(f)

    historique.append({
        "sujet": sujet,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "titres": liste_articles
    })

    with open(HISTO_FILE, "w", encoding="utf-8") as f:
        json.dump(historique, f, indent=2, ensure_ascii=False)

def charger_historique_sujet(sujet):
    if not os.path.exists(HISTO_FILE):
        return []
    with open(HISTO_FILE, "r", encoding="utf-8") as f:
        historique = json.load(f)
    titres_deja_envoyes = []
    for entry in historique:
        if entry["sujet"].lower() == sujet.lower():
            titres_deja_envoyes.extend(entry["titres"])
    return titres_deja_envoyes

# === Email ===
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENTS = [os.getenv("EMAIL_RECIPIENTS")]

def send_email(subject, body, to_emails, html=True):
    api_key = os.getenv("RESEND_API_KEY")
   
    sender_email = "onboarding@resend.dev" #os.getenv("RESEND_SENDER", "onboarding@resend.dev")  # email par défaut Resend
    
    if not api_key:
        return "Erreur : Clé API Resend manquante."

    payload = {
        "from": f"Agent Tech <{sender_email}>",
        "to": to_emails,
        "subject": subject,
        "html": body if html else None,
        "text": body if not html else None
    }

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    print("Resend API : ",response.status_code)
    if response.status_code == 200:
        #print("MAIL OK********")
        return "Email envoyé avec succès via Resend."
    else:
        #print("MAIL KO********")
        return f"Erreur Resend : {response.status_code} - {response.text}"

def send_newsletter(subject: str) -> str:
    raw_content = duck_search(f"dernières actualités {subject}")
    #titres_precedents = charger_historique_sujet(subject)
    #historique_formate = "\n".join(f"- {t}" for t in titres_precedents)

    titres = [re.search(r"- (.*) \(", line).group(1) for line in raw_content.splitlines() if "(" in line]
    # enregistrer_historique(subject, titres)

    from app.agent.logic import llm
    
    prompt = f"""
    Tu es un assistant chargé de créer une newsletter (nouvelle) d'information au format HTML sur le sujet suivant : {subject}.
    À partir des résultats suivants (titre, lien, résumé), écris uniquement une liste HTML de type <ul>.
    Chaque actualité doit être dans un élément <li> et contenir :
    - un titre en gras
    - un résumé en une phrase
    - un lien cliquable vers la source (balise <a>)

    Ne retourne que la liste <ul> avec ses éléments <li>, sans texte avant ou après.

    Résultats :
    {raw_content}
    """

    response = llm.invoke(prompt)
    list_html = response.content.strip()
    list_html_cleaned = re.search(r"<ul>.*?</ul>", list_html, re.DOTALL)
    html_list = list_html_cleaned.group(0) if list_html_cleaned else list_html

    html_content = f"""
    <html><body><h2>📰 Newsletter : {subject.title()}</h2>{html_list}</body></html>
    """
    send_email(f"Newsletter {subject.title()}", html_content, EMAIL_RECIPIENTS, html=True)
    return f"Newsletter sur {subject} envoyée."

# === Définition des outils pour l'agent ===
tools = [
    Tool(
        name="RechercherActus",
        func=duck_search,
        description="Recherche les dernières nouvelles sur un sujet donné."
    ),
    Tool(
        name="EnvoyerNewsletter",
        func=send_newsletter,
        description=(
        "Prépare et envoie une newsletter contenant les dernières nouvelles, informations, ou actualités sur un sujet donné."
        "Utilise cet outil si l'utilisateur demande une newsletter, des informations, des nouvelles, de lui donner des informations ou des nouvelles sur un thème ou une revue sur un thème"
    )
    )
]