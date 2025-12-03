# 🤖 DIY Agent-Based Modeling (ABM) Project

## ✨ General Description

This project implements a foundational **Agent-Based Model (ABM)** simulation focused on modeling the basic **physical and metabolic states** of autonomous software agents. Each agent maintains key biological statistics—such as **weight**, **BMR (Basal Metabolic Rate)**, **hunger**, and **thirst**—and interacts with an environment by consuming resources from its **inventory** (foods and drinks) to sustain survival.

The core mechanism is the **ingestion cycle**, which calculates daily caloric and hydration needs, tracks resource depletion, and triggers iterative consumption until satiety is reached.

---

## 🎯 Motivation: Why I Built This

I created this ABM project to **deeply understand the concepts of Agent-Based Modeling (ABM)** and **apply them using pure, foundational code**—without relying on complex, pre-built simulation frameworks.

This low-level approach allows full transparency and control over:

- Internal agent state updates  
- Metabolism simulations  
- Resource usage  
- Emergent environmental behavior  

---

## ⚙️ Tech Stack

| Component | Technology | Role |
|----------|------------|------|
| **Backend/API** | **Python** | Core simulation logic, ingestion system, database operations |
| **Web Framework** | **FastAPI** | High-performance asynchronous API |
| **Database** | **MongoDB** | Persistent storage for agents and inventories |
| **Frontend** | **HTML, JavaScript, Tailwind CSS** | Real-time dashboard visualization |
| **Environment** | **venv (Virtual Environment)** | Python dependency isolation |
| **Server** | **Uvicorn** | ASGI server for FastAPI |

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

---

### ✅ 1. Prerequisites

Make sure you have the following installed:

- **Python 3.8+**
- **MongoDB** (running locally or accessible via a MongoDB URI)

---

### ✅ 2. Setup & Installation

```bash
# 1. Navigate to the project root directory
cd root/diy-abm-project

# 2. Activate virtual environment (Windows PowerShell)
./venv/Scripts/activate.ps1

# 3. Navigate into the server directory
cd server

# 4. Install Python dependencies
pip install -r requirements.txt
```

---

### ✅ 3. Running the Simulation

Start the FastAPI backend using Uvicorn:

```bash
# Ensure you are inside the 'server' directory
uvicorn app.main:app --reload
```

✅ Server will start at:

```
http://127.0.0.1:8000
```

---

### ✅ 4. Accessing Dashboard & API Docs

| Resource | URL | Description |
|----------|-----|-------------|
| **API Documentation** | `http://localhost:8000/docs` | Interactive Swagger UI |
| **Agent Dashboard** | `root/client/index.html` | Real-time visualization of agent states |

---

## ⚠️ Important Configuration Notes

### 🔹 MongoDB Connection

Ensure your FastAPI server is configured with a valid MongoDB connection URI in your database configuration file.

### 🔹 Metrics Configuration

The simulation relies on physical constants from:

```
.../metrics/physical/ingest_metrics.py
```

Modifying values such as:

- `bmr_weight_co`
- `kcal_per_kg_gain`
- `hydration_decay_rate`

will directly affect:

- Hunger rate  
- Thirst rate  
- Weight gain/loss  
- Survival behavior  

---

## ✅ Key Features

- ✅ Real-time agent metabolism simulation  
- ✅ Dynamic hunger & thirst system  
- ✅ Inventory-based food & water consumption  
- ✅ MongoDB-based persistence  
- ✅ FastAPI-powered real-time API  
- ✅ Frontend live monitoring dashboard  
- ✅ Modular metrics & physics system  

---

## 🧪 Purpose & Future Plans

This project serves as:

- A **learning sandbox for ABM**
- A **foundation for AI-driven social simulations**
- A base for future expansions such as:
  - Agent emotions
  - Reproduction systems
  - Economy
  - Disease spread
  - Social interaction networks

---

## 🧑‍💻 Author

Built with ❤️ for learning and experimentation.

**Developer:** *Nyx Nemesis*  
**Field:** Computer Science / AI / Simulation Systems  

---

## ⭐ Support

If you like this project, feel free to:

- ⭐ Star the repository  
- 🐛 Report issues  
- 🚀 Suggest new features  

---
