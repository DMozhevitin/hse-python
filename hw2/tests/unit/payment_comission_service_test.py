from exception.exceptions import IllegalArgumentException
from unittest.mock import Mock, patch
from unittest import TestCase
import service.payment_comission_service as PaymentComissionService

class CalculateComissionTest(TestCase):
    def test_calculate_comission_success(self):
        self.assertEqual(5.0, PaymentComissionService.calculate_comission(100.0))

    def test_calculate_comission_negative_amount(self):
        with self.assertRaises(IllegalArgumentException):
            PaymentComissionService.calculate_comission(-1.0)

    def test_calculate_comission_zero_amount(self):
        with self.assertRaises(IllegalArgumentException):
            PaymentComissionService.calculate_comission(0.0)
