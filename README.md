# 🛡️ AI-Powered Network Intrusion Detection System (NIDS)

An end-to-end cybersecurity framework designed to monitor network traffic patterns and instantly flag potential malicious behavior. Using the benchmark **NSL-KDD dataset**, this project transitions from exploratory data insights to a production-grade **Random Forest Classifier**, serving predictions via an interactive **Streamlit web dashboard**.

---

## 📌 Project Architecture & Workflow

The project framework is cleanly split into three distinct pipeline layers:

1. **Exploratory Data Analysis (`network analysis data.ipynb`)**
   * Processes the raw text data stream, fixes missing headers, and maps structural shapes.
   * Leverages `matplotlib` and `seaborn` boxplot matrices to isolate numerical traffic outliers.
   * Simplifies 23 hyper-specific network attack categories into a baseline binary classification structure (`0` for normal traffic, `1` for active attacks).

2. **Automated Production Training (`train.py`)**
   * Ingests the raw data and applies categorical structure maps via one-hot encoding.
   * Preserves structural layouts (`model_features.pkl`) to guarantee the web application matches exact input expectations.
   * Trains a Random Forest Classifier ensemble of 100 Decision Trees to make a optimized predictive "brain".
   * Serializes the trained model into a production binary (`nids_model.pkl`).

3. **Interactive Web UI Dashboard (`app.py`)**
   * Built entirely using **Streamlit**, providing a visual UI for router simulation.
   * Allows users to modify packet details dynamically via sliders and selectors.
   * FEeds raw simulated connections to the machine learning engine to spit out real-time threat verdicts and exact percentage confidence scores.

---

## 🗂️ Project File Structure

```text
├── network analysis data.ipynb  # Step 1: Data cleaning, analysis & boxplot visualizations
├── train.py                     # Step 2: Core ML training pipeline execution script
├── app.py                       # Step 3: Streamlit interactive web dashboard layer
├── KDDTrain+.txt                # Raw source NSL-KDD dataset (User provided)
├── requirements.txt             # Unified Python environment dependencies
├── model_features.pkl           # Saved mathematical feature column indices 
├── nids_model.pkl               # Fully optimized, serialized Random Forest model binary
└── LICENSE                      # Legal open-source permissions file (NEW)
```


## 🛠️ Complete Step-by-Step Setup Guide
Follow these steps exactly to configure your environment and execute the project from a blank slate.

**Step 1: Open Your Terminal & Navigate**
Open your Terminal (macOS/Linux) or Command Prompt/PowerShell (Windows) and move into your project root folder:

cd path to your/project-folder

**Step 2: Establish a Virtual Environment (Recommended)**
Creating an isolated virtual environment prevents dependencies from conflicting with other global software on your computer.

# Create the virtual environment named 'nids_env'
python -m venv nids_env

# Activate the environment:

# On Windows (Command Prompt):
nids_env\Scripts\activate
# On Windows (PowerShell):
.\nids_env\Scripts\Activate.ps1

# On macOS / Linux:
source nids_env/bin/activate

**Step 3: Install All Project Dependencies**
Ensure your requirements.txt is populated with pandas, numpy, scikit-learn, joblib, matplotlib, seaborn, notebook, and streamlit. Then run:

pip install --upgrade pip
pip install -r requirements.txt

**Step 4: Verify Dataset Placement**
Ensure that your raw data file, KDDTrain+.txt, is downloaded and placed directly inside your main project root directory alongside train.py.

## 🚀 Execution & Operational Guide
1. (Optional) Run the Notebook Visualizer
To view data distributions, missing value matrices, or outlier boxplots, spin up your local Jupyter environment:

jupyter notebook

Click on network analysis data.ipynb in the opened browser window and run the cells sequentially.

2. Execute the Automated Training Engine
To process the data pipeline, convert labels, and compile your AI models, type:

python train.py

This will create the outputs/ folder and generate your nids_model.pkl and model_features.pkl files.

3. Launch the Streamlit Web UI Application
Once the training script is complete, launch the live network packet simulation dashboard using:

streamlit run app.py

Streamlit will host the application locally and automatically open a tab in your default web browser (usually at http://localhost:8501).

## 📊 Expected Terminal Logging Outputs

During python train.py:
🌱 Random seed set to: 42
📥 Loading dataset from KDDTrain+.txt...
📊 Data successfully split. Training shapes: (100777, 122), Test shapes: (25195, 122)
💾 Feature structural layout saved to: outputs/model_features.pkl
🛡️ Training Random Forest (Trees: 100, Max Depth: 12)...

🧐 Evaluating model performance on validation data...
✨ Validation Accuracy: 0.9924

📋 Detailed Classification Metrics Report:
              precision    recall  f1-score   support

  Normal (0)       0.99      1.00      0.99     13431
  Attack (1)       1.00      0.99      0.99     11764

✅ Training complete. Production model saved successfully at: outputs/nids_model.pkl

## 🛡️ Live Dashboard Guide
Inside the Streamlit Web Application interface, you can test the AI limits:

**Simulate a Safe Connection:**
Set Protocol Type to tcp, Network Service to http, Connection Flag to SF, and leave error sliders down at 0.0. The dashboard will return a 🟢 SYSTEM SECURE confirmation status.

**Simulate a Denial of Service (DoS) Attack:**
Use the sidebar sliders to push the Connections to same host (count) to maximum, and slide the Host Syn Error Rate (serror_rate) up to 1.0. The model will instantly switch, trigger a flashing 💥 ALERT: DETECTED MALICIOUS NETWORK INTRUSION banner, and display an elevated Intrusion Risk Score.

📜 License
This project is open-source and available under the terms of the MIT License.
