from rest_framework import serializers
from Finance.models import User, Account, FamilyUser, Income, Expenses, CategoryLimit, Settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'full_name', 'token', 'date')


class FamilyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyUser
        fields = ('family_user_id', 'user_id', 'full_name')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'user', 'currency', 'account_name', 'amount_check')


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('source_of_income', 'amount_income', 'account_id', 'date')


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ('category', 'title', 'amount_expenses', 'account_id', 'date')


class CategoryLimitSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryLimit
        fields = ('id', 'account_id', 'name_category', 'amount_limit')


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('user', 'user_categories')






