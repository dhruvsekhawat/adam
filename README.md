# **Adam-AI**  
### **An AI-Powered Executive Assistant for Smarter Workflows**  

Adam-AI is an intelligent, privacy-focused AI assistant designed to **automate executive tasks**, **manage communications**, and **seamlessly integrate** with business applications. Unlike traditional cloud-based AI solutions, Adam-AI runs **locally** or in a **self-hosted environment**, ensuring **data privacy and security** while optimizing task management.  

---

## **🚀 Features**
### **1. AI-Powered Task Automation**  
- Draft and send **emails** based on context and history.  
- Automate **calendar scheduling** and meeting coordination.  
- Summarize **Slack & Microsoft Teams messages** and extract key takeaways.  

### **2. Seamless App Integration**  
- Connect with **Outlook, Gmail, Slack, Asana, DocuSign, and other business tools**.  
- Retrieve and analyze **financial reports, contracts, and documents**.  
- Manage **real-time notifications** from multiple applications.

### **3. Privacy-First AI Execution**  
- Runs **locally** using **Mistral-7B** for AI inference, ensuring **data never leaves your system**.  
- **No third-party API dependencies** for AI processing.  
- Secure authentication using **OAuth 2.0**.

### **4. Real-Time AI Assistance**  
- WebSocket-based interactions for **instant task execution**.  
- AI-driven **multi-agent processing** to handle multiple workflows.  

---

## **🛠️ Tech Stack**
| Component  | Technology Used |
|------------|----------------|
| **Frontend**  | React (Vite), Zustand (State Management), TailwindCSS |
| **Backend**   | FastAPI, PostgreSQL, WebSockets |
| **AI Engine** | Mistral-7B (LLM) |
| **Database**  | PostgreSQL (structured data), ChromaDB (RAG for AI memory) |
| **Deployment**| Docker, Docker Compose |

---

## **📂 Project Structure**
```
adam-ai/
│── 📂 apps/                     # Main applications
│   ├── 📂 web/                  # React frontend
│   ├── 📂 api/                  # FastAPI backend
│   ├── 📂 worker/               # Background processing (task queues)
│
│── 📂 services/                  # AI & automation services
│   ├── 📂 auth/                 # OAuth, JWT authentication
│   ├── 📂 chat/                 # WebSockets for real-time messaging
│   ├── 📂 documents/            # DocuSign & document management
│   ├── 📂 email/                # Email automation
│   ├── 📂 notifications/        # Push notifications & alerts
│   ├── 📂 ai/                   # Mistral LLM processing, RAG, and AI logic
│
│── 📂 database/                 # DB models & connections
│── 📂 shared/                   # Common utilities (logging, config)
│── 📂 infra/                    # Docker, CI/CD pipelines
│── 📂 scripts/                  # Deployment automation scripts
│── .env                         # Environment variables
│── README.md                    # Documentation
```

---

## **🔧 Setup & Installation**
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/adam-ai.git
cd adam-ai
```

### **2. Setup the Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **3. Setup the Frontend**
```bash
cd frontend
npm install
npm run dev
```

### **4. Run with Docker**
```bash
docker-compose up --build
```

---

## **🛡️ Security & Privacy**
Adam-AI prioritizes **user data security**:
- **Fully local execution** (no cloud data processing).  
- **OAuth 2.0 authentication** for secure API access.  
- **No hardcoded credentials**, all secrets stored in `.env` files.

---

## **📖 Documentation**
Full documentation is available in the `/docs` folder.


---