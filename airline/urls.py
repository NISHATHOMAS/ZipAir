from django.urls import path
from airline.views import (
    CreateAirLine,
)
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title=" TC APIs")

urlpatterns = [
    path("swagger/", schema_view),
    path("create/", CreateAirLine.as_view(), name="create"),
]
