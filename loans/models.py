from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    monthly_income = models.IntegerField()
    phone_number = models.BigIntegerField()
    approved_limit = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.monthly_income:
            self.approved_limit = round(36 * self.monthly_income, -5)
        super().save(*args, **kwargs)

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    monthly_installment = models.FloatField(null=True, blank=True)

    def calculate_monthly_installment(self):
        if self.interest_rate and self.tenure:
            monthly_rate = self.interest_rate / 100 / 12
            self.monthly_installment = (self.loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -self.tenure)
            self.save()
