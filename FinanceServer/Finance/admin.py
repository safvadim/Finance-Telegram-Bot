from django.contrib import admin
from .models import User, FamilyUser, Account, Income, Expenses


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name', 'token', 'date',)


@admin.register(FamilyUser)
class FamilyUserAdmin(admin.ModelAdmin):
    list_display = ('family_user_id', 'user_id', 'full_name')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['account_id'].queryset = Account.objects.filter(user__account=request.user.pk)
        return super(IncomeAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['account_id'].queryset = Account.objects.filter(user__account=request.user.pk)
        return super(ExpensesAdmin, self).render_change_form(request, context, *args, **kwargs)
