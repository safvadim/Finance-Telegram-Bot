from django.db import models
from django.db.models import F


class User(models.Model):
    user_id = models.CharField(max_length=30, primary_key=True)
    full_name = models.CharField(max_length=10)
    token = models.CharField(max_length=32, null=True, blank=False)
    date = models.DateField()

    class Meta:
        ordering = ('user_id', 'full_name', 'token', 'date',)

    def __str__(self):
        return f"{self.user_id}"


class FamilyUser(models.Model):
    family_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=30, primary_key=True)
    full_name = models.CharField(max_length=10)

    class Meta:
        ordering = ('family_user_id', 'user_id', 'full_name')


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3)
    account_name = models.CharField(max_length=10)
    amount_check = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.currency = self.currency.upper()
        return super(Account, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ('id', 'user', 'currency', 'account_name', 'amount_check',)

    def __str__(self):
        return f"{self.account_name}: {self.amount_check} - {self.currency}"


class Income(models.Model):
    source_of_income = models.CharField(max_length=10)
    amount_income = models.DecimalField(max_digits=10, decimal_places=2)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.account_id.amount_check = F('amount_check') + self.amount_income
        self.account_id.save()

    class Meta:
        ordering = ('source_of_income', 'amount_income', 'account_id', 'date')


class Expenses(models.Model):
    category = models.CharField(max_length=15)
    title = models.CharField(max_length=50)
    amount_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.account_id.amount_check = F('amount_check') - self.amount_expenses
        self.account_id.save()

    class Meta:
        ordering = ('category', 'title', 'amount_expenses', 'account_id', 'date')


class CategoryLimit(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    name_category = models.CharField(max_length=15)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('id', 'account_id', 'name_category', 'amount_limit')


class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_categories = models.CharField(max_length=15, default=None)

    class Meta:
        ordering = ('user', 'user_categories')



