# Projet-IML-2024-SalesPrediction

## Authors
- **Mohamadi Bassirou COMPAORE**
- **Maty NDIONE**

**Supervision**: Mme Mouly DIAW (ML Engineer/Data Scientist)

**Date**: December 2024

---

## Introduction
In an increasingly competitive retail market, it is crucial for Favorita to anticipate customer demand to stay ahead. This sales prediction project aims to offer a data-driven solution to optimize inventory management, better plan operations, and enhance the customer experience.

Using rich and diverse datasets, we developed a model capable of predicting sales fluctuations, considering factors such as promotions, seasonality, and special events.

---

## Data Description

### Training Data:
- Contains dates, store and item information, whether the item was promoted, and unit sales.

### Additional Files:
- Provide supplementary information that can be used to improve model creation.

---

## Data Processing

### Merging and Cleaning:
- The various files were merged to create a unified dataset.
- Missing values were addressed by removing incomplete records.

### Sampling:
- A sample was drawn to make the dataset more manageable while ensuring validity and reliability of results (16% of data retained).

---

## Exploratory Analysis

### Key Steps:
- Dataframes were merged.
- 16% of the data was retained through sampling.
- Missing data was removed.

---

## Modeling

The following machine learning models were implemented:
- **Linear Models**:
  - Ridge Regression
  - Lasso Regression
  - Elastic-Net
- **Ensemble Models**:
  - Random Forest
  - XGBoost
- **Time Series Model**:
  - SARIMA

---

## Results
The results demonstrate the importance of a well-documented and innovative sales strategy. The aim is not just to increase immediate sales figures but also to establish a sustainable framework for continuous growth and success.

**XGBoost** proves to be more suitable, yielding lower errors compared to other models.

---

## Tools & Frameworks Used
- **Python Libraries**: pandas, scikit-learn, XGBoost, statsmodels
- **Visualization**: matplotlib, seaborn

---

## How to Use
1. Clone this repository.
2. Ensure you have the required Python dependencies installed (see `requirements.txt`).
3. Run the Jupyter notebooks or scripts provided to replicate the analysis and modeling.

---

## Acknowledgments
Special thanks to Mme Mouly DIAW for her invaluable guidance and support throughout the project.

---

## Contact
Feel free to reach out for further information or collaboration opportunities:
- **Maty NDIONE**
- **Mohamadi Bassirou COMPAORE**

