from django.urls import path

from my_api import views

urlpatterns = [
    path('', views.create_book),
    path('get_details/', views.get_details),
    path('update_book', views.update_book),
    path('delete_book', views.delet_by_id)
]
