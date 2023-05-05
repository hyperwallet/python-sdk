#!/usr/bin/env python

from .config import SERVER
from .exceptions import HyperwalletException
from .utils import ApiClient

from hyperwallet import (
    User,
    TransferMethod,
    BankAccount,
    BankCard,
    PrepaidCard,
    PaperCheck,
    Transfer,
    AuthenticationToken,
    PayPalAccount,
    VenmoAccount,
    Payment,
    Balance,
    Receipt,
    Program,
    Account,
    StatusTransition,
    TransferMethodConfiguration,
    Webhook,
    TransferRefunds,
    HyperwalletVerificationDocument,
    HyperwalletVerificationDocumentReason,
    RejectReason
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
    :param encryptionData:
        Dictionary with params for encrypted requests (keys: clientPrivateKeySetLocation, hyperwalletKeySetLocation, etc).

    .. note::
        **server** defaults to the Hyperwallet Sandbox URL if not provided.

    '''

    def __init__(self,
                 username=None,
                 password=None,
                 programToken=None,
                 server=SERVER,
                 encryptionData=None):
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

        self.apiClient = ApiClient(self.username, self.password, self.server, encryptionData)

    '''

    Users
    https://portal.hyperwallet.com/docs/api/v3/resources/users

    '''

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

    def getUser(self,
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
            self.__buildUrl('users', userToken)
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
            self.__buildUrl('users', userToken),
            data
        )

        return User(response)

    def listUsers(self,
                  params=None):
        '''
        List Users.

        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Users.
        '''

        if params and not set(list(params)).issubset(User.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet('users', params)

        return [User(x) for x in response.get('data', [])]

    def getUserStatusTransition(self,
                                userToken=None,
                                statusTransitionToken=None):
        '''
        Retrieve a User Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the User Status Transition. **REQUIRED**
        :returns:
            A User Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'status-transitions',
                statusTransitionToken
            )
        )

        return StatusTransition(response)

    def listUserStatusTransitions(self,
                                  userToken=None,
                                  params=None):
        '''
        List User Status Transitions.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of User Status Transitions.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if params and not set(list(params)).issubset(StatusTransition.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'status-transitions'
            ),
            params
        )

        return [StatusTransition(x) for x in response.get('data', [])]

    '''

    Bank Accounts
    https://portal.hyperwallet.com/docs/api/v3/resources/bank-accounts

    '''

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
            self.__buildUrl('users', userToken, 'bank-accounts'),
            data
        )

        return BankAccount(response)

    def getBankAccount(self,
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
            self.__buildUrl(
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

        body = self.__updateTransferMethod(userToken, bankAccountToken, 'bank-accounts', data)
        return BankAccount(body)

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

        if params and not set(list(params)).issubset(BankAccount.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl('users', userToken, 'bank-accounts'),
            params
        )

        return [BankAccount(x) for x in response.get('data', [])]

    def createBankAccountStatusTransition(self,
                                          userToken=None,
                                          bankAccountToken=None,
                                          data=None):
        '''
        Create a Bank Account Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :param data:
            A dictionary containing Bank Account Status Transition information. **REQUIRED**
        :returns:
            A Bank Account Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankAccountToken:
            raise HyperwalletException('bankAccountToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            self.__buildUrl(
                'users',
                userToken,
                'bank-accounts',
                bankAccountToken,
                'status-transitions'
            ),
            data
        )

        return StatusTransition(response)

    def getBankAccountStatusTransition(self,
                                       userToken=None,
                                       bankAccountToken=None,
                                       statusTransitionToken=None):
        '''
        Retrieve a Bank Account Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Bank Account Status Transition. **REQUIRED**
        :returns:
            A Bank Account Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankAccountToken:
            raise HyperwalletException('bankAccountToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'bank-accounts',
                bankAccountToken,
                'status-transitions',
                statusTransitionToken
            )
        )

        return StatusTransition(response)

    def listBankAccountStatusTransitions(self,
                                         userToken=None,
                                         bankAccountToken=None,
                                         params=None):
        '''
        List Bank Account Status Transitions.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Bank Account Status Transitions.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankAccountToken:
            raise HyperwalletException('bankAccountToken is required')

        if params and not set(list(params)).issubset(StatusTransition.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'bank-accounts',
                bankAccountToken,
                'status-transitions'
            ),
            params
        )

        return [StatusTransition(x) for x in response.get('data', [])]

    def deactivateBankAccount(self,
                              userToken=None,
                              bankAccountToken=None,
                              notes=None):
        '''
        Deactivate a Bank Account.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankAccountToken:
            A token identifying the Bank Account. **REQUIRED**
        :param notes:
            A string describing the deactivation.
        :returns:
            A Bank Account Status Transition.
        '''

        data = {
            'transition': 'DE_ACTIVATED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createBankAccountStatusTransition(
            userToken,
            bankAccountToken,
            data
        )

    '''

    Bank Cards
    https://portal.hyperwallet.com/docs/api/v3/resources/bank-cards

    '''

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
            self.__buildUrl('users', userToken, 'bank-cards'),
            data
        )

        return BankCard(response)

    def getBankCard(self,
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
            self.__buildUrl(
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

        body = self.__updateTransferMethod(userToken, bankCardToken, 'bank-cards', data)
        return BankCard(body)

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

        if params and not set(list(params)).issubset(BankCard.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl('users', userToken, 'bank-cards'),
            params
        )

        return [BankCard(x) for x in response.get('data', [])]

    def createBankCardStatusTransition(self,
                                       userToken=None,
                                       bankCardToken=None,
                                       data=None):
        '''
        Create a Bank Card Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankCardToken:
            A token identifying the Bank Card. **REQUIRED**
        :param data:
            A dictionary containing Bank Card Status Transition information. **REQUIRED**
        :returns:
            A Bank Card Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankCardToken:
            raise HyperwalletException('bankCardToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            self.__buildUrl(
                'users',
                userToken,
                'bank-cards',
                bankCardToken,
                'status-transitions'
            ),
            data
        )

        return StatusTransition(response)

    def getBankCardStatusTransition(self,
                                    userToken=None,
                                    bankCardToken=None,
                                    statusTransitionToken=None):
        '''
        Retrieve a Bank Card Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankCardToken:
            A token identifying the Bank Card. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Bank Card Status Transition. **REQUIRED**
        :returns:
            A Bank Card Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankCardToken:
            raise HyperwalletException('bankCardToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'bank-cards',
                bankCardToken,
                'status-transitions',
                statusTransitionToken
            )
        )

        return StatusTransition(response)

    def listBankCardStatusTransitions(self,
                                      userToken=None,
                                      bankCardToken=None,
                                      params=None):
        '''
        List Bank Card Status Transitions.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankCardToken:
            A token identifying the Bank Card. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Bank Card Status Transitions.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not bankCardToken:
            raise HyperwalletException('bankCardToken is required')

        if params and not set(list(params)).issubset(StatusTransition.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'bank-cards',
                bankCardToken,
                'status-transitions'
            ),
            params
        )

        return [StatusTransition(x) for x in response.get('data', [])]

    def deactivateBankCard(self,
                           userToken=None,
                           bankCardToken=None,
                           notes=None):
        '''
        Deactivate a Bank Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param bankCardToken:
            A token identifying the Bank Card. **REQUIRED**
        :param notes:
            A string describing the deactivation.
        :returns:
            A Bank Card Status Transition.
        '''

        data = {
            'transition': 'DE_ACTIVATED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createBankCardStatusTransition(
            userToken,
            bankCardToken,
            data
        )

    '''

    Prepaid Cards
    https://portal.hyperwallet.com/docs/api/v3/resources/prepaid-cards

    '''

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
            self.__buildUrl('users', userToken, 'prepaid-cards'),
            data
        )

        return PrepaidCard(response)

    def updatePrepaidCard(self,
                          userToken=None,
                          prepaidCardToken=None,
                          data=None):
        '''
        Update a Prepaid Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param data:
            A dictionary containing Prepaid Card information. **REQUIRED**
        :returns:
            A Prepaid Card.
        '''

        body = self.__updateTransferMethod(userToken, prepaidCardToken, 'prepaid-cards', data)
        return PrepaidCard(body)

    def getPrepaidCard(self,
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
            self.__buildUrl(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken
            )
        )

        return PrepaidCard(response)

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

        if params and not set(list(params)).issubset(PrepaidCard.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl('users', userToken, 'prepaid-cards'),
            params
        )

        return [PrepaidCard(x) for x in response.get('data', [])]

    def createPrepaidCardStatusTransition(self,
                                          userToken=None,
                                          prepaidCardToken=None,
                                          data=None):
        '''
        Create a Prepaid Card Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param data:
            A dictionary containing Prepaid Card Status Transition information. **REQUIRED**
        :returns:
            A Prepaid Card Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            self.__buildUrl(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'status-transitions'
            ),
            data
        )

        return StatusTransition(response)

    def getPrepaidCardStatusTransition(self,
                                       userToken=None,
                                       prepaidCardToken=None,
                                       statusTransitionToken=None):
        '''
        Retrieve a Prepaid Card Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Prepaid Card Status Transition. **REQUIRED**
        :returns:
            A Prepaid Card Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'status-transitions',
                statusTransitionToken
            )
        )

        return StatusTransition(response)

    def listPrepaidCardStatusTransitions(self,
                                         userToken=None,
                                         prepaidCardToken=None,
                                         params=None):
        '''
        List Prepaid Card Status Transitions.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Prepaid Card Status Transitions.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        if params and not set(list(params)).issubset(StatusTransition.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'status-transitions'
            ),
            params
        )

        return [StatusTransition(x) for x in response.get('data', [])]

    def deactivatePrepaidCard(self,
                              userToken=None,
                              prepaidCardToken=None,
                              notes=None):
        '''
        Deactivate a Prepaid Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param notes:
            A string describing the deactivation.
        :returns:
            A Prepaid Card Status Transition.
        '''

        data = {
            'transition': 'DE_ACTIVATED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createPrepaidCardStatusTransition(
            userToken,
            prepaidCardToken,
            data
        )

    def suspendPrepaidCard(self,
                           userToken=None,
                           prepaidCardToken=None,
                           notes=None):
        '''
        Suspend a Prepaid Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param notes:
            A string describing the suspension.
        :returns:
            A Prepaid Card Status Transition.
        '''

        data = {
            'transition': 'SUSPENDED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createPrepaidCardStatusTransition(
            userToken,
            prepaidCardToken,
            data
        )

    def unsuspendPrepaidCard(self,
                             userToken=None,
                             prepaidCardToken=None,
                             notes=None):
        '''
        Unsuspend a Prepaid Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param notes:
            A string describing the unsuspension.
        :returns:
            A Prepaid Card Status Transition.
        '''

        data = {
            'transition': 'UNSUSPENDED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createPrepaidCardStatusTransition(
            userToken,
            prepaidCardToken,
            data
        )

    def lostOrStolenPrepaidCard(self,
                                userToken=None,
                                prepaidCardToken=None,
                                notes=None):
        '''
        Report a Prepaid Card lost or stolen.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param notes:
            A string describing the lost or stolen report.
        :returns:
            A Prepaid Card Status Transition.
        '''

        data = {
            'transition': 'LOST_OR_STOLEN'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createPrepaidCardStatusTransition(
            userToken,
            prepaidCardToken,
            data
        )

    def lockPrepaidCard(self,
                        userToken=None,
                        prepaidCardToken=None,
                        notes=None):
        '''
        Lock a Prepaid Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param notes:
            A string describing the lock.
        :returns:
            A Prepaid Card Status Transition.
        '''

        data = {
            'transition': 'LOCKED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createPrepaidCardStatusTransition(
            userToken,
            prepaidCardToken,
            data
        )

    def unlockPrepaidCard(self,
                          userToken=None,
                          prepaidCardToken=None,
                          notes=None):
        '''
        Unlock a Prepaid Card.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param notes:
            A string describing the unlock.
        :returns:
            A Prepaid Card Status Transition.
        '''

        data = {
            'transition': 'UNLOCKED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createPrepaidCardStatusTransition(
            userToken,
            prepaidCardToken,
            data
        )

    '''

    Paper Checks
    https://portal.hyperwallet.com/docs/api/v3/resources/paper-checks

    '''

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
            self.__buildUrl('users', userToken, 'paper-checks'),
            data
        )

        return PaperCheck(response)

    def getPaperCheck(self,
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
            self.__buildUrl(
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

        body = self.__updateTransferMethod(userToken, paperCheckToken, 'paper-checks', data)
        return PaperCheck(body)

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

        if params and not set(list(params)).issubset(PaperCheck.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl('users', userToken, 'paper-checks'),
            params
        )

        return [PaperCheck(x) for x in response.get('data', [])]

    def createPaperCheckStatusTransition(self,
                                         userToken=None,
                                         paperCheckToken=None,
                                         data=None):
        '''
        Create a Paper Check Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :param data:
            A dictionary containing Paper Check Status Transition information. **REQUIRED**
        :returns:
            A Paper Check Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not paperCheckToken:
            raise HyperwalletException('paperCheckToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            self.__buildUrl(
                'users',
                userToken,
                'paper-checks',
                paperCheckToken,
                'status-transitions'
            ),
            data
        )

        return StatusTransition(response)

    def getPaperCheckStatusTransition(self,
                                      userToken=None,
                                      paperCheckToken=None,
                                      statusTransitionToken=None):
        '''
        Retrieve a Paper Check Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Paper Check Status Transition. **REQUIRED**
        :returns:
            A Paper Check Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not paperCheckToken:
            raise HyperwalletException('paperCheckToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'paper-checks',
                paperCheckToken,
                'status-transitions',
                statusTransitionToken
            )
        )

        return StatusTransition(response)

    def listPaperCheckStatusTransitions(self,
                                        userToken=None,
                                        paperCheckToken=None,
                                        params=None):
        '''
        List Paper Check Status Transitions.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Paper Check Status Transitions.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not paperCheckToken:
            raise HyperwalletException('paperCheckToken is required')

        if params and not set(list(params)).issubset(StatusTransition.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'paper-checks',
                paperCheckToken,
                'status-transitions'
            ),
            params
        )

        return [StatusTransition(x) for x in response.get('data', [])]

    def deactivatePaperCheck(self,
                             userToken=None,
                             paperCheckToken=None,
                             notes=None):
        '''
        Deactivate a Paper Check.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param paperCheckToken:
            A token identifying the Paper Check. **REQUIRED**
        :param notes:
            A string describing the deactivation.
        :returns:
            A Paper Check Status Transition.
        '''

        data = {
            'transition': 'DE_ACTIVATED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createPaperCheckStatusTransition(
            userToken,
            paperCheckToken,
            data
        )

    '''

    Transfers
    https://portal.hyperwallet.com/docs/api/v3/resources/transfers

    '''

    def createTransfer(self,
                       data=None):
        '''
        Create a Transfer.
        :param data:
            A dictionary containing Transfer information. **REQUIRED**
        :returns:
            A Transfer.
        '''

        if not data:
            raise HyperwalletException('data is required')

        if not ('sourceToken' in data) or not (data['sourceToken']):
            raise HyperwalletException('sourceToken is required')

        if not ('destinationToken' in data) or not (data['destinationToken']):
            raise HyperwalletException('destinationToken is required')

        if not ('clientTransferId' in data) or not (data['clientTransferId']):
            raise HyperwalletException('clientTransferId is required')

        response = self.apiClient.doPost(
            self.__buildUrl('transfers'),
            data
        )

        return Transfer(response)

    def getTransfer(self,
                    transferToken=None):
        '''
        Retrieve a Transfer.
        :param transferToken:
            A token identifying the Transfer. **REQUIRED**
        :returns:
            A Transfer.
        '''

        if not transferToken:
            raise HyperwalletException('transferToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'transfers',
                transferToken
            )
        )

        return Transfer(response)

    def listTransfers(self,
                      params=None):
        '''
        List Transfers.
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Transfers.
        '''

        if params and not set(list(params)).issubset(Transfer.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl('transfers'),
            params
        )

        return [Transfer(x) for x in response.get('data', [])]

    def createTransferStatusTransition(self,
                                       transferToken=None,
                                       data=None):
        '''
        Create a Transfer Status Transition.
        :param transferToken:
            A token identifying the Transfer. **REQUIRED**
        :param data:
            A dictionary containing Transfer Status Transition information. **REQUIRED**
        :returns:
            A Transfer Status Transition.
        '''

        if not transferToken:
            raise HyperwalletException('transferToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            self.__buildUrl(
                'transfers',
                transferToken,
                'status-transitions'
            ),
            data
        )

        return StatusTransition(response)

    '''

    PayPal Accounts

    '''

    def createPayPalAccount(self,
                            userToken=None,
                            data=None):
        '''
        Create a PayPal Account.
        :param userToken:
            A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing PayPal Account information. **REQUIRED**
        :returns:
            A PayPal Account.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        if not ('transferMethodCountry' in data) or not (data['transferMethodCountry']):
            raise HyperwalletException('transferMethodCountry is required')

        if not ('transferMethodCurrency' in data) or not (data['transferMethodCurrency']):
            raise HyperwalletException('transferMethodCurrency is required')

        if not ('email' in data) or not (data['email']):
            raise HyperwalletException('email is required')

        response = self.apiClient.doPost(
            self.__buildUrl('users', userToken, 'paypal-accounts'),
            data
        )

        return PayPalAccount(response)

    def updatePayPalAccount(self,
                            userToken=None,
                            payPalAccountToken=None,
                            data=None):
        '''
        Update a PayPal Account.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param payPalAccountToken:
            A token identifying the PayPal Account. **REQUIRED**
        :param data:
            A dictionary containing PayPal Account information. **REQUIRED**
        :returns:
            A PayPal Account.
        '''

        body = self.__updateTransferMethod(userToken, payPalAccountToken, 'paypal-accounts', data)
        return PayPalAccount(body)

    def getPayPalAccount(self,
                         userToken=None,
                         payPalAccountToken=None):
        '''
        Retrieve a PayPal Account.
        :param userToken:
            A token identifying the User. **REQUIRED**
        :param payPalAccountToken:
            A token identifying the PayPal Account. **REQUIRED**
        :returns:
            A PayPal Account.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not payPalAccountToken:
            raise HyperwalletException('payPalAccountToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'paypal-accounts',
                payPalAccountToken
            )
        )

        return PayPalAccount(response)

    def listPayPalAccounts(self,
                           userToken=None,
                           params=None):
        '''
        List PayPal Accounts.
        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of PayPal Accounts.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if params and not set(list(params)).issubset(PayPalAccount.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl('users', userToken, 'paypal-accounts'),
            params
        )

        return [PayPalAccount(x) for x in response.get('data', [])]

    def createPayPalAccountStatusTransition(self,
                                            userToken=None,
                                            payPalAccountToken=None,
                                            data=None):
        '''
        Create a PayPal Account Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param payPalAccountToken:
            A token identifying the PayPal Account. **REQUIRED**
        :param data:
            A dictionary containing PayPal Account Status Transition information. **REQUIRED**
        :returns:
            A PayPal Account Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not payPalAccountToken:
            raise HyperwalletException('payPalAccountToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            self.__buildUrl(
                'users',
                userToken,
                'paypal-accounts',
                payPalAccountToken,
                'status-transitions'
            ),
            data
        )

        return StatusTransition(response)

    def getPayPalAccountStatusTransition(self,
                                         userToken=None,
                                         payPalAccountToken=None,
                                         statusTransitionToken=None):
        '''
        Retrieve a PayPal Account Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param payPalAccountToken:
            A token identifying the PayPal Account. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the PayPal Account Status Transition. **REQUIRED**
        :returns:
            A PayPal Account Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not payPalAccountToken:
            raise HyperwalletException('payPalAccountToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'paypal-accounts',
                payPalAccountToken,
                'status-transitions',
                statusTransitionToken
            )
        )

        return StatusTransition(response)

    def listPayPalAccountStatusTransitions(self,
                                           userToken=None,
                                           payPalAccountToken=None,
                                           params=None):
        '''
        List PayPal Account Status Transitions.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param payPalAccountToken:
            A token identifying the PayPal Account. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of PayPal Account Status Transitions.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not payPalAccountToken:
            raise HyperwalletException('payPalAccountToken is required')

        if params and not set(list(params)).issubset(StatusTransition.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'paypal-accounts',
                payPalAccountToken,
                'status-transitions'
            ),
            params
        )

        return [StatusTransition(x) for x in response.get('data', [])]

    def deactivatePayPalAccount(self,
                                userToken=None,
                                payPalAccountToken=None,
                                notes=None):
        '''
        Deactivate a PayPal Account.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param payPalAccountToken:
            A token identifying the PayPal Account. **REQUIRED**
        :param notes:
            A string describing the deactivation.
        :returns:
            A PayPal Account Status Transition.
        '''

        data = {
            'transition': 'DE_ACTIVATED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createPayPalAccountStatusTransition(
            userToken,
            payPalAccountToken,
            data
        )

    '''

    Venmo Accounts

    '''

    def createVenmoAccount(self,
                           userToken=None,
                           data=None):
        '''
        Create a Venmo Account.
        :param userToken:
            A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing Venmo Account information. **REQUIRED**
        :returns:
            A Venmo Account.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not data:
            raise HyperwalletException('data is required')

        if not ('transferMethodCountry' in data) or not (data['transferMethodCountry']):
            raise HyperwalletException('transferMethodCountry is required')

        if not ('transferMethodCurrency' in data) or not (data['transferMethodCurrency']):
            raise HyperwalletException('transferMethodCurrency is required')

        if not ('accountId' in data) or not (data['accountId']):
            raise HyperwalletException('accountId is required')

        response = self.apiClient.doPost(
            self.__buildUrl('users', userToken, 'venmo-accounts'),
            data
        )

        return VenmoAccount(response)

    def updateVenmoAccount(self,
                           userToken=None,
                           venmoAccountToken=None,
                           data=None):
        '''
        Update a Venmo Account.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param VenmoAccountToken:
            A token identifying the Venmo Account. **REQUIRED**
        :param data:
            A dictionary containing Venmo Account information. **REQUIRED**
        :returns:
            A Venmo Account.
        '''

        body = self.__updateTransferMethod(userToken, venmoAccountToken, 'venmo-accounts', data)
        return VenmoAccount(body)

    def getVenmoAccount(self,
                        userToken=None,
                        venmoAccountToken=None):
        '''
        Retrieve a Venmo Account.
        :param userToken:
            A token identifying the User. **REQUIRED**
        :param VenmoAccountToken:
            A token identifying the Venmo Account. **REQUIRED**
        :returns:
            A Venmo Account.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not venmoAccountToken:
            raise HyperwalletException('venmoAccountToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'venmo-accounts',
                venmoAccountToken
            )
        )

        return VenmoAccount(response)

    def listVenmoAccounts(self,
                          userToken=None,
                          params=None):
        '''
        List Venmo Accounts.
        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Venmo Accounts.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if params and not set(list(params)).issubset(VenmoAccount.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl('users', userToken, 'venmo-accounts'),
            params
        )

        return [VenmoAccount(x) for x in response.get('data', [])]

    def createVenmoAccountStatusTransition(self,
                                           userToken=None,
                                           venmoAccountToken=None,
                                           data=None):
        '''
        Create a Venmo Account Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param VenmoAccountToken:
            A token identifying the Venmo Account. **REQUIRED**
        :param data:
            A dictionary containing Venmo Account Status Transition information. **REQUIRED**
        :returns:
            A Venmo Account Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not venmoAccountToken:
            raise HyperwalletException('venmoAccountToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            self.__buildUrl(
                'users',
                userToken,
                'venmo-accounts',
                venmoAccountToken,
                'status-transitions'
            ),
            data
        )

        return StatusTransition(response)

    def getVenmoAccountStatusTransition(self,
                                        userToken=None,
                                        venmoAccountToken=None,
                                        statusTransitionToken=None):
        '''
        Retrieve a Venmo Account Status Transition.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param VenmoAccountToken:
            A token identifying the Venmo Account. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Venmo Account Status Transition. **REQUIRED**
        :returns:
            A Venmo Account Status Transition.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not venmoAccountToken:
            raise HyperwalletException('venmoAccountToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'venmo-accounts',
                venmoAccountToken,
                'status-transitions',
                statusTransitionToken
            )
        )

        return StatusTransition(response)

    def listVenmoAccountStatusTransitions(self,
                                          userToken=None,
                                          venmoAccountToken=None,
                                          params=None):
        '''
        List Venmo Account Status Transitions.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param venmoAccountToken:
            A token identifying the Venmo Account. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Venmo Account Status Transitions.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not venmoAccountToken:
            raise HyperwalletException('venmoAccountToken is required')

        if params and not set(list(params)).issubset(StatusTransition.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'venmo-accounts',
                venmoAccountToken,
                'status-transitions'
            ),
            params
        )

        return [StatusTransition(x) for x in response.get('data', [])]

    def deactivateVenmoAccount(self,
                               userToken=None,
                               venmoAccountToken=None,
                               notes=None):
        '''
        Deactivate a Venmo Account.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param venmoAccountToken:
            A token identifying the Venmo Account. **REQUIRED**
        :param notes:
            A string describing the deactivation.
        :returns:
            A Venmo Account Status Transition.
        '''

        data = {
            'transition': 'DE_ACTIVATED'
        }

        if type(notes) is str:
            data.update({'notes': notes})

        return self.createVenmoAccountStatusTransition(
            userToken,
            venmoAccountToken,
            data
        )

    '''

    AuthenticationToken

    '''

    def getAuthenticationToken(self,
                               userToken=None):
        '''
        Get a AuthenticationToken.
        :param userToken:
             A user token. **REQUIRED**
        :returns:
            An AuthenticationToken.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        response = self.apiClient.doPost(
            self.__buildUrl('users', userToken, 'authentication-token'),
            None
        )

        return AuthenticationToken(response)

    '''

    Payments
    https://portal.hyperwallet.com/docs/api/v3/resources/payments

    '''

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

    def getPayment(self,
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
            self.__buildUrl('payments', paymentToken)
        )

        return Payment(response)

    def listPayments(self,
                     params=None):
        '''
        List Payments.

        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Payments.
        '''

        if params and not set(list(params)).issubset(Payment.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet('payments', params)

        return [Payment(x) for x in response.get('data', [])]

    def getPaymentStatusTransition(self,
                                   paymentToken=None,
                                   statusTransitionToken=None):
        '''
        Retrieve a Payment Status Transition.

        :param paymentToken:
            A token identifying the Payment. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Payment Status Transition. **REQUIRED**
        :returns:
            A Payment Status Transition.
        '''

        if not paymentToken:
            raise HyperwalletException('paymentToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'payments',
                paymentToken,
                'status-transitions',
                statusTransitionToken
            )
        )

        return StatusTransition(response)

    def listPaymentStatusTransitions(self,
                                     paymentToken=None,
                                     params=None):
        '''
        List Payment Status Transitions.

        :param paymentToken:
            A token identifying the Payment. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Payment Status Transitions.
        '''

        if not paymentToken:
            raise HyperwalletException('paymentToken is required')

        if params and not set(list(params)).issubset(StatusTransition.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'payments',
                paymentToken,
                'status-transitions'
            ),
            params
        )

        return [StatusTransition(x) for x in response.get('data', [])]

    def createPaymentStatusTransition(self,
                                      paymentToken=None,
                                      data=None):
        '''
        Create Payment Status Transition.

        :param paymentToken:
            A token identifying the Payment. **REQUIRED**
        :param data:
            A dictionary containing User Status Transition information. **REQUIRED**
        :returns:
            A Payment Status Transition.
        '''

        if not paymentToken:
            raise HyperwalletException('paymentToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            self.__buildUrl(
                'payments',
                paymentToken,
                'status-transitions'
            ),
            data
        )

        return StatusTransition(response)

    '''

    Balances
    https://portal.hyperwallet.com/docs/api/v3/resources/balances

    '''

    def listBalancesForUser(self,
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

        if params and not set(list(params)).issubset(Balance.filters_array_user):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl('users', userToken, 'balances'),
            params
        )

        return [Balance(x) for x in response.get('data', [])]

    def listBalancesForPrepaidCard(self,
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

        if params and not set(list(params)).issubset(Balance.filters_array_prepaid_card):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'balances'
            ),
            params
        )

        return [Balance(x) for x in response.get('data', [])]

    def listBalancesForAccount(self,
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

        if params and not set(list(params)).issubset(Balance.filters_array_account):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
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

    Receipts
    https://portal.hyperwallet.com/docs/api/v3/resources/receipts

    '''

    def listReceiptsForUser(self,
                            userToken=None,
                            params=None):
        '''
        List User Receipts.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Receipts.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if params and not set(list(params)).issubset(Receipt.filters_array_user):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl('users', userToken, 'receipts'),
            params
        )

        return [Receipt(x) for x in response.get('data', [])]

    def listReceiptsForPrepaidCard(self,
                                   userToken=None,
                                   prepaidCardToken=None,
                                   params=None):
        '''
        List Prepaid Card Receipts.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param prepaidCardToken:
            A token identifying the Prepaid Card. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Receipts.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not prepaidCardToken:
            raise HyperwalletException('prepaidCardToken is required')

        if params and not set(list(params)).issubset(Receipt.filters_array_prepaid_card):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'prepaid-cards',
                prepaidCardToken,
                'receipts'
            ),
            params
        )

        return [Receipt(x) for x in response.get('data', [])]

    def listReceiptsForAccount(self,
                               programToken=None,
                               accountToken=None,
                               params=None):
        '''
        List Account Receipts.

        :param programToken:
            A token identifying the Program. **REQUIRED**
        :param accountToken:
            A token identifying the Account. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Receipts.
        '''

        if not programToken:
            raise HyperwalletException('programToken is required')

        if not accountToken:
            raise HyperwalletException('accountToken is required')

        if params and not set(list(params)).issubset(Receipt.filters_array_account):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'programs',
                programToken,
                'accounts',
                accountToken,
                'receipts'
            ),
            params
        )

        return [Receipt(x) for x in response.get('data', [])]

    '''

    Programs
    https://portal.hyperwallet.com/docs/api/v3/resources/programs

    '''

    def getProgram(self,
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
            self.__buildUrl('programs', programToken)
        )

        return Program(response)

    '''

    Accounts
    https://portal.hyperwallet.com/docs/api/v3/resources/accounts

    '''

    def getAccount(self,
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
            self.__buildUrl(
                'programs',
                programToken,
                'accounts',
                accountToken
            )
        )

        return Account(response)

    '''

    Transfer Methods
    https://portal.hyperwallet.com/docs/api/v3/resources/transfer-method-configurations

    '''

    def createTransferMethod(self,
                             userToken=None,
                             cacheToken=None,
                             data=None):
        '''
        Create a Transfer Method.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param cacheToken:
            A cache token identifying the Transfer Method. **REQUIRED**
        :param data:
            A dictionary containing Field Restriction information.
        :returns:
            A Transfer Method.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not cacheToken:
            raise HyperwalletException('cacheToken is required')

        headers = {'Json-Cache-Token': cacheToken}

        response = self.apiClient.doPost(
            self.__buildUrl(
                'users',
                userToken,
                'transfer-methods'
            ),
            data,
            headers
        )

        transfer_method_types = {
            'BANK_ACCOUNT': BankAccount,
            'WIRE_ACCOUNT': BankAccount,
            'BANK_CARD': BankCard,
            'PAPER_CHECK': PaperCheck
        }

        transfer_method_type = response.get('type')

        if transfer_method_type in transfer_method_types:
            return transfer_method_types[transfer_method_type](response)

        return TransferMethod(response)

    def getTransferMethodConfiguration(self,
                                       userToken=None,
                                       country=None,
                                       currency=None,
                                       transferMethodType=None,
                                       profileType=None):
        '''
        Retrieve a Transfer Method Configuration.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param country:
            An ISO 3166-1 code identifying the country. **REQUIRED**
        :param currency:
            An ISO 4217-1 code identifying the currency. **REQUIRED**
        :param transferMethodType:
            A string identifying the type of Transfer Method. **REQUIRED**
        :param profileType:
            A string identifying the type of User. **REQUIRED**
        :returns:
            A Transfer Method Configuration.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not country:
            raise HyperwalletException('country is required')

        if not currency:
            raise HyperwalletException('currency is required')

        if not transferMethodType:
            raise HyperwalletException('type is required')

        if not profileType:
            raise HyperwalletException('profileType is required')

        response = self.apiClient.doGet(
            'transfer-method-configurations',
            {
                'userToken': userToken,
                'country': country,
                'currency': currency,
                'type': transferMethodType,
                'profileType': profileType
            }
        )

        return TransferMethodConfiguration(response)

    def listTransferMethodConfigurations(self,
                                         userToken=None,
                                         params={}):
        '''
        List Transfer Method Configurations.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Transfer Method Configurations.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if params and not set(list(params)).issubset(TransferMethodConfiguration.filters_array):
            raise HyperwalletException('Invalid filter')

        params.update({'userToken': userToken})

        response = self.apiClient.doGet(
            'transfer-method-configurations',
            params
        )

        configurations = []

        data = response.get('data')

        if not data:
            return []

        for collection in data:
            countries = collection.pop('countries', [])
            currencies = collection.pop('currencies', [])

            for country in countries:
                for currency in currencies:
                    configuration = collection.copy()
                    configuration.update({'countries': [country]})
                    configuration.update({'currencies': [currency]})

                    configurations.append(configuration)

        return [TransferMethodConfiguration(x) for x in configurations]

    def __updateTransferMethod(self,
                               userToken=None,
                               transferMethodToken=None,
                               transferMethodName=None,
                               data=None):
        '''
        Update a Transfer method.

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param transferMethodToken:
            A token identifying the Transfer Method. **REQUIRED**
        :param transferMethodName:
            A Transfer Method name used in url. **REQUIRED**
        :param data:
            A dictionary containing Transfer Method information. **REQUIRED**
        :returns:
            An updated Transfer Method object.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if not transferMethodToken:
            raise HyperwalletException('transfer method token is required')

        if not data:
            raise HyperwalletException('data is required')

        return self.apiClient.doPut(
            self.__buildUrl(
                'users',
                userToken,
                transferMethodName,
                transferMethodToken
            ),
            data
        )

    '''

    Webhook Notifications
    https://portal.hyperwallet.com/docs/api/v3/resources/webhook-notifications

    '''

    def getWebhookNotification(self,
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
            self.__buildUrl('webhook-notifications', webhookToken)
        )

        return Webhook(response)

    def listWebhookNotifications(self,
                                 params=None):
        '''
        List Webhook Notifications.

        :param params:
            A dictionary containing query parameters.
        :returns:
            An array of Webhooks.
        '''

        if params and not set(list(params)).issubset(Webhook.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet('webhook-notifications', params)

        return [Webhook(x) for x in response.get('data', [])]

    def __buildUrl(self, *paths):
        return '/'.join(s.strip('/') for s in paths)

    def setDocumentAndReasonFromResponseHelper(self,
                                               data=None):
        '''
        Helper to modify dictionary with Document and Reason classes

        :param data:
            A dictionary containing data for either a User
            sample data:
            jsonData={'data': ['{"documents": [{"type": "DRIVERS_LICENSE", "country": "US", "category": "IDENTIFICATION", "reasons": {"name": 0, "description": "STRING_VAL"}}]}']};
        :returns:
            A Dictionary with documents and reasons information
        '''

        if "documents" in data.keys():
            documents = data["documents"]
            listOfDocs = []
            for dVal in documents:
                if "reasons" in dVal.keys():
                    reasons = dVal["reasons"]
                    dVal["reasons"] = []
                    for rVal in reasons:
                        if type(rVal["name"]) == str:
                            rVal["name"] = RejectReason[rVal["name"]]
                        else:
                            rVal["name"] = RejectReason(rVal["name"])
                        rVal = HyperwalletVerificationDocumentReason(rVal)
                        dVal["reasons"].append(rVal)
                dVal = HyperwalletVerificationDocument(dVal)
                listOfDocs.append(dVal)
            data["documents"] = listOfDocs
        return data

    def uploadDocumentsForUser(self,
                               userToken=None,
                               data=None,
                               files=None):
        '''
        Upload documents for Users

        :param userToken:
            A token identifying the User. **REQUIRED**
        :param data:
            A dictionary containing data for the input documents. **REQUIRED**
            sample data:
            jsonData={'data': ['{"documents": [{"type": "DRIVERS_LICENSE", "country": "US", "category": "IDENTIFICATION"}]}']};
        :param files: Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload. **REQUIRED**
            sample data:
            files = {
            'drivers_license_front': open('F1.png', 'rb'),
            'drivers_license_back': open('F22.png', 'rb')
            }
        :returns:
            A User with documents information
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        response = self.apiClient.putDocument(
            self.__buildUrl(
                'users',
                userToken
            ),
            data,
            files
        )
        response = self.setDocumentAndReasonFromResponseHelper(response)
        return User(response)

    '''

    Transfer Refunds

    '''

    def createTransferRefund(self,
                             transferToken=None,
                             data=None):
        '''
        Create a Transfer Refund.
        :param transferToken:
            A token identifying the Transfer. **REQUIRED**
        :param data:
            A dictionary containing Transfer Refund information. **REQUIRED**
        :returns:
            A Transfer Refund.
        '''

        if not transferToken:
            raise HyperwalletException('transferToken is required')

        if not data:
            raise HyperwalletException('data is required')

        response = self.apiClient.doPost(
            self.__buildUrl(
                'transfers',
                transferToken,
                'refunds'
            ),
            data
        )

        return TransferRefunds(response)

    def createTransferSpendBackRefund(self,
                                      transferToken=None,
                                      sourceToken=None,
                                      params=None):
        '''
        Create a Transfer Refund.
        :param transferToken:
            A token identifying the Transfer. **REQUIRED**
        :param data:
            A dictionary containing Transfer Refund information. **REQUIRED**
        :returns:
            A Transfer Refund.
        '''

        if not transferToken:
            raise HyperwalletException('transferToken is required')

        if not sourceToken:
            raise HyperwalletException('sourceToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'transfers',
                transferToken,
                'refunds',
                sourceToken
            ),
            params
        )

        return TransferRefunds(response)

    '''

        Create User Status Transition

    '''

    def createUserStatusTransition(self,
                                   userToken=None,
                                   data=None):
        '''
        Create User Status Transition.
        :param userToken:
            A token identifying the User Create UserToken. **REQUIRED**
        :param data:
            A dictionary containing User Status Create Data information. **REQUIRED**
        :returns:
            StatusTransition.
        '''
        if not userToken:
            raise HyperwalletException('userToken is required')
        if not data:
            raise HyperwalletException('data is required')
        response = self.apiClient.doPost(
            self.__buildUrl(
                'users',
                userToken,
                'status-transitions'
            ),
            data
        )

        return StatusTransition(response)

    def activateUser(self,
                     userToken=None):

        '''
         Create User Activate Status Transition.
         :param userToken:
             A token identifying the User Create UserToken. **REQUIRED**
         :returns:
             StatusTransition.
         '''
        if not userToken:
            raise HyperwalletException('userToken is required')

        data = {
            'transition': 'ACTIVATED'
        }

        return self.createUserStatusTransition(
            userToken,
            data
        )

    def deactivateUser(self,
                       userToken=None):

        '''
         Create User DeActivate Status Transition.
         :param userToken:
             A token identifying the User Create UserToken. **REQUIRED**
         :returns:
             StatusTransition.
         '''
        if not userToken:
            raise HyperwalletException('userToken is required')

        data = {
            'transition': 'DE_ACTIVATED'
        }

        return self.createUserStatusTransition(
            userToken,
            data
        )

    def preactivateUser(self,
                        userToken=None):

        '''
         Create User Pre Activate Status Transition.
         :param userToken:
             A token identifying the User Create UserToken. **REQUIRED**
         :returns:
             StatusTransition.
         '''
        if not userToken:
            raise HyperwalletException('userToken is required')
        data = {
            'transition': 'PRE-ACTIVATED'
        }

        return self.createUserStatusTransition(
            userToken,
            data
        )

    def freezeUser(self,
                   userToken=None):

        '''
         Create User Freeze Status Transition.
         :param userToken:
             A token identifying the User Create UserToken. **REQUIRED**
         :returns:
             StatusTransition.
         '''
        if not userToken:
            raise HyperwalletException('userToken is required')

        data = {
            'transition': 'FROZEN'
        }

        return self.createUserStatusTransition(
            userToken,
            data
        )

    def lockUser(self,
                 userToken=None):

        '''
         Create User Lock Status Transition.
         :param userToken:
             A token identifying the User Create UserToken. **REQUIRED**
         :returns:
             StatusTransition.
         '''
        if not userToken:
            raise HyperwalletException('userToken is required')

        data = {
            'transition': 'LOCKED'
        }

        return self.createUserStatusTransition(
            userToken,
            data
        )

    '''

        Get Transfer Refund

    '''

    def getTransferRefund(self,
                          transferToken=None,
                          refundToken=None):

        '''
        Get a Transfer Refund.
        :param transferToken:
            A token identifying the Transfer. **REQUIRED**
        :param refundToken:
            A token identifying Transfer Refund . **REQUIRED**
        :returns:
            Get Transfer Refund.
        '''

        if not transferToken:
            raise HyperwalletException('transferToken is required')

        if not refundToken:
            raise HyperwalletException('refundToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'transfers',
                transferToken,
                'refunds',
                refundToken
            )
        )

        return TransferRefunds(response)

    '''

        List Transfer Refunds

    '''

    def listTransferRefunds(self,
                            transferToken=None,
                            params=None):

        '''
        List a Transfer Refund.
        :param transferToken:
            A token identifying the Transfer. **REQUIRED**
        :returns:
            List Transfer Refund.
        '''

        if not transferToken:
            raise HyperwalletException('transferToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'transfers',
                transferToken,
                'refunds'
            ),
            params
        )

        return TransferRefunds(response)

    '''
        List Transfer Methods
    '''

    def listTransferMethods(self,
                            userToken=None,
                            params=None):

        '''
        List a Transfer Methods.
        :param userToken:
            A token identifying the Transfer. **REQUIRED**
        :returns:
            List Transfer Methods.
        '''

        if not userToken:
            raise HyperwalletException('userToken is required')

        if params and not set(list(params)).issubset(TransferMethod.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'users',
                userToken,
                'transfer-methods'
            ),
            params
        )

        return TransferMethod(response)

    '''

        Get Transfer Status Transition

    '''

    def getTransferStatusTransition(self,
                                    transferToken=None,
                                    statusTransitionToken=None):
        '''
        Retrieve a Transfer Status Transition.

        :param transferToken:
            A token identifying the Transfer. **REQUIRED**
        :param statusTransitionToken:
            A token identifying the Transfer Status Transition. **REQUIRED**
        :returns:
            A Transfer Status Transition.
        '''

        if not transferToken:
            raise HyperwalletException('transferToken is required')

        if not statusTransitionToken:
            raise HyperwalletException('statusTransitionToken is required')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'transfers',
                transferToken,
                'status-transitions',
                statusTransitionToken
            )
        )

        return StatusTransition(response)

    '''

        List Transfer Status Transition

    '''

    def listTransferStatusTransitions(self,
                                      transferToken=None,
                                      params=None):
        '''
        Retrieve a Transfer Status Transition.

        :param transferToken:
            A token identifying the Transfer. **REQUIRED**
        :returns:
            A Transfer Status Transition.
        '''

        if not transferToken:
            raise HyperwalletException('transferToken is required')

        if params and not set(list(params)).issubset(StatusTransition.filters_array):
            raise HyperwalletException('Invalid filter')

        response = self.apiClient.doGet(
            self.__buildUrl(
                'transfers',
                transferToken,
                'status-transitions'
            ),
            params
        )

        return StatusTransition(response)
