# Guided Analytics Platform 🚀

Transform your raw CSV data into actionable business intelligence in minutes. This Streamlit-based application allows users to upload datasets, automatically map columns to a standardized schema, and visualize key metrics through a premium, executive-level dashboard.

## ✨ Key Features

- **📂 Easy Data Upload**: Drag & drop support for CSV files with flexible schema support.
- **🧠 Intelligent Auto-Mapping**: Automatically detects and maps columns (e.g., Dates, Revenue, Quantity) to a canonical schema using robust rule-based logic.
- **📊 Executive Dashboard**:
    - **Time Series Analysis**: Track revenue and sales trends over custom timeframes.
    - **Cohort Analysis**: Analyze customer retention and behavioral cohorts.
    - **Segmentation**: Deep dive into top-performing products, customer demographics, and more.
- **🛡️ Reliable Processing**: built on deterministic logic to ensure 100% accuracy in data handling.
- **🎨 Premium UI**: Designed with a modern, dark-mode aesthetic and fully interactive Plotly charts.

## 🛠️ Prerequisites

- Python 3.11 or higher

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd guided-analytics-platform
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # Linux/Mac
    python -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

Run the application using Streamlit:

```bash
streamlit run main.py
```

Navigate to `http://localhost:8501` in your browser.

## 📂 Project Structure

```text
guided-analytics-platform/
├── main.py                 # Application entry point and landing page
├── models/                 # Data validation schemas (Pydantic)
├── pages/                  # Streamlit application pages
│   ├── 1_Upload_Data.py    # Data ingestion and mapping interface
│   └── 2_Analytics.py      # Interactive analytics dashboard
├── utils/                  # Helper utilities
│   ├── mapping_rules.py    # Heuristic logic for column mapping
│   ├── ui.py               # Custom UI styling and components
│   └── ...                 # Validation, profiling, and canonical logic
└── requirements.txt        # Project dependencies
```

## 💡 How It Works

1.  **Upload**: Navigate to the **Upload Data** page and provide your raw CSV file.
2.  **Map**: The system scans your file and suggests mappings for standard fields (e.g., *Date*, *Revenue*, *Product*). Review and adjust these mappings if necessary.
3.  **Analyze**: Switch to the **Analytics** page to explore the automatically generated insights and visualizations.

## 🤝 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.
