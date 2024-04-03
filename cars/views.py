from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Car, Fueling
from .serializers import CarSerializer, FuelingSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the car-collector api home route!'}
    return Response(content)


class CarList(generics.ListCreateAPIView):
  queryset = Car.objects.all()
  serializer_class = CarSerializer

class CarDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Car.objects.all()
  serializer_class = CarSerializer
  lookup_field = 'id'

class FuelingListCreate(generics.ListCreateAPIView):
  serializer_class = FuelingSerializer

  def get_queryset(self):
    car_id = self.kwarg['car_id']
    return Fueling.objects.filter(car_id=car_id)
  
  def perform_create(self, serializer):
    car_id = self.kwargs['car_id']
    car = Car.objects.get(id=car_id)
    serializer.save(car=car)

class FuelingDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = FuelingSerializer
  lookup_field = 'id'

  def get_queryset(self):
    car_id = self.kwargs['car_id']
    return Fueling.objects.filter(car_id=car_id)