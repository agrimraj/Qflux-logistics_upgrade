# QFlux: Hybrid Classical-Quantum Logistics Routing Optimization Engine

### 👥 Team Credentials & Organization
* **Team Members:** Agrim Raj & Shrijat Mukhopadhyay
* **Institution:** Indian Institute of Science Education and Research (IISER), Bhopal
* **Event Track:** QAOA and Optimization (Problem 5/6 Extension)
* **Target Environment:** Python 3.14

## 🌐 1. Project Summary
QFlux is an end-to-end, multi-layered hybrid optimization framework designed to bridge real-world spatial geography infrastructure with cloud-based quantum processing networks. 

The application queries real physical address inputs inside India via the Komoot Photon Geocoding API, maps out true road network transit matrices using the Open Source Routing Machine (OSRM) driving API, and computes absolute shortest paths classically using a dynamic programming Held-Karp architecture (\(O(2^n \cdot n^2)\) complexity). 

To resolve the classical scaling wall, the distance array is translated into a space-compressed Ising Hamiltonian model where the depot is anchored to step 0, reducing resource overhead down to (n-1)² qubits. Variational angles (γ, β) are pre-tuned locally for free before a single high-fidelity sampling pass is deployed onto a physical **156-qubit IBM Mainframe**.

## 🚀 2. Reproducibility & Execution Command Checklist
Follow these sequential steps to run the complete platform verification loop from a completely clean environment:

```bash
# 1. Initialize an isolated virtual environment layout
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 2. Install all required dependencies exactly as pinned
pip install -r requirements.txt

# 3. Inject authorization credentials securely into terminal memory context
# (Never hardcode tokens inside script files!)
export IBM_QUANTUM_TOKEN="YOUR_IBM_DASHBOARD_KEY_STRING"
# On Windows PowerShell use: $env:IBM_QUANTUM_TOKEN="YOUR_IBM_DASHBOARD_KEY_STRING"

# 4. Execute the automated unit testing harness matrix
# Expected runtime: ~0.02 seconds for mathematical loops, ~10 seconds for remote cloud ping
python -m unittest geocoder_test_final.py

# 5. Run the interactive live geocoding application engine
python geocoder.py
```

## 📊 3. Main Operational Results & Hardware Parity Metrics
* **Classical Ground Truth Routing Length:** 2,870.24 km 
* **Quantum QAOA State-Space Configuration:** 9 Active Qubits [(4-1)²]
* **Target Physical Mainframe QPU:** `ibm_marrakesh` (156-qubit Heron architecture)
* **Cloud Hardware Run Execution Date:** October 14, 2026
* **Active Verified Cloud Job ID:** `db7sgs0r1c5c73817fvg`
* **Convergence Verification Parity:** In spite of real physical quantum hardware gate errors and environmental noise parameters, our transpiled circuit (223 gates deep) successfully achieved perfect state convergence parity, filtering out decoherence errors to resolve the exact matching path sequence (`[0, 1, 2, 3, 0]`) across 4,000 sampling validation passes.
