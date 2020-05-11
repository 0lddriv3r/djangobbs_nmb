from django.urls import path
import devproject.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('searchphoto/', views.searchphoto, name='searchphoto'),
    path('search/', views.search, name='search'),
    path('publish/', views.publish, name='publish'),
    path('comment/', views.comment, name='comment'),
    path('register/', views.register, name='register'),
    path('category/<str:categorynick>/page/<int:pageindex>', views.page, name='page'),
    path('category/<str:categorynick>/thread/<int:threadid>/page/<int:pageindex>', views.detailpage, name='detailpage'),
    path('category/<str:categorynick>/thread/<int:threadid>', views.detail, name='detail'),
    path('category/<str:categorynick>/thread/<int:threadid>/next', views.detailnext, name='detailnext'),
    path('category/<str:categorynick>', views.category, name='category'),
]
