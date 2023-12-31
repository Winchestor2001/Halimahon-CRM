from django.urls import path
from .views import HomeAPI, MyTokenObtainPairView, StaffLoginAPI, PatientAPI, ServiceAPI, AllStaffAPI, \
    PetientFilterAPI, RoomsAPI, PatientProfileAPI, AnalysisAPIView, DoctorConclusionAPIView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', HomeAPI.as_view()),
    path('ishchi/', StaffLoginAPI.as_view()),
    path('doctors/', AllStaffAPI.as_view()),
    path('bemorlar/', PatientAPI.as_view()),
    path('bemor/<int:pk>/', PatientProfileAPI.as_view()),
    path('xizmatlar/', ServiceAPI.as_view()),
    path('honalar/', RoomsAPI.as_view()),
    path('analysis/', AnalysisAPIView.as_view()),
    path('external/', DoctorConclusionAPIView.as_view()),

    path('bemorlar_filter/', PetientFilterAPI.as_view()),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
