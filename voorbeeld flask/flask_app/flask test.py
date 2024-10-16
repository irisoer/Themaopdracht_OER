from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#tekstverwerking
@app.route('/process', methods=['POST'])
def process_text():
    input_text = request.form['user_input']
    processed_text = input_text.upper()
    return render_template('result.html', result=processed_text)

if __name__ == '__main__':
    app.run(debug=True)
