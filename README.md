# Prediction of Placement and Admission based on Demographic Attributes

A machine learning-based web application that predicts admission and placement outcomes for students using demographic attributes.

## Overview

This project leverages machine learning to predict academic admissions and job placements based on demographic data. It aims to provide valuable insights for educational institutions and employers to make data-driven decisions.

## About the Project

### Aim
To provide accurate predictions of placement and admission outcomes based on demographic attributes.

### Problem Statement
The application uses predictive modeling to forecast admission and placement outcomes for students based on their demographic attributes. By analyzing factors such as age, gender, ethnicity, socioeconomic status, and academic qualifications, the system determines the likelihood of admission and subsequent placement in academic programs or job positions.

The goal is to identify the most influential demographic attributes in determining outcomes, helping institutions and employers make more informed decisions through data-driven insights.

## Features

- **User Authentication**: Secure login/signup system with profile management
- **Data Analysis**: Upload and analyze CSV datasets
- **Model Training**: Choose between default and custom feature selection
- **Prediction Visualization**: Interactive charts showing prediction outcomes
- **Exportable Results**: Download charts and prediction data

## Tech Stack

- **Frontend**: Streamlit for interactive UI components
- **Backend**: Python
- **Machine Learning**: TensorFlow/Keras, scikit-learn
- **Visualization**: Plotly
- **Authentication**: Custom cookie-based system

## How It Works

1. **Data Upload**: Users upload CSV files containing demographic data
2. **Feature Selection**: Choose specific features or use default automatic selection
3. **Model Training**: Neural network or traditional ML models are trained on the data
4. **Prediction**: New data is analyzed using the trained model
5. **Visualization**: Results are displayed through interactive charts and graphs

## Getting Started

### Prerequisites
```
streamlit-lottie
extra-streamlit-components
streamlit-option-menu
kaleido
openai
```

### Installation

1. Clone the repository
   ```
   git clone https://github.com/JairajKolhatkar/Admission-Placement-Prediction.git
   ```
   
2. Install required packages
   ```
   pip install -r requirements.txt
   ```

3. Run the application
   ```
   streamlit run streamlit_app.py
   ```

## Contact

For questions or collaboration:
- Email: jairajkolhatkar@gmail.com
- LinkedIn: [Jairaj Kolhatkar](https://www.linkedin.com/in/jairaj-kolhatkar-77a81730a/)
- GitHub: [JairajKolhatkar](https://github.com/JairajKolhatkar)
