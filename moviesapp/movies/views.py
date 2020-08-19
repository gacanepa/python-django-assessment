# -*- coding: utf-8 -*-

"""Movies views."""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy

from .models import Movie
from .forms import MovieModelForm

class MovieListView(ListView):
    """Show all movies."""
    model = Movie
    context_object_name = 'movie_list'

class MovieDetailView(DetailView):
    """Show the requested movie."""
    model = Movie
    context_object_name = 'movie'
    def get(self, request, *args, **kwargs):
        try:
            return super(MovieDetailView, self).get(request, *args, **kwargs)
        except Http404:
            return redirect('/')
    def get_object(self):
        return get_object_or_404(Movie, **self.kwargs)

class MovieCreateView(CreateView):
    """Create a new movie."""
    template_name = 'movies/movie_form.html'
    form_class = MovieModelForm
    queryset = Movie.objects.all()

class MovieUpdateView(UpdateView):
    """Update the requested movie."""


class MovieDeleteView(DeleteView):
    """Delete the requested movie."""
