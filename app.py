from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


def earliest_unanswered():
    """Returns index of earliest question that hasn't been answered"""
    num_questions = len(survey.questions)
    ordered_answers = [session["responses"][str(i)] for i in range(num_questions)]
    return ordered_answers.index(None)

@app.get("/")
def survey_start():
    """Returns survery start page"""

    return render_template("survey_start.html",
                        title=survey.title,
                        instructions=survey.instructions)


@app.post("/begin")
def handle_begin():
    """handles post request to begin endpoint"""

    session["responses"] = {str(i): None for i in range(len(survey.questions))}

    return redirect("/questions/0")


@app.get("/questions/<int:index>")
def handle_questions(index):
    """handles get request to questions, outputs specific question"""
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(session["responses"].values())
    if None not in session["responses"].values():
        return redirect("/completion")

    num_questions = len(survey.questions)

    if index >= num_questions:
        return redirect(f"/questions/{earliest_unanswered()}")

    session["active_question"] = str(index)
    return render_template("question.html", question = survey.questions[index])


@app.post("/answer")
def handle_answer():
    """handles post request to answer, appends answer to
    responses and redirects to next question"""

    answers = session['responses']
    answers[str(session["active_question"])] = (request.form["answer"])
    session['responses'] = answers



    return redirect(f"/questions/{earliest_unanswered()}")


@app.get("/completion")
def handle_completion():
    """handles get request to completion page, returns thank you page"""

    return render_template("completion.html", survey=survey)