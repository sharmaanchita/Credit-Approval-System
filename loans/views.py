import pandas as pd
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer

def calculate_credit_score(customer):
    try:
        # Load historical loan data
        loan_data = pd.read_excel('loan_data.xlsx')
        customer_loans = loan_data[loan_data['customer_id'] == customer.id]

        # Calculate credit score components
        past_loans_paid_on_time = customer_loans['paid_on_time'].sum()
        number_of_loans = len(customer_loans)
        loan_activity_current_year = customer_loans[customer_loans['year'] == pd.Timestamp.now().year].count()
        total_approved_volume = customer_loans['approved_volume'].sum()

        # Here, implement your logic to calculate credit score based on the components
        credit_score = (past_loans_paid_on_time + number_of_loans + loan_activity_current_year + total_approved_volume) / 4
        return min(max(0, credit_score), 100)  # Ensure credit score is between 0 and 100

    except Exception as e:
        return 0  # Return 0 in case of error

def calculate_total_current_emis(customer):
    total_emis = Loan.objects.filter(customer=customer, is_approved=True).aggregate(Sum('monthly_installment'))['monthly_installment__sum'] or 0
    return total_emis

class RegisterCustomer(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckEligibility(APIView):
    def post(self, request):
        customer = get_object_or_404(Customer, id=request.data['customer_id'])
        loan_amount = float(request.data['loan_amount'])
        interest_rate = float(request.data['interest_rate'])

        credit_score = calculate_credit_score(customer)

        if loan_amount > customer.approved_limit:
            credit_score = 0

        approval_data = {
            'customer_id': customer.id,
            'approval': False,
            'corrected_interest_rate': interest_rate,
            'tenure': request.data['tenure'],
        }

        if credit_score > 50:
            approval_data['approval'] = True
        elif 50 >= credit_score > 30 and interest_rate > 12:
            approval_data['corrected_interest_rate'] = 12
        elif 30 >= credit_score > 10 and interest_rate > 16:
            approval_data['corrected_interest_rate'] = 16
        elif credit_score <= 10:
            approval_data['approval'] = False

        total_current_emis = calculate_total_current_emis(customer)
        if total_current_emis > 0.5 * customer.monthly_income:
            approval_data['approval'] = False

        return Response(approval_data)

class CreateLoan(APIView):
    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.save()
            loan.calculate_monthly_installment()
            loan.is_approved = True  # Assuming loan is approved for this example
            loan.save()
            return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewLoan(APIView):
    def get(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id)
        customer = loan.customer
        return Response({
            'loan_id': loan.id,
            'customer': {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'phone_number': customer.phone_number,
                'age': customer.age
            },
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'monthly_installment': loan.monthly_installment,
            'tenure': loan.tenure,
            'is_approved': loan.is_approved
        })

class ViewLoansByCustomer(APIView):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        loans = Loan.objects.filter(customer=customer)
        loan_list = LoanSerializer(loans, many=True).data
        return Response(loan_list)