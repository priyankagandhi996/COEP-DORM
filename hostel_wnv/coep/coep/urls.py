"""coep URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from app1 import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('fe_pdf_boys/', views.fe_pdf_boys, name='fe_pdf_boys'),
    path('se_pdf_boys/', views.se_pdf_boys, name='se_pdf_boys'),
    path('te_pdf_boys/', views.te_pdf_boys, name='te_pdf_boys'),
    path('be_pdf_boys/', views.be_pdf_boys, name='be_pdf_boys'),
    path('fe_pdf_girls/', views.fe_pdf_girls, name='fe_pdf_girls'),
    path('se_pdf_girls/', views.se_pdf_girls, name='se_pdf_girls'),
    path('te_pdf_girls/', views.te_pdf_girls, name='te_pdf_bgirls'),
    path('be_pdf_girls/', views.be_pdf_girls, name='be_pdf_girls'),

    path('signup/', views.signup, name='signup'),
    #('login/', views.loginuser, name='login'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
]



if settings.DEBUG :
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

