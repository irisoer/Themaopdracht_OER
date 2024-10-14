from flask import Flask, render_template, request

app = Flask(__name__)

# Route voor de homepage met het formulier
@app.route('/')
def home():
    return render_template('index.html')

# Route voor tekstverwerking (POST)
@app.route('/process', methods=['POST'])
def process_text():
    # Haal de ingevoerde tekst op uit het formulier
    input_text = request.form['user_input']
    # Verwerk de tekst (bijvoorbeeld: omzetten naar hoofdletters)
    processed_text = input_text.upper()
    # Stuur het resultaat naar de pagina
    return render_template('result.html', result=processed_text)

if __name__ == '__main__':
    app.run(debug=True)
