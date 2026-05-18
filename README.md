# Nigerian Job Market Intelligence

> A data science project that scrapes, analyses and predicts salaries in the Nigerian job market.

**Live App** → [job-market-intelligence.streamlit.app](https://job-market-intelligence-jobberman-4v9q8l5phf4fegncrzfsae.streamlit.app/)

---

## The Problem

As a Nigerian navigating the job market, one of the most frustrating experiences is not knowing what a role actually pays. Most listings say "Confidential" or give a range so wide it tells you nothing. This project tries to fix that.

---

## What I Built

An end-to-end data science project that:

- Scraped 3,400+ real job listings from Jobberman.com
- Cleaned and analysed the data to uncover hiring trends
- Extracted in-demand skills from job descriptions using NLP
- Trained a salary range classifier using XGBoost
- Deployed an interactive web app any Nigerian job seeker can use

---

## App Features

Given a job title, experience level, location and qualification the app returns:

- Predicted salary range
- Top skills required for that role
- Top companies hiring
- Market demand (number of active listings)
- Common salary ranges posted for that role

---

## Project Structure

```
├── app.py                      # Streamlit web application
├── salary_model.pkl            # Trained XGBoost model
├── model_columns.json          # Feature columns used in training
├── top_titles.json             # Job titles used in dropdown
├── jobbermann_cleaned.csv      # Cleaned dataset
├── requirements.txt            # Dependencies
├── data/
│   └── jobberman_jobs.csv      # Raw scraped data
└── web scraping/
    └── main.py                 # Jobberman scraping script
```

---

## Key Findings

- **Sales, Marketing and Accounting** are the top hiring industries on Jobberman
- **Lagos** accounts for over 60% of all job listings
- **Communication** is the most requested skill across all industries — appearing in nearly 1,600 listings
- Over **52%** of job listings require a university degree
- The XGBoost model achieved **71% accuracy** predicting salary category

---

## Models Compared

| Model | Accuracy | Entry Level F1 | Mid Level F1 | Senior F1 |
|---|---|---|---|---|
| Logistic Regression | 71% | 0.78 | 0.65 | 0.63 |
| Random Forest | 69% | 0.75 | 0.65 | 0.60 |
| XGBoost | 71% | 0.77 | 0.65 | 0.66 |

XGBoost was selected for deployment due to its highest precision on Senior/Executive roles.

---

## Tools & Libraries

- **Scraping** — BeautifulSoup, Requests
- **Analysis** — Pandas, NumPy, Matplotlib, Seaborn
- **Modelling** — Scikit-learn, XGBoost, imbalanced-learn (SMOTE)
- **Deployment** — Streamlit, Streamlit Cloud

---

## Author

Built by [Abisolami](https://github.com/abisolami)
