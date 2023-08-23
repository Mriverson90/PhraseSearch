import os
from flask import Flask, render_template, request

app = Flask(__name__)

def find_all_phrases_with_context(file_content, search_phrase, context_lines=2):
    contexts = []
    lines = file_content.split('\n')
    
    for line_number, line in enumerate(lines):
        if search_phrase in line:
            start_line = max(0, line_number - context_lines)
            end_line = min(len(lines), line_number + context_lines + 1)
            context = '\n'.join(lines[start_line:end_line])
            contexts.append(context)
    
    return contexts

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_folder = request.files.getlist('folder')
        search_phrase = request.form['phrase']
        context_lines = int(request.form['context_lines'])
        contexts = []

        if uploaded_folder and search_phrase:
            for uploaded_file in uploaded_folder:
                file_content = uploaded_file.read().decode('utf-8')
                file_contexts = find_all_phrases_with_context(file_content, search_phrase, context_lines)
                contexts.extend(file_contexts)
            
            return render_template('index.html', contexts=contexts, search_phrase=search_phrase, context_lines=context_lines)

    return render_template('index.html', contexts=None, search_phrase=None, context_lines=None)

if __name__ == '__main__':
    app.run(debug=True)

