"""
URL configuration for detectionproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include

from myapp import views

urlpatterns = [

    path('',views.home,name='home'),
    path('login.html/',views.login,name='login'),

    # ========================================================================
    path('admin_index',views.admin_index,name='admin_index'),
    path('admin_add_locopilot',views.admin_add_locopilot,name='admin_add_locopilot'),

    path('admin_camera', views.admin_camera, name='admin_camera'),
    path('edit_camera/<int:id>/', views.edit_camera, name='edit_camera'),
    path('delete_camera/<int:id>/', views.delete_camera, name='delete_camera'),

    path('admin_awareness', views.admin_awareness, name='admin_awareness'),

    path('admin_history', views.admin_history, name='admin_history'),
    path('admin_complaint', views.admin_complaint, name='admin_complaint'),
    path('admin_train', views.admin_train, name='admin_train'),
    path('edit_train/<int:id>/', views.edit_train, name='edit_train'),
    path('delete_train/<int:id>/', views.delete_train, name='delete_train'),
    path('admin_logout', views.admin_logout, name='admin_logout'),

    # ===========================================================================
    path('locopilot_index', views.locopilot_index, name='locopilot_index'),
    path('locopilot_live_Camera',views.locopilot_live_Camera,name='locopilot_live_Camera '),
    path('locopilot_risk_level', views.locopilot_risk_level, name='locopilot_risk_level'),
    path('locopilot_camera', views.locopilot_camera, name='locopilot_camera'),
    path('locopilot_awareness', views.locopilot_awareness, name='locopilot_awareness'),
    path('locopilot_complaint', views.locopilot_complaint, name='locopilot_complaint'),
    path('edit-complaint/<int:id>/', views.edit_complaint, name='edit_complaint'),
    path('delete-complaint/<int:id>/', views.delete_complaint, name='delete_complaint'),
    path('locopilot_history', views.locopilot_history, name='locopilot_history'),
    path('edit_locopilot/<int:id>/', views.edit_locopilot, name='edit_locopilot'),
    path('delete_locopilot/<int:id>/', views.delete_locopilot, name='delete_locopilot'),
    path('admin_reply/<int:id>/', views.admin_reply, name='admin_reply'),
    path('locopilot_logout', views.locopilot_logout, name='locopilot_logout'),

    path('detect_camera/<int:camera_id>/', views.detect_camera_view, name='detect_camera_view'),
    path('view_alert/',views.view_alert,name="view_alert"),
path("camera_stream/", views.camera_stream, name="camera_stream"),
path("video_stream/", views.video_stream, name="video_stream"),

    path('locopilot-chatbot/', views.locopilot_chatbot_api, name='locopilot_chatbot'),
    path('chatbot/', views.locopilot_chatbot_page,name='chatbot'),
]
