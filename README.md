# SafePause 🛡️

**A simulated UPI payment safety system that identifies suspicious payment patterns and pauses risky transactions for review.**

SafePause is a prototype that demonstrates how a payment safety layer can evaluate multiple risk signals before a simulated payment is approved.

## ✨ Features

- **Risk classification:** Classifies simulated payments into GREEN, AMBER, or RED risk tiers.
- **Multiple risk signals:** Considers phone calls, remote access, first-time payees, simulated mule lists, and behavioral signals.
- **Mock bank API:** Simulates payment processing based on the risk assessment.
- **Fail-safe behavior:** Does not process a payment when the risk engine is unavailable.
- **Browser interface:** Provides a simple interface to submit simulated payments and view risk explanations.
- **Explainable decisions:** Returns the risk factors that contributed to each decision.

## 🏗️ Architecture

```text
Browser UI (phone.html)
        |
        v
Mock Bank API (Port 8002)
        |
        v
Risk Engine API (Port 8001)
        |
        v
Rule-Based Risk Classification
        |
        v
GREEN / AMBER / RED
```

## 🧰 Tech Stack

- Python
- FastAPI
- Uvicorn
- HTML and JavaScript
- Pydantic
- Requests
- Pytest-style assertions for basic rule testing

## 📁 Project Structure

```text
safepause/
├── bank/
│   └── api.py
├── engine/
│   ├── api.py
│   ├── rules.py
│   └── test_rules.py
├── eval/
├── sim/
│   └── scenarios.json
├── ui/
│   └── phone.html
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Setup and Run

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd safepause
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start the risk engine

Open a terminal in the project directory:

```powershell
python -m uvicorn engine.api:app --reload --port 8001
```

### 5. Start the mock bank API

Open a second terminal, activate the virtual environment, and run:

```powershell
python -m uvicorn bank.api:app --reload --port 8002
```

### 6. Open the interface

Open `ui/phone.html` in your browser and submit a simulated payment.

The interface sends requests to the mock bank API, which requests a risk assessment from the risk engine.

## 🧪 Run the Rule Tests

With the virtual environment activated, run:

```powershell
python -m engine.test_rules
```

The tests check GREEN, AMBER, and RED classifications.

## 🔐 Important Disclaimer

SafePause is an educational prototype. It does not connect to UPI, a real bank, or any live payment network. Its risk signals are simulated, and its classifications should not be interpreted as a production-grade fraud detection system.

## 🔮 Future Improvements

- Add more simulated payment scenarios and evaluation metrics.
- Build a more detailed transaction-risk dashboard.
- Improve rule testing and document false-positive and false-negative cases.
- Explore machine-learning-based risk scoring and model evaluation.
