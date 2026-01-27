from collections import Counter

def identify_research_gaps(keywords_per_paper, labels, min_freq=2):
    """
    Identify research gaps based on low-frequency but important keywords
    """

    # Flatten all keywords
    all_keywords = [kw for paper in keywords_per_paper for kw in paper]

    keyword_counts = Counter(all_keywords)

    # Low-frequency keywords
    low_freq_keywords = {
        kw for kw, count in keyword_counts.items()
        if count <= min_freq
    }

    gaps = {}

    # Associate gaps with clusters
    for paper_keywords, cluster_id in zip(keywords_per_paper, labels):
        for kw in paper_keywords:
            if kw in low_freq_keywords:
                gaps.setdefault(cluster_id, set()).add(kw)

    return gaps