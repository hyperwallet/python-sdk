# Thanks to Twitter Python SDK
# https://github.com/bear/python-twitter/blob/master/twitter/models.py

import json


class HyperwalletModel(object):
    '''
    The base Hyperwallet Model from which all other models will inherit.

    :param data: A dictionary containing the attributes for the Model.
    '''

    def __init__(self, data):
        '''
        Create an instance of the base HyperwalletModel.
        '''

        self.defaults = {}

    def __str__(self):
        '''
        Return a string representation of the HyperwalletModel.
        '''

        return json.dumps(self._to_dict(), sort_keys=True)

    def _to_dict(self):
        '''
        Create a dictionary representation of the Model.
        '''

        data = {}

        for (key, value) in self.defaults.items():
            if isinstance(getattr(self, key, None), (list, tuple, set)):
                data[key] = list()
                for subobj in getattr(self, key, None):
                    if getattr(subobj, '_to_dict', None):
                        data[key].append(subobj._to_dict())
                    else:
                        data[key].append(subobj)

            elif getattr(getattr(self, key, None), '_to_dict', None):
                data[key] = getattr(self, key)._to_dict()

            elif getattr(self, key, None):
                data[key] = getattr(self, key, None)

        return data


class User(HyperwalletModel):
    '''
    The User Model.

    :param data: A dictionary containing the attributes for the User.
    '''

    def __init__(self, data):
        '''
        Create a new User with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'programToken': None,
            'status': None,
            'verificationStatus': None,
            'createdOn': None,
            'clientUserId': None,
            'profileType': None,
            'email': None,
            'firstName': None,
            'middleName': None,
            'lastName': None,
            'dateOfBirth': None,
            'gender': None,
            'language': None,
            'phoneNumber': None,
            'mobileNumber': None,
            'employerId': None,
            'passportId': None,
            'governmentId': None,
            'driversLicenseId': None,
            'addressLine1': None,
            'addressLine2': None,
            'city': None,
            'stateProvince': None,
            'postalCode': None,
            'country': None,
            'countryOfBirth': None,
            'countryOfNationality': None,
            'businessType': None,
            'businessName': None,
            'businessRegistrationId': None,
            'businessRegistrationCountry': None,
            'businessRegistrationStateProvince': None,
            'businessContactRole': None,
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "User({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )


class BankAccount(HyperwalletModel):
    '''
    The BankAccount Model.

    :param data: A dictionary containing the attributes for the BankAccount.
    '''

    def __init__(self, data):
        '''
        Create a new BankAccount with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'status': None,
            'createdOn': None,
            'userToken': None,
            'email': None,
            'profileType': None,
            'firstName': None,
            'middleName': None,
            'lastName': None,
            'dateOfBirth': None,
            'phoneNumber': None,
            'mobileNumber': None,
            'governmentId': None,
            'passportId': None,
            'driverLicenseId': None,
            'addressLine1': None,
            'addressLine2': None,
            'city': None,
            'stateProvince': None,
            'postalCode': None,
            'country': None,
            'countryOfBirth': None,
            'countryOfNationality': None,
            'businessName': None,
            'businessRegistrationId': None,
            'businessRegistrationCountry': None,
            'type': None,
            'bankId': None,
            'bankName': None,
            'bankAccountId': None,
            'bankAccountPurpose': None,
            'bankAccountRelationship': None,
            'branchAddressLine1': None,
            'branchCity': None,
            'branchCountry': None,
            'branchId': None,
            'branchName': None,
            'branchPostalCode': None,
            'branchStateProvince': None,
            'intermediaryBankAccountId': None,
            'intermediaryBankAddressLine1': None,
            'intermediaryBankCity': None,
            'intermediaryBankCountry': None,
            'intermediaryBankId': None,
            'intermediaryBankName': None,
            'intermediaryBankPostalCode': None,
            'intermediaryBankStateProvince': None,
            'transferMethodCountry': None,
            'transferMethodCurrency': None,
            'wireInstructions': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "BankAccount({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )


class Payment(HyperwalletModel):
    '''
    The Payment Model.

    :param data: A dictionary containing the attributes for the Payment.
    '''

    def __init__(self, data):
        '''
        Create a new Payment with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'createdOn': None,
            'clientPaymentId': None,
            'amount': None,
            'currency': None,
            'notes': None,
            'memo': None,
            'purpose': None,
            'releaseOn': None,
            'expiresOn': None,
            'destinationToken': None,
            'programToken': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "Payment({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )


class Webhook(HyperwalletModel):
    '''
    The Webhook Model.

    :param data: A dictionary containing the attributes for the Webhook.
    '''

    def __init__(self, data):
        '''
        Create a new Webhook with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'type': None,
            'createdOn': None,
            'object': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

        wh_object = Webhook.make_object(self.type, self.object)

        if wh_object is not None:
            self.object = wh_object

    def __repr__(self):
        return "Webhook({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )

    @staticmethod
    def make_object(wh_type, wh_object):

        if wh_type is None:
            return None

        if type(wh_object) is not dict:
            return None

        types = {
            'PAYMENTS': Payment,
            'BANK_ACCOUNTS': BankAccount,
            # 'PREPAID_CARDS': 'prepaidCard',
            'USERS': User
        }

        base, sub = wh_type.split('.')[:2]

        if sub in types:
            return types[sub](wh_object)
        elif base in types:
            return types[base](wh_object)

        return None
