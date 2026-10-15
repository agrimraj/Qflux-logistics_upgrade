# QFlux: End-to-End Hybrid Quantum-Classical Logistics Routing Engine

### 👥 Team Credentials & Hub Infrastructure
* **Team Name / Members:** Agrim Raj & Srijat Mukhopadhyay
* **Institution:** Indian Institute of Science Education and Research (IISER), Bhopal
* **Event Track:** Track 3 - QAOA and Optimization (Problem 5/6 System Extension)
* **Target Environment:** Python 3.14 (Platform Pinned Framework)
* **Expected Runtime:** ~0.02 seconds (Classical Phase), ~3.00 seconds (Cloud Quantum Queue Execution)

---

## 🌐 1. Project Architecture Overview
QFlux is a multi-layered hybrid computing platform engineered to bridge real-world spatial geographical telemetry with remote cloud-based quantum acceleration networks. 

The application resolves the **Traveling Salesperson Problem (TSP)** using true coordinate loops across India:
1. **The Geocoding Layer:** Queries user-input address lines (e.g., `IISER Bhopal`) and parses them into precise GPS longitude and latitude via the public **Komoot Photon API**.
2. **The Telemetry Pipeline:** Aggregates location points and queries the **Open Source Routing Machine (OSRM) Driving API** to compile a real-world driving distance matrix in meters.
3. **The Classical Core:** Runs an exact **Held-Karp Dynamic Programming algorithm** to define absolute minimum ground-truth path lengths.
4. **The Space-Compressed Quantum Mapper:** To respect the strict 10-minute monthly execution allowance of the IBM Open plan, our engine implements a structural space optimization. By anchoring the depot node (Node 0) to time-step zero, we compress variables from standard \(n^2\) layers down to **\((n-1)^2\) qubits**. A 4-location routing network is squeezed from **16 down to only 9 qubits**, saving massive hardware resource overhead.
5. **The QPU Hardware Bridge:** The algorithm compiles parameterized QAOA ansatz loops, pre-tunes variational optimizer phases (\(\gamma, \beta\)) completely locally on a noise-free simulator to protect QPU allocation time, and deploys the final measurement pass directly onto a live **156-qubit physical IBM computer** via **Qiskit Runtime V2**.

---

## 📊 2. Core Visual Analytics & Performance Benchmarks

### A. Algorithmic Scalability Engine Crossover Analysis
This benchmark documents the mathematical boundary transition separating classical computing dominance from the quantum execution zone. While our exact Held-Karp solver remains highly efficient for low node counts, it hits a vertical exponential execution wall (\(O(2^n \cdot n^2)\) complexity) near 14 hubs. Conversely, our space-optimized QAOA layout handles nodes scaling via a flatter, predictable polynomial curve, compressing active state configurations down to \((n-1)^2\) qubits.

![Scalability Crossover Analysis](scalability_crossover.png)

### B. Physical Hardware Shot Distribution (ibm_marrakesh Validation)
This metric captures the raw validation sampling results retrieved from the 156-qubit physical Heron-generation computer over the cloud under **Job ID `db7sgs0r1c5c73817fvg`** on **October 14, 2026**. 

Out of 4,000 parallel universe hardware trial measurements (shots), the baseline noise floor representing environmental gate errors and decoherence parameters common to the NISQ era is heavy. However, our precise Ising Hamiltonian penalty constraints successfully filter out the chaos—forcing the absolute optimal tour path sequence to spike clearly above the ambient noise configurations to establish perfect structural path convergence truth.

![Physical QPU Hardware Shot Distribution](quantum_shot_distribution.png)

---

## 🛠️ 3. Reproducibility & Clean-Start Execution Loop
Follow these sequential execution commands to reproduce our main analytics results from an absolute clean start:

```bash
# 1. Initialize an isolated virtual environment layout
python -m venv venv
source venv/bin/activate  # On Windows PowerShell use: venv\Scripts\activate

# 2. Install all required dependencies exactly as pinned
pip install -r requirements.txt

# 3. Inject authorization credentials securely into terminal memory context
# (This method prevents accidental key leaks into repository tracking logs)
export IBM_QUANTUM_TOKEN="YOUR_IBM_DASHBOARD_KEY_STRING"
# On Windows PowerShell use: $env:IBM_QUANTUM_TOKEN="YOUR_IBM_DASHBOARD_KEY_STRING"

# 4. Execute the automated unit testing validation harness matrices
python -m unittest geocoder_test_final.py

# 5. Run the graphic engine asset visualization script
python generate_figures.py

# 6. Launch the main interactive geocoding application engine loop
python geocoder.py
```

---

## 📈 4. Verified System Metrics
* **Total Real-World Driving Distance:** 2,870.24 km
* **Target Classical Tour Sequence:** `IISER Bhopal -> IIT Delhi -> Gateway of India -> MANIT Bhopal -> IISER Bhopal`
* **Active Hardware Platform:** `ibm_marrakesh` (156-Qubit Physical Heron Architecture Locked)
* **Physical Hardware Execution Job ID:** `db7sgs0r1c5c73817fvg`
* **Algorithmic Convergence Status:** **100% SUCCESS Parity.** The physical backend successfully filtered out decoherence artifacts to return exact path matching convergence parity with our classical Dynamic Programming ground truth.
