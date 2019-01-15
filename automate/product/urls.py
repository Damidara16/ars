from django.conf.urls import url
from django.contrib.auth.views import login, logout, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

app_name = 'product'

urlpatterns = [
    url(r'^home/$', views.Home, name='home'),
    url(r'^login/$', login, {'template_name': 'product/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'product/unauthHome.html'}, name='logout'),
    url(r'^r/$', views.register, name='Register'),

    url(r'view/items/$', views.listItem, name='vItem'),
    url(r'^create/item/$', views.createItem.as_view(), name='cItem'),
    url(r'^edit/item/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.editItem, name='eItem'),
    url(r'^delete/item/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.deleteItem, name='dItem'),
    url(r'^retrieve/item/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.retrieveItem, name='rItem'),

    url(r'^create/pitem/$', views.createPrintTagItems.as_view(), name='cPItem'),
    url(r'^edit/pitem/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.editPrintTagItems, name='ePItem'),
    url(r'^delete/pitem/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.deletePrintTagItems, name='dPItem'),
    url(r'^retrieve/pitem/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.retrievePrintTagItems, name='rPItem'),

    url(r'view/category/$', views.listCategory, name='vCategory'),
    url(r'^create/category/$', views.createCategory.as_view(), name='cCategory'),
    url(r'^edit/category/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.editCategory, name='eCategory'),
    url(r'^delete/category/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.deleteCategory, name='dCategory'),
    url(r'^retrieve/category/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.retrieveCategory, name='rCategory'),

    url(r'^create/ReturnPolicy/$', views.createReturnPolicy.as_view(), name='cReturnPolicy'),
    url(r'^edit/ReturnPolicy/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.editReturnPolicy, name='eReturnPolicy'),
    url(r'^delete/ReturnPolicy/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.deleteReturnPolicy, name='dReturnPolicy'),
    url(r'^retrieve/ReturnPolicy/(?P<uuid>[\w]{8}(-[\w]{4}){3}-[\w]{12})/$', views.retrieveReturnPolicy, name='rReturnPolicy'),


    url(r'^edit/store/$', views.editStore.as_view, name='eStore')
]
