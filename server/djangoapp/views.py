# Uncomment the required imports before adding the code

import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        data = json.loads(request.body)
        username = data["userName"]
        password = data["password"]

    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    else:
        data = {"userName": username, "status": "Failed to authenticate"}

    return JsonResponse(data)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# Create a `logout_request` view to handle sign out request
def logout_user(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# ...


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    # context = {}

    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    username_exist = False
    # email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except ValueError as e:
        # If not, simply log this is a new user
        logger.debug("{} is new user. Exception: {}".format(username, str(e)))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


# Method to get the list of cars (Car Makes and Car Models)
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()  # This function populates car data if no records exist
    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})


# Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a method to get dealer reviews based on dealer_id
def get_dealer_reviews(request, dealer_id):
    # If dealer_id has been provided
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)

        # Analyze sentiments for each review
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail["review"])
            print(response)  # Log the response for debugging
            review_detail["sentiment"] = response["sentiment"]

        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a method to get dealer details based on dealer_id
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Load the data from the request body
        data = json.loads(request.body)
        try:
            # Call the post_request method with the review data
            response = post_review(data)
            print(response)  # Print the response for debugging

            # Return a success status and message
            return JsonResponse(
                {"status": 200, "message": "Review posted successfully."}
            )
        except Exception as e:
            # Handle errors during the posting process
            print(f"Error in posting review: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        # Return unauthorized status if the user is not authenticated
        return JsonResponse({"status": 403, "message": "Unauthorized"})
