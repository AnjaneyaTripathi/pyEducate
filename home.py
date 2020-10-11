from flask import Flask, render_template, request, send_from_directory, send_file
from utils.prac import *
from utils.knowledge_graph import generate_knowledge_graph
from utils.ques_generation.generate_questions import get_questions
from utils.domain_summarizer import get_domain_summary
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

# ROUTES FOR SUMMARY GENERATION

@app.route("/summary")
def summary_page():
    return render_template('summary.html')

@app.route("/generate_summary", methods=['GET', 'POST'])
def generate_summary():
    if request.method=='POST':
        text_input = request.form['original_text']
        choice = request.form['purpose']
        result = ""
        if choice=="gen":
            sentences =  clean_text(text_input)
            text_data = cnt_in_sent(sentences)

            freq_list = freq_dict(sentences)
            tf_scores = calc_TF(text_data, freq_list)
            idf_scores = calc_IDF(text_data, freq_list)

            tfidf_scores = calc_TFIDF(tf_scores, idf_scores)

            sent_data = sent_scores(tfidf_scores, sentences, text_data)
            result = summary(sent_data)
        else:
            result = get_domain_summary(text_input,choice)

        return render_template('summary_gen.html', result=result, original=text_input)

# ROUTES FOR MIND MAP GENERATION
@app.route("/map", methods=['GET','POST'])
def map():
    if request.method=='POST':
        text = request.form['kg_text']
        image_title = generate_knowledge_graph(text)
        if image_title==False:
            return render_template('mindmap.html')
        else:
            return render_template('mindmap.html', image_title=image_title)
    else:
        return render_template('map.html')

# view/download mindmap
@app.route('/<path:filename>', methods=['GET', 'POST'])
def view(filename):
    image_dir = os.path.join(app.root_path, "/static/media/")
    return send_from_directory(directory=image_dir, filename=filename.split("/")[-1],as_attachment=True,attachment_filename=filename.split("/")[-1]) 


# ROUTES FOR QUESTION GENERATION

@app.route("/question")
def question():
    return render_template('question.html')  
 

@app.route("/generate_questions", methods=['GET', 'POST'])
def generate_questions():
    text_input = request.form['original_text']
    question = get_questions(text_input)
    if question == []:
        return render_template('question_gen.html', original=text_input)
    return render_template('question_gen.html', original=text_input, result=question)
  

if __name__ == '__main__':
    app.run(debug = True)

