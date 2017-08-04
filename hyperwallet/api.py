#!/usr/bin/env python

import os

from config import SERVER
from exceptions import HyperwalletException
from utils import ApiClient

from hyperwallet import (
    User,
    BankAccount,
    BankCard,
    PrepaidCard,
    PaperCheck,
    Payment,
    Balance,
    Program,
    Account,
    Webhook
)


class Api(object):
    '''
    A Python interface for the Hyperwallet API.

    :param username:
        The username of this API user. **REQUIRED**
    :param password:
        The password of this API user. **REQUIRED**
    :param programToken:
        The token for the program this user is accessing. **REQUIRED**
    :param server:
        Your UAT or Production API URL if applicable.

    .. note::
        **server** defaults to the Hyperwallet Sandbox URL if not provided.

    '''

    def __init__(self,
                 username=None,
                 password=None,
                 programToken=None,
                 server=SERVER):
        '''
        Create an instance of the API interface.
        This is the main interface the user will call to interact with the API.
        '''

        if not username:
            raise HyperwalletException('username is required')

        if not password:
            raise HyperwalletException('password is required')

        if not programToken:
            raise HyperwalletException('programToken is required')

        self.username = username
        self.password = password
        self.programToken = programToken
        self.server = server

        self.apiClient = ApiClient(self.username, self.password, self.server)

    '''

    USERS
    https://portal.hyperwallet.com/docs/api/v3/resources/users

    '''

    def listUsers(self,
                  params=None):
        '''
        List Users.

        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Users.
        '''

        response = self.apiClient.doGet('users', params)

        return [User(x) for x in response.get('data', [])]

    def createUser(self,
                   data=None):
        '''
        Create a User.

        :param data:
            A dictionary containing User information. **REQUIRED**
        :returns:
            A User.
        '''

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost('users', data)

        return User(response)

    def retrieveUser(self,
                     userToken=None):
        '''
        Retrieve a User.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :returns:
            A User.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        response = self.apiClient.doGet(
            os.path.join('users', userToken)
        )

        return User(response)

    def updateUser(self,
                   userToken=None,
                   data=None):
        '''
        Update a User.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing User information. **REQUIRED**
        :returns:
            A User.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPut(
            os.path.join('users', userToken),
            data
        )

        return User(response)

    '''

    BANK ACCOUNTS
    https://portal.hyperwallet.com/docs/api/v3/resources/bank-accounts

    '''

    def listBankAccounts(self,
                         userToken=None,
                         params=None):
        '''
        List Bank Accounts.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Bank Accounts.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        response = self.apiClient.doGet(
            os.path.join('users', userToken, 'bank-accounts'),
            params
        )

        return [BankAccount(x) for x in response.get('data', [])]

    def createBankAccount(self,
                          userToken=None,
                          data=None):
        '''
        Create a Bank Account.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing Bank Account information. **REQUIRED**
        :returns:
            A Bank Account.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            os.path.join('users', userToken, 'bank-accounts'),
            data
        )

        return BankAccount(response)

    def retrieveBankAccount(self,
                            userToken=None,
                            bankAccountToken=None):
        '''
        Retrieve a Bank Account.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :returns:
            A Bank Account.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankAccountToken:
            raise HyperwalletException('bankAccountToken is required')

        response = self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'bank-accounts',
                bankAccountToken
            )
        )

        return BankAccount(response)

    def updateBankAccount(self,
                          userToken=None,
                          bankAccountToken=None,
                          data=None):
        '''
        Update a Bank Account.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :param data:
            A dictionary containing Bank Account information. **REQUIRED**
        :returns:
            A Bank Account.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankAccountToken:
            raise HyperwalletException('bankAccountToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPut(
            os.path.join(
                'users',
                userToken,
                'bank-accounts',
                bankAccountToken
            ),
            data
        )

        return BankAccount(response)

    '''

    BANK CARDS
    https://portal.hyperwallet.com/docs/api/v3/resources/bank-cards

    '''

    def listBankCards(self,
                      userToken=None,
                      params=None):
        '''
        List Bank Cards.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Bank Cards.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        response = self.apiClient.doGet(
            os.path.join('users', userToken, 'bank-cards'),
            params
        )

        return [BankCard(x) for x in response.get('data', [])]

    def createBankCard(self,
                       userToken=None,
                       data=None):
        '''
        Create a Bank Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing Bank Card information. **REQUIRED**
        :returns:
            A Bank Card.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            os.path.join('users', userToken, 'bank-cards'),
            data
        )

        return BankCard(response)

    def retrieveBankCard(self,
                         userToken=None,
                         bankCardToken=None):
        '''
        Retrieve a Bank Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankCardToken:
            A token identifying the Bank Card. **REQUIRED**
        :returns:
            A Bank Card.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankCardToken:
            raise HyperwalletException('bankCardToken is required')

        response = self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'bank-cards',
                bankCardToken
            )
        )

        return BankCard(response)

    def updateBankCard(self,
                       userToken=None,
                       bankCardToken=None,
                       data=None):
        '''
        Update a Bank Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankCardToken:
            A token identifying the Bank Card. **REQUIRED**
        :param data:
            A dictionary containing Bank Card information. **REQUIRED**
        :returns:
            A Bank Card.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankCardToken:
            raise HyperwalletException('bankCardToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPut(
            os.path.join(
                'users',
                userToken,
                'bank-cards',
                bankCardToken
            ),
            data
        )

        return BankCard(response)

    '''

    PREPAID CARDS
    https://portal.hyperwallet.com/docs/api/v3/resources/prepaid-cards

    '''

    def listPrepaidCards(self,
                         userToken=None,
                         params=None):
        '''
        List Prepaid Cards.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Prepaid Cards.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        response = self.apiClient.doGet(
            os.path.join('users', userToken, 'prepaid-cards'),
            params
        )

        return [PrepaidCard(x) for x in response.get('data', [])]

    def createPrepaidCard(self,
                          userToken=None,
                          data=None):
        '''
        Create a Prepaid Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing Prepaid Card information. **REQUIRED**
        :returns:
            A Prepaid Card.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            os.path.join('users', userToken, 'prepaid-cards'),
            data
        )

        return PrepaidCard(response)

    def retrievePrepaidCard(self,
                            userToken=None,
                            prepaidCardToken=None):
        '''
        Retrieve a Prepaid Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :returns:
            A Prepaid Card.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        response = self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken
            )
        )

        return PrepaidCard(response)

    '''

    PAPER CHECKS
    https://portal.hyperwallet.com/docs/api/v3/resources/paper-checks

    '''

    def listPaperChecks(self,
                        userToken=None,
                        params=None):
        '''
        List Paper Checks.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Paper Checks.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        response = self.apiClient.doGet(
            os.path.join('users', userToken, 'paper-checks'),
            params
        )

        return [PaperCheck(x) for x in response.get('data', [])]

    def createPaperCheck(self,
                         userToken=None,
                         data=None):
        '''
        Create a Paper Check.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing Paper Check information. **REQUIRED**
        :returns:
            A Paper Check.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            os.path.join('users', userToken, 'paper-checks'),
            data
        )

        return PaperCheck(response)

    def retrievePaperCheck(self,
                           userToken=None,
                           paperCheckToken=None):
        '''
        Retrieve a Paper Check.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :returns:
            A Paper Check.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not paperCheckToken:
            raise HyperwalletException('paperCheckToken is required')

        response = self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'paper-checks',
                paperCheckToken
            )
        )

        return PaperCheck(response)

    def updatePaperCheck(self,
                         userToken=None,
                         paperCheckToken=None,
                         data=None):
        '''
        Update a Paper Check.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :param data:
            A dictionary containing Paper Check information. **REQUIRED**
        :returns:
            A Paper Check.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not paperCheckToken:
            raise HyperwalletException('paperCheckToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPut(
            os.path.join(
                'users',
                userToken,
                'paper-checks',
                paperCheckToken
            ),
            data
        )

        return PaperCheck(response)

    '''

    PAYMENTS
    https://portal.hyperwallet.com/docs/api/v3/resources/payments

    '''

    def listPayments(self,
                     params=None):
        '''
        List Payments.

        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Payments.
        '''

        response = self.apiClient.doGet('payments', params)

        return [Payment(x) for x in response.get('data', [])]

    def createPayment(self,
                      data=None):
        '''
        Create a Payment.

        :param data:
            A dictionary containing Payment information. **REQUIRED**
        :returns:
            A Payment.
        '''

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost('payments', data)

        return Payment(response)

    def retrievePayment(self,
                        paymentToken=None):
        '''
        Retrieve a Payment.

        :param paymentToken:
            A token identifying the Payment. **REQUIRED**
        :returns:
            A Payment.
        '''

        if not paymentToken:
            raise HyperwalletException('paymentToken is required')

        response = self.apiClient.doGet(
            os.path.join('payments', paymentToken)
        )

        return Payment(response)

    '''

    BALANCES
    https://portal.hyperwallet.com/docs/api/v3/resources/balances

    '''

    def listUserBalances(self,
                         userToken=None,
                         params=None):
        '''
        List User Balances.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Balances.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        response = self.apiClient.doGet(
            os.path.join('users', userToken, 'balances'),
            params
        )

        return [Balance(x) for x in response.get('data', [])]

    def listPrepaidCardBalances(self,
                                userToken=None,
                                prepaidCardToken=None,
                                params=None):
        '''
        List Prepaid Card Balances.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Balances.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        response = self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'balances'
            ),
            params
        )

        return [Balance(x) for x in response.get('data', [])]

    def listAccountBalances(self,
                            programToken=None,
                            accountToken=None,
                            params=None):
        '''
        List Account Balances.

        :param programToken:
            A token identifying the Program. **REQUIRED**
        :param accountToken:
            A token identifying the Account. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Balances.
        '''

        if not programToken:
            raise HyperwalletException('programToken is required')

        if not accountToken:
            raise HyperwalletException('accountToken is required')

        response = self.apiClient.doGet(
            os.path.join(
                'programs',
                programToken,
                'accounts',
                accountToken,
                'balances'
            ),
            params
        )

        return [Balance(x) for x in response.get('data', [])]

    '''

    PROGRAMS
    https://portal.hyperwallet.com/docs/api/v3/resources/programs

    '''

    def retrieveProgram(self,
                        programToken=None):
        '''
        Retrieve a Program.

        :param programToken:
            A token identifying the Program. **REQUIRED**
        :returns:
            A Program.
        '''

        if not programToken:
            raise HyperwalletException('programToken is required')

        response = self.apiClient.doGet(
            os.path.join('programs', programToken)
        )

        return Program(response)

    '''

    ACCOUNTS
    https://portal.hyperwallet.com/docs/api/v3/resources/accounts

    '''

    def retrieveAccount(self,
                        programToken=None,
                        accountToken=None):
        '''
        Retrieve an Account.

        :param programToken:
            A token identifying the Program. **REQUIRED**
        :param accountToken:
            A token identifying the Account. **REQUIRED**
        :returns:
            An Account.
        '''

        if not programToken:
            raise HyperwalletException('programToken is required')

        if not accountToken:
            raise HyperwalletException('accountToken is required')

        response = self.apiClient.doGet(
            os.path.join(
                'programs',
                programToken,
                'accounts',
                accountToken
            )
        )

        return Account(response)

    '''

    WEBHOOK NOTIFICATIONS
    https://portal.hyperwallet.com/docs/api/v3/resources/webhook-notifications

    '''

    def listWebhooks(self,
                     params=None):
        '''
        List Webhook Notifications.

        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Webhooks.
        '''

        response = self.apiClient.doGet('webhook-notifications', params)

        return [Webhook(x) for x in response.get('data', [])]

    def retrieveWebhook(self,
                        webhookToken=None):
        '''
        Retrieve a Webhook Notification.

        :param webhookToken:
            A token identifying the Webhook. **REQUIRED**
        :returns:
            A Webhook.
        '''

        if not webhookToken:
            raise HyperwalletException('webhookToken is required')

        response = self.apiClient.doGet(
            os.path.join('webhook-notifications', webhookToken)
        )

        return Webhook(response)
