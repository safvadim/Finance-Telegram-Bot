from django.contrib import admin
from django.urls import path, include, re_path
from Finance.views import UserViewSet, FamilyUserViewSet, AccountViewSet, AccountList,\
    IncomeViewSet, ExpensesViewSet, ExpensesList, IncomeList, ExpensesListCategory, UserTokenList,\
    CategoryLimitViewSet, CategoryLimitList, CategoryLimitAccountList, SettingsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'family_users', FamilyUserViewSet, basename='family_users')
router.register(r'accounts', AccountViewSet, basename='accounts')
router.register(r'incomes', IncomeViewSet, basename='incomes')
router.register(r'expenses', ExpensesViewSet, basename='expenses')
router.register(r'category_limits', CategoryLimitViewSet, basename='category_limits')
router.register(r'settings', SettingsViewSet, basename='settings')
urlpatterns = router.urls


urlpatterns += [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path(r'', include('Finance.urls')),
    re_path('^user_token/(?P<token>.+)/$', UserTokenList.as_view()),
    re_path('^account/(?P<user>.+)/$', AccountList.as_view()),
    re_path('^expense/(?P<account_id>.+)/$', ExpensesList.as_view()),
    re_path('^income/(?P<account_id>.+)/$', IncomeList.as_view()),
    re_path('^expense_categ/(?P<account_id>.+)/(?P<category>.+)/$', ExpensesListCategory.as_view()),
    re_path('^limit_categ/(?P<account_id>.+)/(?P<name_category>.+)/$', CategoryLimitList.as_view()),
    re_path('^limit_account/(?P<account_id>.+)/$', CategoryLimitAccountList.as_view()),
]
