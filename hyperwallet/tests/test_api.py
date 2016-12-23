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
            'input': 'value'
        }
        self.expected_output = {
            'output': 'value'
        }

        self.mock_response = mock.Mock()
        self.mock_response.json.return_value = self.expected_output

    def test_add_program_token_with_non_dictonary(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api._addProgramToken(1)

        self.assertEqual(
            exc.exception.message,
            'data must be a dictionary object'
        )

    def test_add_program_token_with_empty_dictonary(self):

        response = self.api._addProgramToken({})

        self.assertEquals(response.get('programToken'), self.program_token)

    def test_add_program_token_with_primed_dictonary(self):

        response = self.api._addProgramToken(self.data)

        self.assertEquals(response.get('programToken'), self.program_token)

    def test_add_program_token_with_dictonary_contains_program_token(self):

        response = self.api._addProgramToken(
            {'programToken': self.program_token}
        )

        self.assertEquals(response.get('programToken'), self.program_token)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_users(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listUsers()

        self.assertEqual(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_with_nothing(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createUser()

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_with_data(self, mock_post):

        mock_post.return_value = self.mock_response
        response = self.api.createUser(self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_user_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_user_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrieveUser('token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_user_with_nothing(self, mock_put):

        mock_put.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_user_with_user_token(self, mock_put):

        mock_put.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateUser('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_user_with_user_token_and_data(self, mock_put):

        mock_put.return_value = self.mock_response
        response = self.api.updateUser('token', self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_balances_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listUserBalances()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_balances_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listUserBalances('token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_receipts_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listUserReceipts()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_receipts_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listUserReceipts('token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_accounts_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccounts()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_accounts_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listBankAccounts('token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_with_nothing(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_with_user_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccount('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_with_user_token_and_data(self, mock_post):

        mock_post.return_value = self.mock_response
        response = self.api.createBankAccount('token', self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_bank_account_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_bank_account_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveBankAccount('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_bank_account_with_user_token_and_bank_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrieveBankAccount('token', 'bank')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_account_with_nothing(self, mock_put):

        mock_put.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_account_with_user_token(self, mock_put):

        mock_put.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_account_with_user_token_and_bank_token(self, mock_put):

        mock_put.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount('token', 'bank')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_account_with_user_token_and_bank_token_and_data(self, mock_put):

        mock_put.return_value = self.mock_response
        response = self.api.updateBankAccount('token', 'bank', self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_transition_with_nothing(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_transition_with_user_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_transition_with_user_token_and_bank_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccountStatusTransition('token', 'bank')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_transition_with_user_token_and_bank_token_and_data(self, mock_post):

        mock_post.return_value = self.mock_response
        response = self.api.createBankAccountStatusTransition(
            'token', 'bank', self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_bank_account_transition_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveBankAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_bank_account_transition_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveBankAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_bank_account_transition_with_user_token_and_bank_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveBankAccountStatusTransition('token', 'bank')

        self.assertEqual(exc.exception.message,
                         'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_bank_account_transition_with_user_token_and_bank_token_and_transition_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrieveBankAccountStatusTransition(
            'token', 'bank', 'status-token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_cards_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCards()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_cards_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listPrepaidCards('token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_with_nothing(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_with_user_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_with_user_token_and_data(self, mock_post):

        mock_post.return_value = self.mock_response
        response = self.api.createPrepaidCard('token', self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_prepaid_card_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_prepaid_card_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_prepaid_card_with_user_token_and_card_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrievePrepaidCard('token', 'card')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_status_transitions_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_status_transitions_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_status_transitions_with_user_token_and_card_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listPrepaidCardStatusTransitions('token', 'card')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_status_transition_with_nothing(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_status_transition_with_user_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_status_transition_with_user_token_and_card_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCardStatusTransition('token', 'card')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_status_transition_with_user_token_and_card_token_and_data(self, mock_post):

        mock_post.return_value = self.mock_response
        response = self.api.createPrepaidCardStatusTransition(
            'token', 'card', self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_prepaid_card_status_transition_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePrepaidCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_prepaid_card_status_transition_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePrepaidCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_prepaid_card_status_transition_with_user_token_and_card_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePrepaidCardStatusTransition('token', 'card')

        self.assertEqual(exc.exception.message,
                         'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_prepaid_card_status_transition_with_user_token_and_card_token_and_transition_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrievePrepaidCardStatusTransition(
            'token', 'card', 'status-token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_repaid_card_balances_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardBalances()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_repaid_card_balances_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardBalances('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_repaid_card_balances_with_user_token_and_card_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listPrepaidCardBalances('token', 'card')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_repaid_card_receipts_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardReceipts()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_repaid_card_receipts_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardReceipts('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_repaid_card_receipts_with_user_token_and_card_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listPrepaidCardReceipts('token', 'card')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paper_checks_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperChecks()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paper_checks_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listPaperChecks('token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_with_nothing(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_with_user_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheck('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_with_user_token_and_data(self, mock_post):

        mock_post.return_value = self.mock_response
        response = self.api.createPaperCheck('token', self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_paper_check_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_paper_check_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePaperCheck('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_paper_check_with_user_token_and_paper_check_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrievePaperCheck('token', 'check')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_paper_check_with_nothing(self, mock_put):

        mock_put.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_paper_check_with_user_token(self, mock_put):

        mock_put.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_paper_check_with_user_token_and_paper_check_token(self, mock_put):

        mock_put.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck('token', 'bank')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_paper_check_with_user_token_and_paper_check_token_and_data(self, mock_put):

        mock_put.return_value = self.mock_response
        response = self.api.updatePaperCheck('token', 'check', self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_transition_with_nothing(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheckStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_transition_with_user_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheckStatusTransition('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_transition_with_user_token_and_bank_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheckStatusTransition('token', 'check')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_transition_with_user_token_and_bank_token_and_data(self, mock_post):

        mock_post.return_value = self.mock_response
        response = self.api.createPaperCheckStatusTransition(
            'token', 'check', self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_paper_check_transition_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePaperCheckStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_paper_check_transition_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePaperCheckStatusTransition('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_paper_check_transition_with_user_token_and_check_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePaperCheckStatusTransition('token', 'check')

        self.assertEqual(exc.exception.message,
                         'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_paper_check_transition_with_user_token_and_check_token_and_transition_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrievePaperCheckStatusTransition(
            'token', 'check', 'status-token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_payments(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listPayments()

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_payment_with_nothing(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayment()

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_payment_with_data(self, mock_post):

        mock_post.return_value = self.mock_response
        response = self.api.createPayment(self.data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_payment_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrievePayment()

        self.assertEqual(exc.exception.message, 'paymentToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_payment_with_payment_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrievePayment('payment')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_account_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveAccount()

        self.assertEqual(exc.exception.message, 'programToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_account_with_program_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveAccount('program-token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_account_with_program_token_and_account_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrieveAccount('program-token', 'account-token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_balances_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listAccountBalances()

        self.assertEqual(exc.exception.message, 'programToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_balances_with_program_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listAccountBalances('program-token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_balances_with_program_token_and_account_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listAccountBalances(
            'program-token', 'account-token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_receipts_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listAccountReceipts()

        self.assertEqual(exc.exception.message, 'programToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_receipts_with_program_token(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listAccountReceipts('program-token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_receipts_with_program_token_and_account_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listAccountReceipts(
            'program-token', 'account-token')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_program_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveProgram()

        self.assertEqual(exc.exception.message, 'programToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_program_with_program_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.retrieveProgram('payment')

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_method_configurations_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransferMethodConfigurations()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_method_configurations_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response
        response = self.api.listTransferMethodConfigurations(
            {'userToken': 'value'})

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_transfer_method_configuration_with_nothing(self, mock_get):

        mock_get.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveTransferMethodConfiguration()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_transfer_method_configuration_with_user_token(self, mock_get):

        mock_get.return_value = self.mock_response

        data = {
            'userToken': 'value'
        }

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveTransferMethodConfiguration(data)

        self.assertEqual(exc.exception.message, 'country is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_transfer_method_configuration_with_user_token_and_country(self, mock_get):

        mock_get.return_value = self.mock_response

        data = {
            'userToken': 'value',
            'country': 'value'
        }

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveTransferMethodConfiguration(data)

        self.assertEqual(exc.exception.message, 'currency is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_transfer_method_configuration_with_user_token_and_country_and_currency(self, mock_get):

        mock_get.return_value = self.mock_response

        data = {
            'userToken': 'value',
            'country': 'value',
            'currency': 'value'
        }

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveTransferMethodConfiguration(data)

        self.assertEqual(exc.exception.message, 'type is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_transfer_method_configuration_with_user_token_and_country_and_currency_and_type(self, mock_get):

        mock_get.return_value = self.mock_response

        data = {
            'userToken': 'value',
            'country': 'value',
            'currency': 'value',
            'type': 'value'
        }

        with self.assertRaises(HyperwalletException) as exc:
            self.api.retrieveTransferMethodConfiguration(data)

        self.assertEqual(exc.exception.message, 'profileType is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_retrieve_transfer_method_configuration_with_user_token_and_country_and_currency_and_type_and_profile_type(self, mock_get):

        mock_get.return_value = self.mock_response

        data = {
            'userToken': 'value',
            'country': 'value',
            'currency': 'value',
            'type': 'value',
            'profileType': 'value'
        }

        response = self.api.retrieveTransferMethodConfiguration(data)

        self.assertTrue(response.json(), self.expected_output)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_method_with_nothing(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferMethod()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_method_with_user_token(self, mock_post):

        mock_post.return_value = self.mock_response

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferMethod('token')

        self.assertEqual(exc.exception.message, 'cacheToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_method_with_user_token_and_cache_token(self, mock_post):

        mock_post.return_value = self.mock_response
        response = self.api.createTransferMethod('token', 'cache-token')

        self.assertTrue(response.json(), self.expected_output)


if __name__ == '__main__':
    unittest.main()
