from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.auth_urls')),
    path('profile/', include('api.auth.profile_urls')),
    path('recommendations/', include('api.recommendations.urls')),
    path('scoring/', include('api.scoring.urls'))
]
