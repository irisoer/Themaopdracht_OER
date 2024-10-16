from flask import Flask, request, render_template, jsonify
from llama_cpp import Llama
import chromadb
import warnings

warnings.filterwarnings('ignore')

#flask setup
app = Flask(__name__)
client = chromadb.Client()
collection = client.get_or_create_collection("information")

documents = []
metadata = []
ids = []
counter = 0

with open('/workspaces/Themaopdracht_OER/data/Opleidngsdeel_OER_HBO-ICT_Zwolle_2024-2025_Filterd_Modified_Long_Lines.txt', 'r', encoding='utf-8') as lines:
    for line in lines:
        line = line.split(" - ")  
        metadata.append({'kopje': line[1]})  
        documents.append(line[0])  
        ids.append(str(counter))  
        counter += 1

#documenten toevoegen aan de collectie
collection.add(
    documents=documents,
    metadatas=metadata,
    ids=ids
)

#GEITje inladen
llm = Llama.from_pretrained(
    repo_id="BramVanroy/GEITje-7B-ultra-GGUF",
    filename="geitje-7b-ultra-q8_0.gguf",
)

#manier om de main page dalijk te maken met de user input
@app.route('/')
def home():
    return render_template('index.html')

# Define route for querying the collection
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form.get('question')


    results = collection.query(
        query_texts=[user_input],
        n_results=1
    )


    if results['documents']:
        #resultaat ophalen
        result = results['metadatas'][0][0]['kopje'] + " - " + results['documents'][0][0][:-1]

        #voorbereiden prompt voor in llama
        prompt = f"""
        voorgestelde antwoord: {result}
        User input: {user_input}
        stel een nieuw antwoord voor op basis van het voorgestelde antwoord.
        """

        inference = llm(prompt, max_tokens=300)
        generated_text = inference['choices'][0]['text']
    else:
        generated_text = "Geen resultaten gevonden."

    #return resultaat naar front-end
    return jsonify({
        'inference': generated_text
    })

if __name__ == '__main__':
    app.run(debug=True)
