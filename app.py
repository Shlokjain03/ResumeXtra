from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import os

# AI modules
from ai_modules.resume_parser import extract_text
from ai_modules.analyzer import analyze_resume, extract_skills
from ai_modules.job_matcher import recommend_jobs

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------------- AI RESUME ANALYZER SECTION ----------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_resume')
def upload_resume():
    return render_template('upload_resume.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume_file():
    if 'resume' not in request.files:
        return "No file uploaded."

    file = request.files['resume']
    if file.filename == '':
        return "No file selected."

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filepath)

    extracted_text = extract_text(filepath)
    suggestions, score = analyze_resume(extracted_text)
    skills = extract_skills(extracted_text)
    jobs = recommend_jobs(skills)

    return render_template('analysis.html', suggestions=suggestions, score=score, jobs=jobs)

# ---------------------- RESUME BUILDER SECTION ----------------------

@app.route('/step1', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        session['template'] = request.form.get('template')
        return redirect(url_for('step2'))
    return render_template('step1.html')

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['city'] = request.form.get('city')
        session['phone'] = request.form.get('phone')
        session['email'] = request.form.get('email')
        return redirect(url_for('step3'))
    return render_template('step2.html')

@app.route('/step3', methods=['GET', 'POST'])
def step3():
    if 'experiences' not in session:
        session['experiences'] = []
    if request.method == 'POST':
        experience = {
            'job_title': request.form.get('job_title'),
            'employer': request.form.get('employer'),
            'start_date': request.form.get('start_date'),
            'end_date': request.form.get('end_date'),
            'description': request.form.get('description')
        }
        session['experiences'].append(experience)
        session.modified = True
        if 'add_another' in request.form:
            return redirect(url_for('step3'))
        return redirect(url_for('step4'))
    return render_template('step3.html', experiences=session.get('experiences', []))

@app.route('/step4', methods=['GET', 'POST'])
def step4():
    if 'educations' not in session:
        session['educations'] = []
    if request.method == 'POST':
        education = {
            'college': request.form.get('college'),
            'course': request.form.get('course'),
            'start_year': request.form.get('start_year'),
            'end_year': request.form.get('end_year')
        }
        session['educations'].append(education)
        session.modified = True
        if 'add_another' in request.form:
            return redirect(url_for('step4'))
        return redirect(url_for('step5'))
    return render_template('step4.html', educations=session.get('educations', []))

@app.route('/step5', methods=['GET', 'POST'])
def step5():
    if 'skills' not in session:
        session['skills'] = []
    if request.method == 'POST':
        skill = request.form.get('skill')
        if skill:
            session['skills'].append(skill)
            session.modified = True
        if 'add_another' in request.form:
            return redirect(url_for('step5'))
        return redirect(url_for('step6'))
    return render_template('step5.html', skills=session.get('skills', []))

@app.route('/step6', methods=['GET', 'POST'])
def step6():
    if request.method == 'POST':
        session['summary'] = request.form.get('summary')
        return redirect(url_for('step7'))
    return render_template('step6.html')

@app.route('/step7', methods=['GET', 'POST'])
def step7():
    if 'certifications' not in session:
        session['certifications'] = []
    if request.method == 'POST':
        certification = request.form.get('certification')
        if certification:
            session['certifications'].append(certification)
            session.modified = True
        if 'add_another' in request.form:
            return redirect(url_for('step7'))
        return redirect(url_for('generate_resume'))
    return render_template('step7.html', certifications=session.get('certifications', []))

@app.route('/generate-resume')
def generate_resume():
    template = session.get('template', 'resume1')
    return render_template(f'{template}.html', 
        name=session.get('name'),
        city=session.get('city'),
        phone=session.get('phone'),
        email=session.get('email'),
        experiences=session.get('experiences', []),
        educations=session.get('educations', []),
        skills=session.get('skills', []),
        summary=session.get('summary'),
        certifications=session.get('certifications', []))

@app.route('/download-resume')
def download_resume():
    template = session.get('template', 'resume1')
    html = render_template(f'{template}.html', 
        name=session.get('name'),
        city=session.get('city'),
        phone=session.get('phone'),
        email=session.get('email'),
        experiences=session.get('experiences', []),
        educations=session.get('educations', []),
        skills=session.get('skills', []),
        summary=session.get('summary'),
        certifications=session.get('certifications', []))

    filename = f"resume_{session.get('name', 'user')}.html"
    filepath = os.path.join('uploads', filename)
    with open(filepath, 'w') as f:
        f.write(html)

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
