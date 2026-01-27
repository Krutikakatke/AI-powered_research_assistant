import re
from collections import defaultdict
import matplotlib.pyplot as plt


def extract_year_from_filename(filename):
    """
    Extract publication year from arXiv-style filenames
    Example: 2104.05314v2.pdf -> 2021
    """
    match = re.match(r"(\d{2})(\d{2})\.", filename)
    if match:
        year_prefix = int(match.group(1))
        return 2000 + year_prefix
    return None


def compute_keyword_trends(paper_keywords, paper_years):
    """
    Count keyword frequency per year

    paper_keywords: list of keyword lists (per paper)
    paper_years: list of years (per paper)
    """

    trends = defaultdict(lambda: defaultdict(int))

    for keywords, year in zip(paper_keywords, paper_years):
        if year is None:
            continue
        for kw in keywords:
            trends[kw][year] += 1

    return trends


def plot_keyword_trends(trends, top_n=5):
    """
    Plot trend lines for top keywords
    """

    # Select top keywords by total frequency
    keyword_totals = {
        kw: sum(year_counts.values())
        for kw, year_counts in trends.items()
    }

    top_keywords = sorted(
        keyword_totals, key=keyword_totals.get, reverse=True
    )[:top_n]

    for kw in top_keywords:
        years = sorted(trends[kw])
        counts = [trends[kw][y] for y in years]
        plt.plot(years, counts, marker='o', label=kw)

    plt.xlabel("Year")
    plt.ylabel("Frequency")
    plt.title("Research Keyword Trends Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()