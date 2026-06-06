import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="ResumeIQ",
    page_icon="📑",
    layout="centered"
)

st.markdown("""
<h1 style='text-align:center;'>
ResumeIQ
</h1>

<p style='text-align:center;color:gray;'>
ATS Resume Analysis Platform
</p>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("ResumeIQ")

    st.write("""
    Upload your resume and compare it
    against a job description to estimate
    ATS compatibility.
    """)

    st.info("Supports PDF resumes")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if uploaded_file and job_description:

    pdf = PdfReader(uploaded_file)

    resume_text = ""

    for page in pdf.pages:
        text = page.extract_text()

        if text:
            resume_text += text

    skills = [
        "python",
        "sql",
        "excel",
        "html",
        "css",
        "javascript",
        "c++",
        "git",
        "mysql",
        "pandas",
        "numpy",
        "streamlit"
    ]

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    matched = []

    for skill in skills:
        if skill in resume_text and skill in job_description:
            matched.append(skill)

    jd_skills = []

    for skill in skills:
        if skill in job_description:
            jd_skills.append(skill)

    if len(jd_skills) > 0:
        score = (len(matched) / len(jd_skills)) * 100
    else:
        score = 0

    resume_skills = []

    for skill in skills:
        if skill in resume_text:
            resume_skills.append(skill)

    missing_skills = []

    for skill in skills:
        if skill in job_description and skill not in resume_text:
            missing_skills.append(skill)

    st.markdown(f"""
<div style="
background:#111827;
padding:30px;
border-radius:20px;
text-align:center;
margin-bottom:25px;
border:1px solid #374151;
">

<h3 style="color:white;">
ATS SCORE
</h3>

<h1 style="color:#22c55e;">
{score:.2f}%
</h1>

</div>
""", unsafe_allow_html=True)

    st.progress(int(score))

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Matched", len(matched))

    with col2:
        st.metric("Missing", len(missing_skills))

    with col3:
        st.metric("Resume Skills", len(resume_skills))

    if score >= 80:
        st.success("Excellent Resume Match")

    elif score >= 60:
        st.warning("Good Resume Match - Improvements Recommended")

    else:
        st.error("Resume Needs Improvement")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Skills Found")

        if resume_skills:
            for skill in resume_skills:
                st.write("•", skill.title())
        else:
            st.write("No skills detected")

    with col2:
        st.subheader("Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.write("•", skill.title())
        else:
            st.write("No missing skills")

    recommendations = []

    for skill in missing_skills:
        recommendations.append(
            f"Consider adding {skill.title()} to improve ATS score."
        )

    st.subheader("Matched Skills")

    if matched:
        st.write(", ".join([s.title() for s in matched]))
    else:
        st.write("No matching skills found")

    with st.expander("Resume Preview"):
        st.write(resume_text[:2000])

    st.subheader("Analysis Summary")

    st.write(
        f"""
        Resume contains {len(resume_skills)} recognized skills.

        {len(matched)} skills match the job description.

        {len(missing_skills)} skills are missing and may improve ATS performance.
        """
    )

    st.subheader("Recommendations")

    if recommendations:
        for rec in recommendations:
            st.warning(rec)
    else:
        st.success("No major skill gaps detected.")

    chart_data = pd.DataFrame(
        {
            "Category": ["Matched", "Missing"],
            "Count": [
                len(matched),
                len(missing_skills)
            ]
        }
    )

    st.subheader("Skill Analysis")

    st.bar_chart(
        chart_data.set_index("Category")
    )
    def create_pdf_report():

        pdf_file = "ATS_Report.pdf"

        doc = SimpleDocTemplate(pdf_file)

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph("ResumeIQ ATS Report", styles["Title"])
        )

        content.append(
            Paragraph(f"ATS Score: {score:.2f}%", styles["Normal"])
        )

        content.append(
            Paragraph(
                f"Matched Skills: {', '.join(matched)}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Missing Skills: {', '.join(missing_skills)}",
                styles["Normal"]
            )
        )

        doc.build(content)

        return pdf_file


    pdf_file = create_pdf_report()

    with open(pdf_file, "rb") as file:

        st.download_button(
            "Download ATS Report",
            file,
            "ATS_Report.pdf",
            "application/pdf"
        )