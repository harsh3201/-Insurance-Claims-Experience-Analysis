# Insurance Claims Experience Analysis 🧩

### Project Overview
This project analyzes the insurance claim lifecycle to identify bottlenecks, evaluate channel performance, and suggest product improvements. By treating insurance claims as a product problem, we aim to reduce Turnaround Time (TAT) and improve the transparency of the user journey.

### 📊 Key Metrics
*   **Average TAT:** Overall time from submission to approval.
*   **Approval Rate:** Percentage of successfully processed claims.
*   **Rejection Rate:** Analysis of why claims fail (Top reason: Missing Documents).
*   **Channel Performance:** Comparison of App vs. Web efficiency.

### 🚀 Key Insights
1.  **Life Claims Friction:** Life insurance claims take ~23 days, compared to ~7 days for Motor claims.
2.  **The "Missing Document" Gap:** Over 50% of rejections are due to incomplete documentation at the time of submission.
3.  **App Supremacy:** App users have an 88% document completeness rate, significantly outperforming Web users.

### 💡 Product Recommendations
*   **Smart Document Checklist:** Pre-submission validation to catch missing files.
*   **Claim Status Tracker:** Visual progress bars to improve transparency.
*   **OCR Integration:** Immediate feedback on document quality (blur/legibility).
*   **Omnichannel Guidance:** Shifting users to the App for high-accuracy document uploads.

### 📂 Repository Structure
```text
Insurance-Claims-Experience-Analysis/
│
├── data/
│   └── claims_data.csv             # Simulated dataset (1500 rows)
├── analysis/
│   └── claims_analysis.ipynb       # Jupyter Notebook for EDA
├── dashboard/
│   ├── app.py                      # Streamlit Dashboard code
│   └── dashboard_screenshots/       # Visualizations
├── problem.md                      # Product Question & Context
├── insights.md                     # Detailed data-backed findings
├── recommendations.md              # Proposed product solutions
└── README.md                       # Executive Summary
```

### 🛠 Tech Stack
*   **Python:** Pandas for data manipulation.
*   **Streamlit:** Interactive dashboard.
*   **Matplotlib/Seaborn:** Data visualization.
*   **GitHub:** Project documentation and structure.

---
https://harsh3201--insurance-claims-experience-anal-dashboardapp-pyrj84.streamlit.app/
*Developed as a Product Analyst Portfolio Project.*

