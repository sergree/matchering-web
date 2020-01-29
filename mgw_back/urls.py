from django.urls import path

from mgw_back import views

app_name = 'mgw_back'
urlpatterns = [
    path('session/', views.SessionCreate.as_view()),
    path('session/<slug:token>/', views.SessionView.as_view()),
    path('upload/<slug:token>/<slug:file_type>/', views.UploadFile.as_view()),
]
