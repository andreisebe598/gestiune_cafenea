# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path('', views.main, name='main'),
#     path('menu/', views.menu, name='menu'),
#     path('about/', views.about, name='about'),
#     path('contact/', views.contact, name='contact'),
#     path('dashboard/', views.dashboard_rapoarte, name='dashboard'),
#     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
#     path('adauga_produs/', views.adauga_produs, name='adauga_produs'),
#     path('adauga_angajat/', views.adauga_angajat, name='adauga_angajat'),
#     path('register/', views.register, name='register'),

#     path('resetare-parola/', 
#          auth_views.PasswordResetView.as_view(template_name="password_reset.html"), 
#          name="reset_password"),

#     path('resetare-parola-trimisa/', 
#          auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
#          name="password_reset_done"),

#     path('reset/<uidb64>/<token>/', 
#          auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
#          name="password_reset_confirm"),

#     path('resetare-parola-completa/', 
#          auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), 
#          name="password_reset_complete"),

#     path('cart/', views.cart_detail, name='cart_detail'),
#     path('cart/add/<int:produs_id>/', views.cart_add, name='cart_add'),
#     path('cart/remove/<int:produs_id>/', views.cart_remove, name='cart_remove'),
#     path('cart/checkout/', views.checkout, name='checkout'),

#     path('profil/', views.profil, name='profil'),
# ]


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     # --- Rutele existente ---
     path('', views.main, name='main'),
     path('menu/', views.menu, name='menu'),
     path('about/', views.about, name='about'),
     path('contact/', views.contact, name='contact'),
     path('dashboard/', views.dashboard_rapoarte, name='dashboard'),
     
     # Auth
     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
     path('register/', views.register, name='register'),
     path('profil/', views.profil, name='profil'),

     # Resetare parola 
    path('resetare-parola/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    path('resetare-parola-trimisa/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    path('resetare-parola-completa/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),

     # Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:produs_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:produs_id>/', views.cart_remove, name='cart_remove'),
    path('cart/checkout/', views.checkout, name='checkout'),

     # === ZONA GESTIUNE ===
    path('gestiune/produse/', views.lista_gestiune_produse, name='lista_gestiune_produse'),
    path('gestiune/produse/nou/', views.adauga_produs, name='adauga_produs'),
    path('gestiune/produse/edit/<int:pk>/', views.modifica_produs, name='modifica_produs'),
    path('gestiune/produse/sterge/<int:pk>/', views.sterge_produs, name='sterge_produs'),

    path('gestiune/agajati/', views.lista_gestiune_angajati, name='lista_gestiune_angajati'),
    path('gestiune/angajati/nou/', views.adauga_angajat, name='adauga_angajat'),
    path('gestiune/angajati/edit/<int:pk>/', views.modifica_angajat, name='modifica_angajat'),
    path('gestiune/angajati/sterge/<int:pk>/', views.sterge_angajat, name='sterge_angajat'),

    path('gestiune/comenzi/', views.lista_gestiune_comenzi, name='lista_gestiune_comenzi'),
    path('gestiune/comenzi/detalii/<int:pk>/', views.detalii_comanda, name='detalii_comanda'),
    path('gestiune/comenzi/sterge/<int:pk>/', views.sterge_comanda, name='sterge_comanda'),

    path('gestiune/stiri/', views.lista_gestiune_stiri, name='lista_gestiune_stiri'),
    path('gestiune/stiri/nou/', views.adauga_stire, name='adauga_stire'),
    path('gestiune/stiri/edit/<int:pk>/', views.modifica_stire, name='modifica_stire'),
    path('gestiune/stiri/sterge/<int:pk>/', views.sterge_stire, name='sterge_stire'),
]