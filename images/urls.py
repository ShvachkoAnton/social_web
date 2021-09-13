from django.urls import path,include
from . import views
app_name = 'images'
urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.ImageDetail.as_view(), name='image_detail'),
    path('image_like/<int:id>/<slug:slug>/', views.ImagePostLike, name='image_like'),

]