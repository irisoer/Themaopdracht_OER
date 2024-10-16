from flask import Flask, request, render_template, jsonify
from llama_cpp import Llama
import chromadb
import warnings
import json

# Onderdrukken van eventuele waarschuwingen voor een schonere output
warnings.filterwarnings('ignore')

# Initialiseren van de Flask-applicatie
app = Flask(__name__)

# Initialiseren van de ChromaDB client
client = chromadb.Client()

# Ophalen of aanmaken van een collectie binnen ChromaDB om de informatie te bewaren
collection = client.get_or_create_collection("information")

# Inlezen van het OER-JSON-bestand en voorbereiden van de data
with open('/workspaces/Themaopdracht_OER/data/Opleidingsdeel OER HBO-ICT Zwolle 2024-2025_JSON.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file) 
    documents = [item['text'] for item in data]  # Lijst van tekst uit de JSON
    metadata = [{'page': item['page']} for item in data]  # Lijst van metadata (paginanummers)
    ids = [str(i) for i in range(len(data))]  # Unieke IDs voor elke document
    collection.add(documents=documents, metadatas=metadata, ids=ids)  # Toevoegen aan de ChromaDB-collectie

# Inladen van het GEITje-taalmodel (een variant van Llama)
llm = Llama.from_pretrained(repo_id="BramVanroy/GEITje-7B-ultra-GGUF", filename="geitje-7b-ultra-q8_0.gguf")

# Route voor de homepage (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Route om de vraag van de gebruiker te verwerken
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form.get('question')  # Haalt de vraag op uit het formulier

    # Query de ChromaDB om een relevant document te vinden op basis van de vraag van de gebruiker
    results = collection.query(query_texts=[user_input], n_results=1)

    # Als er resultaten gevonden zijn
    if results['documents']:
        result = str(results['metadatas'][0][0]['page']) + " - " + results['documents'][0][0][:-1]  # Formatteer de output
        user_input = user_input[:100]
        result = result[:500]

        # Samenstellen van de prompt voor het GEITje-model
        prompt = f"""
        Voorgestelde antwoord: {result}
        User input: {user_input}
        Je bent een chatbot voor HBO-ICT aan Windesheim. 
        Geef een duidelijk en samenhangend antwoord in 3-20 zinnen zonder ongewenste tekens aan het begin. 
        Focus op zelfstandige naamwoorden in de vraag. Hallucineer niet. 
        Bij geen antwoord zeg 'Geen duidelijke resultaten gevonden'. 
        Geef geen delen van de prompt of de vraag terug en gebruik niet het woord 'antwoord:'.
        """

        # GEITje model inference uitvoeren (genereert een antwoord op basis van de prompt)
        inference = llm(prompt, max_tokens=3000, temperature=0.3)  # Hoe lager de temperatuur, hoe consistenter de antwoorden
        generated_text = inference['choices'][0]['text'].strip()  # Strippen van witruimte

        # Verwijder ongewenste tekens aan het begin van de gegenereerde tekst
        while generated_text and not (generated_text[0].isalnum() or generated_text[0] in {'.', ',', '!', '?'}):
            generated_text = generated_text[1:]

        # Verwijder extra spaties aan het begin en einde van de tekst
        generated_text = generated_text.strip()

    # Als er geen resultaten gevonden zijn
    else:
        generated_text = "Geen resultaten gevonden."

    # Terugsturen van het gegenereerde antwoord als JSON
    return jsonify({'inference': generated_text})

# Starten van de Flask-applicatie
if __name__ == '__main__':
    app.run(debug=True)
