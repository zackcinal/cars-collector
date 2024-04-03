from django.urls import path
from .views import Home, CarList, CarDetail, FuelingDetail, FuelingListCreate

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('cars/', CarList.as_view(), name='car-list'),
  path('cars/<int:id>/', CarDetail.as_view(), name='car-detail'),
  path('cars/<int:car_id>/fuelings/', FuelingListCreate.as_view(), name='fueling-list-create'),
  path('cars/<int:car_id>/fuelings/<int:id>', FuelingDetail.as_view(), name='fueling-detail'),
]