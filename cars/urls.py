from django.urls import path
from .views import Home, CarList, CarDetail, FuelingDetail, FuelingListCreate, AddAccessoryToCar, AccessoryList, AccessoryDetail, RemoveAccessoryFromCar

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('cars/', CarList.as_view(), name='car-list'),
  path('cars/<int:id>/', CarDetail.as_view(), name='car-detail'),
  path('cars/<int:car_id>/fuelings/', FuelingListCreate.as_view(), name='fueling-list-create'),
  path('cars/<int:car_id>/fuelings/<int:id>', FuelingDetail.as_view(), name='fueling-detail'),
  path('accessory/', AccessoryList.as_view(), name='accessory-list'),
  path('accessory/<int:id>/', AccessoryDetail.as_view(), name='accessory-detail'),
  path('cars/<int:car_id>/add_accessory/<int:accessory_id>/', AddAccessoryToCar.as_view(), name='add-accessory-to-car'),
  path('cats/<int:car_id>/remove_accessory/<int:accessory_id>/', RemoveAccessoryFromCar.as_view(), name='remove-accesssory-from-car'),

]