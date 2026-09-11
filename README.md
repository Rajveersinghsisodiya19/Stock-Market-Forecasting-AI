

````markdown
# Stock Market Prediction AI

An AI-powered stock market prediction system that uses Machine Learning and Deep Learning models to predict the **next trading day's Open, High, Low, and Close (OHLC) prices** of selected stocks.

The project combines a **React frontend**, **FastAPI backend**, trained machine learning models, and the **Twelve Data API** for live historical market data.

> **Disclaimer:** This project is built for educational and research purposes. Stock market predictions are uncertain and should not be considered financial advice.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [System Architecture](#system-architecture)
- [Prediction Pipeline](#prediction-pipeline)
- [Machine Learning Models](#machine-learning-models)
- [Data](#data)
- [Prediction Output](#prediction-output)
- [Percentage Change](#percentage-change)
- [Charts](#charts)
- [Model Evaluation](#model-evaluation)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Fork and Clone the Repository](#fork-and-clone-the-repository)
- [Open the Project in VS Code](#open-the-project-in-vs-code)
- [Backend Setup](#backend-setup)
- [Twelve Data API Setup](#twelve-data-api-setup)
- [Run the Backend](#run-the-backend)
- [Frontend Setup](#frontend-setup)
- [Run the Frontend](#run-the-frontend)
- [Run the Complete Project](#run-the-complete-project)
- [Using the Application](#using-the-application)
- [API](#api)
- [Git Workflow](#git-workflow)
- [Contributing](#contributing)
- [Future Improvements](#future-improvements)
- [Disclaimer](#disclaimer)
- [Author](#author)

---

# Overview

Stock market data is a type of time-series data containing values that change over time.

This project explores how different Machine Learning and Deep Learning algorithms can learn patterns from historical stock market data and use those patterns to predict the **next trading day's prices**.

The system uses three models:

1. Random Forest
2. XGBoost
3. LSTM

Each model predicts:

- Open
- High
- Low
- Close

The predictions from all three models are displayed on the same web application, allowing the user to compare their results.

---

# Features

- Next trading day stock price prediction
- Multiple supported companies
- Live historical market data
- Twelve Data API integration
- Random Forest model
- XGBoost model
- LSTM neural network
- Open price prediction
- High price prediction
- Low price prediction
- Close price prediction
- Historical price charts
- Prediction visualization
- Percentage change calculation
- Increase / Decrease / No Change indicators
- Model comparison
- React frontend
- FastAPI backend
- REST API communication
- Company-specific preprocessing/scaling
- Saved trained models
- Interactive API documentation

---

# Supported Stocks

The current project supports:

| Symbol | Company |
|---|---|
| INFY | Infosys |
| AAPL | Apple |
| MSFT | Microsoft |
| GOOGL | Alphabet |
| AMZN | Amazon |
| NVDA | NVIDIA |
| TSLA | Tesla |
| META | Meta |

The supported symbols are controlled by the backend configuration.

---

# How It Works

The application follows a simple process.

```text
User
 │
 │ Selects Stock
 ▼
React Frontend
 │
 │ HTTP Request
 ▼
FastAPI Backend
 │
 ▼
Twelve Data API
 │
 │ Historical Market Data
 ▼
Preprocessing
 │
 ▼
Company-Specific Scaling
 │
 ├──────────────┬──────────────┐
 ▼              ▼              ▼
Random Forest   XGBoost        LSTM
 │              │              │
 └──────────────┴──────────────┘
                │
                ▼
        Next-Day OHLC
                │
                ▼
       Inverse Transformation
                │
                ▼
        Real Price Values
                │
                ▼
        FastAPI JSON Response
                │
                ▼
         React Frontend
                │
        ┌───────┴────────┐
        ▼                ▼
      Charts          Comparison
````

---

# System Architecture

The project follows a **client-server architecture**.

```text
                         ┌──────────────────┐
                         │      USER        │
                         │  Web Browser     │
                         └────────┬─────────┘
                                  │
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │    REACT FRONTEND      │
                     │                        │
                     │ Prediction Form        │
                     │ Charts                 │
                     │ Model Results          │
                     │ Model Comparison       │
                     └────────────┬───────────┘
                                  │
                                  │ REST API
                                  ▼
                     ┌────────────────────────┐
                     │    FASTAPI BACKEND     │
                     │                        │
                     │ API Endpoints          │
                     │ Data Processing        │
                     │ Preprocessing          │
                     │ Model Inference        │
                     └────────────┬───────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
             ┌────────────┐ ┌───────────┐ ┌───────────┐
             │   Random   │ │  XGBoost  │ │   LSTM    │
             │   Forest   │ │           │ │           │
             └────────────┘ └───────────┘ └───────────┘
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                                  ▼
                         ┌────────────────┐
                         │  OHLC Results  │
                         │                │
                         │ Open           │
                         │ High           │
                         │ Low            │
                         │ Close          │
                         └────────────────┘

                                  ▲
                                  │
                                  │ Historical Data
                                  │
                         ┌────────────────┐
                         │ Twelve Data API│
                         └────────────────┘
```

---

# Prediction Pipeline

The complete prediction process is:

```text
1. User selects a company
            │
            ▼
2. Frontend sends prediction request
            │
            ▼
3. FastAPI receives request
            │
            ▼
4. Backend requests historical data
   from Twelve Data
            │
            ▼
5. Latest 60 trading days are obtained
            │
            ▼
6. Data is sorted chronologically
            │
            ▼
7. Required features are extracted
            │
            ▼
8. Company-specific scaler is applied
            │
            ▼
9. Input sequence is created
            │
            ▼
10. Three models generate predictions
            │
      ┌─────┼─────┐
      ▼     ▼     ▼
      RF   XGB   LSTM
      │     │     │
      └─────┼─────┘
            ▼
11. Predictions are inverse transformed
            │
            ▼
12. Predictions converted to real prices
            │
            ▼
13. Backend returns JSON response
            │
            ▼
14. React displays results and charts
```

---

# Prediction Period

The current production system predicts **only the next trading day**.

```text
Historical Data
───────────────────────────────────────────────►
Day -59 ... Day -3 ... Day -2 ... Day -1
                                      │
                                      ▼
                                  ML Models
                                      │
                                      ▼
                                Next Trading Day
```

The application does **not** currently perform direct 30-day or 60-day forecasting.

---

# Machine Learning Models

## Random Forest

Random Forest is an ensemble learning algorithm based on multiple decision trees.

Instead of using a single decision tree, Random Forest creates multiple trees and combines their predictions.

### Advantages

* Handles nonlinear relationships
* Robust against noise
* Works well with structured data
* Reduces overfitting compared with a single decision tree
* Easy to use for regression problems

---

## XGBoost

XGBoost stands for **Extreme Gradient Boosting**.

It is a gradient boosting algorithm that builds decision trees sequentially.

Each new tree attempts to reduce the errors made by previous trees.

### Advantages

* Strong performance on tabular data
* Handles nonlinear relationships
* Efficient training
* Regularization support
* Widely used for regression and classification

---

## LSTM

LSTM stands for **Long Short-Term Memory**.

It is a type of **Recurrent Neural Network (RNN)** designed for sequential and time-series data.

Unlike traditional feed-forward neural networks, LSTM networks can maintain information from previous time steps.

Conceptually:

```text
Historical Time Series

Day 1 ──►
Day 2 ──►
Day 3 ──►
  ...      │
Day 60 ──►│
           ▼
       LSTM Network
           │
           ▼
     Next Trading Day
           │
     ┌─────┼─────┐
     ▼     ▼     ▼
    Open  High  Low  Close
```

LSTM is particularly useful for time-series problems because it can learn temporal dependencies.

---

# Data

The project uses historical stock market data.

The main market features are:

* Open
* High
* Low
* Close
* Volume

The trained models use the feature representation defined during the training pipeline.

The application does not predict future volume as an output.

The prediction target is:

```text
Open
High
Low
Close
```

---

# Data Source

Live historical market data is retrieved through the **Twelve Data API**.

The backend requests recent trading data for the selected stock.

The data then passes through the preprocessing pipeline before being given to the trained models.

```text
Twelve Data API
      │
      ▼
Historical OHLCV Data
      │
      ▼
Data Cleaning
      │
      ▼
Feature Preparation
      │
      ▼
Scaling
      │
      ▼
Machine Learning Models
```

---

# Prediction Output

Every model produces four predicted values.

```text
Random Forest
 ├── Open
 ├── High
 ├── Low
 └── Close

XGBoost
 ├── Open
 ├── High
 ├── Low
 └── Close

LSTM
 ├── Open
 ├── High
 ├── Low
 └── Close
```

Therefore, the system produces:

```text
3 Models × 4 OHLC Predictions
= 12 Model Outputs
```

---

# Percentage Change

The application compares the predicted value with the latest actual value retrieved from Twelve Data.

The formula is:

```text
Percentage Change =
((Predicted Price - Last Actual Price)
 / Last Actual Price) × 100
```

Example:

```text
Last Actual Close = $225.73
Predicted Close   = $227.04

Percentage Change =
((227.04 - 225.73) / 225.73) × 100

≈ +0.58%
```

The application categorizes the result as:

```text
Positive  → Increase
Negative  → Decrease
Zero      → No Change
```

The comparison is performed separately for:

* Open
* High
* Low
* Close

---

# Charts

The frontend displays separate charts for each model.

There are:

```text
3 Models × 4 OHLC Values = 12 Charts
```

The charts include:

* Historical prices
* Next-day prediction
* Prediction boundary
* Numeric price axis
* Date-based X-axis

Each chart contains two primary data lines:

```text
Historical Data
       +
Predicted Value
```

The historical data contains the latest 60 trading days.

The final prediction represents the next trading day.

---

# Model Comparison

The application compares all three models.

Example structure:

| Model         |      Open |      High |       Low |     Close |
| ------------- | --------: | --------: | --------: | --------: |
| Random Forest | Value / % | Value / % | Value / % | Value / % |
| XGBoost       | Value / % | Value / % | Value / % | Value / % |
| LSTM          | Value / % | Value / % | Value / % | Value / % |

This makes it easier to compare how each model predicts the next trading day.

---

# Model Evaluation

The models can be evaluated using regression metrics.

## MAE

**Mean Absolute Error**

```text
MAE = average(|Actual - Predicted|)
```

MAE represents the average absolute difference between actual and predicted values.

Lower MAE is generally better.

---

## MSE

**Mean Squared Error**

```text
MSE = average((Actual - Predicted)²)
```

MSE penalizes larger errors more heavily.

Lower MSE is generally better.

---

## RMSE

**Root Mean Squared Error**

```text
RMSE = √MSE
```

RMSE represents prediction error in the same unit as the target variable.

Lower RMSE is generally better.

---

## R²

**Coefficient of Determination**

```text
R² = 1 - SSres / SStot
```

R² measures how much of the variance in the target is explained by the model.

A value closer to `1` generally indicates a better fit.

---

# Technologies Used

## Frontend

### React

Used to build the web interface.

Responsibilities include:

* User interface
* Stock selection
* Sending API requests
* Displaying predictions
* Rendering charts
* Model comparison

### Vite

Used as the frontend development server and build tool.

### JavaScript

Used for:

* Application logic
* API communication
* Calculations
* Dynamic rendering

### JSX

Used to define React components.

### CSS

Used for:

* Styling
* Layout
* Dark theme
* Responsive interface
* Charts and components

---

# Backend

## Python

Main programming language used for the backend and machine learning components.

## FastAPI

FastAPI provides the REST API used by the frontend.

Responsibilities include:

* Receiving prediction requests
* Retrieving market data
* Data preprocessing
* Running trained models
* Returning prediction results

## Uvicorn

Uvicorn is used as the ASGI server for running FastAPI.

## Pandas

Used for:

* Data manipulation
* Data cleaning
* Time-series handling
* Data processing

## NumPy

Used for:

* Numerical computation
* Arrays
* Model input preparation

## Scikit-learn

Used for:

* Random Forest
* Feature preprocessing
* Scaling
* Evaluation metrics

## XGBoost

Used for the XGBoost machine learning model.

## TensorFlow / Keras

Used for:

* LSTM model
* Neural network inference
* Loading trained `.keras` models

## Joblib

Used to save and load machine learning models and preprocessing objects.

## python-dotenv

Used to load environment variables from `.env`.

---

# Technology Stack

```text
┌─────────────────────────────────────────┐
│                 FRONTEND                │
│                                         │
│ React + Vite + JavaScript + JSX + CSS  │
└────────────────────┬────────────────────┘
                     │
                     │ REST API / HTTP
                     ▼
┌─────────────────────────────────────────┐
│                 BACKEND                 │
│                                         │
│ Python + FastAPI + Uvicorn             │
└────────────────────┬────────────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
     Scikit-learn XGBoost   TensorFlow
          │          │          │
          ▼          ▼          ▼
     Random Forest XGBoost     LSTM
                     │
                     ▼
              Prediction Output
                     ▲
                     │
              Twelve Data API
```

---

# Project Structure

```text
Stock-Market-Prediction-AI/
│
├── backend/
│   ├── main.py
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PredictionForm.jsx
│   │   │   ├── ForecastChart.jsx
│   │   │   ├── ModelResults.jsx
│   │   │   └── Comparison.jsx
│   │   │
│   │   ├── utils/
│   │   │   ├── predictionMetrics.js
│   │   │   └── chartGeometry.js
│   │   │
│   │   ├── App.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── ...
│
├── Data/
│   ├── historical_data.csv
│   └── Train_test_data.npz
│
├── Data creation and collection/
│   └── feature_engineering.py
│
├── models/
│   └── company_scalers.pkl
│
├── trained_models/
│   ├── LSTM_stock_model.keras
│   ├── Random_Forest_stock_model.pkl
│   └── XGBoost_stock_model.pkl
│
├── .gitignore
├── README.md
└── ...
```

---

# Requirements

Before running the project, install:

* Git
* Python 3.12
* Node.js
* npm
* VS Code
* Twelve Data API key

---

# Fork and Clone the Repository

## Step 1 — Fork

Open the GitHub repository.

Click:

```text
Fork
```

GitHub will create your own copy of the repository.

---

## Step 2 — Clone Your Fork

Open PowerShell, Terminal, or the VS Code terminal.

Run:

```bash
git clone https://github.com/YOUR-USERNAME/Stock-Market-Prediction-AI.git
```

Replace:

```text
YOUR-USERNAME
```

with your GitHub username.

Then:

```bash
cd Stock-Market-Prediction-AI
```

---

# Open the Project in VS Code

From the project directory:

```bash
code .
```

If the `code` command is not available:

1. Open VS Code.
2. Select **File → Open Folder**.
3. Select the cloned repository.

You should see:

```text
backend/
frontend/
Data/
models/
trained_models/
README.md
```

---

# Backend Setup

Open the VS Code terminal.

Make sure you are in the project root:

```text
Stock-Market-Prediction-AI/
```

---

## Create Virtual Environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Your terminal should now show:

```text
(venv)
```

---

## Install Backend Dependencies

Install the main backend packages:

```powershell
python -m pip install fastapi uvicorn python-dotenv
```

For the machine learning dependencies:

```powershell
python -m pip install pandas numpy scikit-learn joblib xgboost tensorflow
```

If the repository contains a `requirements.txt`, you can instead run:

```powershell
python -m pip install -r requirements.txt
```

---

# Twelve Data API Setup

The application requires a Twelve Data API key to retrieve market data.

Create an account with Twelve Data and obtain an API key.

Create a `.env` file according to the location expected by the backend.

Example:

```env
TWELVE_DATA_API_KEY=your_api_key_here
```

Replace:

```text
your_api_key_here
```

with your actual API key.

### Never commit your API key

Make sure `.env` is included in `.gitignore`.

Example:

```gitignore
.env
venv/
__pycache__/
node_modules/
```

---

# Run the Backend

From the **project root**, activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Then start FastAPI:

```powershell
python -m uvicorn backend.main:app --reload --port 8000
```

You should see:

```text
Uvicorn running on http://127.0.0.1:8000
```

The backend is now running.

Keep this terminal open.

---

# Backend API Documentation

FastAPI automatically provides interactive API documentation.

After starting the backend, open:

```text
http://127.0.0.1:8000/docs
```

You can use the Swagger interface to inspect and test the available API endpoints.

---

# Frontend Setup

Open a **second terminal** in VS Code.

Navigate to the frontend:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

---

# Run the Frontend

Run:

```powershell
npm run dev
```

Vite will display a local URL similar to:

```text
http://localhost:5173
```

Open the URL in your browser.

---

# Run the Complete Project

The project requires two terminals.

## Terminal 1 — Backend

From the project root:

```powershell
.\venv\Scripts\Activate.ps1

python -m uvicorn backend.main:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

---

## Terminal 2 — Frontend

```powershell
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# Complete Startup Flow

```text
Terminal 1
   │
   ▼
Activate Python Environment
   │
   ▼
Start FastAPI
   │
   ▼
Port 8000
   │
   │
   │
Terminal 2
   │
   ▼
Open frontend/
   │
   ▼
npm install
   │
   ▼
npm run dev
   │
   ▼
Port 5173
   │
   ▼
Open Browser
```

---

# Using the Application

After starting both servers:

### Step 1

Open:

```text
http://localhost:5173
```

### Step 2

Select a supported stock.

Example:

```text
NVDA
```

### Step 3

Select the prediction period.

Currently:

```text
1 Day
```

### Step 4

The application retrieves recent historical data.

### Step 5

The backend runs:

```text
Random Forest
XGBoost
LSTM
```

### Step 6

The application displays predictions for:

```text
Open
High
Low
Close
```

### Step 7

The frontend displays:

* Historical price charts
* Next-day predictions
* Percentage changes
* Increase / Decrease indicators
* Model comparison

---

# Example

For a selected stock such as NVDA:

```text
Latest Historical Data
          │
          ▼
     60 Trading Days
          │
          ▼
    ┌─────┼─────┐
    ▼     ▼     ▼
   RF    XGB   LSTM
    │     │     │
    ▼     ▼     ▼
   OHLC  OHLC  OHLC
    │     │     │
    └─────┼─────┘
          ▼
      Comparison
          │
          ▼
       Charts
```

---

# REST API Architecture

The frontend communicates with the backend using HTTP requests.

```text
React
 │
 │ HTTP Request
 ▼
FastAPI
 │
 ├── Validate Request
 │
 ├── Fetch Market Data
 │
 ├── Preprocess Data
 │
 ├── Load Models
 │
 ├── Run Inference
 │
 └── Return JSON
 │
 ▼
React
 │
 ├── Display Prediction
 ├── Calculate Percentage Change
 └── Render Charts
```

---

# Git Workflow

After making changes:

Check the repository status:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Update stock prediction system"
```

Push:

```bash
git push origin main
```

If your branch is named `master`:

```bash
git push origin master
```

---

# Creating a Feature Branch

For larger changes, create a new branch:

```bash
git checkout -b feature/new-feature
```

Make your changes and then:

```bash
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

Then create a Pull Request on GitHub.

---

# Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Clone your fork.
3. Create a feature branch.
4. Make your changes.
5. Test the project.
6. Commit your changes.
7. Push your branch.
8. Open a Pull Request.

---

# Future Improvements

Possible future improvements include:

* Additional machine learning algorithms
* Hyperparameter optimization
* Ensemble models
* Improved LSTM architectures
* More historical data
* News sentiment analysis
* Market sentiment analysis
* Technical indicators
* Backtesting
* Confidence intervals
* Model uncertainty estimation
* Automated model retraining
* Cloud deployment
* Database integration
* User authentication
* Portfolio analysis
* Market trend classification

---

# Limitations

The project has several important limitations.

### Stock prices are difficult to predict

Financial markets are affected by many factors that cannot be captured completely using historical OHLC data.

### Predictions are not guaranteed

A model that performs well on historical testing data may not perform equally well on future unseen market conditions.

### Next-day prediction only

The current production system is designed for predicting the next trading day.

### API dependency

Live predictions depend on the availability of the Twelve Data API and the configured API key.

### Model dependency

The quality of predictions depends on the quality and representativeness of the training data.

---

# Security

Do not commit sensitive information to GitHub.

Never upload:

```text
.env
API keys
Passwords
Private credentials
```

Use environment variables instead.

Example:

```env
TWELVE_DATA_API_KEY=your_api_key
```

---

# License

This project is intended for educational and research purposes.

If you want others to freely use, modify, and distribute the project, add an appropriate open-source license such as the MIT License.

---

# Disclaimer

This project is **not financial advice**.

Machine learning predictions are estimates based on historical data and model behavior.

The predictions generated by this application can be incorrect.

Do not use the application as the sole basis for buying, selling, or trading financial assets.

Always conduct your own research and consult a qualified financial professional when making investment decisions.

---

# Author

## Rajveersingh Sisodiya

Stock Market Prediction AI

GitHub:

```text
https://github.com/YOUR-USERNAME
```

---

# Project Summary

```text
┌───────────────────────────────────────────────┐
│          STOCK MARKET PREDICTION AI           │
├───────────────────────────────────────────────┤
│                                               │
│ Frontend                                      │
│ React + Vite + JavaScript + CSS              │
│                                               │
│ Backend                                       │
│ Python + FastAPI + Uvicorn                   │
│                                               │
│ Machine Learning                              │
│ Random Forest + XGBoost                      │
│                                               │
│ Deep Learning                                 │
│ LSTM + TensorFlow/Keras                      │
│                                               │
│ Data Source                                   │
│ Twelve Data API                               │
│                                               │
│ Prediction                                    │
│ Next Trading Day                              │
│                                               │
│ Output                                        │
│ Open + High + Low + Close                    │
│                                               │
└───────────────────────────────────────────────┘
```

---

## Quick Start

If you already have everything installed:

### Terminal 1

```powershell
cd Stock-Market-Prediction-AI

.\venv\Scripts\Activate.ps1

python -m uvicorn backend.main:app --reload --port 8000
```

### Terminal 2

```powershell
cd Stock-Market-Prediction-AI\frontend

npm install

npm run dev
```

Then open:

```text
http://localhost:5173
```

Select a stock and generate the next-day prediction.

```

**One important correction before you publish it:** replace `YOUR-USERNAME` with your actual GitHub username, and make sure the `.env` location/name in the README matches what your `backend/main.py` actually loads. Also, if your repository has a `requirements.txt`, keep that as the authoritative dependency list; the README can still contain the manual install commands as a fallback.
```
