# -*- coding: utf-8 -*-

"""Movies views."""

# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import json
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce

# API
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from .serializers import *

from .models import Movie, Rating
# from .forms import MovieModelForm

class MovieListView(SuccessMessageMixin, ListAPIView):
    """Show all movies."""
    queryset = Movie.objects.annotate(num_votes=Count('rating'), avg_rating=Coalesce(Avg('rating__rating_number'), 0))
    #context_object_name = 'movie_list'
    serializer_class = MovieSerializer

class MovieCreateView(SuccessMessageMixin, CreateAPIView):
    """Create a new movie."""
    serializer_class = MovieSerializer
    success_message = "The movie created successfully"
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'The movie created successfully',
            'data': response.data
        })

class MovieRetrieveUpdateView(SuccessMessageMixin, RetrieveUpdateAPIView):
    """Show the requested movie."""
    model = Movie
    context_object_name = 'movie'
    serializer_class = MovieSerializer
    success_message = "The movie updated successfully"
    def get(self, request, *args, **kwargs):
        try:
            return super(MovieRetrieveUpdateView, self).get(request, *args, **kwargs)
        except Http404:
            return redirect('/')
    def get_object(self):
        return get_object_or_404(Movie, **self.kwargs)

class MovieDeleteView(DestroyAPIView):
    """Delete the requested movie."""
    model = Movie
    serializer_class = MovieSerializer
    success_url = '/movies'
    def get(self, request, *args, **kwargs):
        try:
            return super(MovieDeleteView, self).get(request, *args, **kwargs)
        except Http404:
            return redirect('/movies')
    def get_object(self):
        return get_object_or_404(Movie, **self.kwargs)
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'The movie deleted successfully')
        return response

def vote(request, movie_id):
    body = json.loads(request.body)
    rating = body['rating']
    rating = Rating(movie_id=movie_id, rating_number=rating)
    rating.save()
    messages.success(request, 'Your vote was recorded successfully')
    return HttpResponseRedirect(reverse('movies:index'))