from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('goodfind', views.goodfind, name='goodfind'),
    path('cvsscalc/', views.cvsscalc, name="cvsscalc"),
    path('report/', views.report, name="report"),
]