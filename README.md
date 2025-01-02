# DocQ - AI-Powered Document Q&A Assistant

**DocQ** is an AI-powered assistant designed to help you extract insights from documents effortlessly. Whether you're dealing with PDFs, spreadsheets, or images, DocQ uses advanced AI to analyze content and provide accurate answers based on user questions.

---

## Features
- **AI-Powered Search:** Utilizes embeddings and similarity metrics for fast and accurate results.
- **Natural Language Queries:** Ask questions in plain English, and get meaningful responses.
- **User-Friendly Interface:** Easy-to-use interface built with Streamlit.

---

## Getting Started

### **1. Clone the Repository**
```bash
git clone https://github.com/username/DocQ.git
cd DocQ
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set Environment Variables**
Create a `.env` file in the root directory and add the following:
```
OPENAI_API_KEY="your_openai_api_key"
``` 

### **4. Run the Application**
```bash
streamlit run app.py
```

---

## Usage
1. **Upload Documents:** Use the sidebar to upload PDFs, spreadsheets, docs or directly from the web.
2. **Ask Questions:** Enter your query in the input box.
3. **Get Answers:** View responses based on your document.

---

## Technologies Used
- **Python**: Core programming language.
- **OpenAI GPT Models**: For natural language processing.
- **Streamlit**: User interface framework.
- **Sentence-Transformers**: For embedding generation.
- **OCR**: For extracting text from images.

---
