from flask import Flask, request, render_template, jsonify
from llama_cpp import Llama
import chromadb
import warnings

warnings.filterwarnings('ignore')

# Flask app setup
app = Flask(__name__)

# Load your model and ChromaDB collection
client = chromadb.Client()
collection = client.get_or_create_collection("information")

# Load documents into ChromaDB
documents = []
metadata = []
ids = []
counter = 0

with open('/workspaces/Themaopdracht_OER/data/Opleidngsdeel_OER_HBO-ICT_Zwolle_2024-2025_Filterd_Modified_Long_Lines.txt', 'r', encoding='utf-8') as lines:
    for line in lines:
        line = line.split(" - ")  # Spells are separated by their description by a " - "
        metadata.append({'kopje': line[1]})  # Use the spell name as metadata
        documents.append(line[0])  # Use the description as documents
        ids.append(str(counter))  # Use the counter as ID
        counter += 1

# Add documents to the collection, ignored for ids that already exist
collection.add(
    documents=documents,
    metadatas=metadata,
    ids=ids
)

# Load the Llama model
llm = Llama.from_pretrained(
    repo_id="BramVanroy/GEITje-7B-ultra-GGUF",
    filename="geitje-7b-ultra-q8_0.gguf",
)

# Route to render the main page with the input form
@app.route('/')
def home():
    return render_template('index.html')

# Define route for querying the collection
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form.get('question')

    # Query ChromaDB collection
    results = collection.query(
        query_texts=[user_input],
        n_results=1
    )

    # Check if there are results
    if results['documents']:
        # Retrieve result
        result = results['metadatas'][0][0]['kopje'] + " - " + results['documents'][0][0][:-1]

        # Prepare prompt for Llama
        prompt = f"""
        voorgestelde antwoord: {result}
        User input: {user_input}
        stel een nieuw antwoord voor op basis van het voorgestelde antwoord.
        """

        # Run inference
        inference = llm(prompt, max_tokens=300)
        generated_text = inference['choices'][0]['text']
    else:
        generated_text = "Geen resultaten gevonden."

    # Return the result to the frontend
    return jsonify({
        'inference': generated_text
    })

if __name__ == '__main__':
    app.run(debug=True)
