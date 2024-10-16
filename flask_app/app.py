from flask import Flask, request, render_template, jsonify
from llama_cpp import Llama
import chromadb
import warnings
import json

warnings.filterwarnings('ignore')

app = Flask(__name__)
client = chromadb.Client()
collection = client.get_or_create_collection("information")

# Inlezen van de JSON-bestand
with open('/workspaces/Themaopdracht_OER/data/Opleidingsdeel OER HBO-ICT Zwolle 2024-2025_JSON.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file) 
    documents = [item['text'] for item in data]
    metadata = [{'page': item['page']} for item in data]
    ids = [str(i) for i in range(len(data))]
    collection.add(documents=documents, metadatas=metadata, ids=ids)

# GEITje inladen
llm = Llama.from_pretrained(repo_id="BramVanroy/GEITje-7B-ultra-GGUF", filename="geitje-7b-ultra-q8_0.gguf")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form.get('question')
    results = collection.query(query_texts=[user_input], n_results=1)

    if results['documents']:
        result = str(results['metadatas'][0][0]['page']) + " - " + results['documents'][0][0][:-1]
        user_input = user_input[:100]
        result = result[:500]

        prompt = f"""
        Voorgestelde antwoord: {result}
        User input: {user_input}
        Je bent een chatbot voor HBO-ICT aan Windesheim. 
        Geef een duidelijk en samenhangend antwoord in 3-20 zinnen zonder ongewenste tekens aan het begin. 
        Focus op zelfstandige naamwoorden in de vraag. Hallucineer niet. 
        Bij geen antwoord zeg 'Geen duidelijke resultaten gevonden'. 
        Geef geen delen van de prompt of de vraag terug en gebruik niet het woord 'antwoord:'.
        """

        inference = llm(prompt, max_tokens=3000, temperature=0.3) #hoe lager temperature, hoe meer consistent de antwoorden
        generated_text = inference['choices'][0]['text'].strip()

        # Verwijder ongewenste tekens aan het begin
        while generated_text and not (generated_text[0].isalnum() or generated_text[0] in {'.', ',', '!', '?'}):
            generated_text = generated_text[1:]

        # Verwijder extra spaties aan het begin en einde van de tekst
        generated_text = generated_text.strip()
        
    else:
        generated_text = "Geen resultaten gevonden."

    return jsonify({'inference': generated_text})


if __name__ == '__main__':
    app.run(debug=True)
