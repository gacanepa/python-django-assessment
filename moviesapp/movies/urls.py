# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.authtoken import views as token_views
from . import views

app_name = 'movies'

urlpatterns = [
    path('', view=views.MovieListView.as_view(), name='index'),
    path('<int:id>/', view=views.MovieRetrieveUpdateView.as_view(), name='detail'),
    path('create/', view=views.MovieCreateView.as_view(), name='create'),
    path('update/<int:id>/', view=views.MovieRetrieveUpdateView.as_view(), name='update'),
    path('delete/<int:id>/', view=views.MovieDeleteView.as_view(), name='delete'),
    path('<int:movie_id>/vote/', views.vote, name='vote'),
    path('auth/', token_views.obtain_auth_token),
]
