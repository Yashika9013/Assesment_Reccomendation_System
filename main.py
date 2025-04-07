from dataset import shl_catalog  # Assuming your dataset is in a file called dataset.py
from recommender import recommend_assessments

# This file is just for testing outside the UI (optional use)
if __name__ == "__main__":
    query = "I am looking for a mid-level management role in the finance sector with leadership responsibilities."
    recommendations = recommend_assessments(query, shl_catalog)

    print("✅ Recommended Assessments:\n")
    for idx, item in enumerate(recommendations, 1):
        print(f"{idx}. {item['name']}")
        print(f"   🔗 URL: {item['url']}")
        print(f"   📄 Description: {item['description']}")
        print(f"   🧠 Type: {item['type']}")
        print(f"   ⏱ Duration: {item['duration']} mins")
        print(f"   🌐 Remote: {item['remote']}")
        print("-" * 60)
