from django.urls import path
from rest_framework_simplejwt_mongoengine import views as jwt_views
from accounts import views
from rest_framework_simplejwt_mongoengine.views import TokenObtainPairView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/obtain/', views.ObtainTokenPairWithThemeView.as_view(), name='token_create'),  # ==login
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', views.bistrouser_create, name="create_user"),
    path('api/logout/', views.bistrouser_logout, name="logout_user"),
    path('api/bistro/user/', views.bistrouser_detail, name="get_user"),
]
