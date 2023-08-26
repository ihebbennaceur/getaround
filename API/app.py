# Importing libraries
import mlflow 
import uvicorn
import json
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile


mlflow.set_tracking_uri("https://flow-iheb-c952c67878b8.herokuapp.com/")


description = """
Welcome to the Car Rental Price Prediction API. This app is made for you to determine the price to rent your car! Try it out 🕹️

## Introduction Endpoint

Here is the first endpoint you can try:
* `/`: **GET** request that displays a simple default message.

## Machine Learning Endpoint

This is a Machine Learning endpoint that predicts the price to rent a car given the car features.

* `/predict`: **POST** request that helps you predict the price.



Check out documentation below 👇 for more information on each endpoint. 
"""


tags_metadata = [
    {
        "name": "Introduction Endpoint",
        "description": "Simple endpoint to try out!",
    },

    {
        "name": "Machine Learning Endpoint",
        "description": "Car Price Rental Prediction endpoint."
    }
]


app = FastAPI(
    title="💸 Car Rental Price Prediction",
    description=description,
    version="0.1",
    contact={
        "name": "Iheb",
        "url": "https://fr.linkedin.com/in/ihebbennaceur",
    },
    openapi_tags=tags_metadata
)


class PredictionFeatures(BaseModel):
    model_key: str = "Citroën"
    mileage: int = 140411
    engine_power: int = 100
    fuel: str = "diesel"
    paint_color: str = "black"
    car_type: str = "convertible"
    private_parking_available: bool = True
    has_gps: bool = True
    has_air_conditioning: bool = False
    automatic_car: bool = False
    has_getaround_connect: bool = True
    has_speed_regulator: bool = True
    winter_tires: bool = True


@app.get("/", tags=["Introduction Endpoint"])
async def index():

    message = 'This is the API default endpoint. To get more information about the API, go to "/docs".'
    return message



@app.post("/predict", tags=["Machine Learning Endpoint"])
async def predict(features: PredictionFeatures):
    """
    Estimation of car price rental based on car features.
    """
    # Read data 
    df = pd.DataFrame(dict(features), index=[0])

    # Log model from mlflow 
    logged_model = 'runs:/5274e21ce0d6464389020e789d268bcc/Car_Rental_Price_Predictor'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    prediction = loaded_model.predict(df)

    # Format response
    response = {"prediction": prediction.tolist()}
    return response


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here we define our web server to run the `app` variable 
                                                # (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)