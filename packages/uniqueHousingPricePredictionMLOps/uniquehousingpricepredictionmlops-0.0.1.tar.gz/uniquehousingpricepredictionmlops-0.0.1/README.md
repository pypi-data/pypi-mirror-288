# HousingPricePredictionMLOps

## Problem Statement

You are hired by a company, Home Realty Co Ltd. You are provided with a dataset containing details about various houses and their selling prices. The company is looking to optimize its profit by distinguishing between higher and lower priced houses. Your task is to help the company predict the price of a house based on the given attributes, so they can better assess the value of each property and make informed decisions to maximize their profit. Additionally, identify and provide the top 5 attributes that are the most important in determining the house prices.

## Data Dictionary

- **Area** - The total area of the house in square feet.
- **Bedrooms** - The number of bedrooms in the house.
- **Bathrooms** - The number of bathrooms in the house.
- **Stories** - The number of stories (levels) in the house.
- **Mainroad** - Indicates whether the house is located on a main road (Yes or No).
- **Guestroom** - Indicates whether the house has a guestroom (Yes or No).
- **Basement** - Indicates whether the house has a basement (Yes or No).
- **Hotwaterheating** - Indicates whether the house has hot water heating (Yes or No).
- **Airconditioning** - Indicates whether the house has air conditioning (Yes or No).
- **Parking** - The number of parking spaces available with the house.
- **Prefarea** - Indicates whether the house is in a preferred area (Yes or No).
- **Furnishingstatus** - The furnishing status of the house, with options: Not Furnished, Semi-Furnished, Furnished.
- **Price** - The selling price of the house.

### Create project template hierarchy
```bash
python template.py
```

### Setup development environment
```bash
bash init_setup.sh
```

### Acivate environment
```bash
source activate ./env
```

### Install project as local package
```bash
pip install -r requirement.txt
```

## Pipelines
### Training Pipeline
* Data Ingestion (fetched data from source)
* Data Transformation (Feature Engineering, Data Preprocessing)
* Model Builing (Create a model using the processed data)

## MLFlow
```bash
python src/HousingPricePrediction/pipelines/training_pipeline.py
mlflow ui
```

#### Command to train the pipeline
```bash
python src\HousingPricePrediction\pipelines\training_pipeline.py
```

### Prediction Pipeline
* Two types of prediction pipeline
* Single record prediction
* Batch prediction


## Explainer Dashboard

* Feature Importance
* Regression Stats
* Individual Predictions
* What if?
* Feature Dependence

```bash
python dashboard.py
```

## Flask App
```bash
python app.py
```

## Streamlit App
```bash
streamlit run streamlit_app.py
```

## Data version control (DVC)
```bash
dvc init
dvc add notebooks/data/Housing.csv
git add .
git commit -m "Add data"
git push
git log
git checkout <commit ID>
dvc checkout
```

## Deployment of DockerImage
```bash
docker build -t housing_price_prediction .
docker run -p 8000:5000 housing_price_prediction
docker login
docker tag housing_price_prediction asangkumarsingh/unique_housing_price_prediction
docker push asangkumarsingh/unique_housing_price_prediction
```
## Docker hub repo:
* https://hub.docker.com/r/asangkumarsingh/projecthousinpriceprediction/tags

## Dataset Link
* https://www.kaggle.com/datasets/yasserh/housing-prices-dataset
