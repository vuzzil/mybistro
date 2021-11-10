from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from accounts import views

urlpatterns = [
    path('api/token/obtain/', views.ObtainTokenPairWithThemeView.as_view(), name='token_create'),  # override sjwt stock token,
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', views.bistrouser_create, name="create_user"),
    path('api/bistro/user/', views.bistrouser_detail, name="get_user"),
]
