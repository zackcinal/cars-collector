from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Car, Fueling, Accessory
from .serializers import CarSerializer, FuelingSerializer, AccessorySerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the car-collector api home route!'}
    return Response(content)

class AccessoryList(generics.ListCreateAPIView):
  queryset = Accessory.objects.all()
  serializer_class = AccessorySerializer

class AccessoryDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Accessory.objects.all()
  serializer_class = AccessorySerializer
  lookup_field = 'id'

class CarList(generics.ListCreateAPIView):
  queryset = Car.objects.all()
  serializer_class = CarSerializer

class CarDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Car.objects.all()
  serializer_class = CarSerializer
  lookup_field = 'id'

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializers = self.get_serializer(instance)

    accessories_not_assiciated = Accessory.objects.exclude(id__in=instance.accessories.all())
    accessories_serializer = AccessorySerializer(accessories_not_assiciated, many=True)

    return Response({
      'car': serializers.data,
      'accessories_not_assiciated': accessories_serializer.data
    })

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


class AddAccessoryToCar(APIView):
  def post(self, request, car_id, accessory_id):
    car = Car.objects.get(id=car_id)
    accessory = Accessory.objects.get(id=accessory_id)
    car.accessories.add(accessory)
    return Response({'message': f'Accessory {accessory.name} added to Car {car.make}'})
  
class RemoveAccessoryFromCar(APIView):
  def post(self, request, car_id, accessory_id):
    car = Car.objects.get(id=car_id)
    accessory = Accessory.objects.get(id=accessory_id)
    car.accessories.remove(accessory)
    return Response({'message': f'Accessory {accessory.name} removed from Car {car.make}'})
