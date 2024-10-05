# Uncomment the following imports before adding the Model code


from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    # You can add any other fields as needed

    def __str__(self):
        return self.name  # String representation of the CarMake object


# Car Model model
class CarModel(models.Model):
    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE
    )  # Many-to-One relationship
    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        # Add more types if needed
    ]

    type = models.CharField(max_length=10, choices=CAR_TYPES, default="SUV")

    # Year with a min value of 2015 and max value of 2023
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)]
    )

    # Any other fields you would like to include

    def __str__(self):
        # String representation of CarMake and CarModel
        return f"{self.car_make.name} {self.name}"  
