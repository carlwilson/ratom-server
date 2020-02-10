from django.urls import path

from rest_framework_simplejwt import views as jwt_views
from .views import (
    user_detail,
    account_list,
    account_detail,
    message_detail,
    MessageDocumentView,
    reset_fake_data,
)

# Auth
urlpatterns = [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", user_detail, name="user_detail"),
]

# Accounts
urlpatterns += [
    path("accounts/", account_list, name="account_list"),
    path("accounts/<int:pk>/", account_detail, name="account_detail"),
]

# Messages
urlpatterns += [
    path(
        "messages/",
        MessageDocumentView.as_view({"get": "list"}),
        name="search_messages",
    ),
    path("messages/<int:pk>/", message_detail, name="message_detail"),
]

# Fake data
urlpatterns += [
    path("reset-fake-data/", reset_fake_data, name="reset_fake_data"),
]

ratom_urlpatterns = urlpatterns
