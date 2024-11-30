from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer, Loan

class CustomerLoanTests(APITestCase):

    def setUp(self):
        self.customer_data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "monthly_income": 50000,
            "phone_number": 9876543210
        }
        self.customer = Customer.objects.create(**self.customer_data)

    def test_register_customer(self):
        response = self.client.post(reverse('register_customer'), self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)  # One from setUp and one from this test
        self.assertEqual(response.data['first_name'], self.customer_data['first_name'])

    def test_check_eligibility(self):
        loan_data = {
            "customer_id": self.customer.id,
            "loan_amount": 200000,
            "interest_rate": 10,
            "tenure": 12
        }
        response = self.client.post(reverse('check_eligibility'), loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('approval', response.data)

    def test_create_loan(self):
        loan_data = {
            "customer": self.customer.id,
            "loan_amount": 200000,
            "interest_rate": 10,
            "tenure": 12
        }
        response = self.client.post(reverse('create_loan'), loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)

    def test_view_loan(self):
        loan_data = {
            "customer": self.customer.id,
            "loan_amount": 200000,
            "interest_rate": 10,
            "tenure": 12
        }
        loan_response = self.client.post(reverse('create_loan'), loan_data, format='json')
        loan_id = loan_response.data['id']

        response = self.client.get(reverse('view_loan', args=[loan_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['loan_id'], loan_id)

    def test_view_loans_by_customer(self):
        loan_data = {
            "customer": self.customer.id,
            "loan_amount": 200000,
            "interest_rate": 10,
            "tenure": 12
        }
        self.client.post(reverse('create_loan'), loan_data, format='json')
        response = self.client.get(reverse('view_loans', args=[self.customer.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return one loan
