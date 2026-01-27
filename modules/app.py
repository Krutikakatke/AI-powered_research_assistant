import os
from flask import Flask, render_template, request

from modules.pdf_extraction import process_pdf
from modules.preprocessing import clean_text
from modules.keyword_extraction import extract_keywords
from modules.clustering import cluster_papers
from modules.gap_detection import identify_research_gaps
from modules.recommendation import generate_recommendations
from modules.report_saver import save_report

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    results = None

    if request.method == "POST":
        files = request.files.getlist("pdfs")

        corpus = []
        paper_names = []

        # Save uploaded PDFs
        for file in files:
            if file.filename.endswith(".pdf"):
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)

                data = process_pdf(filepath)
                raw_text = data["abstract"] + " " + data["body"]
                cleaned = clean_text(raw_text)

                corpus.append(cleaned)
                paper_names.append(file.filename)

        # Run pipeline only if enough papers
        if len(corpus) >= 2:
            # Module 3: Keyword Extraction
            keywords, tfidf_matrix, _ = extract_keywords(corpus, top_n=10)

            # Module 4: Clustering
            labels, _ = cluster_papers(tfidf_matrix, num_clusters=3)

            # Module 6: Gap Detection
            gaps = identify_research_gaps(keywords, labels)

            # Human-readable cluster labels
            cluster_labels = {
                0: "Foundations of Machine Learning",
                1: "Explainable AI",
                2: "Model Performance and Evaluation"
            }

            # Module 7: Recommendations
            recommendations = generate_recommendations(gaps, cluster_labels)

            # Combine paper-wise results
            paper_results = []
            for name, kws, label in zip(paper_names, keywords, labels):
                paper_results.append({
                    "name": name,
                    "keywords": kws,
                    "cluster": cluster_labels.get(label, f"Cluster {label}")
                })

            # 🔥 FINAL RESULTS DICTIONARY
            results = {
                "papers": paper_results,
                "gaps": gaps,
                "recommendations": recommendations
            }

            # ✅ SAVE OUTPUT HERE (CORRECT PLACE)
            saved_file = save_report(results)
            results["saved_file"] = saved_file

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)