from django.conf.urls import include, url
from .views import GaryBotView

urlpatterns = [
    url(r'^b345e21cca34732679d2804b16ac4d376c412817887a689305/?$', GaryBotView.as_view())
]