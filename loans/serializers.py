from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'age', 'monthly_income', 'phone_number', 'approved_limit']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'customer', 'loan_amount', 'interest_rate', 'tenure', 'is_approved', 'monthly_installment']