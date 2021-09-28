from unittest.mock import Mock, patch
from unittest import TestCase
from model.account import Account
from model.currency_type import CurrencyType
from exception.exceptions import EntityNotFoundException, IllegalArgumentException
import service.account_service as AccountService

class WithdrawTest(TestCase):
    @patch('db.account_dao.load_by_id')
    def test_withdraw_success(self, account_dao_mock: Mock):
        mock_account = Account(id=1, owner_id=1, currency_type = CurrencyType.RUB, balance=100.0)
        account_dao_mock.return_value = mock_account
        self.assertEqual(90, AccountService.withdraw(mock_account.id, 10).balance)

    @patch('db.account_dao.load_by_id')
    def test_withdraw_not_enough_balance(self, accounts_dao_mock: Mock):
        mock_account = Account(id=1, owner_id=1, currency_type = CurrencyType.USD, balance = 1.0)
        accounts_dao_mock.return_value = mock_account
        with self.assertRaises(IllegalArgumentException):
            AccountService.withdraw(mock_account.id, 10)

    @patch('db.account_dao.load_by_id')
    def test_withdraw_account_does_not_exist(self, account_dao_mock: Mock):
        account_dao_mock.return_value = None
        with self.assertRaises(EntityNotFoundException):
            AccountService.withdraw(2, 1)

    @patch('db.account_dao.load_by_id')
    def test_withdraw_negative_amount(self, account_dao_mock: Mock):
        mock_account = Account(id=1, owner_id=1, currency_type = CurrencyType.USD, balance = 1000.0)
        account_dao_mock.return_value = mock_account
        with self.assertRaises(IllegalArgumentException):
            AccountService.withdraw(mock_account.id, -1)

class RefillTest(TestCase):
    @patch('db.account_dao.load_by_id')
    def test_refill_success(self, account_dao_mock: Mock):
        mock_account = Account(id=1, owner_id=1, currency_type = CurrencyType.RUB, balance=100.0)
        account_dao_mock.return_value = mock_account
        self.assertEqual(110, AccountService.refill(mock_account.id, 10).balance)

    @patch('db.account_dao.load_by_id')
    def test_refill_account_does_not_exist(self, account_dao_mock: Mock):
        account_dao_mock.return_value = None
        with self.assertRaises(EntityNotFoundException):
            AccountService.refill(2, 1)

    @patch('db.account_dao.load_by_id')
    def test_refill_negative_amount(self, account_dao_mock: Mock):
        mock_account = Account(id=1, owner_id=1, currency_type = CurrencyType.EUR, balance = 100.0)
        account_dao_mock.return_value = mock_account
        with self.assertRaises(IllegalArgumentException):
            AccountService.refill(mock_account.id, -1)

class TransferTest(TestCase):
    @patch('db.account_dao.load_by_id')
    @patch('service.payment_comission_service.calculate_comission')
    def test_transfer_success(self, comission_service_mock: Mock, account_dao_mock: Mock):
        mock_accounts = {
            1: Account(id=1, owner_id=1, currency_type = CurrencyType.RUB, balance = 100.0),
            2: Account(id=2, owner_id=1, currency_type = CurrencyType.RUB, balance = 10.0)
        }

        def getter(*args, **kwargs):
            return mock_accounts.get(args[0])

        account_dao_mock.side_effect = getter
        comission_service_mock.return_value = 1.0

        sender, receiver = AccountService.transfer(1, 2, 10.0)
        self.assertEqual(90, sender.balance)
        self.assertEqual(19, receiver.balance)


    @patch('db.account_dao.load_by_id')
    @patch('service.payment_comission_service.calculate_comission')
    def test_transfer_not_enough_balance(self, comission_service_mock: Mock, account_dao_mock: Mock):
        mock_accounts = {
            1: Account(id=1, owner_id=1, currency_type = CurrencyType.RUB, balance = 100.0),
            2: Account(id=2, owner_id=1, currency_type = CurrencyType.RUB, balance = 10.0)
        }

        def getter(*args, **kwargs):
            return mock_accounts.get(args[0])

        account_dao_mock.side_effect = getter
        comission_service_mock.return_value = 1.0

        with self.assertRaises(IllegalArgumentException):
            AccountService.transfer(1, 2, 101.0)

    @patch('db.account_dao.load_by_id')
    @patch('service.payment_comission_service.calculate_comission')
    def test_transfer_to_self(self, comission_service_mock: Mock, account_dao_mock: Mock):
        with self.assertRaises(IllegalArgumentException):
            AccountService.transfer(1, 1, 1)

    @patch('db.account_dao.load_by_id')
    @patch('service.payment_comission_service.calculate_comission')
    def test_transfer_between_different_currencies(self, comission_service_mock: Mock, account_dao_mock: Mock):
        mock_accounts = {
            1: Account(id=1, owner_id=1, currency_type = CurrencyType.RUB, balance = 100.0),
            2: Account(id=2, owner_id=1, currency_type = CurrencyType.EUR, balance = 10.0)
        }

        def getter(*args, **kwargs):
            return mock_accounts.get(args[0])

        account_dao_mock.side_effect = getter
        comission_service_mock.return_value = 1.0

        with self.assertRaises(IllegalArgumentException):
            AccountService.transfer(1, 2, 1.0)

    @patch('db.account_dao.load_by_id')
    @patch('service.payment_comission_service.calculate_comission')
    def test_transfer_sender_does_not_exist(self, comission_service_mock: Mock, account_dao_mock: Mock):
        mock_accounts = {
            1: None,
            2: Account(id=2, owner_id=1, currency_type = CurrencyType.EUR, balance = 10.0)
        }

        def getter(*args, **kwargs):
            return mock_accounts.get(args[0])

        account_dao_mock.side_effect = getter
        comission_service_mock.return_value = 1.0

        with self.assertRaises(EntityNotFoundException):
            AccountService.transfer(1, 2, 1.0)

    @patch('db.account_dao.load_by_id')
    @patch('service.payment_comission_service.calculate_comission')
    def test_transfer_receiver_does_not_exist(self, comission_service_mock: Mock, account_dao_mock: Mock):
        mock_accounts = {
            1: Account(id=1, owner_id=1, currency_type = CurrencyType.RUB, balance = 100.0),
            2: None
        }

        def getter(*args, **kwargs):
            return mock_accounts.get(args[0])

        account_dao_mock.side_effect = getter
        comission_service_mock.return_value = 1.0

        with self.assertRaises(EntityNotFoundException):
            AccountService.transfer(1, 2, 1.0)
