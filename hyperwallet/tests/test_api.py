#!/usr/bin/env python

import mock
import unittest
import hyperwallet

from hyperwallet.config import SERVER
from hyperwallet.exceptions import HyperwalletException


class ApiInitializationTest(unittest.TestCase):

    def test_no_username(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api = hyperwallet.Api()

        self.assertEqual(exc.exception.message, 'username is required')

    def test_no_password(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api = hyperwallet.Api(
                'username'
            )

        self.assertEqual(exc.exception.message, 'password is required')

    def test_no_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api = hyperwallet.Api(
                'username',
                'password'
            )

        self.assertEqual(exc.exception.message, 'programToken is required')


class ApiTest(unittest.TestCase):

    def setUp(self):

        self.program_token = 'prg-12345'
        self.api = hyperwallet.Api(
            'test-user',
            'test-pass',
            self.program_token
        )

        self.data = {
            'token': '123'
        }

        self.balance = {
            'currency': 'USD'
        }

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_users(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listUsers()

        self.assertEqual(response[0].token, self.data.get('token'))

    def test_create_user_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createUser()

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_with_data(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createUser(self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_retrieve_user_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_user_with_user_token(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.retrieveUser('token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_user_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_user_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateUser('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_user_with_user_token_and_data(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateUser('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_accounts_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccounts()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_accounts_with_user_token(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankAccounts('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_bank_account_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_account_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccount('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_with_user_token_and_data(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankAccount('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_retrieve_bank_account_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_retrieve_bank_account_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveBankAccount('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_bank_account_with_user_token_and_bank_token(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.retrieveBankAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_bank_account_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_bank_account_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    def test_update_bank_account_with_user_token_and_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_account_with_user_token_and_bank_token_and_data(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateBankAccount('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_cards_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankCards()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_cards_with_user_token(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankCards('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_bank_card_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_card_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCard('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_card_with_user_token_and_data(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankCard('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_retrieve_bank_card_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_retrieve_bank_card_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveBankCard('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_bank_card_with_user_token_and_card_token(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.retrieveBankCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_bank_card_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_bank_card_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankCard('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    def test_update_bank_card_with_user_token_and_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankCard('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_card_with_user_token_and_card_token_and_data(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateBankCard('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_prepaid_cards_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCards()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_cards_with_user_token(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPrepaidCards('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_prepaid_card_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_prepaid_card_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_with_user_token_and_data(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPrepaidCard('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_retrieve_prepaid_card_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_retrieve_prepaid_card_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_prepaid_card_with_user_token_and_card_token(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.retrievePrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_paper_checks_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperChecks()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paper_checks_with_user_token(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaperChecks('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_paper_check_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_paper_check_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheck('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_with_user_token_and_data(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPaperCheck('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_retrieve_paper_check_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_retrieve_paper_check_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePaperCheck('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_paper_check_with_user_token_and_paper_check_token(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.retrievePaperCheck('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_paper_check_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_paper_check_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    def test_update_paper_check_with_user_token_and_paper_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_paper_check_with_user_token_and_paper_check_token_and_data(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updatePaperCheck('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_payments(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPayments()

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_payment_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayment()

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_payment_with_data(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPayment(self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_retrieve_payment_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePayment()

        self.assertEqual(exc.exception.message, 'paymentToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_payment_with_payment_token(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.retrievePayment('token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_user_balances_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listUserBalances()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_balances_with_user_token(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listUserBalances('token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_repaid_card_balances_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardBalances()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_repaid_card_balances_with_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardBalances('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_repaid_card_balances_with_user_token_and_card_token(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listPrepaidCardBalances('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_account_balances_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listAccountBalances()

        self.assertEqual(exc.exception.message, 'programToken is required')

    def test_list_account_balances_with_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listAccountBalances('token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_balances_with_program_token_and_account_token(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listAccountBalances('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_retrieve_program_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveProgram()

        self.assertEqual(exc.exception.message, 'programToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_program_with_program_token(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.retrieveProgram('token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_retrieve_account_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveAccount()

        self.assertEqual(exc.exception.message, 'programToken is required')

    def test_retrieve_account_with_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveAccount('token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_account_with_program_token_and_account_token(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.retrieveAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_webhooks(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listWebhooks()

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_retrieve_webhooks_with_nothing(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveWebhook()

        self.assertEqual(exc.exception.message, 'webhookToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_webhook_with_webhook_token(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.retrieveWebhook('token')

        self.assertTrue(response.token, self.data.get('token'))


if __name__ == '__main__':
    unittest.main()
