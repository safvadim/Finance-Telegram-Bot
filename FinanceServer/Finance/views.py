from rest_framework import viewsets, generics
from Finance.models import User, FamilyUser, Account, Income, Expenses, CategoryLimit, Settings
from Finance.serializers import UserSerializer, AccountSerializer, FamilyUserSerializer, \
    IncomeSerializer, ExpensesSerializer, CategoryLimitSerializer, SettingsSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserTokenList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        token = self.kwargs['token']
        return User.objects.filter(token=token)


class FamilyUserViewSet(viewsets.ModelViewSet):
    queryset = FamilyUser.objects.all()
    serializer_class = FamilyUserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountList(generics.ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        user = self.kwargs['user']
        return Account.objects.filter(user_id=user)


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class IncomeList(generics.ListAPIView):
    serializer_class = IncomeSerializer

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        return Income.objects.filter(account_id=account_id)


class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer


class ExpensesList(generics.ListAPIView):
    serializer_class = ExpensesSerializer

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        return Expenses.objects.filter(account_id=account_id)


class ExpensesListCategory(generics.ListAPIView):
    serializer_class = ExpensesSerializer

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        category = self.kwargs['category']
        return Expenses.objects.filter(account_id=account_id, category=category)


class CategoryLimitViewSet(viewsets.ModelViewSet):
    queryset = CategoryLimit.objects.all()
    serializer_class = CategoryLimitSerializer


class CategoryLimitList(generics.ListAPIView):
    serializer_class = CategoryLimitSerializer

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        name_category = self.kwargs['name_category']
        return CategoryLimit.objects.filter(account_id=account_id, name_category=name_category)


class CategoryLimitAccountList(generics.ListAPIView):
    serializer_class = CategoryLimitSerializer

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        return CategoryLimit.objects.filter(account_id=account_id)


class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer