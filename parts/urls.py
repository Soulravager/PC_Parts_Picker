from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import submit_review,submit_rating,toggle_share_build
from .views import toggle_favorite,favorite_profile,cart_profile,toggle_cart,purchase_parts
from .views import get_motherboards, get_ram,update_part_ratings,staff_report
from .views import shared_build_detail,shared_builds_list,part_detail,contact_form_submission,telegram_webhook,newsletter_subscription
from django.urls import path, re_path
from .views import error

#from .views import part_detail

urlpatterns = [
    path('', views.index, name='index'),  # Root URL now loads index.html
    #basic Sites
    path('about_us/', views.about_us, name='about_us'),
    path('contacts/', views.contacts, name='contacts'),
    path('contact/', views.contacts, name='contacts'), 
    path('build-help/', views.build_help, name='build_help'),  
    path('error/', views.error, name='error'),
    #User LOGIN/LOGOUT
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    #BUILD PC SITE
    path('build/', views.pc_build, name='pcbuild'),    
    path('delete-build/<int:build_id>/', views.delete_build, name='delete_build'),    
    path('toggle-share/<int:build_id>/', toggle_share_build, name='toggle_share_build'),
    path('purchase/', views.purchase_view, name='purchase'),    
    path('confirm_purchase/', views.confirm_purchase_view, name='confirm_purchase'),    
    path('get_motherboards/', get_motherboards, name='get_motherboards'),
    path('get_ram/', get_ram, name='get_ram'),
    path("newsletter-subscribe/", newsletter_subscription, name="newsletter-subscription"),
    path('cart/<str:part_model>/', toggle_cart, name='toggle_cart'),
    path('profile/<str:part_model>/', cart_profile, name='cart_profile'),    
    path("purchase_parts/", purchase_parts, name="purchase_parts"),

    #PARTS SITES
   # path('component_details/<str:component_type>/', views.component_details, name='component_details'),
    path('parts/<str:part_model>/', views.part_detail, name='part_detail'),  # Part detail page]
    path('component/<str:part_model>/', views.component_list, name='component'),  # Part detail page]
    path('parts/', views.parts_list, name='parts_list'),  # List of all parts
    path('part-details/<str:category>/<int:part_id>/', views.part_details, name='part_details'),   
    
    #Chat BOT
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path("contact-submit/", contact_form_submission, name="contact_form_submission"),
    path("telegram-webhook/", telegram_webhook, name="telegram_webhook"),
    #Review and Rating     
    path('favorite/<str:part_model>/', toggle_favorite, name='toggle_favorite'),     
    path('profile/remove_fav/<str:part_model>/', favorite_profile, name='favorite_profile'),
    path("update-ratings/", update_part_ratings, name="update_part_ratings"),
    path("submit-review/", submit_review, name="submit_review"),
    path("submit-rating/", submit_rating, name="submit_rating"),  # URL for submitting ratings
    # Staff Dashboard URLs (New) 
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/dashboard/<str:category>/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/add/<str:category>/', views.staff_add_part, name='staff_add_part'),
    path('staff/edit/<str:category>/<int:part_id>/', views.staff_edit_part, name='staff_edit_part'),
    path('staff/delete/<str:category>/<int:part_id>/', views.staff_delete_part, name='staff_delete_part'),
    path('staff_report/', staff_report, name='staff_report'),
    #   Share BUild
    path('share_build/<int:build_id>/', shared_build_detail, name='shared_build_detail'),
    path('shared-builds/', shared_builds_list, name='shared_builds_list'),  
    
    #ERROR PAGE
   # re_path(r'^.*$', error),
   #re_path(r'^(?!media/|static/).*$', views.error), 
     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    #path('pc-parts/', views.pc_parts_list, name='pc_parts_list'),
     #path('part/<str:part_type>/<int:part_id>/', views.part_detail, name='part_detail'),
     #path('<str:model_name>/<int:part_id>/', part_detail, name='part_detail'),
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
