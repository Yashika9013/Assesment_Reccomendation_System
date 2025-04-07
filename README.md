# 🧠 SHL GenAI Assessment Recommender

An intelligent recommendation system that matches job-related queries or descriptions to SHL’s catalog of pre-built assessments. Built using **FastAPI** for the backend and **Streamlit** for the interactive frontend demo.

---

## 🌐 Demo

**Live Streamlit App**: [🔗 Click here to try the demo](#)  
*(Replace `#` with your deployed URL)*

---

## 📌 Features

- 🔍 **Natural Language Input** — Just type a job role or description.
- 📊 **Intelligent Matching** — Recommends best-fit SHL assessments.
- 💡 **Prebuilt Catalog** — Uses structured SHL test data.
- 🧪 **Evaluation Module** — Benchmark Recall@3 and MAP@3.
- 🌐 **REST API** — POST endpoint to get JSON-based recommendations.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Similarity Matching**: scikit-learn TF-IDF
- **Data**: SHL Assessment Catalog (structured as JSON/dict)

---

## 🚀 API Usage

### Endpoint: `POST /recommend`

**URL**: `http://127.0.0.1:8000/recommend`  
**Body:**

```json
{
  "query": "I'm hiring for a customer support role in retail."
}
