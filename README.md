# AI Powered Regulatory Compliance Checker for Contracts

This project aims to build an AI-driven platform that automatically analyzes contracts and verifies their compliance against applicable laws, regulations, and policies. By leveraging Advanced Large Language Models (LLMs) and LangChain frameworks the system helps businesses, legal teams, and compliance officers reduce manual effort, minimize risks, and ensure adherence to evolving regulations.

---
## 🎯 Key Features
- **Contract Ingestion** – upload contracts in pdf or doc format
- **Compliance Analysis** – detect non-compliance clauses and highlight risks  
- **Explainable AI Reports** – summaries with risk scoring and recommendations
- **Accessible Reports** - AI rewrites high/medium risk clauses for better compliance which can be downloaded by the user as a pdf.
---
- **Note** - AI does not change the original contract with rewritten clauses. It is only meant for better understanding of the user and is up to them to apply those changes.
---
## 📁 Project Structure

```bash
Compliance-Checker/
│
├── app.py                    # Main application entry (UI / execution)
├── config.py                 # Model-switching 
├── contract_analyzer.py      # Contract analysis logic
├── llm_analyzer.py           # LLM-based clause understanding & inference
├── data_handler.py           # File handling, preprocessing, chunking
├── pdf_generator.py          # Generates final analysis report (PDF)
├── email_notifier.py         # Sends report via email (optional)
├── auth_manager.py           # Authentication / access control
│
├── requirements.txt          # Project dependencies
├── .env.example              # Environment variables template
├── .gitignore
├── LICENSE
├── README.md
│
└── ARCHITECTURE.jpg         # System architecture diagram
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Shriya-Guptaa/Regulatory-Compliance-Checker.git
cd Regulatory-Compliance-Checker
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file using the template:

```bash
cp .env.example .env
```

Update values such as:

* API keys (LLM provider if used)
* Email credentials (for notifications)

---

### 5. Run the Application

```bash
python app.py
```

---

## 🧠 System Workflow

1. **Input Handling**

   * Upload contract (PDF)

2. **Preprocessing**

   * Text extraction using `data_handler.py`
   * Chunking for LLM processing

3. **Clause Analysis**

   * `llm_analyzer.py` extracts clause-level meaning
   * Semantic understanding using fine-tuned LLM

4. **Compliance Checking**

   * `contract_analyzer.py` applies rules/policies
   * Flags non-compliant clauses with explanations

5. **Report Generation**

   * Structured output generated via `pdf_generator.py`

6. **Notification**

   * Report sent via `email_notifier.py`
