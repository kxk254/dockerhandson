from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'solitonRE'
urlpatterns = [
    path('', views.main, name="main"),
    path('売上/', views.売上ListView.as_view(), name='売上-list'),
    path('売上/input/', views.売上InputView.as_view(), name='売上-input'),
    path('console/', views.console, name='console'),
    path('backup_database/', views.backup_database, name='backup_database'),

    path('費用/', views.費用InputView.as_view(), name='費用-input'),

    path('input/', views.InputFieldView.as_view(), name='input_field_view'),  # or InputFieldView.as_view()
    path('input/<int:pk>/', views.InputFieldView.as_view(), name='input_field_view_pk'),  # or InputFieldView.as_view()

    path('ステータス/input/', views.ステータスView.as_view(), name='ステータス-input'),
    path('ステータス/input/<int:pk>/', views.ステータスView.as_view(), name='ステータス-input-pk'),

    path('契約/input/', views.契約View.as_view(), name='契約-input'),
    path('契約/input/<int:pk>/', views.契約View.as_view(), name='契約-input-pk'),

    path('物件/input/', views.物件View.as_view(), name='物件-input'),
    path('物件/input/<int:pk>/', views.物件View.as_view(), name='物件-input-pk'),

    path('テナント/input/', views.テナントView.as_view(), name='テナント-input'),
    # path('テナント/input/<int:pk>/', views.テナントView.as_view(), name='テナント-input-pk'),

    path('敷金保証金/input/', views.敷金保証金View.as_view(), name='敷金保証金-input'),
    # path('敷金保証金/input/<int:pk>/', views.敷金保証金View.as_view(), name='敷金保証金-input-pk'),

    path('管理項目/input/', views.管理項目View.as_view(), name='管理項目-input'),
    # path('管理項目/input/<int:pk>/', views.管理項目View.as_view(), name='管理項目-input-pk'),

    path('保証会社/input/', views.保証会社View.as_view(), name='保証会社-input'),
    # path('保証会社/input/<int:pk>/', views.保証会社View.as_view(), name='保証会社-input-pk'),

    path('支払先/input/', views.支払先View.as_view(), name='支払先-input'),
    # path('支払先/input/<int:pk>/', views.支払先View.as_view(), name='支払先-input-pk'),

    path('bminput/', views.BMInputFieldView.as_view(), name='bminput_field_view'),  # or InputFieldView.as_view()　###　BM入力を設定する（物件ソート）
    path('bmitem/', views.BMItemView.as_view(), name='bm_item_field_view'),  # or InputFieldView.as_view()
    path('bm/', views.BMView.as_view(), name='bm_view'),  # or InputFieldView.as_view()

]