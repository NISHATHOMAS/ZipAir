from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
)

from airline.custommessages import CustomMessage
from airline.serilizers import CreateAirLineSerializer
from airline.utils import format_serializers_error

MSG_OBJ = CustomMessage()


class CreateAirLine(CreateAPIView):
    """Feed the data and create an AirLine"""

    authentication_classes = []
    permission_classes = []
    queryset = None
    serializer_class = CreateAirLineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response_dict = {
                "code": 0,
                "msg": MSG_OBJ.create_failure,
                "response": format_serializers_error(serializer.errors),
            }
            return JsonResponse(data=response_dict, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
        serializer_data = serializer.data
        headers = self.get_success_headers(serializer_data)
        response_dict = {
            "code": 1,
            "msg": MSG_OBJ.create_success,
            "response": serializer_data,
        }
        return JsonResponse(data=response_dict, status=status.HTTP_201_CREATED, headers=headers)
