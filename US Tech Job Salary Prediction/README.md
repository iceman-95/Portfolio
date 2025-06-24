# US Tech Job Salary Prediction System

A comprehensive machine learning system for predicting tech job salaries in the US. This interactive tool provides data-driven insights, model comparisons, and personalized salary predictions based on the `ds_salaries.csv` dataset.

## 🎯 Project Overview

This project demonstrates my skills in:
- **Data Science & Machine Learning**: Implementing 18 different ML models (11 regression, 7 classification)
- **Data Analysis & Visualization**: Creating comprehensive visualizations and statistical analysis
- **Software Engineering**: Building an interactive command-line application with modular design
- **Feature Engineering**: Advanced preprocessing and encoding techniques
- **Model Evaluation**: Comprehensive performance comparison and metrics analysis

## ✨ Features

- **Interactive Menu**: A user-friendly command-line interface to navigate through different functionalities
- **Comprehensive Summary**: Get a quick overview of the dataset including key statistics, salary distributions, and top-paying jobs and locations
- **Data Visualization**: Generate and save detailed plots to understand salary trends, including:
    - Salary distributions by experience and company size
    - Average salary trends over years
    - Top 10 highest paying countries and job titles
    - Impact of remote work on salary
- **Model Training & Comparison**: Train 18 different machine learning models (11 regression, 7 classification) and compare their performance using R², RMSE, and Accuracy metrics
- **Personalized Predictions**: Predict your salary with an interactive prompt that asks for your professional details

## 🛠️ Technologies Used

- **Python 3.x**
- **Machine Learning**: scikit-learn (Random Forest, Gradient Boosting, SVM, etc.)
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Data Preprocessing**: LabelEncoder, StandardScaler

## 📊 Dataset

The system uses the `ds_salaries.csv` dataset which contains 3,757 records of tech job salaries with 11 features, including work year, experience level, job title, salary in USD, and company location.

## 🚀 Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Navigate to the project directory:
    ```bash
    cd <repository-directory>
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 📖 How to Run

Execute the main script from your terminal:

```bash
python salary_predictor.py
```

You will be greeted with a menu to choose from the following options:

```
🎯 WHAT WOULD YOU LIKE TO DO?
============================================================
1. 📋 Display Analysis Summary
2. 📊 Create comprehensive visualizations
3. 🤖 Train & Compare All 18 Models
4. 🎯 Show Example Predictions
5. 💬 Predict Your Salary
0. ❌ Exit
============================================================
```

### 1. Display Analysis Summary
Get a quick, text-based summary of the key insights from the dataset.

### 2. Create Comprehensive Visualizations
Generate and view detailed plots. You can choose to create:
- `salary_overview_analysis.png`: Overview of salary distributions and trends
- `top_categories_analysis.png`: Top countries, job titles, and remote work analysis
- `classification_deep_dive.png`: Deeper look into how different factors affect salary classification

### 3. Train & Compare All 18 Models
This option trains all 11 regression and 7 classification models, and then generates a `model_comparison.png` plot to visualize their performance.

### 4. Show Example Predictions
See pre-defined examples of salary predictions for different job profiles.

### 5. Predict Your Salary
An interactive prompt will ask for your details to provide a personalized salary prediction. The inputs are case-insensitive for categorical fields (e.g., 'se' for Senior level is accepted).

-   **Work Year**: e.g., 2023
-   **Experience Level**: EN, MI, SE, EX
-   **Employment Type**: PT, FT, CT, FL
-   **Job Title**: e.g., "Data Scientist" (case-sensitive)
-   **Employee Residence**: e.g., US, GB, CA
-   **Remote Ratio**: 0, 50, 100
-   **Company Location**: e.g., US, GB, CA
-   **Company Size**: S, M, L

## 📈 Key Achievements

- **18 ML Models**: Successfully implemented and compared 11 regression and 7 classification models
- **High Performance**: Achieved strong R² scores and accuracy metrics across multiple algorithms
- **Comprehensive Analysis**: Created detailed visualizations and statistical summaries
- **User-Friendly Interface**: Built an intuitive command-line interface for easy interaction
- **Robust Preprocessing**: Implemented advanced feature engineering and data preprocessing techniques

## 📁 Output Files

The script can generate the following files in the project directory:

-   `salary_overview_analysis.png`
-   `top_categories_analysis.png`
-   `classification_deep_dive.png`
-   `model_comparison.png`

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to suggest improvements or add new features.

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

For questions or suggestions, please open an issue in the repository. 