from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    path('/Tests', views.get_tests, name='get_tests'),
    url(r'file_manager/edit_filename',
        views.edit_filename,
        name="file-manager-edit-filename"),
    url(r'file_manager/delete_file',
        views.delete_file,
        name="file-manager-delete-file"),
    url(r'algorithm_manager/set_algorithm',
        views.set_algorithm,
        name="algorithm-manager-set-algorithm"),
    url(r'algorithm_manager/get_past_runs',
        views.get_past_runs,
        name="algorithm-manager-get-past-runs"),
    url(r'algorithm_manager/get_past_data',
        views.get_past_data,
        name="algorithm-manager-get-past-data"),
    url(r'algorithm_manager/upload_algorithm',
        views.upload_algorithm,
        name="algorithm-manager-upload-algorithm"),
    url(r'algorithm_manager/get_algorithms',
        views.get_algorithms,
        name="algorithm-manager-get-algorithms"),
    path('getdb', views.getdb, name='getdb')
]
