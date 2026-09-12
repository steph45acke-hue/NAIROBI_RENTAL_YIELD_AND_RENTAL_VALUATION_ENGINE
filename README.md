# Nairobi Real Estate Valuation & Rental Yield Analytics Platform

## Project Description
This project is an end-to-end data science and software engineering platform designed to analyze, structure, model, and visualize real estate data across Nairobi. The system transitions from raw data generation and rigorous statistical diagnostics to a normalized relational database architecture, machine learning predictive modeling, and a fully interactive web application dashboard.

## Reason Behind This Project
The motivation behind this project is to bridge the gap between raw real estate market data and actionable, data-driven investment decisions in Nairobi's property sector. By applying advanced statistical modeling, relational database design, and modern machine learning frameworks, this platform demonstrates production-grade software development and data science capabilities tailored to urban economics.

## The Problem Involved
Navigating the Nairobi real estate market often involves fragmented data, lack of transparent property valuation models, and difficulty in accurately forecasting purchase prices based on physical attributes and micro-locations. Real estate investors and buyers struggle to quickly assess fair market values, rental yields, and the precise impact of features like square footage, number of bedrooms, and sub-county locations on property pricing.

## The Solution
The platform provides a comprehensive, automated pipeline that solves these challenges through:
* **Synthetic Data Generation & Scraping:** Simulating robust, structured real estate listings reflecting real Nairobi neighborhoods (e.g., Kilimani, Karen, Kileleshwa, Westlands, Langata).
* **3NF Relational Database Migration:** Structuring data into normalized tables (`Locations`, `Properties`, `Valuations`) managed via SQLAlchemy and MySQL to ensure data integrity.
* **Rigorous Statistical & ML Modeling:** Utilizing Ordinary Least Squares (OLS) regression diagnostics and Random Forest machine learning models to analyze price drivers and feature importances.
* **Interactive Web Dashboard:** Delivering real-time market metrics, dynamic scatter plots, and valuation tools via a Streamlit web interface.

---

## Explanation of Screenshots

### 1. Data Generation Pipeline
![Data Generation Pipeline](assets/Screenshot%20(203).png)
* **Explanation:** This terminal output shows the initialization and execution of the data generation script (`scraper.py`). It successfully generates 250 structured real estate records into a CSV file, previewing attributes like property ID, location, property type, bedrooms, size in square meters, monthly rent, purchase price, and calculated rental yield.

### 2. MySQL Relational Database Ingestion
![MySQL Relational Database Ingestion](assets/Screenshot%20(204).png)
* **Explanation:** This screen illustrates the 3NF migration pipeline (`ingest_to_mysql.py`) running in the terminal. It loads the 250 rows and successfully populates the normalized relational database tables (`Locations`, `Properties`, and `Valuations`), establishing foreign key dependencies and data integrity.

### 3. Database Data Extraction
![Database Data Extraction](assets/Screenshot%20(205).png)
* **Explanation:** Here, the pipeline extracts joined rows directly from the MySQL database back into Python for model consumption. The terminal preview displays properties from Karen with their associated dimensions, pricing, and rental yields.

### 4. Advanced Model Training & Explainability (SHAP)
![Advanced Model Training](assets/Screenshot%20(206).png)
* **Explanation:** This terminal log displays an advanced model training iteration (`train_valuation_model_v2.py`). It extracts data from MySQL, trains on the properties, outputs evaluation metrics ($R^2$ score and Mean Absolute Error), and generates SHAP (SHapley Additive exPlanations) model explanations to interpret feature impacts.

### 5. Statistical Diagnostics & OLS Regression (Part 1)
![OLS Regression Diagnostics](assets/Screenshot%20(209).png)
* **Explanation:** A detailed Ordinary Least Squares (OLS) regression and hypothesis testing diagnostic report. It provides statistical metrics including coefficients, standard errors, $t$-values, $P>|t|$ significance p-values, confidence intervals, R-squared values, and F-statistics to evaluate linear relationships between property features and purchase price.

### 6. Statistical Diagnostics Execution
![Statistical Diagnostics Execution](assets/Screenshot%20(210).png)
* **Explanation:** The terminal view showing the execution command and resulting OLS regression table output, highlighting econometric diagnostics and warnings regarding multicollinearity conditions.

### 7. Regression Diagnostics Script Output
![Regression Diagnostics Script](assets/Screenshot%20(211).png)
* **Explanation:** The execution of `diagnose_regression.py`, confirming the connection to the 3NF database and outputting the full statistical hypothesis testing and OLS regression summary report.

### 8. Random Forest Machine Learning Training
![Random Forest Training](assets/Screenshot%20(212).png)
* **Explanation:** This terminal view displays the training results of the Random Forest Regressor (`train_model.py`). It splits the data into training and testing sets, evaluates performance using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE), and lists the Top 5 price-driving features with their respective feature importances (led by `size_sqm`).

### 9. Streamlit Dashboard: Interactive Scatter Plot View
![Streamlit Scatter Plot](assets/Screenshot%20(213).png)
* **Explanation:** The Streamlit web dashboard running locally at `localhost:8501`, displaying an interactive Plotly scatter plot (`Property Size vs. Purchase Price`) mapping out property distributions across different sub-counties and property types with a custom color-coded legend.

### 10. Streamlit Dashboard: Main Overview & KPIs
![Streamlit Main Dashboard](assets/Screenshot%20(214).png)
* **Explanation:** The main landing view of the Nairobi Real Estate Valuation & Analytics Platform web interface. It highlights high-level Key Performance Indicators (KPIs), including total properties analyzed (250), average purchase price (KES 3,946,648), and average monthly rent (KES 25,162).

### 11. Streamlit Dashboard: Detailed Size vs. Price Distribution
![Detailed Size vs. Price View](assets/Screenshot%20(215).png)
* **Explanation:** A closer look at the interactive Plotly visualization within the Streamlit app, demonstrating dynamic chart controls (zoom, pan, hover tooltips) analyzing property sizes against purchase prices across Nairobi sub-counties.

### 12. Streamlit Dashboard: Sub-County Market Analytics
![Sub-County Analytics Bar Chart](assets/Screenshot%20(216).png)
* **Explanation:** A bar chart visualization within the web dashboard illustrating the average purchase price across various Nairobi sub-counties (Karen, Kileleshwa, Kilimani, Langata, Lavington, Parklands, South B, and Westlands).

---

## The Technology Behind This
* **Programming Language:** Python
* **Data Manipulation & Machine Learning:** Pandas, NumPy, Scikit-Learn (Random Forest Regressor)
* **Statistical Analysis:** Statsmodels (OLS Regression)
* **Relational Database & ORM:** MySQL Server 8.0, SQLAlchemy, MySQL Workbench
* **Web Framework & Visualizations:** Streamlit, Plotly Express
* **DevOps & Version Control:** Git, GitHub Actions (CI/CD pipeline)

## How to Use It

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/steph45acke-hue/NAIROBI_RENTAL_YIELD_AND_REAL_ESTATE_VALUATION.git](https://github.com/steph45acke-hue/NAIROBI_RENTAL_YIELD_AND_REAL_ESTATE_VALUATION.git)
   cd NAIROBI_RENTAL_YIELD_AND_REAL_ESTATE_VALUATION
Set up a virtual environment:

Bash
python -m venv venv
venv\Scripts\Activate
Install dependencies:

Bash
pip install --upgrade pip
pip install -r requirements.txt
Initialize the database & data pipeline:

Run the data generator: python scraper.py

Migrate data to MySQL: python ingest_to_mysql.py

Train the machine learning model: python train_model.py

Launch the web application:

Bash
streamlit run app.py