from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def survey_start():
    """Returns survery start page"""

    return render_template("survey_start.html",
                           title=survey.title,
                           instructions=survey.instructions)


@app.post("/begin")
def handle_begin():
    """handles post request to begin endpoint"""

    return redirect("/questions/0")


@app.get("/questions/<num>")
def handle_questions(num):
    """handles get request to questions, outputs specific question"""

    if int(num) >= len(survey.questions):
        return redirect("/completion")

    return render_template("question.html", question = survey.questions[int(num)] )


@app.post("/answer")
def handle_answer():
    """handles post request to answer, appends answer to
    responses and redirects to next question"""

    responses.append(request.form["answer"])
    return redirect(f"/questions/{len(responses)}")


@app.get("/completion")
def handle_completion():
    """handles get request to completion page, returns thank you page"""

    return render_template("completion.html",
                           survey=survey,
                           responses=responses,
                           range = range(len(survey.questions)))
