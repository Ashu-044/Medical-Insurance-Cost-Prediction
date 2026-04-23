# 🚀 Medical Insurance Cost Prediction 

## 📌 Project Overview

This project predicts the **medical insurance cost** of an individual using Machine Learning techniques based on personal and health-related attributes such as age, BMI, smoking status, and region.

The solution uses a **Random Forest Regressor** and is deployed through an interactive **Streamlit web application**, enabling real-time predictions along with personalized recommendations.

---

## 🎯 Problem Statement

Estimating insurance premiums is a complex task due to multiple influencing factors such as lifestyle, health conditions, and demographics.

### Traditional methods often fail to:

* Capture non-linear relationships
* Provide personalized estimations
* Adapt to varying combinations of features

👉 This project addresses these challenges using a **data-driven Machine Learning approach**.

---

## 💡 Proposed Solution

The system takes user inputs:

* Age
* Gender
* BMI
* Number of children
* Smoking status
* Region

### Output:

* 📊 Predicted insurance cost
* ⚠️ Risk classification (Low / Medium / High)
* 💡 Personalized recommendations

---

## 🧠 Machine Learning Model

* **Model Used:** Random Forest Regressor
* **Type:** Supervised Learning (Regression)

### ✔️ Why Random Forest?

* Handles non-linear relationships effectively
* Performs well on structured/tabular data
* Reduces overfitting using ensemble learning
* Requires minimal hyperparameter tuning

---

## 🔄 Project Workflow

1. Data Collection
2. Data Cleaning & Preprocessing
3. Exploratory Data Analysis (EDA)
4. Feature Engineering
5. Model Training & Evaluation
6. Model Saving (`.joblib`)
7. Deployment using Streamlit

---

## 📊 Exploratory Data Analysis (EDA)

### Distribution of Charges

<img width="705" height="458" alt="image" src="https://github.com/user-attachments/assets/b886a2f7-6781-4d23-804b-7ff55038e684" />



### Smokers vs Charges

<img width="750" height="435" alt="image" src="https://github.com/user-attachments/assets/950d1814-79fc-4ea5-bd7f-acb4f7bd9a83" />


---

## 🛠️ Technologies Used

### 🔹 Programming Language

* Python

### 🔹 Libraries

* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Joblib

### 🔹 Tools & Frameworks

* Jupyter Notebook
* Streamlit

---

## 🌐 Application Features

* 📊 Real-time insurance cost prediction
* 📋 User-friendly input interface
* ⚠️ Risk classification system
* 💡 Personalized health recommendations
* 📈 Visualization of predicted cost

---

## 📂 Project Structure

```
insurance-prediction/
│
├── insurance.csv
├── notebook.ipynb
├── insurance_model.joblib
├── columns.json
├── app.py
├── requirements.txt
└── README.md
```

---

## 🖥️ Application Interface (Output Screens)

### 🔹 Input & Prediction

![UI 1](https://github.com/user-attachments/assets/5161388c-b264-4c88-ae05-65807b23e5f6)

### 🔹 Prediction + Recommendations

![UI 2](https://github.com/user-attachments/assets/79b657cc-0077-4126-9312-9dffc08c3f05)

---

## ▶️ How to Run the Project

### 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd insurance-prediction
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Application

```bash
streamlit run app.py
```

---

## 📊 Sample Output

* Estimated Insurance Cost
* Risk Level
* Personalized Recommendations

---

## 👨‍💻 Author

**Ashutosh Thakare**

---

## ⭐ Acknowledgement

Dataset sourced from publicly available insurance dataset on Kaggle.
