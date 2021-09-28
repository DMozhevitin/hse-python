from unittest import TestCase
import os
import service.account_service as AccountService
import service.payment_comission_service as PaymentComissionService
from db import account_dao
from model.account import Account
from model.currency_type import CurrencyType

class WithdrawIntegrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['ACCOUNTS_DB_PATH'] = 'db/data/accounts_test.pickle'

    @classmethod
    def tearDownClass(cls):
        os.remove(os.environ['ACCOUNTS_DB_PATH'])
        os.environ['ACCOUNTS_DB_PATH'] = 'db/data/accounts.pickle'


    def setUp(self):
        init_accounts = {
            1: Account(id=1, owner_id=1, currency_type=CurrencyType.RUB, balance=10_000.0),
            2: Account(id=2, owner_id=1, currency_type=CurrencyType.EUR, balance=100.0),
            3: Account(id=3, owner_id=2, currency_type=CurrencyType.RUB, balance=1000.0)
        }

        account_dao.delete_all()
        for _, acc in init_accounts.items():
            account_dao.save(acc)

    def tearDown(self):
        account_dao.delete_all()

    def test_withdraw(self):
        balance_before = AccountService.get_account_by_id(1).balance
        AccountService.withdraw(1, 10.0)
        balance_after = AccountService.get_account_by_id(1).balance
        self.assertEqual(10.0, balance_before - balance_after)

    def test_refill(self):
        balance_before = AccountService.get_account_by_id(1).balance
        AccountService.refill(1, 10.0)
        balance_after = AccountService.get_account_by_id(1).balance
        self.assertEqual(10.0, balance_after - balance_before)

    def test_refill(self):
        balance_before = AccountService.get_account_by_id(1).balance
        AccountService.refill(1, 10.0)
        balance_after = AccountService.get_account_by_id(1).balance
        self.assertEqual(10.0, balance_after - balance_before)

    def test_transfer(self):
        balance_sender_before = AccountService.get_account_by_id(1).balance
        balance_receiver_before = AccountService.get_account_by_id(3).balance
        AccountService.transfer(1, 3, 100.0)
        balance_sender_after = AccountService.get_account_by_id(1).balance
        balance_receiver_after = AccountService.get_account_by_id(3).balance
        self.assertEqual(100.0, balance_sender_before - balance_sender_after)
        self.assertEqual(100.0 - 100.0 * PaymentComissionService.RATE, balance_receiver_after - balance_receiver_before)
