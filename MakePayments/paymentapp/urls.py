from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.ngo_donation),
    url('payment-status', views.payment_status),
]
