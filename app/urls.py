from django.urls import path
from app import views
from django.contrib.auth import views as auth_view
from django.conf.urls.static import static
from django.conf import settings
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.product_detail.as_view(), name='product-detail'),
    path('category/<slug:val>',views.CategoryView.as_view(), name='category'),
    path('category-brand/<val>',views.CategoryBrandView.as_view(), name='category-brand'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('search/',views.search, name='search'), 

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
   
    path('mobile/', views.mobile, name='mobile'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),    
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
   
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),

    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),


    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
