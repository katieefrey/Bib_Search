from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #login/out
    path("login", views.login_form, name="login_form"),
    path("login_view", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("account", views.account, name="account"),
    #search related
    path("help", views.help, name="help"),
    path('queued', views.queued, name='queued'),
    path('search', views.search, name='search'),
    path('history', views.history, name='history'),
    path('report/<int:reid>', views.report, name='report'),
    path('export_author', views.export_author, name='export_author'),
    path('export_journal', views.export_journal, name='export_journal'),
    #testing celery
    path('home', views.home, name='home'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)