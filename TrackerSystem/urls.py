"""TrackerSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.utils.functional import curry
from django.views.defaults import server_error, page_not_found, permission_denied
from TrackerSystem import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('tracker/', include('tasks.urls')),
                  path('auth/', include('django.contrib.auth.urls')),
                  path('', include('accounts.urls')),
                  path('chat/', include('chat.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)

handler404 = curry(page_not_found, exception=Exception('Page not Found'), template_name='404.html')
# handler500 = error_500
