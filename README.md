# Ames Housing — House Price Prediction

A machine learning application that predicts house prices using two models (basic and advanced) trained on the Ames Housing dataset. Built with Flask and deployed on Render.

---

## Project Overview

This project demonstrates a complete machine learning workflow — from data preprocessing to model training to deployment — by predicting house prices based on property characteristics. It features **two prediction models**:

1. **Basic Model**: Simple, fast predictions using 9 key features and an HTML form interface.
2. **Advanced Model**: Comprehensive predictions using 80+ features through a JSON API.

Both models are trained using Linear Regression on the Ames Housing dataset and packaged as a Flask web application.

---

## Dataset: Ames Housing

- **Source**: Ames Housing dataset (from OpenML)
- **Records**: 1,460 houses
- **Features**: 80+ property characteristics (size, quality, year built, garage, basement, etc.)
- **Target**: Sale price (in USD)
- **Type**: Regression problem

---

## Machine Learning Workflow

### Data Preprocessing

The `code.ipynb` notebook implements a comprehensive preprocessing pipeline:

1. **Handling Missing Values**:
   - Fill categorical missing values with "None" (pool, garage, basement, fireplace features)
   - Use grouped median for numeric missing values (LotFrontage)
   - Use mode for remaining values (Electrical)

2. **Feature Engineering**:
   - Create binary features (e.g., `HasBasement` from `BsmtQual`)
   - Keep original numeric and categorical features
   - Drop highly null columns

3. **Encoding**:
   - Convert categorical variables to numeric using one-hot encoding
   - Result: ~300+ numeric features for the advanced model

4. **Target Transformation**:
   - Apply `log1p()` to sale price (log transformation helps with skewed data)
   - During prediction, apply inverse transform `expm1()` to get actual prices

### Model Training

**Algorithm**: Linear Regression from scikit-learn

**Advanced Model**:
- Features: ~300 (all features after preprocessing and one-hot encoding)
- Train-test split: 80/20 with random_state=42
- Scaling: StandardScaler (fit on training data)
- Performance: Validated against test set

**Basic Model** (simplified version):
- Features: 9 key indicators
  - OverallQual, GrLivArea, GarageCars, TotalBsmtSF, YearBuilt, FullBath, TotRmsAbvGrd, 1stFlrSF, GarageArea
- Scaling: Separate StandardScaler
- Performance: R² = 0.868 (explains 87% of price variance)

### Prediction Flow

```
Feature Input → Scaling → Model Prediction (log-scale) → Inverse Transform → Actual Price Output
```

---

## Backend Architecture: Flask Routes

The Flask app (`app.py`) exposes four main routes:

| Route | Method | Model | Purpose |
|-------|--------|-------|---------|
| `/` | GET | — | Home page with navigation |
| `/predict` | POST | Advanced | API endpoint for advanced predictions (JSON) |
| `/basic-form` | GET | Basic | HTML form for basic model input |
| `/predict-basic` | POST | Basic | Process form and return prediction |
| `/basic-result` | GET | Basic | Display prediction result |

**Model & Scaler Loading**:
- Advanced: `regmodel.pkl` + `scaler.pkl`
- Basic: `basic_model.pkl` + `basic_scaler.pkl`
- Loaded on app startup using `pickle`

**Prediction Logic**:
1. Receive input features (JSON or form)
2. Scale features using the appropriate scaler
3. Pass scaled data to the model
4. Inverse transform the prediction to get actual price
5. Return result as JSON or render HTML

---

## Frontend: HTML Templates

**`templates/home.html`** — Advanced Model Interface
- Overview of the project
- Navigation to basic model or API documentation
- Styled with dark blue gradient and modern design

**`templates/basic_form.html`** — Basic Model Input Form
- Simple, user-friendly form with 9 input fields
- Real-time form validation
- Gradient background (purple)
- Responsive design for mobile/desktop

**`templates/basic_result.html`** — Prediction Result Page
- Display predicted price
- Show model performance info (R² = 0.868)
- Options to make another prediction or explore advanced model

---

## Two-Level Approach: Basic vs Advanced

| Aspect | Basic | Advanced |
|--------|-------|----------|
| **Features** | 9 key indicators | ~300 (all preprocessed) |
| **Interface** | HTML form | JSON API |
| **Speed** | Very fast | Slightly slower |
| **Accuracy** | R² = 0.868 | Higher (full preprocessing) |
| **Use Case** | Quick estimates | Detailed analysis |
| **Beginner-Friendly** | Yes | Developers only |

**User Journeys**:
- **Basic**: Home → `/basic-form` → Fill fields → `/predict-basic` → View result on `/basic-result`
- **Advanced**: Home → JSON API call to `/predict` with all features

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python, Flask |
| **ML/Data** | scikit-learn, pandas, NumPy |
| **Serialization** | pickle |
| **Frontend** | HTML, CSS, JavaScript |
| **Deployment** | Docker, Render, gunicorn |

---

## Running Locally

### Prerequisites
- Python 3.8+
- pip

### Setup & Run

1. **Clone or navigate to the project directory**:
   ```bash
   cd "Ames Housing Study"
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate          # On macOS/Linux
   # or
   venv\Scripts\activate             # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app**:
   ```bash
   python app.py
   ```

5. **Open your browser**:
   - Home page: `http://127.0.0.1:5000/`
   - Basic model form: `http://127.0.0.1:5000/basic-form`

### Testing the Advanced Model

Use a REST client (Postman, curl, or Python `requests`) to send a POST request:

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"feature_1": 1.0, "feature_2": 2.0, ...}'
```

The response will be:
```json
{"predicted_price": 185000.50}
```

---

## Deployment: Render

This project is deployed on **Render** as a Python Web Service.

### Deployment Setup

**Dockerfile**:
- Base image: `python:3.11-slim`
- Installs dependencies from `requirements.txt`
- Exposes port 10000 (Render standard)
- Runs the app with `gunicorn` (WSGI server)

**Start Command**:
```bash
gunicorn app:app --bind 0.0.0.0:10000
```

**Why Gunicorn?**
- Production-grade WSGI server (Flask's development server is single-threaded)
- Handles multiple requests concurrently
- Suitable for containerized deployments

**Live URL**: https://ames-housing-study-046.onrender.com

### Continuous Integration (Optional)

The project includes GitHub Actions workflow for automated testing and deployment (if configured). This allows automatic deployment when you push to the main branch.

---

## Project Structure

```
Ames Housing Study/
├── app.py                      # Flask app (routes & predictions)
├── code.ipynb                  # ML training notebook
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── README.md                   # This file
├── BASIC_MODEL_README.md       # Basic model documentation
├── regmodel.pkl                # Advanced model (trained)
├── scaler.pkl                  # Advanced model scaler
├── basic_model.pkl             # Basic model (trained)
├── basic_scaler.pkl            # Basic model scaler
└── templates/
    ├── home.html               # Home page & navigation
    ├── basic_form.html         # Basic model input form
    └── basic_result.html       # Basic model result display
```

---

## Key Files Explained

- **`app.py`**: Core Flask application with all routes and prediction endpoints.
- **`code.ipynb`**: Jupyter notebook containing the complete ML pipeline (load data → preprocess → train → evaluate → save).
- **`requirements.txt`**: Lists all Python package dependencies (Flask, scikit-learn, pandas, etc.).
- **`Dockerfile`**: Containerization recipe for Render deployment.
- **`.pkl` files**: Serialized (pickled) trained models and scalers for fast loading.

---

## Model Performance

**Advanced Model** (on test set):
- Mean Absolute Error: ~$25,000–$30,000
- R² Score: Typically 0.75–0.85 (depending on test split)

**Basic Model** (on test set):
- R² Score: 0.868 (explains 87% of price variance)
- Mean Absolute Error: ~$20,765

---

## Learning Outcomes

This project demonstrates:
- ✅ Data cleaning and preprocessing at scale
- ✅ Feature engineering and encoding
- ✅ Model training and evaluation (Linear Regression)
- ✅ Predictive pipeline with scaling and transformation
- ✅ Flask web framework and REST APIs
- ✅ Frontend-backend integration (HTML + JavaScript + Python)
- ✅ Model serialization and deployment
- ✅ Containerization with Docker
- ✅ Cloud deployment on Render

---

## Future Enhancements

- Add cross-validation for more robust performance estimates
- Experiment with non-linear models (Random Forest, XGBoost)
- Implement feature importance visualization
- Add confidence intervals to predictions
- Create a admin dashboard for model monitoring
- Add model versioning and A/B testing

---

## License

This project is open source and available for educational purposes.

---

## Contact & Questions

For questions or suggestions, please open an issue or reach out. This project is suitable for:
- **Students**: Learning ML workflows and Flask development
- **Data Science portfolios**: Demonstrating end-to-end ML projects
- **Beginners**: Understanding how ML models work in production