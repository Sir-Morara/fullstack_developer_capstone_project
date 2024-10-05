# Uncomment the imports below before you add the function code
import os

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            # Using f-string for cleaner formatting
            params += f"{key}={value}&"
    request_url = (
        backend_url + endpoint + "?" + params.strip("&")
    )  # Remove the last '&' character
    print(f"GET from {request_url}")  # Using f-string for cleaner formatting
    try:
        # Call the get method of requests library with URL and parameters
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        # If any error occurs, print the error message
        print(f"Network exception occurred: {e}")


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except ValueError as e:
        print(f"Network exception occurred: {e}")
