
from django.urls import path,include
from . import views

urlpatterns = [
    
    path("",views.index,name="ShopHome"),
    
    path("about/", views.about,name="About"),
    path("contact/", views.contact,name="ContactUs"),
    path("tracker/", views.tracker,name="TrackingStatus"),
    path("search/", views.search,name="Search"),
    path("products/<int:id>", views.prodView,name="productview"),
    path("checkout/", views.checkout,name="Checkout"),
    path("handlerequest/", views.handlerequest,name="handlerequest"),
]