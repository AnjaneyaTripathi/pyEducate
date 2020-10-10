from flask import Flask, render_template, request, send_from_directory, send_file
from utils.prac import *
from utils.knowledge_graph import *

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
        sentences =  clean_text(text_input)
        text_data = cnt_in_sent(sentences)

        freq_list = freq_dict(sentences)
        tf_scores = calc_TF(text_data, freq_list)
        idf_scores = calc_IDF(text_data, freq_list)

        tfidf_scores = calc_TFIDF(tf_scores, idf_scores)

        sent_data = sent_scores(tfidf_scores, sentences, text_data)
        result = summary(sent_data)
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


# ROUTES FOR QUESTION GENERATION

@app.route("/question")
def question():
    return render_template('question.html')   

if __name__ == '__main__':
    app.run(debug = True)

