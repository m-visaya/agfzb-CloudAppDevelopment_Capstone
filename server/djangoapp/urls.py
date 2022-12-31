from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route='', view=views.get_dealerships, name='index'),
    path(route='about/', view=views.get_aboutus, name='about'),
    path(route='contact/', view=views.get_contactus, name='contact'),
    path(route='register/', view=views.registration_request, name='registration'),
    path(route='login/', view=views.login_request, name='login'),
    path(route='logout/', view=views.logout_request, name='logout'),
    path(route='registration/', view=views.registration_request, name='registration'),
    path('dealer/<int:dealer_id>/<str:dealer_name>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/<str:dealer_name>/addreview/', views.add_review, name='add_review')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)