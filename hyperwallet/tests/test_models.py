#!/usr/bin/env python

import json
import unittest

from hyperwallet import (
    HyperwalletModel,
    User,
    TransferMethod,
    BankAccount,
    BankCard,
    PrepaidCard,
    PaperCheck,
    Transfer,
    PayPalAccount,
    Payment,
    Balance,
    Receipt,
    Program,
    Account,
    StatusTransition,
    TransferMethodConfiguration,
    Webhook
)


class ModelTest(unittest.TestCase):

    def setUp(self):

        self.simple_data = {
            'key': 'value',
            'dict': {
                'key': 'value'
            },
            'list': [
                'item',
                'value',
                {
                    'key': 'value'
                }
            ]
        }

        self.hyperwallet_data = {
            "token": "usr-00000000-0000-0000-0000-000000000000",
            "status": "PRE_ACTIVATED",
            "createdOn": "2017-01-01T00:00:00",
            "clientUserId": "1234567890",
            "profileType": "INDIVIDUAL",
            "firstName": "Hyperwallet",
            "lastName": "User",
            "dateOfBirth": "1990-01-01",
            "addressLine1": "575 Market Street",
            "city": "San Francisco",
            "stateProvince": "CA",
            "country": "US",
            "postalCode": "94105",
            "language": "en",
            "programToken": "prg-00000000-0000-0000-0000-000000000000",
            "links": [
                {
                    "params": {
                        "rel": "self"
                    },
                    "href": "https://api.paylution.com/rest/v3/users/usr-00000000-0000-0000-0000-000000000000"
                }
            ]
        }

        self.user_data = {
            'token': 'usr-12345',
            'createdOn': '2017-01-01'
        }

        self.transfer_method_data = {
            'token': 'trm-12345',
            'createdOn': '2017-01-01'
        }

        self.receipt_data = {
            'entry': 'DEBIT',
            'amount': '10',
            'details': {
                'clientPaymentId': '12345'
            }
        }

    '''

    Hyperwallet Model

    '''

    def test_hyperwallet_model_simple_data(self):

        test_hyperwallet = HyperwalletModel(self.simple_data)

        self.assertEqual(
            json.dumps(
                self.simple_data,
                sort_keys=True,
                separators=(',', ':'),
                indent=4
            ),
            test_hyperwallet.__str__()
        )

    def test_hyperwallet_model_hyperwallet_data(self):

        test_hyperwallet = HyperwalletModel(self.hyperwallet_data)

        self.assertEqual(
            json.dumps(self.hyperwallet_data, sort_keys=True),
            json.dumps(test_hyperwallet.asDict(), sort_keys=True)
        )

    '''

    User

    '''

    def test_user_model(self):

        test_user = User(self.user_data)

        self.assertEqual(
            test_user.__repr__(),
            'User({date}, {token})'.format(
                date=self.user_data.get('createdOn'),
                token=self.user_data.get('token')
            )
        )

    '''

    Transfer Method

    '''

    def test_transfer_method_model(self):

        test_transfer_method = TransferMethod(self.transfer_method_data)

        self.assertEqual(
            test_transfer_method.__repr__(),
            'TransferMethod({date}, {token})'.format(
                date=self.transfer_method_data.get('createdOn'),
                token=self.transfer_method_data.get('token')
            )
        )

    '''

    Bank Account

    '''

    def test_bank_account_model(self):

        test_bank_account = BankAccount(self.transfer_method_data)

        self.assertEqual(
            test_bank_account.__repr__(),
            'BankAccount({date}, {token})'.format(
                date=self.transfer_method_data.get('createdOn'),
                token=self.transfer_method_data.get('token')
            )
        )

    '''

    Bank Card

    '''

    def test_bank_card_model(self):

        test_bank_card = BankCard(self.transfer_method_data)

        self.assertEqual(
            test_bank_card.__repr__(),
            'BankCard({date}, {token})'.format(
                date=self.transfer_method_data.get('createdOn'),
                token=self.transfer_method_data.get('token')
            )
        )

    '''

    Prepaid Card

    '''

    def test_prepaid_card_model(self):

        test_prepaid_card = PrepaidCard(self.transfer_method_data)

        self.assertEqual(
            test_prepaid_card.__repr__(),
            'PrepaidCard({date}, {token})'.format(
                date=self.transfer_method_data.get('createdOn'),
                token=self.transfer_method_data.get('token')
            )
        )

    '''

    Paper Check

    '''

    def test_paper_check_model(self):

        test_paper_check = PaperCheck(self.transfer_method_data)

        self.assertEqual(
            test_paper_check.__repr__(),
            'PaperCheck({date}, {token})'.format(
                date=self.transfer_method_data.get('createdOn'),
                token=self.transfer_method_data.get('token')
            )
        )

    '''

    Transfer

    '''

    def test_transfer_model(self):

        test_transfer = Transfer(self.transfer_method_data)

        self.assertEqual(
            test_transfer.__repr__(),
            'Transfer({date}, {token})'.format(
                date=self.transfer_method_data.get('createdOn'),
                token=self.transfer_method_data.get('token')
            )
        )

    '''

    PayPal Account

    '''

    def test_paypal_account_model(self):

        test_paypal_account = PayPalAccount(self.transfer_method_data)

        self.assertEqual(
            test_paypal_account.__repr__(),
            'PayPalAccount({date}, {token})'.format(
                date=self.transfer_method_data.get('createdOn'),
                token=self.transfer_method_data.get('token')
            )
        )

    '''

    Payment

    '''

    def test_payment_model(self):

        payment_data = {
            'token': 'pmt-12345',
            'createdOn': '2017-01-01'
        }

        test_payment = Payment(payment_data)

        self.assertEqual(
            test_payment.__repr__(),
            'Payment({date}, {token})'.format(
                date=payment_data.get('createdOn'),
                token=payment_data.get('token')
            )
        )

    '''

    Balance

    '''

    def test_balance_model(self):

        balance_data = {
            'currency': 'USD',
            'amount': '10'
        }

        test_balance = Balance(balance_data)

        self.assertEqual(
            test_balance.__repr__(),
            'Balance({currency}, {amount})'.format(
                currency=balance_data.get('currency'),
                amount=balance_data.get('amount')
            )
        )

    '''

    Receipt

    '''

    def test_receipt_model(self):

        test_receipt = Receipt(self.receipt_data)

        self.assertEqual(
            test_receipt.__repr__(),
            'Receipt({entry}, {amount})'.format(
                entry=self.receipt_data.get('entry'),
                amount=self.receipt_data.get('amount')
            )
        )

    '''

    Program

    '''

    def test_program_model(self):

        program_data = {
            'token': 'prg-12345',
            'createdOn': '2017-01-01'
        }

        test_program = Program(program_data)

        self.assertEqual(
            test_program.__repr__(),
            'Program({date}, {token})'.format(
                date=program_data.get('createdOn'),
                token=program_data.get('token')
            )
        )

    '''

    Account

    '''

    def test_account_model(self):

        account_data = {
            'token': 'act-12345',
            'createdOn': '2017-01-01'
        }

        test_account = Account(account_data)

        self.assertEqual(
            test_account.__repr__(),
            'Account({date}, {token})'.format(
                date=account_data.get('createdOn'),
                token=account_data.get('token')
            )
        )

    '''

    Status Transition

    '''

    def test_status_transition_model(self):

        status_transition_data = {
            'token': 'sts-12345',
            'createdOn': '2017-01-01'
        }

        test_status_transition = StatusTransition(status_transition_data)

        self.assertEqual(
            test_status_transition.__repr__(),
            'StatusTransition({date}, {token})'.format(
                date=status_transition_data.get('createdOn'),
                token=status_transition_data.get('token')
            )
        )

    '''

    Transfer Method Configuration

    '''

    def test_transfer_method_configuration_model(self):

        transfer_method_configuration_data = {
            'countries': ['US'],
            'type': 'BANK_ACCOUNT'
        }

        test_transfer_method_configuration = TransferMethodConfiguration(
            transfer_method_configuration_data
        )

        print(transfer_method_configuration_data.get('countries'))
        self.assertEqual(
            test_transfer_method_configuration.__repr__(),
            'TransferMethodConfiguration({country}, {type})'.format(
                country=transfer_method_configuration_data.get('countries')[0],
                type=transfer_method_configuration_data.get('type')
            )
        )

    '''

    Webhook

    '''

    def test_webhook_model(self):

        webhook_data = {
            'token': 'wbh-12345',
            'createdOn': '2017-01-01',
            'type': 'USERS.CREATED',
            'object': self.user_data
        }

        test_webhook = Webhook(webhook_data)

        self.assertEqual(
            test_webhook.__repr__(),
            'Webhook({date}, {token})'.format(
                date=webhook_data.get('createdOn'),
                token=webhook_data.get('token')
            )
        )

    def test_webhook_model_good_sub_type(self):

        webhook_data = {
            'token': 'wbh-12345',
            'createdOn': '2017-01-01',
            'type': 'USER.BANK_ACCOUNTS.CREATED',
            'object': self.transfer_method_data
        }

        test_webhook = Webhook(webhook_data)

        self.assertEqual(
            test_webhook.object.__repr__(),
            'BankAccount({date}, {token})'.format(
                date=self.transfer_method_data.get('createdOn'),
                token=self.transfer_method_data.get('token')
            )
        )

    def test_webhook_model_bad_object(self):

        webhook_data = {
            'token': 'wbh-12345',
            'createdOn': '2017-01-01',
            'type': 'USERS.CREATED',
            'object': 'hi'
        }

        test_webhook = Webhook(webhook_data)

        self.assertEqual(test_webhook.object, webhook_data.get('object'))

    def test_webhook_model_bad_type(self):

        webhook_data = {
            'token': 'wbh-12345',
            'createdOn': '2017-01-01',
            'type': 'USER.PAYMENT',
            'object': self.user_data
        }

        test_webhook = Webhook(webhook_data)

        self.assertEqual(test_webhook.object, webhook_data.get('object'))


if __name__ == '__main__':
    unittest.main()
