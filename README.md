# SafePause 🛡️

**A simulation-only UPI payment safety prototype that evaluates suspicious payment patterns and flags risky transactions for review.**

SafePause demonstrates how a payment safety layer can evaluate multiple risk signals before a simulated payment decision is made. It combines a rule-based risk engine, a mock bank API, and a browser-based interface to explain why a transaction receives a particular risk tier.

> **Disclaimer:** SafePause is an educational prototype. It does not connect to UPI, real banks, or live payment networks. Its risk signals and transactions are simulated and are not evidence of production-grade fraud detection.

## ✨ Features

- **Three-tier risk classification:** Assigns simulated transactions GREEN, AMBER, or RED risk tiers.
- **Multiple risk signals:** Considers phone calls, remote access, screen sharing, first-time payees, simulated mule lists, VPA lookalike scores, unusual behavior, and recent device or SIM changes.
- **Explainable decisions:** Returns risk factors and explanations alongside the classification.
- **Mock bank API:** Maps risk decisions to simulated approval, user confirmation, or review.
- **Fail-safe handling:** Returns an error when the risk engine is unavailable instead of silently approving a transaction.
- **Browser interface:** Supports simulated payment submissions and displays risk results.
- **Transaction history:** Stores recent simulated transaction records in browser local storage.
- **Automated testing:** Includes rule-engine, API, payment-flow, and failure-handling tests.
- **Evaluation scripts:** Evaluates risk-tier scenarios and a manually labelled synthetic dataset.

## 🏗️ Architecture

```text
Browser UI (ui/phone.html)
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
          |
          v
Simulated Payment Decision
```

### Risk decision mapping

| Risk tier | Simulated outcome |
|---|---|
| GREEN | `SIMULATED_APPROVED` |
| AMBER | `CONFIRM_WITH_USER` |
| RED | `PAUSED_FOR_REVIEW` |

These outcomes demonstrate prototype behavior only; they do not represent decisions made by a real bank.

## 🧰 Tech Stack

- **Language:** Python
- **Backend APIs:** FastAPI, Uvicorn
- **Request validation:** Pydantic
- **HTTP communication:** Requests
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** Pytest, FastAPI TestClient
- **Evaluation:** Python-based evaluation scripts and synthetic labelled scenarios
- **Version control:** Git and GitHub

## 📁 Project Structure

```text
safepause/
├── bank/
│   ├── __init__.py
│   ├── api.py
│   └── test_api.py
├── engine/
│   ├── __init__.py
│   ├── api.py
│   ├── rules.py
│   ├── test_rules.py
│   └── test_api.py
├── eval/
│   ├── run_evaluation.py
│   ├── labelled_scenarios.json
│   ├── evaluate_classifier.py
│   └── add_label_rationales.py
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

Replace `YOUR_REPOSITORY_URL` with your actual Git repository URL.

```powershell
git clone YOUR_REPOSITORY_URL
cd safepause
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, follow your system's Python environment policy rather than changing security settings blindly.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
python -m pip install pytest httpx
```

The second command installs the test tools if they are not already listed in `requirements.txt`.

### 4. Start the risk engine

Open a terminal in the project root:

```powershell
python -m uvicorn engine.api:app --reload --port 8001
```

The risk engine runs at `http://127.0.0.1:8001`.

Interactive API documentation is available at `http://127.0.0.1:8001/docs`.

### 5. Start the mock bank API

Open a second terminal, activate the virtual environment, and run:

```powershell
python -m uvicorn bank.api:app --reload --port 8002
```

The mock bank API runs at `http://127.0.0.1:8002`.

Interactive API documentation is available at `http://127.0.0.1:8002/docs`.

### 6. Open the browser interface

Open `ui/phone.html` in your browser and submit a simulated payment.

The interface sends the payment request to the mock bank API, which requests a risk assessment from the risk engine. The resulting tier and explanation are displayed in the interface.

## 🔌 API Overview

### Risk engine

**Endpoint:** `POST /score`

Example request:

```json
{
  "on_call": true,
  "payee_first_time": true
}
```

This combination is expected to produce an AMBER decision under the current rules.

### Mock bank API

**Endpoint:** `POST /event`

Accepts a simulated payment request and its risk signals. The bank API calls the risk engine and returns a simulated payment outcome.

If risk scoring is unavailable, the API is designed to return HTTP `503 Service Unavailable` rather than treating the payment as approved.

See the interactive API documentation for the complete request schema and response format.

## 🧪 Automated Testing

Run the complete test suite from the project root with the virtual environment activated:

```powershell
python -m pytest -v
```

**Latest recorded test result: 23 passed.**

The tests cover:

- Risk-engine rule behavior.
- GREEN, AMBER, and RED classifications.
- API responses and input validation.
- Mock bank payment outcomes.
- Error handling when the risk engine is unavailable.

Run individual test groups if needed:

```powershell
python -m pytest engine/test_api.py -v
python -m pytest bank/test_api.py -v
python -m engine.test_rules
```

The recorded result is from the current development environment. Run the tests again after code or dependency changes to verify the current state.

## 📊 Evaluation

SafePause includes two evaluation approaches:

1. **Risk-tier scenario evaluation:** Checks the rule engine against predefined scenarios. The latest recorded result was 13/13 scenarios passing.
2. **Synthetic binary classification evaluation:** Evaluates manually labelled NORMAL and RISKY scenarios using a confusion matrix, precision, recall, F1 score, and accuracy.

The latest recorded synthetic classification results were:

| Metric | Result |
|---|---:|
| Accuracy | 88.00% |
| Precision | 88.89% |
| Recall | 94.12% |
| F1 score | 91.43% |

These figures describe performance on a small, manually labelled synthetic dataset only. They must not be interpreted as real-world UPI fraud-detection accuracy or evidence of effectiveness on live banking data.

## 🔐 Limitations

- No connection to real UPI infrastructure, banks, or payment gateways.
- No real payment authorization, transfer, reversal, or settlement.
- Risk signals are simulated rather than obtained from trusted device or banking integrations.
- Rule thresholds and classifications require further validation.
- Synthetic evaluation data is small and manually labelled.
- Browser transaction history is stored locally and is not a shared or server-side audit log.

## 🔮 Future Improvements

- Expand and diversify the synthetic evaluation dataset.
- Investigate false positives and false negatives and improve rule calibration.
- Add more automated tests for invalid requests, timeouts, and unexpected API responses.
- Add structured logging and server-side audit records for the prototype.
- Improve dashboard analytics and risk explanations.
- Compare the rule-based baseline with a carefully evaluated machine-learning model.
- Add authentication and stronger security controls before any broader deployment experiment.

## 👩‍💻 Project Status

SafePause is an actively developed educational prototype focused on explainable risk classification, simulated payment decisions, API integration, and automated testing.
