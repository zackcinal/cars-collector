from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Car, Fueling, Accessory
from .serializers import CarSerializer, FuelingSerializer, AccessorySerializer, UserSerializer

# Define the home view
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })

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
  serializer_class = CarSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    return Car.objects.filter(user=user)
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class CarDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = CarSerializer
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Car.objects.filter(user=user)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializers = self.get_serializer(instance)

    accessories_not_assiciated = Accessory.objects.exclude(id__in=instance.accessories.all())
    accessories_serializer = AccessorySerializer(accessories_not_assiciated, many=True)

    return Response({
      'car': serializers.data,
      'accessories_not_assiciated': accessories_serializer.data
    })
  
  def perform_update(self, serializer):
    car = self.get_object()
    if car.user != self.request.user:
      raise PermissionDenied({"message": "You do not have permission to edit this car"})
    serializer.save()

    def perform_destroy(self, instance):
      if instance.user != self.request.user:
          raise PermissionDenied({"message": "You do not have permission to delete this car."})
      instance.delete()

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
