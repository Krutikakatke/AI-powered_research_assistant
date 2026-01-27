import os
from datetime import datetime


def save_report(results):
    """
    Save analysis results to a text file
    """

    os.makedirs("outputs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"outputs/paperlens_report_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write("PAPERLENS AI – ANALYSIS REPORT\n")
        f.write("=" * 40 + "\n\n")

        # Paper-wise results
        f.write("PAPER-WISE KEYWORDS & CLUSTERS\n\n")
        for paper in results["papers"]:
            f.write(f"Paper: {paper['name']}\n")
            f.write(f"Cluster: {paper['cluster']}\n")
            f.write("Keywords:\n")
            for kw in paper["keywords"]:
                f.write(f" - {kw}\n")
            f.write("\n")

        # Research gaps
        f.write("\nRESEARCH GAPS\n\n")
        for cluster, kws in results["gaps"].items():
            f.write(f"Cluster {cluster}:\n")
            for kw in kws:
                f.write(f" - {kw}\n")
            f.write("\n")

        # Recommendations
        f.write("\nFUTURE RESEARCH RECOMMENDATIONS\n\n")
        for rec in results["recommendations"]:
            f.write(f"- {rec}\n")

    return filename