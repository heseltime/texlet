from django.urls import path

from . import views

# after '/app/' as well as default index for the project
urlpatterns = [
    path('', views.write_letter, name='letter'),
    path('letter', views.write_letter, name='letter'),
    path('pickup', views.pickup, name='pickup'),
    path('direct-pickup', views.direct_pickup, name='direct-pickup'),
    path('manage-profile', views.manage_profile, name='manage-profile'),
    path('delete-profile', views.delete_profile, name='delete-profile'),
    path('add-addressee', views.add_addressee, name='add-addressee'),
]