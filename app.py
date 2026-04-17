import os
from flask import Flask, render_template, request, redirect, url_for, flash
from utils.text_utils import (
    extract_text_from_file,
    preprocess_text,
    extract_skills,
    enhance_jd,
    compute_similarity_score,
    compute_resume_score,
    build_suggestions,
    improve_resume_text,
    compute_keyword_density,
    detect_resume_sections,
    predict_job_roles,
    build_ideal_candidate_skills,
    compare_with_ideal,
    generate_smart_suggestions,
    compute_score_breakdown,
    optimize_resume_text,
)

ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_PREVIEW_CHARS = 2500


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
    return app


app = create_app()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()

    if resume_file is None or resume_file.filename == "":
        flash("No resume file uploaded. Please select a PDF or DOCX file.")
        return redirect(url_for("index"))

    if not allowed_file(resume_file.filename):
        flash("Invalid file type. Upload a PDF or DOCX resume.")
        return redirect(url_for("index"))

    if not job_description:
        flash("Please paste the job description to analyze.")
        return redirect(url_for("index"))

    try:
        resume_text = extract_text_from_file(resume_file)
    except Exception as exc:
        flash(f"Could not extract text from resume: {exc}")
        return redirect(url_for("index"))

    if not resume_text.strip():
        flash("Resume text could not be extracted. Please upload a valid file.")
        return redirect(url_for("index"))

    job_description = enhance_jd(job_description)
    clean_resume_text = preprocess_text(resume_text)
    clean_job_text = preprocess_text(job_description)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched_skills = sorted(set(resume_skills).intersection(jd_skills))
    missing_skills = sorted(set(jd_skills).difference(resume_skills))

    similarity_score = compute_similarity_score(clean_resume_text, clean_job_text)
    resume_score = compute_resume_score(matched_skills, missing_skills, similarity_score)
    skill_match_rate = int(round(len(matched_skills) / max(len(jd_skills), 1) * 100))

    keyword_density = compute_keyword_density(resume_text, resume_skills + jd_skills)
    section_report = detect_resume_sections(resume_text)
    role_predictions = predict_job_roles(resume_skills, job_description)
    ideal_skills = build_ideal_candidate_skills(jd_skills)
    ideal_candidate_skills, ideal_missing = compare_with_ideal(resume_skills, ideal_skills)
    smart_suggestions = generate_smart_suggestions(missing_skills, role_predictions, section_report)
    score_breakdown = compute_score_breakdown(matched_skills, missing_skills, keyword_density, section_report)
    optimized_resume = optimize_resume_text(resume_text, missing_skills)
    rewrite_suggestions = improve_resume_text(resume_text)
    suggestions = build_suggestions(missing_skills, resume_text, job_description, resume_score)

    return render_template(
        "results.html",
        resume_score=resume_score,
        similarity_score=int(similarity_score * 100),
        skill_match_rate=skill_match_rate,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        keyword_density=keyword_density,
        section_report=section_report,
        role_predictions=role_predictions,
        ideal_candidate_skills=ideal_candidate_skills,
        ideal_missing=ideal_missing,
        smart_suggestions=smart_suggestions,
        score_breakdown=score_breakdown,
        optimized_resume=optimized_resume,
        rewrite_suggestions=rewrite_suggestions,
        suggestions=suggestions,
        resume_text=resume_text,
        job_description=job_description,
        preview_limit=MAX_PREVIEW_CHARS,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
