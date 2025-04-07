# recommender.py
from sentence_transformers import SentenceTransformer, util

# Load model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

SIMILARITY_THRESHOLD = 0.5  # Only include results above this threshold

def recommend_assessments(user_input, shl_catalog, top_n=10):
    """
    Recommend SHL assessments based on semantic similarity of user input.
    """
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    catalog_texts = [item["name"] + " " + item["description"] for item in shl_catalog]
    catalog_embeddings = model.encode(catalog_texts, convert_to_tensor=True)

    similarity_scores = util.cos_sim(user_embedding, catalog_embeddings)[0]
    
    # Filter and sort based on similarity threshold
    scored_items = [
        (float(score), item)
        for score, item in zip(similarity_scores, shl_catalog)
        if float(score) >= SIMILARITY_THRESHOLD
    ]
    scored_items.sort(reverse=True, key=lambda x: x[0])

    return [item for _, item in scored_items[:top_n]]


# --- Accuracy Eval (Optional) ---
def evaluate_accuracy(test_queries, shl_catalog, ground_truth):
    """
    Evaluates Recall@3 and MAP@3 for a set of test queries.
    test_queries: list of user input strings
    ground_truth: list of list of ground truth assessment names (each element is list of expected results)
    """
    recall_at_3 = []
    average_precisions = []

    for query, expected in zip(test_queries, ground_truth):
        results = recommend_assessments(query, shl_catalog, top_n=3)
        predicted = [item['name'] for item in results]

        # Recall@3
        hits = sum(1 for name in predicted if name in expected)
        recall = hits / len(expected) if expected else 0
        recall_at_3.append(recall)

        # MAP@3
        ap = 0.0
        hits = 0
        for i, name in enumerate(predicted):
            if name in expected:
                hits += 1
                ap += hits / (i + 1)
        ap /= min(len(expected), 3)
        average_precisions.append(ap)

    return {
        "Mean Recall@3": sum(recall_at_3) / len(recall_at_3),
        "Mean AP@3": sum(average_precisions) / len(average_precisions)
    }