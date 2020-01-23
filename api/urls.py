from django.urls import path
from django.contrib import admin

from rest_framework_simplejwt import views as jwt_views
from .views import (
    user_detail,
    account_list,
    account_detail,
    message_detail,
    MessageDocumentView,
)

# Auth
urlpatterns = [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", user_detail),
]

# Accounts
urlpatterns += [
    path("accounts/", account_list),
    path("accounts/<int:pk>/", account_detail),
]

# Messages
urlpatterns += [
    path("messages/", MessageDocumentView.as_view({"get": "list"})),
    path("messages/<int:pk>/", message_detail),
]

ratom_urlpatterns = urlpatterns