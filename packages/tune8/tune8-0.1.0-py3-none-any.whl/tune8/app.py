import os
from flask import Flask, render_template, request, jsonify, send_file
import json

app = Flask(__name__)

JSONL_FILE = os.path.join(os.path.dirname(__file__), 'prompts.jsonl')
DEFAULT_SYSTEM_FILE = os.path.join(os.path.dirname(__file__), 'default_system.txt')

def load_prompts():
    if not os.path.exists(JSONL_FILE):
        return []
    with open(JSONL_FILE, 'r') as f:
        return [json.loads(line) for line in f]

def save_prompts(prompts):
    with open(JSONL_FILE, 'w') as f:
        for prompt in prompts:
            f.write(json.dumps(prompt) + '\n')

@app.route('/')
def index():
    prompts = load_prompts()
    return render_template('index.html', prompts=prompts)

@app.route('/get_default_system')
def get_default_system():
    if os.path.exists(DEFAULT_SYSTEM_FILE):
        with open(DEFAULT_SYSTEM_FILE, 'r') as f:
            return jsonify(default_system=f.read())
    return jsonify(default_system='')

@app.route('/save_default_system', methods=['POST'])
def save_default_system():
    system = request.form.get('system')
    with open(DEFAULT_SYSTEM_FILE, 'w') as f:
        f.write(system)
    return jsonify(success=True)

@app.route('/edit_all_system', methods=['POST'])
def edit_all_system():
    new_system = request.form.get('system')
    prompts = load_prompts()
    for prompt in prompts:
        prompt['messages'][0]['content'] = new_system
    save_prompts(prompts)
    return jsonify(success=True)

@app.route('/manage_prompts', methods=['POST'])
def manage_prompts():
    action = request.form.get('action')
    prompts = load_prompts()

    if action == 'add':
        new_prompt = {
            "messages": [
                {"role": "system", "content": request.form.get('system')},
                {"role": "user", "content": request.form.get('prompt')},
                {"role": "assistant", "content": request.form.get('ideal_answer')}
            ]
        }
        prompts.append(new_prompt)
    elif action == 'edit':
        index = int(request.form.get('index'))
        prompts[index]["messages"][1]["content"] = request.form.get('prompt')
        prompts[index]["messages"][2]["content"] = request.form.get('ideal_answer')
    elif action == 'delete':
        index = int(request.form.get('index'))
        prompts.pop(index)

    save_prompts(prompts)
    return jsonify(success=True)

@app.route('/export_jsonl')
def export_jsonl():
    return send_file(JSONL_FILE, as_attachment=True, download_name='prompts.jsonl')

@app.route('/import_jsonl', methods=['POST'])
def import_jsonl():
    if 'file' not in request.files:
        return jsonify(success=False, error="No file part")
    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, error="No selected file")
    if file:
        file.save(JSONL_FILE)
        return jsonify(success=True)

def run_app():
    app.run(debug=True)

if __name__ == '__main__':
    run_app()