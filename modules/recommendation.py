def generate_recommendations(gaps, cluster_labels):
    """
    Generate future research recommendations from identified gaps

    gaps: dict {cluster_id: set(keywords)}
    cluster_labels: dict {cluster_id: cluster_name}
    """

    recommendations = []

    for cluster_id, keywords in gaps.items():
        if not keywords:
            continue

        theme = cluster_labels.get(cluster_id, "this research area")
        keywords_text = ", ".join(sorted(keywords))

        recommendation = (
            f"Future research can focus on {keywords_text} "
            f"in the context of {theme}."
        )

        recommendations.append(recommendation)

    return recommendations