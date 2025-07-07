from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session handling

# Load questions
df = pd.read_excel("data/questions.xlsx")

# Configure Gemini
genai.configure(api_key="AIzaSyAtoba2HJx3XcgR_4ZsJ7xhiYtxlJi87cE")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'question_index' not in session:
        session['question_index'] = 0
        session['responses'] = []

    if session['question_index'] >= len(df):
        return redirect(url_for('results'))
    index = session['question_index']

    print(f"Current index: {session['question_index']} / Total questions: {len(df)}")


    

    question = df.iloc[index]['Question']
    feedback = ""
    user_code = ""
    language = ""

    if request.method == 'POST':
        user_code = request.form['code']
        language = request.form['language']

        prompt = f"""You are a coding evaluator.
The question is:
{question}

The student's answer in {language} is:
{user_code}

Please do the following:
1. Point out syntax or logic mistakes (be lenient).
2. If logic is correct, suggest improvements.
3. Be friendly and motivating.
4.see if the logic is correct but they had small synatx errors then thats fine fine.
5.reply must be within 300 words
6.use emojis to motivate,and at the start display the score of the code out of 10.
7.write with good spacing and leave a line and give so its easy to read the feedback
8. remember they are writing answer in a blank ide,you are here to guide them with good review.


Give the response in clear, friendly HTML format with:
1. A heading with a score out of 10.
2. A few short paragraphs (use <p> tags).
3. If there's improved code, show it inside <pre><code> ... </code></pre>.
4. Use bullet points <ul><li> for tips or observations if needed.

Avoid long paragraphs. Make it readable and motivating!"""

        try:
            response = model.generate_content(prompt)
            feedback = response.text
        except Exception as e:
            feedback = "Sorry, error while evaluating. Try again."

        session['responses'].append({
            'question': question,
            'answer': user_code,
            'language': language,
            'feedback': feedback
        })

        session['question_index'] += 1
        if session['question_index'] >= len(df):
            return redirect(url_for('results'))
        return redirect(url_for('index'))


    return render_template("index.html", question=question, feedback=feedback, user_code=user_code, language=language)

@app.route('/results')
def results():
    return render_template("results.html", responses=session.get('responses', []))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
