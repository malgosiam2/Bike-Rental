from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from equipment.utils import render_xml_with_xsl
from equipment.views import price_offer_view, offer_view
from review.views import home, user_view, add_review, edit_review
from order.views import create_order, edit_order, delete_order
from user.views import register_view, delete_account_view, confirm_email_view, confirm_delete_view, logout_view, login_view, forgot_password_view, reset_password_view, change_password_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("register/", register_view, name="register"),
    path('confirm_email/<str:code>/', confirm_email_view, name='confirm_email'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('offer/', offer_view, name='offer'),
    path('forgot_password/', forgot_password_view, name='forgot_password'),
    path('reset_password/<str:code>/', reset_password_view, name='reset_password'),
    path('prices/', price_offer_view, name="prices"),
    path('create-order/', create_order, name='create-order'),
    path('orders/<int:pk>/order/', edit_order, name='edit_order'),
    path('review/<int:pk>/order/', add_review, name='add_review'),
    path('user/', user_view, name='user'),
    path('change_password/', change_password_view, name='change_password'),
    path('delete_account/', delete_account_view, name='delete_account'),
    path('confirm_delete/<str:code>/', confirm_delete_view, name='confirm_delete'),
    path('orders/<int:pk>/delete/', delete_order, name='delete_order'),
    path('edit_review/<int:pk>/', edit_review, name='edit_review'),
    path('equipment/', render_xml_with_xsl, name='equipment_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
