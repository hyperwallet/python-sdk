#!/usr/bin/env python

import os

from config import SERVER
from exceptions import HyperwalletException
from utils import ApiClient


class Api(object):
    '''
    A Python interface for the Hyperwallet API.

    :param username: The username of this API user. **REQUIRED**
    :param password: The password of this API user. **REQUIRED**
    :param programToken:
        The token for the program this user is accessing. **REQUIRED**
    :param server: Your UAT or Production API URL if applicable.

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

    def _addProgramToken(self, data):
        '''
        Add the program token to the data object.

        :param data:
            A dictionary containing values defining a resource. **REQUIRED**
        :returns:
            A dictionary containing the provided values and the program token.
        '''

        if not isinstance(data, dict):
            raise HyperwalletException('data must be a dictionary object')

        if 'programToken' in data:
            return data

        data['programToken'] = self.programToken

        return data

    def listUsers(self,
                  params=None):
        '''
        List Users.

        :param params: A dictionary containing query parameters.
        :returns: The List Users API response.
        '''

        return self.apiClient.doGet('users', params)

    def createUser(self,
                   data=None):
        '''
        Create a User.

        :param data: A dictionary containing User information. **REQUIRED**
        :returns: The Create a User API response.
        '''

        if not data:
            raise HyperwalletException('data is required')

        self._addProgramToken(data)

        return self.apiClient.doPost('users', data)

    def retrieveUser(self,
                     userToken=None):
        '''
        Retrieve a User.

        :param userToken: A token identifying the User. **REQUIRED**
        :returns: The Retrieve a User API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        return self.apiClient.doGet(
            os.path.join('users', userToken)
        )

    def updateUser(self,
                   userToken=None,
                   data=None):
        '''
        Update a User.

        :param userToken: A token identifying the User. **REQUIRED**
        :param data: A dictionary containing User information. **REQUIRED**
        :returns: The Update a User API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPut(
            os.path.join('users', userToken),
            data
        )

    def listUserBalances(self,
                         userToken=None,
                         params=None):
        '''
        List User Balances.

        :param userToken: A token identifying the User. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The List User Balances API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        return self.apiClient.doGet(
            os.path.join('users', userToken, 'balances'),
            params
        )

    def listUserReceipts(self,
                         userToken=None,
                         params=None):
        '''
        List User Receipts.

        :param userToken: A token identifying the User. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The List User Receipts API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        return self.apiClient.doGet(
            os.path.join('users', userToken, 'receipts'),
            params
        )

    def listBankAccounts(self,
                         userToken=None,
                         params=None):
        '''
        List Bank Accounts.

        :param userToken: A token identifying the User. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The List Bank Accounts API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        return self.apiClient.doGet(
            os.path.join('users', userToken, 'bank-accounts'),
            params
        )

    def createBankAccount(self,
                          userToken=None,
                          data=None):
        '''
        Create a Bank Account.

        :param userToken: A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing Bank Account information. **REQUIRED**
        :returns: The Create a Bank Account API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPost(
            os.path.join('users', userToken, 'bank-accounts'),
            data
        )

    def retrieveBankAccount(self,
                            userToken=None,
                            bankAccountToken=None):
        '''
        Retrieve a Bank Account.

        :param userToken: A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :returns: The Retrieve a Bank Account API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankAccountToken:
            raise HyperwalletException('bankAccountToken is required')

        return self.apiClient.doGet(
            os.path.join('users', userToken, 'bank-accounts', bankAccountToken)
        )

    def updateBankAccount(self,
                          userToken=None,
                          bankAccountToken=None,
                          data=None):
        '''
        Update a Bank Account.

        :param userToken: A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :param data:
            A dictionary containing Bank Account information. **REQUIRED**
        :returns: The Update a Bank Account API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankAccountToken:
            raise HyperwalletException('bankAccountToken is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPut(
            os.path.join(
                'users',
                userToken,
                'bank-accounts',
                bankAccountToken
            ),
            data
        )

    def createBankAccountStatusTransition(self,
                                          userToken=None,
                                          bankAccountToken=None,
                                          data=None):
        '''
        Create a Bank Account Status Transition.

        :param userToken: A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :param data:
            A dictionary containing Bank Account Status Transition information.
            **REQUIRED**
        :returns: The Create a Bank Account Status Transition API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankAccountToken:
            raise HyperwalletException('bankAccountToken is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPost(
            os.path.join(
                'users',
                userToken,
                'bank-accounts',
                bankAccountToken,
                'status-transitions'
            ),
            data
        )

    def retrieveBankAccountStatusTransition(self,
                                            userToken=None,
                                            bankAccountToken=None,
                                            statusTransitionToken=None):
        '''
        Retrieve a Bank Account Status Transition.

        :param userToken: A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Bank Account Status Transition.
            **REQUIRED**
        :returns: The Retrieve a Bank Account Status Transition API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankAccountToken:
            raise HyperwalletException('bankAccountToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        return self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'bank-accounts',
                bankAccountToken,
                'status-transitions',
                statusTransitionToken
            )
        )

    def listPrepaidCards(self,
                         userToken=None,
                         params=None):
        '''
        List Prepaid Cards for User.

        :param userToken: A token identifying the User. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The List Prepaid Cards for User API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        return self.apiClient.doGet(
            os.path.join('users', userToken, 'prepaid-cards'),
            params
        )

    def createPrepaidCard(self,
                          userToken=None,
                          data=None):
        '''
        Create a Prepaid Card.

        :param userToken: A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing Prepaid Card information. **REQUIRED**
        :returns: The Create a Prepaid Card API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPost(
            os.path.join('users', userToken, 'prepaid-cards'),
            data
        )

    def retrievePrepaidCard(self,
                            userToken=None,
                            prepaidCardToken=None):
        '''
        Retrieve a Prepaid Card.

        :param userToken: A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :returns: The Retrieve a Prepaid Card API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        return self.apiClient.doGet(
            os.path.join('users', userToken, 'prepaid-cards', prepaidCardToken)
        )

    def listPrepaidCardStatusTransitions(self,
                                         userToken=None,
                                         prepaidCardToken=None):
        '''
        List Status Transitions for Prepaid Card.

        :param userToken: A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :returns: The List Status Transitions for Prepaid Card API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        return self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'status-transitions'
            )
        )

    def createPrepaidCardStatusTransition(self,
                                          userToken=None,
                                          prepaidCardToken=None,
                                          data=None):
        '''
        Create a Prepaid Card Status Transition.

        :param userToken: A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param data:
            A dictionary containing Prepaid Card Status Transition information.
            **REQUIRED**
        :returns: The Create a Prepaid Card Status Transition API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPost(
            os.path.join(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'status-transitions'
            ),
            data
        )

    def retrievePrepaidCardStatusTransition(self,
                                            userToken=None,
                                            prepaidCardToken=None,
                                            statusTransitionToken=None):
        '''
        Retrieve a Prepaid Card Status Transition.

        :param userToken: A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Prepaid Card Status Transition.
            **REQUIRED**
        :returns: The Retrieve a Prepaid Card Status Transition API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        return self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'status-transitions',
                statusTransitionToken
            )
        )

    def listPrepaidCardBalances(self,
                                userToken=None,
                                prepaidCardToken=None,
                                params=None):
        '''
        List Prepaid Card Balances.

        :param userToken: A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The List Prepaid Card Balances API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        return self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'balances'
            ),
            params
        )

    def listPrepaidCardReceipts(self,
                                userToken=None,
                                prepaidCardToken=None,
                                params=None):
        '''
        List Prepaid Card Receipts.

        :param userToken: A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The List Prepaid Card Receipts API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        return self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'receipts'
            ),
            params
        )

    def listPaperChecks(self,
                        userToken=None,
                        params=None):
        '''
        List Paper Checks.

        :param userToken: A token identifying the User. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The List Paper Checks API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        return self.apiClient.doGet(
            os.path.join('users', userToken, 'paper-checks'),
            params
        )

    def createPaperCheck(self,
                         userToken=None,
                         data=None):
        '''
        Create a Paper Check.

        :param userToken: A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing Paper Check information. **REQUIRED**
        :returns: The Create a Paper Check API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPost(
            os.path.join('users', userToken, 'paper-checks'),
            data
        )

    def retrievePaperCheck(self,
                           userToken=None,
                           paperCheckToken=None):
        '''
        Retrieve a Paper Check.

        :param userToken: A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :returns: The Retrieve a Paper Check API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not paperCheckToken:
            raise HyperwalletException('paperCheckToken is required')

        return self.apiClient.doGet(
            os.path.join('users', userToken, 'paper-checks', paperCheckToken)
        )

    def updatePaperCheck(self,
                         userToken=None,
                         paperCheckToken=None,
                         data=None):
        '''
        Update a Paper Check.

        :param userToken: A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :param data:
            A dictionary containing Paper Check information. **REQUIRED**
        :returns: The Update a Paper Check API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not paperCheckToken:
            raise HyperwalletException('paperCheckToken is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPut(
            os.path.join('users', userToken, 'paper-checks', paperCheckToken),
            data
        )

    def createPaperCheckStatusTransition(self,
                                         userToken=None,
                                         paperCheckToken=None,
                                         data=None):
        '''
        Create a Paper Check Status Transition.

        :param userToken: A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :param data:
            A dictionary containing Paper Check Status Transition information.
            **REQUIRED**
        :returns: The Create a Paper Check Status Transition API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not paperCheckToken:
            raise HyperwalletException('paperCheckToken is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPost(
            os.path.join(
                'users',
                userToken,
                'paper-checks',
                paperCheckToken,
                'status-transitions'
            ),
            data
        )

    def retrievePaperCheckStatusTransition(self,
                                           userToken=None,
                                           paperCheckToken=None,
                                           statusTransitionToken=None):
        '''
        Retrieve a Paper Check Status Transition.

        :param userToken: A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Paper Check Status Transition. **REQUIRED**
        :returns: The Retrieve a Paper Check Status Transition API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not paperCheckToken:
            raise HyperwalletException('paperCheckToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        return self.apiClient.doGet(
            os.path.join(
                'users',
                userToken,
                'paper-checks',
                paperCheckToken,
                'status-transitions',
                statusTransitionToken
            )
        )

    def listPayments(self,
                     params=None):
        '''
        List Payments.

        :param params: A dictionary containing query parameters.
        :returns: The List Payments API response.
        '''

        return self.apiClient.doGet('payments', params)

    def createPayment(self,
                      data=None):
        '''
        Create a Payment.

        :param data: A dictionary containing Payment information. **REQUIRED**
        :returns: The Create a Payment API response.
        '''

        if not data:
            raise HyperwalletException('data is required')

        self._addProgramToken(data)

        return self.apiClient.doPost('payments', data)

    def retrievePayment(self,
                        paymentToken=None):
        '''
        Retrieve a Payment.

        :param paymentToken: A token identifying the Payment. **REQUIRED**
        :returns: The Retrieve a Payment API response.
        '''

        if not paymentToken:
            raise HyperwalletException('paymentToken is required')

        return self.apiClient.doGet(os.path.join('payments', paymentToken))

    def retrieveAccount(self,
                        programToken=None,
                        accountToken=None):
        '''
        Retrieve an Account.

        :param programToken: A token identifying the Program. **REQUIRED**
        :param accountToken: A token identifying the Account. **REQUIRED**
        :returns: The Retrieve an Account API response.
        '''

        if not programToken:
            raise HyperwalletException('programToken is required')

        if not accountToken:
            raise HyperwalletException('accountToken is required')

        return self.apiClient.doGet(
            os.path.join('programs', programToken, 'accounts', accountToken)
        )

    def listAccountBalances(self,
                            programToken=None,
                            accountToken=None,
                            params=None):
        '''
        List Account Balances.

        :param programToken: A token identifying the Program. **REQUIRED**
        :param accountToken: A token identifying the Account. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The List Account Balances API response.
        '''

        if not programToken:
            raise HyperwalletException('programToken is required')

        if not accountToken:
            raise HyperwalletException('accountToken is required')

        return self.apiClient.doGet(
            os.path.join(
                'programs',
                programToken,
                'accounts',
                accountToken,
                'balances'
            ),
            params
        )

    def listAccountReceipts(self,
                            programToken=None,
                            accountToken=None,
                            params=None):
        '''
        List Account Receipts.

        :param programToken: A token identifying the Program. **REQUIRED**
        :param accountToken: A token identifying the Account. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The List Account Receipts API response.
        '''

        if not programToken:
            raise HyperwalletException('programToken is required')

        if not accountToken:
            raise HyperwalletException('accountToken is required')

        return self.apiClient.doGet(
            os.path.join(
                'programs',
                programToken,
                'accounts',
                accountToken,
                'receipts'
            ),
            params
        )

    def retrieveProgram(self,
                        programToken=None):
        '''
        Retrieve a Program.

        :param programToken: A token identifying the Program. **REQUIRED**
        :returns: The Retrieve a Program API response.
        '''

        if not programToken:
            raise HyperwalletException('programToken is required')

        return self.apiClient.doGet(os.path.join('programs', programToken))

    def listTransferMethodConfigurations(self,
                                         params={}):
        '''
        List Transfer Method Configurations.

        :param params: A dictionary containing query parameters. **REQUIRED**
        :returns: The List Transfer Method Configurations API response.

        .. warning::
            **userToken** must be present in the params dictionary.
        '''

        if 'userToken' not in params:
            raise HyperwalletException('userToken is required')

        return self.apiClient.doGet('transfer-method-configurations', params)

    def retrieveTransferMethodConfiguration(self,
                                            params={}):
        '''
        Retrieve a Transfer Method Configuration.

        :param params: A dictionary containing query parameters. **REQUIRED**
        :returns: The Retrieve a Transfer Method Configuration API response.

        .. warning::
            **userToken** must be present in the params dictionary.

        .. warning::
            **country** must be present in the params dictionary.

        .. warning::
            **currency** must be present in the params dictionary.

        .. warning::
            **type** must be present in the params dictionary.

        .. warning::
            **profileType** must be present in the params dictionary.
        '''

        if 'userToken' not in params:
            raise HyperwalletException('userToken is required')

        if 'country' not in params:
            raise HyperwalletException('country is required')

        if 'currency' not in params:
            raise HyperwalletException('currency is required')

        if 'type' not in params:
            raise HyperwalletException('type is required')

        if 'profileType' not in params:
            raise HyperwalletException('profileType is required')

        return self.apiClient.doGet('transfer-method-configurations', params)

    def createTransferMethod(self,
                             userToken=None,
                             cacheToken=None,
                             data=None):
        '''
        Create a Transfer Method.

        :param userToken: A token identifying the User. **REQUIRED**
        :param cacheToken:
            A cache token identifying the Transfer Method. **REQUIRED**
        :param data: A dictionary containing Field Restriction information.
        :returns: The Create a Transfer Method API response.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not cacheToken:
            raise HyperwalletException('cacheToken is required')

        headers = {'Json-Cache-Token': cacheToken}

        return self.apiClient.doPost(
            os.path.join('users', userToken, 'transfer-methods'),
            data,
            headers
        )
