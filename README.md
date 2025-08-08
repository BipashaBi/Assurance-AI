# Assurance AI – Bajaj Finserv Hackathon Submission  

## 🚀 Overview  

**Assurance AI** is an intelligent document reasoning platform designed to simplify the analysis of complex insurance policy documents.  
Users can upload one or more policy files (PDF or DOCX) and ask natural language questions.  
The system uses **FAISS** for semantic clause retrieval and **Gemini 1.5 Flash** for reasoning, delivering structured, justified answers in JSON format.  

> 💡 Inspired by real-world challenges in the insurance sector, Assurance AI aims to bring speed, accuracy, and transparency to policy understanding.  

---

## 🎯 Problem Statement  

Insurance policy documents are often lengthy, full of technical terms, and prone to misinterpretation.  
Manual reading takes time, and missing critical clauses can have serious consequences for customers and insurers alike.  

**Assurance AI** addresses this problem by:  
- Parsing and structuring uploaded policy documents  
- Retrieving the most relevant clauses using semantic search  
- Generating clear, structured, and justified answers using AI  

📌 Problem Statement: [HackRx 6.0](https://hackrx.in/#problem-statement)  

---

## ✅ Key Features  

- **Multi-File Upload** – Supports multiple PDF/DOCX files in a single session  
- **Session-Based Indexing** – Each session has its own FAISS index for data isolation  
- **Smart Clause Search** – AI retrieves only the most relevant clauses for the query  
- **Structured JSON Decisions** – Consistent, machine-readable outputs for integration  
- **Streamlit UI** – Intuitive front-end for document upload and Q&A  

---

## 🧠 Tech Stack  

| Component     | Technology/Tool                 | Version                      |
| ------------- | ------------------------------- | ---------------------------- |
| Backend       | FastAPI                         | 0.110.0                      |
| Embedding     | SentenceTransformers (MiniLM)   | sentence-transformers==2.2.2 |
| Vector Search | FAISS                           | faiss-cpu==1.7.4             |
| LLM           | Gemini 1.5 Flash (Google AI)    | gemini-1.5-flash             |
| Frontend      | Streamlit                       | 1.33.0                       |
| Storage       | Session-based folders in `/data`| -                            |

---

## 🧩 Version Progress  

### **V1 – Basic Version**  
- Single document upload  
- Static FAISS index location  
- Simple Gemini-based Q&A  

### **V2 – Enhanced Version**  
- Multiple document upload in one session  
- Dynamic session-based FAISS index (`session_<timestamp>`)  
- Persistent session ID for repeated queries  
- Fully integrated upload → query loop in UI  

---
## 🗂️ Folder Structure
```
project/
├── app/
│ ├── core/
│ │ ├── engine.py # Gemini prompting logic
│ │ ├── retriever.py # FAISS index building & querying
│ │ └── embedder.py # Text embeddings
│ ├── ingestion/
│ │ ├── load.py # Load content from files
│ │ └── chunk.py # Chunk raw text
│ └── main.py # FastAPI app
├── ui/
│ └── app.py # Streamlit interface
├── data/
│ └── session_<id>/index/ # Saved FAISS index + chunks
├── config/
│ └── config.yaml # API keys and settings



```
Mermaid Diagram: [AssuranceAI](assuranceAI.png)  

---

## 🔍 Example Output  

**Query:**  
*"Is cataract surgery covered?"*  

**JSON Output:**  
```json
{
  "decision": "rejected",
  "amount": null,
  "justification": "The provided policy clauses do not contain any information regarding coverage for cataract."

}

```

**Referenced Clauses**:

* Clause 1: "We cover maternity-related hospitalization expenses..."
* Clause 2: "Air ambulance service is provided in emergency..."

---

## 🚰 How It Works

1. **Upload Endpoint** (`/upload_docs`) parses and chunks all uploaded files
2. **Text is embedded** and stored in a FAISS index saved under `/data/session_<timestamp>/`
3. **Query Endpoint** (`/query`) takes user query + session ID, retrieves relevant clauses, and forwards them to Gemini
4. **Gemini generates** a JSON-based decision with reasoning and references

---

## 💡 Future Improvements

* Multi-user login & session history
* Highlighting relevant source lines in UI
* Exportable reports (PDF/JSON)
* Analytics dashboard for policy trends

---


## 👥 Team

**Team Leader**: Archita Saha
**Hackathon**: Bajaj Finserv Hackathon 2025

---

## 📬 Contact

* **LinkedIn** – [Archita Saha](https://www.linkedin.com/in/architasaha21/)
* **Mail** - archita.saha2106@gmail.com
* **LinkedIn** - [Bipasha Biswas](www.linkedin.com/in/bipasha-biswas-9jan2005/)
* **Mail** - bipashab497@gmail.com

---
