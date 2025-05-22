from flask import Flask, jsonify, render_template
import json
import random

app = Flask(__name__)

# Dictionnaire pour mettre en cache les fichiers JSON
cached_reasons = {}

def load_reasons(lang):
    # Test if we have data in cache
    if lang in cached_reasons:
        return cached_reasons[lang]

    # Get data from json file
    with open(f'reason/{lang}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Put data in cache
    cached_reasons[lang] = data
    return data

cached_hireme = {}

def load_hireme(lang):
    # Test if we have data in cache
    if lang in cached_hireme:
        return cached_hireme[lang]

    # Get data from json file
    with open(f'hireme/{lang}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Put data in cache
    cached_hireme[lang] = data
    return data

@app.route('/')
def home():
    return render_template('reason.html')

@app.route('/no')
def no():
    return render_template('reason.html')

@app.route('/no/<lang>', methods=['GET'])
def get_random_reason(lang):
    try:
        reasons = load_reasons(lang)
        random_reason = random.choice(reasons)
        response = jsonify({"reason": random_reason})
        response.data = json.dumps({"reason": random_reason}, ensure_ascii=False)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    except FileNotFoundError:
        return jsonify({"error": "Language not supported"}), 404
    
@app.route('/hireme')
def hireme():
    return render_template('hireme.html')

@app.route('/hireme/<lang>', methods=['GET'])
def get_random_hireme(lang):
    try:
        reasons = load_hireme(lang)
        random_reason = random.choice(reasons)
        response = jsonify({"reason": random_reason})
        response.data = json.dumps({"reason": random_reason}, ensure_ascii=False)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    except FileNotFoundError:
        return jsonify({"error": "Language not supported"}), 404

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000, debug=True)
