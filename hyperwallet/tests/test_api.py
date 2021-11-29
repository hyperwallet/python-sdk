#!/usr/bin/env python

import mock
import unittest
import hyperwallet

from hyperwallet.exceptions import HyperwalletException


class ApiInitializationTest(unittest.TestCase):

    def test_initialize_fail_need_username(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api = hyperwallet.Api()

        self.assertEqual(exc.exception.message, 'username is required')

    def test_initialize_fail_need_password(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api = hyperwallet.Api(
                'username'
            )

        self.assertEqual(exc.exception.message, 'password is required')

    def test_initialize_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api = hyperwallet.Api(
                'username',
                'password'
            )

        self.assertEqual(exc.exception.message, 'programToken is required')


class ApiTest(unittest.TestCase):

    def setUp(self):

        self.api = hyperwallet.Api(
            'test-user',
            'test-pass',
            'prg-12345'
        )

        self.data = {
            'token': 'tkn-12345'
        }

        self.data_with_type = {
            'token': 'tkn-12345',
            'type': 'BANK_ACCOUNT'
        }

        self.balance = {
            'currency': 'USD'
        }

        self.configuration = {
            'countries': ['US'],
            'currencies': ['USD'],
            'type': 'INDIVIDUAL'
        }

        self.uploadSuccessData = {
            'token': 'tkn-12345',
            "documents": [{
                "category": "IDENTIFICATION",
                "type": "DRIVERS_LICENSE",
                "country": "AL",
                "status": "NEW"
            }]
        }

        self.uploadRejectionData = {
            'token': 'tkn-12345',
            "documents": [{
                "category": "IDENTIFICATION",
                "type": "DRIVERS_LICENSE",
                "country": "AL",
                "status": "INVALID",
                "reasons": [
                    {
                        "name": "DOCUMENT_CORRECTION_REQUIRED",
                        "description": "Document requires correction"
                    },
                    {
                        "name": "DOCUMENT_NOT_DECISIVE",
                        "description": "Decision cannot be made based on document. Alternative document required"
                    }
                ],
                "createdOn": "2020-11-24T19:05:02"
            }]
        }

        self.value = {
            'data': ['{"documents": [{"type": "DRIVERS_LICENSE", "country": "AL", "category": "IDENTIFICATION"}]}']
        }
    '''

    Users

    '''

    def test_create_user_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createUser()

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createUser(self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_user_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_user_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getUser('token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_user_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_user_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateUser('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_user_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateUser('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_users_with_params_invalid(self):
        options = {'status': 'test', 'city': 'US'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listUsers(options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_users_with_params_valid(self, mock_get):
        options = {'status': 'test'}

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listUsers(options)

        self.assertEqual(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_users_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listUsers()

        self.assertEqual(response[0].token, self.data.get('token'))

    def test_get_user_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getUserStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_user_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getUserStatusTransition('token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_user_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getUserStatusTransition('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_user_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listUserStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_user_status_transitions_fail_need_params_invalid(self):

        options = {'transition': 'test', 'fromStatus': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listUserStatusTransitions('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_status_transitions_params_valid(self, mock_get):

        options = {'transition': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listUserStatusTransitions('token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listUserStatusTransitions('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    '''

    Bank Accounts

    '''

    def test_create_bank_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_account_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccount('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankAccount('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_bank_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_bank_account_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccount('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_bank_account_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getBankAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_bank_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_bank_account_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount('token')

        self.assertEqual(exc.exception.message, 'transfer method token is required')

    def test_update_bank_account_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankAccount('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_account_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateBankAccount('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_accounts_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccounts()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_bank_accounts_fail_need_params_invalid(self):

        options = {'status': 'test', 'bankName': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccounts('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_accounts_params_valid(self, mock_get):

        options = {'status': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankAccounts('token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_accounts_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankAccounts('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_bank_account_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_account_status_transition_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    def test_create_bank_account_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankAccountStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_account_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankAccountStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_bank_account_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_bank_account_status_transition_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    def test_get_bank_account_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankAccountStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_bank_account_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getBankAccountStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_account_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccountStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_bank_account_status_transitions_fail_need_params_invalid(self):

        options = {'transition': 'test', 'fromStatus': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccountStatusTransitions('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_account_status_transitions_params_valid(self, mock_get):

        options = {'transition': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankAccountStatusTransitions('token', 'token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_list_bank_account_status_transitions_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankAccountStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_account_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankAccountStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_bank_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateBankAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_bank_account_fail_need_bank_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateBankAccount('token')

        self.assertEqual(exc.exception.message, 'bankAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_bank_account_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivateBankAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_bank_account_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivateBankAccount('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    Bank Cards

    '''

    def test_create_bank_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_card_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCard('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankCard('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_bank_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_bank_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCard('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_bank_card_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getBankCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_bank_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_bank_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankCard('token')

        self.assertEqual(exc.exception.message, 'transfer method token is required')

    def test_update_bank_card_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateBankCard('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_bank_card_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateBankCard('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_cards_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankCards()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_bank_cards_fail_need_params_invalid(self):

        options = {'type': 'test', 'cardNumber': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankCards('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_cards_params_valid(self, mock_get):

        options = {'type': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankCards('token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_cards_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankCards('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_bank_card_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_bank_card_status_transition_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    def test_create_bank_card_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createBankCardStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_bank_card_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createBankCardStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_bank_card_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_bank_card_status_transition_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    def test_get_bank_card_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getBankCardStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_bank_card_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getBankCardStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_bank_card_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankCardStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_bank_card_status_transitions_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankCardStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    def test_list_bank_card_status_transitions_fail_need_params_invalid(self):

        options = {'transition': 'test', 'fromStatus': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBankCardStatusTransitions('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_card_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankCardStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_bank_card_status_transitions_success(self, mock_get):

        options = {'transition': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listBankCardStatusTransitions('token', 'token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_bank_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateBankCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_bank_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateBankCard('token')

        self.assertEqual(exc.exception.message, 'bankCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_bank_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivateBankCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_bank_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivateBankCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    Prepaid Cards

    '''

    def test_create_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_prepaid_card_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPrepaidCard('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePrepaidCard('token')

        self.assertEqual(exc.exception.message, 'transfer method token is required')

    def test_update_prepaid_card_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePrepaidCard('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_prepaid_card_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updatePrepaidCard('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_prepaid_card_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_prepaid_cards_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCards()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_prepaid_cards_fail_need_params_invalid(self):

        options = {'status': 'test', 'cardPackage': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCards('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_cards_params_valid(self, mock_get):

        options = {'status': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPrepaidCards('token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_cards_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPrepaidCards('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_prepaid_card_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_prepaid_card_status_transition_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    def test_create_prepaid_card_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPrepaidCardStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_prepaid_card_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPrepaidCardStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_prepaid_card_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCardStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_prepaid_card_status_transition_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCardStatusTransition('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    def test_get_prepaid_card_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPrepaidCardStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_prepaid_card_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPrepaidCardStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_prepaid_card_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_prepaid_card_status_transitions_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    def test_list_prepaid_card_status_transitions_fail_need_params_invalid(self):

        options = {'transition': 'test', 'status': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPrepaidCardStatusTransitions('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_status_transitions_success(self, mock_get):

        options = {'transition': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPrepaidCardStatusTransitions('token', 'token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPrepaidCardStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivatePrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivatePrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_suspend_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.suspendPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_suspend_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.suspendPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_suspend_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.suspendPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_suspend_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.suspendPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_unsuspend_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.unsuspendPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_unsuspend_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.unsuspendPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_unsuspend_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.unsuspendPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_unsuspend_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.unsuspendPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_lost_or_stolen_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.lostOrStolenPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_lost_or_stolen_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.lostOrStolenPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_lost_or_stolen_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.lostOrStolenPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_lost_or_stolen_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.lostOrStolenPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_lock_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.lockPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_lock_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.lockPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_lock_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.lockPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_lock_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.lockPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    def test_unlock_prepaid_card_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.unlockPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_unlock_prepaid_card_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.unlockPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_unlock_prepaid_card_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.unlockPrepaidCard('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_unlock_prepaid_card_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.unlockPrepaidCard('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    Paper Checks

    '''

    def test_create_paper_check_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_paper_check_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheck('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPaperCheck('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_paper_check_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_paper_check_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheck('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_paper_check_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPaperCheck('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_update_paper_check_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_paper_check_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck('token')

        self.assertEqual(exc.exception.message, 'transfer method token is required')

    def test_update_paper_check_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePaperCheck('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_paper_check_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updatePaperCheck('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_paper_checks_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperChecks()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_paper_checks_fail_need_params_invalid(self):

        options = {'status': 'test', 'city': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperChecks('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paper_checks_params_valid(self, mock_get):

        options = {'status': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaperChecks('token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paper_checks_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaperChecks('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_paper_check_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheckStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_paper_check_status_transition_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheckStatusTransition('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    def test_create_paper_check_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaperCheckStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paper_check_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPaperCheckStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_paper_check_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheckStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_paper_check_status_transition_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheckStatusTransition('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    def test_get_paper_check_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaperCheckStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_paper_check_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPaperCheckStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_paper_check_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperCheckStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_paper_check_status_transitions_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperCheckStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    def test_list_paper_check_status_transitions_fail_need_params_invalid(self):

        options = {'transition': 'test', 'city': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaperCheckStatusTransitions('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paper_check_status_transitions_params_valid(self, mock_get):

        options = {'transition': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaperCheckStatusTransitions('token', 'token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paper_check_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaperCheckStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_paper_check_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePaperCheck()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_paper_check_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePaperCheck('token')

        self.assertEqual(exc.exception.message, 'paperCheckToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_paper_check_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivatePaperCheck('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_paper_check_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivatePaperCheck('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    Transfers

    '''

    def test_create_transfer_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransfer()

        self.assertEqual(exc.exception.message, 'data is required')

    def test_create_transfer_fail_need_source_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransfer(self.data)

        self.assertEqual(exc.exception.message, 'sourceToken is required')

    def test_create_transfer_fail_need_destination_token(self):

        transfer_data = {
            'sourceToken': 'test-source-token'
        }
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransfer(transfer_data)

        self.assertEqual(exc.exception.message, 'destinationToken is required')

    def test_create_transfer_fail_need_client_transfer_id(self):

        transfer_data = {
            'sourceToken': 'test-source-token',
            'destinationToken': 'test-destination-token'
        }
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransfer(transfer_data)

        self.assertEqual(exc.exception.message, 'clientTransferId is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_success(self, mock_post):

        transfer_data = {
            'sourceToken': 'test-source-token',
            'destinationToken': 'test-destination-token',
            'clientTransferId': 'test-clientTransferId'
        }
        mock_post.return_value = transfer_data
        response = self.api.createTransfer(transfer_data)

        self.assertTrue(response.sourceToken, transfer_data.get('sourceToken'))

    def test_get_transfer_fail_need_transfer_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransfer()

        self.assertEqual(exc.exception.message, 'transferToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_transfer_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getTransfer('token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_transfers_fail_need_params_invalid(self):

        options = {'clientTransferId': 'test', 'status': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransfers(options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfers_params_valid(self, mock_get):

        options = {'clientTransferId': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listTransfers(options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfers_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listTransfers()

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_transfer_status_transition_fail_need_transfer_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferStatusTransition()

        self.assertEqual(exc.exception.message, 'transferToken is required')

    def test_create_transfer_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferStatusTransition('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createTransferStatusTransition('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    '''

    PayPal Accounts

    '''

    def test_create_paypal_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayPalAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_paypal_account_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayPalAccount('token')

        self.assertEqual(exc.exception.message, 'data is required')

    def test_create_paypal_account_fail_need_transfer_method_country(self):

        paypal_account_data = {
            'token': 'test-token'
        }
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayPalAccount('token', paypal_account_data)

        self.assertEqual(exc.exception.message, 'transferMethodCountry is required')

    def test_create_paypal_account_fail_need_transfer_method_currency(self):

        paypal_account_data = {
            'transferMethodCountry': 'test-transfer-method-country'
        }
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayPalAccount('token', paypal_account_data)

        self.assertEqual(exc.exception.message, 'transferMethodCurrency is required')

    def test_create_paypal_account_fail_need_email(self):

        paypal_account_data = {
            'transferMethodCountry': 'test-transfer-method-country',
            'transferMethodCurrency': 'test-transfer-method-currency'
        }
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayPalAccount('token', paypal_account_data)

        self.assertEqual(exc.exception.message, 'email is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paypal_account_success(self, mock_post):

        paypal_account_data = {
            'transferMethodCountry': 'test-transfer-method-country',
            'transferMethodCurrency': 'test-transfer-method-currency',
            'email': 'test-email'
        }
        mock_post.return_value = paypal_account_data
        response = self.api.createPayPalAccount('token', paypal_account_data)

        self.assertTrue(response.email, paypal_account_data.get('token'))

    def test_update_paypal_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePayPalAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_paypal_account_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePayPalAccount('token')

        self.assertEqual(exc.exception.message, 'transfer method token is required')

    def test_update_paypal_account_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updatePayPalAccount('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_paypal_account_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updatePayPalAccount('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_paypal_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPayPalAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_paypal_account_fail_need_paypal_account_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPayPalAccount('token')

        self.assertEqual(exc.exception.message, 'payPalAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_paypal_account_success(self, mock_get):

        paypal_account_data = {
            'email': 'test-email'
        }
        mock_get.return_value = paypal_account_data
        response = self.api.getPayPalAccount('token', 'token')

        self.assertTrue(response.email, paypal_account_data.get('email'))

    def test_list_paypal_accounts_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPayPalAccounts()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_transfers_fail_need_params_invalid(self):

        options = {'type': 'test', 'email': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPayPalAccounts('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paypal_accounts_params_valid(self, mock_get):

        options = {'type': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPayPalAccounts('token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paypal_accounts_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPayPalAccounts('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_paypal_account_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayPalAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_paypal_account_status_transition_fail_need_paypal_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayPalAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'payPalAccountToken is required')

    def test_create_paypal_account_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayPalAccountStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_paypal_account_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPayPalAccountStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_paypal_account_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPayPalAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_paypal_account_status_transition_fail_need_paypal_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPayPalAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'payPalAccountToken is required')

    def test_get_paypal_account_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPayPalAccountStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_paypal_account_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPayPalAccountStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_paypal_account_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPayPalAccountStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_paypal_account_status_transitions_fail_need_paypal_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPayPalAccountStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'payPalAccountToken is required')

    def test_list_paypal_account_status_transitions_fail_need_params_invalid(self):

        options = {'transition': 'test', 'email': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPayPalAccountStatusTransitions('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paypal_account_status_transitions_params_valid(self, mock_get):

        options = {'transition': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPayPalAccountStatusTransitions('token', 'token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_paypal_account_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPayPalAccountStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_paypal_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePayPalAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_paypal_account_fail_need_paypal_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivatePayPalAccount('token')

        self.assertEqual(exc.exception.message, 'payPalAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_paypal_account_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivatePayPalAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_paypal_account_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivatePayPalAccount('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    Venmo Accounts

    '''

    def test_create_venmo_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createVenmoAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_venmo_account_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createVenmoAccount('token')

        self.assertEqual(exc.exception.message, 'data is required')

    def test_create_venmo_account_fail_need_transfer_method_country(self):

        venmo_account_data = {
            'token': 'test-token'
        }
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createVenmoAccount('token', venmo_account_data)

        self.assertEqual(exc.exception.message, 'transferMethodCountry is required')

    def test_create_venmo_account_fail_need_transfer_method_currency(self):

        venmo_account_data = {
            'transferMethodCountry': 'test-transfer-method-country'
        }
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createVenmoAccount('token', venmo_account_data)

        self.assertEqual(exc.exception.message, 'transferMethodCurrency is required')

    def test_create_venmo_account_fail_need_account_id(self):

        venmo_account_data = {
            'transferMethodCountry': 'test-transfer-method-country',
            'transferMethodCurrency': 'test-transfer-method-currency'
        }
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createVenmoAccount('token', venmo_account_data)

        self.assertEqual(exc.exception.message, 'accountId is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_venmo_account_success(self, mock_post):

        venmo_account_data = {
            'transferMethodCountry': 'test-transfer-method-country',
            'transferMethodCurrency': 'test-transfer-method-currency',
            'accountId': 'test-account-id'
        }
        mock_post.return_value = venmo_account_data
        response = self.api.createVenmoAccount('token', venmo_account_data)

        self.assertTrue(response.accountId, venmo_account_data.get('token'))

    def test_update_venmo_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateVenmoAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_update_venmo_account_fail_need_check_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateVenmoAccount('token')

        self.assertEqual(exc.exception.message, 'transfer method token is required')

    def test_update_venmo_account_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.updateVenmoAccount('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_update_venmo_account_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.updateVenmoAccount('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_venmo_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getVenmoAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_venmo_account_fail_need_venmo_account_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getVenmoAccount('token')

        self.assertEqual(exc.exception.message, 'venmoAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_venmo_account_success(self, mock_get):

        venmo_account_data = {
            'accountId': 'test-account-id'
        }
        mock_get.return_value = venmo_account_data
        response = self.api.getVenmoAccount('token', 'token')

        self.assertTrue(response.accountId, venmo_account_data.get('accountId'))

    def test_list_venmo_accounts_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listVenmoAccounts()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_venmo_accounts_fail_need_params_invalid(self):

        options = {'type': 'test', 'email': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listVenmoAccounts('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_venmo_accounts_params_valid(self, mock_get):

        options = {'type': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listVenmoAccounts('token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_venmo_accounts_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listVenmoAccounts('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_venmo_account_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createVenmoAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_venmo_account_status_transition_fail_need_venmo_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createVenmoAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'venmoAccountToken is required')

    def test_create_venmo_account_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createVenmoAccountStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_venmo_account_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createVenmoAccountStatusTransition('token', 'token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_venmo_account_status_transition_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getVenmoAccountStatusTransition()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_venmo_account_status_transition_fail_need_venmo_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getVenmoAccountStatusTransition('token')

        self.assertEqual(exc.exception.message, 'venmoAccountToken is required')

    def test_get_venmo_account_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getVenmoAccountStatusTransition('token', 'token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_venmo_account_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getVenmoAccountStatusTransition('token', 'token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_venmo_account_status_transitions_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listVenmoAccountStatusTransitions()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_venmo_account_status_transitions_fail_need_venmo_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listVenmoAccountStatusTransitions('token')

        self.assertEqual(exc.exception.message, 'venmoAccountToken is required')

    def test_list_venmo_account_status_transitions_fail_need_params_invalid(self):

        options = {'transition': 'test', 'email': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listVenmoAccountStatusTransitions('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_venmo_account_status_transitions_params_valid(self, mock_get):

        options = {'transition': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listVenmoAccountStatusTransitions('token', 'token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_venmo_account_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listVenmoAccountStatusTransitions('token', 'token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_deactivate_venmo_account_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateVenmoAccount()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_deactivate_venmo_account_fail_need_venmo_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateVenmoAccount('token')

        self.assertEqual(exc.exception.message, 'venmoAccountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_venmo_account_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.deactivateVenmoAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_deactivate_venmo_account_success_with_notes(self, mock_post):

        data = self.data.copy()
        data.update({'notes': 'closing'})

        mock_post.return_value = data
        response = self.api.deactivateVenmoAccount('token', 'token', 'notes')

        self.assertTrue(response.notes, data.get('notes'))

    '''

    AuthenticationToken

    '''

    def test_get_authentication_token_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getAuthenticationToken()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_authentication_token_success(self, mock_post):

        authentication_token_data = {
            'value': 'test-value'
        }
        mock_post.return_value = authentication_token_data
        response = self.api.getAuthenticationToken('user-token')

        self.assertTrue(response.value, authentication_token_data.get('value'))

    '''

    Payments

    '''

    def test_create_payment_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPayment()

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_payment_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPayment(self.data)

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_payment_fail_need_payment_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPayment()

        self.assertEqual(exc.exception.message, 'paymentToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_payment_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPayment('token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_payments_fail_need_params_invalid(self):

        options = {'currency': 'test', 'email': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPayments(options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_payments_params_valid(self, mock_get):

        options = {'currency': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPayments(options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_payments_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPayments()

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_get_payment_status_transition_fail_need_payment_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaymentStatusTransition()

        self.assertEqual(exc.exception.message, 'paymentToken is required')

    def test_get_payment_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getPaymentStatusTransition('token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_payment_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getPaymentStatusTransition('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_payment_status_transitions_fail_need_payment_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaymentStatusTransitions()

        self.assertEqual(exc.exception.message, 'paymentToken is required')

    def test_list_payment_status_transitions_fail_need_params_invalid(self):

        options = {'transition': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listPaymentStatusTransitions('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_payment_status_transitions_params_valid(self, mock_get):

        options = {'transition': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaymentStatusTransitions('token', options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_payment_status_transitions_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listPaymentStatusTransitions('token')

        self.assertTrue(response[0].token, self.data.get('token'))

    def test_create_payment_status_transition_fail_need_payment_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaymentStatusTransition()

        self.assertEqual(exc.exception.message, 'paymentToken is required')

    def test_create_payment_status_transition_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createPaymentStatusTransition('token')

        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_payment_status_transition_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createPaymentStatusTransition('token', self.data)

        self.assertTrue(response.token, self.data.get('token'))

    '''

    Balances

    '''

    def test_list_user_balances_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_user_balances_fail_need_params_invalid(self):

        options = {'currency': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForUser('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_balances_params_valid(self, mock_get):

        options = {'currency': 'test'}
        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listBalancesForUser('token', options)

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_balances_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listBalancesForUser('token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_prepaid_card_balances_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_prepaid_card_balances_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    def test_list_prepaid_card_balances_fail_need_params_invalid(self):

        options = {'limit': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForPrepaidCard('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_balances_params_valid(self, mock_get):

        options = {'createdBefore': 'test'}
        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listBalancesForPrepaidCard('token', 'token', options)

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_balances_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listBalancesForPrepaidCard('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_account_balances_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForAccount()

        self.assertEqual(exc.exception.message, 'programToken is required')

    def test_list_account_balances_fail_need_account_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForAccount('token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    def test_list_account_balances_fail_need_params_invalid(self):

        options = {'currency': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listBalancesForAccount('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_balances_params_valid(self, mock_get):

        options = {'currency': 'test'}
        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listBalancesForAccount('token', 'token', options)

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_balances_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listBalancesForAccount('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    '''

    Receipts

    '''

    def test_list_user_receipts_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_user_receipts_fail_need_params_invalid(self):

        options = {'currency': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForUser('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_receipts_params_valid(self, mock_get):

        options = {'currency': 'test'}
        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listReceiptsForUser('token', options)

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_user_receipts_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listReceiptsForUser('token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_prepaid_card_receipts_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForPrepaidCard()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_prepaid_card_receipts_fail_need_card_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForPrepaidCard('token')

        self.assertEqual(exc.exception.message, 'prepaidCardToken is required')

    def test_list_prepaid_card_receipts_fail_need_params_invalid(self):

        options = {'createdBefore': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForPrepaidCard('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_receipts_params_valid(self, mock_get):

        options = {'createdBefore': 'test'}
        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listReceiptsForPrepaidCard('token', 'token', options)

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_prepaid_card_receipts_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listReceiptsForPrepaidCard('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    def test_list_account_receipts_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForAccount()

        self.assertEqual(exc.exception.message, 'programToken is required')

    def test_list_account_receipts_fail_need_account_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForAccount('token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    def test_list_account_receipts_fail_need_params_invalid(self):

        options = {'currency': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listReceiptsForAccount('token', 'token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_receipts_params_valid(self, mock_get):

        options = {'currency': 'test'}
        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listReceiptsForAccount('token', 'token', options)

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_account_receipts_success(self, mock_get):

        mock_get.return_value = {'data': [self.balance]}
        response = self.api.listReceiptsForAccount('token', 'token')

        self.assertTrue(response[0].currency, self.balance.get('currency'))

    '''

    Programs

    '''

    def test_get_program_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getProgram()

        self.assertEqual(exc.exception.message, 'programToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_program_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getProgram('token')

        self.assertTrue(response.token, self.data.get('token'))

    '''

    Accounts

    '''

    def test_get_account_fail_need_program_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getAccount()

        self.assertEqual(exc.exception.message, 'programToken is required')

    def test_get_account_fail_need_account_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getAccount('token')

        self.assertEqual(exc.exception.message, 'accountToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_account_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getAccount('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    '''

    Transfer Methods

    '''

    def test_create_transfer_method_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferMethod()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_transfer_method_fail_need_cache_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferMethod('token')

        self.assertEqual(exc.exception.message, 'cacheToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_method_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createTransferMethod('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_method_success_with_type(self, mock_post):

        mock_post.return_value = self.data_with_type
        response = self.api.createTransferMethod('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_get_transfer_method_configuration_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_get_transfer_method_configuration_fail_need_country(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration('token')

        self.assertEqual(exc.exception.message, 'country is required')

    def test_get_transfer_method_configuration_fail_need_currency(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration('token', 'country')

        self.assertEqual(exc.exception.message, 'currency is required')

    def test_get_transfer_method_configuration_fail_need_type(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration('token', 'country', 'currency')

        self.assertEqual(exc.exception.message, 'type is required')

    def test_get_transfer_method_configuration_fail_need_profile_type(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferMethodConfiguration('token', 'country', 'currency', 'type')

        self.assertEqual(exc.exception.message, 'profileType is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_transfer_method_configuration_success(self, mock_get):

        mock_get.return_value = self.configuration
        response = self.api.getTransferMethodConfiguration('token', 'country', 'currency', 'type', 'token')

        self.assertTrue(response.type, self.configuration.get('type'))

    def test_list_transfer_method_configurations_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransferMethodConfigurations()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_transfer_method_configurations_fail_need_params_invalid(self):

        options = {'userToken': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransferMethodConfigurations('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_method_configurations_params_valid(self, mock_get):

        options = {'offset': 'test'}
        mock_get.return_value = {'data': [self.configuration]}
        response = self.api.listTransferMethodConfigurations('token', options)

        self.assertTrue(response[0].type, self.configuration.get('type'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_method_configurations_success(self, mock_get):

        mock_get.return_value = {'data': [self.configuration]}
        response = self.api.listTransferMethodConfigurations('token')

        self.assertTrue(response[0].type, self.configuration.get('type'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_method_configurations_success_empty(self, mock_get):

        mock_get.return_value = {}
        response = self.api.listTransferMethodConfigurations('token')

        self.assertEqual(response, [])

    '''

    Webhook Notifications

    '''

    def test_get_webhook_fail_need_webhook_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getWebhookNotification()

        self.assertEqual(exc.exception.message, 'webhookToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_webhook_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getWebhookNotification('token')

        self.assertTrue(response.token, self.data.get('token'))

    def test_list_webhooks_fail_need_params_invalid(self):

        options = {'type': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listWebhookNotifications(options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_webhooks_params_valid(self, mock_get):

        options = {'type': 'test'}
        mock_get.return_value = {'data': [self.data]}
        response = self.api.listWebhookNotifications(options)

        self.assertTrue(response[0].token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_webhooks_success(self, mock_get):

        mock_get.return_value = {'data': [self.data]}
        response = self.api.listWebhookNotifications()

        self.assertTrue(response[0].token, self.data.get('token'))

    '''

    Upload Documents

    '''
    def test_uploadDocumentsForUser_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.uploadDocumentsForUser()

        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_uploadDocumentsForUser_success(self, mock_put):

        mock_put.return_value = self.data
        response = self.api.uploadDocumentsForUser('token', self.value)

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_uploadDocumentsForUserAndParse_success(self, mock_put):

        mock_put.return_value = self.uploadSuccessData
        response = self.api.uploadDocumentsForUser('token', self.value)

        self.assertEqual(response.token, self.uploadSuccessData.get('token'))
        self.assertEqual(response.documents[0].type, self.uploadSuccessData.get("documents")[0].type)

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_uploadDocumentsForUserAndParseRejection_success(self, mock_put):

        mock_put.return_value = self.uploadRejectionData
        response = self.api.uploadDocumentsForUser('token', self.value)

        # print(response.documents)
        # print(response.documents[0].reasons[0].name.name)

        self.assertEqual(response.token, self.uploadRejectionData.get('token'))
        self.assertEqual(response.documents[0].reasons[0].name.name, self.uploadRejectionData.get("documents")[0].reasons[0].name.name)
        self.assertEqual(response.documents[0].reasons[1].name.name, self.uploadRejectionData.get("documents")[0].reasons[1].name.name)
        self.assertEqual(response.documents[0].type, self.uploadRejectionData.get("documents")[0].type)

    '''

    Transfer Refunds

    '''

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_refunds_success(self, mock_post):

        mock_post.return_value = self.data
        response = self.api.createTransferRefund('token', self.data)
        self.assertTrue(response.token, self.data.get('token'))

    def test_create_transfer_refunds_fail_need_payment_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferRefund()

        self.assertEqual(exc.exception.message, 'transferToken is required')

    def test_create_transfer_refunds_fail_need_data(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferRefund('token')

        self.assertEqual(exc.exception.message, 'data is required')

    '''

    Transfer Spend Back Refunds

    '''

    def test_create_transfer_spend_back_refunds_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferSpendBackRefund()

        self.assertEqual(exc.exception.message, 'transferToken is required')

    def test_create_transfer_spend_back_refunds_fail_need_payment_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.createTransferSpendBackRefund('token')

        self.assertEqual(exc.exception.message, 'sourceToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_transfer_spend_back_refunds_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.createTransferSpendBackRefund('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    '''

        Create User Status Transition

    '''

    def test_create_user_status_transition_user_token(self):
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createUserStatusTransition()
        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_create_user_status_transition_data(self):
        with self.assertRaises(HyperwalletException) as exc:
            self.api.createUserStatusTransition('token')
        self.assertEqual(exc.exception.message, 'data is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_status_transition_success(self, mock_get):
        mock_get.return_value = self.data
        response = self.api.createUserStatusTransition('token', 'token')
        self.assertTrue(response.token, self.data.get('token'))

    def test_create_user_lockUser_status_transition_user_token(self):
        with self.assertRaises(HyperwalletException) as exc:
            self.api.lockUser()
        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_lockUser_status_transition_success(self, mock_get):
        mock_get.return_value = self.data
        response = self.api.lockUser('token')
        self.assertTrue(response.token, self.data.get('token'))

    def test_create_user_freezeUser_status_transition_user_token(self):
        with self.assertRaises(HyperwalletException) as exc:
            self.api.freezeUser()
        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_freezeUser_status_transition_success(self, mock_get):
        mock_get.return_value = self.data
        response = self.api.freezeUser('token')
        self.assertTrue(response.token, self.data.get('token'))

    def test_create_user_preactivate_status_transition_user_token(self):
        with self.assertRaises(HyperwalletException) as exc:
            self.api.preactivateUser()
        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_preactivate_status_transition_success(self, mock_get):
        mock_get.return_value = self.data
        response = self.api.preactivateUser('token')
        self.assertTrue(response.token, self.data.get('token'))

    def test_create_user_deactivate_status_transition_user_token(self):
        with self.assertRaises(HyperwalletException) as exc:
            self.api.deactivateUser()
        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_deactivate_status_transition_success(self, mock_get):
        mock_get.return_value = self.data
        response = self.api.deactivateUser('token')
        self.assertTrue(response.token, self.data.get('token'))

    def test_create_user_activate_status_transition_user_token(self):
        with self.assertRaises(HyperwalletException) as exc:
            self.api.activateUser()
        self.assertEqual(exc.exception.message, 'userToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_create_user_activate_status_transition_success(self, mock_get):
        mock_get.return_value = self.data
        response = self.api.activateUser('token')
        self.assertTrue(response.token, self.data.get('token'))

    '''

        Get Transfer Status Transition

    '''

    def test_get_transfer_status_transition_fail_need_transfer_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferStatusTransition()

        self.assertEqual(exc.exception.message, 'transferToken is required')

    def test_get_transfer_status_transition_fail_need_transition_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferStatusTransition('token')

        self.assertEqual(exc.exception.message, 'statusTransitionToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_transfer_status_transition_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getTransferStatusTransition('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    '''

        List Transfer Status Transition

    '''

    def test_list_transfer_status_transitions_fail_need_transfer_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransferStatusTransitions()

        self.assertEqual(exc.exception.message, 'transferToken is required')

    def test_list_transfer_status_transitions_fail_need_params_invalid(self):

        options = {'transition': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransferStatusTransitions('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_status_transitions_params_valid(self, mock_get):

        options = {'transition': 'SCHEDULED'}
        mock_get.return_value = self.data
        response = self.api.listTransferStatusTransitions('token', options)

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_status_transitions_success(self, mock_get):

        options = {'transition': 'SCHEDULED'}
        mock_get.return_value = self.data
        response = self.api.listTransferStatusTransitions('token', options)

        self.assertTrue(response.token, self.data.get('token'))

    '''

        Get Transfer Refunds

    '''

    def test_get_transfer_refund_fail_need_transfer_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferRefund()

        self.assertEqual(exc.exception.message, 'transferToken is required')

    def test_get_transfer_refund_fail_need_refund_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.getTransferRefund('token')

        self.assertEqual(exc.exception.message, 'refundToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_get_transfer_refund_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.getTransferRefund('token', 'token')

        self.assertTrue(response.token, self.data.get('token'))

    '''

        List Transfer Refunds

    '''

    def test_list_transfer_refunds_fail_need_transfer_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransferRefunds()

        self.assertEqual(exc.exception.message, 'transferToken is required')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_refunds_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.listTransferRefunds('token')

        self.assertTrue(response.token, self.data.get('token'))

    '''

        List Transfer Methods

    '''

    def test_list_transfer_methods_fail_need_user_token(self):

        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransferMethods()

        self.assertEqual(exc.exception.message, 'userToken is required')

    def test_list_transfer_methods_fail_need_params_invalid(self):

        options = {'type': 'test', 'token': 'test'}
        with self.assertRaises(HyperwalletException) as exc:
            self.api.listTransferMethods('token', options)

        self.assertEqual(exc.exception.message, 'Invalid filter')

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_methods_params_valid(self, mock_get):

        options = {'type': 'test'}
        mock_get.return_value = self.data
        response = self.api.listTransferMethods('token', options)

        self.assertTrue(response.token, self.data.get('token'))

    @mock.patch('hyperwallet.utils.ApiClient._makeRequest')
    def test_list_transfer_methods_success(self, mock_get):

        mock_get.return_value = self.data
        response = self.api.listTransferMethods('token')

        self.assertTrue(response.token, self.data.get('token'))


if __name__ == '__main__':
    unittest.main()
