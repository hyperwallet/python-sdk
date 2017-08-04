# Thanks to Twitter Python SDK
# https://github.com/bear/python-twitter/blob/master/twitter/models.py

import json


class HyperwalletModel(object):
    '''
    The base Hyperwallet Model from which all other models will inherit.

    :param data:
        A dictionary containing the attributes for the Model.
    '''

    def __init__(self, data):
        '''
        Create an instance of the base HyperwalletModel.
        '''

        self.defaults = {}

    def __str__(self):
        '''
        Return a string representation of the HyperwalletModel. By default this
        is the same as asJsonString().
        '''

        return self.asJsonString()

    def asJsonString(self):
        '''
        Return a JSON string of the HyperwalletModel based on key/value pairs
        returned from the asDict() function.
        '''

        return json.dumps(self.asDict(), sort_keys=True)

    def asDict(self):
        '''
        Return a dictionary representation of the Model.
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

    :param data:
        A dictionary containing the attributes for the User.
    '''

    def __init__(self, data):
        '''
        Create a new User with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'createdOn': None,
            'status': None,
            'verificationStatus': None,
            'email': None,
            'profileType': None,
            'firstName': None,
            'middleName': None,
            'lastName': None,
            'dateOfBirth': None,
            'countryOfBirth': None,
            'countryOfNationality': None,
            'gender': None,
            'phoneNumber': None,
            'mobileNumber': None,
            'governmentId': None,
            'passportId': None,
            'driversLicenseId': None,
            'employerId': None,
            'businessType': None,
            'businessName': None,
            'businessRegistrationId': None,
            'businessRegistrationStateProvince': None,
            'businessRegistrationCountry': None,
            'businessContactRole': None,
            'addressLine1': None,
            'addressLine2': None,
            'city': None,
            'stateProvince': None,
            'country': None,
            'postalCode': None,
            'language': None,
            'programToken': None,
            'clientUserId': None
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

    :param data:
        A dictionary containing the attributes for the Bank Account.
    '''

    def __init__(self, data):
        '''
        Create a new Bank Account with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'createdOn': None,
            'status': None,
            'type': None,
            'email': None,
            'profileType': None,
            'firstName': None,
            'middleName': None,
            'lastName': None,
            'dateOfBirth': None,
            'countryOfBirth': None,
            'countryOfNationality': None,
            'gender': None,
            'phoneNumber': None,
            'mobileNumber': None,
            'governmentId': None,
            'passportId': None,
            'driverLicenseId': None,
            'businessType': None,
            'businessName': None,
            'businessRegistrationId': None,
            'businessRegistrationStateProvince': None,
            'businessRegistrationCountry': None,
            'businessContactRole': None,
            'addressLine1': None,
            'addressLine2': None,
            'city': None,
            'stateProvince': None,
            'country': None,
            'postalCode': None,
            'transferMethodCountry': None,
            'transferMethodCurrency': None,
            'bankName': None,
            'bankId': None,
            'bankAccountRelationship': None,
            'branchName': None,
            'branchId': None,
            'bankAccountId': None,
            'bankAccountPurpose': None,
            'branchAddressLine1': None,
            'branchAddressLine2': None,
            'branchCity': None,
            'branchStateProvince': None,
            'branchCountry': None,
            'branchPostalCode': None,
            'wireInstructions': None,
            'intermediaryBankId': None,
            'intermediaryBankName': None,
            'intermediaryBankAccountId': None,
            'intermediaryBankAddressLine1': None,
            'intermediaryBankAddressLine2': None,
            'intermediaryBankCity': None,
            'intermediaryBankStateProvince': None,
            'intermediaryBankCountry': None,
            'intermediaryBankPostalCode': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "BankAccount({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )


class BankCard(HyperwalletModel):
    '''
    The BankCard Model.

    :param data:
        A dictionary containing the attributes for the Bank Card.
    '''

    def __init__(self, data):
        '''
        Create a new Bank Card with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'createdOn': None,
            'status': None,
            'type': None,
            'profileType': None,
            'businessName': None,
            'addressLine1': None,
            'city': None,
            'stateProvince': None,
            'country': None,
            'postalCode': None,
            'transferMethodCountry': None,
            'transferMethodCurrency': None,
            'cardNumber': None,
            'cardType': None,
            'cardBrand': None,
            'dateOfExpiry': None,
            'isDefaultTransferMethod': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "BankCard({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )


class PrepaidCard(HyperwalletModel):
    '''
    The PrepaidCard Model.

    :param data:
        A dictionary containing the attributes for the Prepaid Card.
    '''

    def __init__(self, data):
        '''
        Create a new Prepaid Card with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'createdOn': None,
            'status': None,
            'type': None,
            'transferMethodCountry': None,
            'transferMethodCurrency': None,
            'cardType': None,
            'cardPackage': None,
            'cardNumber': None,
            'cardBrand': None,
            'dateOfExpiry': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "PrepaidCard({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )


class PaperCheck(HyperwalletModel):
    '''
    The PaperCheck Model.

    :param data:
        A dictionary containing the attributes for the Paper Check.
    '''

    def __init__(self, data):
        '''
        Create a new Paper Check with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'createdOn': None,
            'status': None,
            'type': None,
            'profileType': None,
            'firstName': None,
            'middleName': None,
            'lastName': None,
            'dateOfBirth': None,
            'countryOfBirth': None,
            'countryOfNationality': None,
            'phoneNumber': None,
            'mobileNumber': None,
            'governmentId': None,
            'businessName': None,
            'businessRegistrationId': None,
            'businessRegistrationCountry': None,
            'addressLine1': None,
            'city': None,
            'stateProvince': None,
            'country': None,
            'postalCode': None,
            'transferMethodCountry': None,
            'transferMethodCurrency': None,
            'bankName': None,
            'bankId': None,
            'bankAccountRelationship': None,
            'branchName': None,
            'branchId': None,
            'bankAccountId': None,
            'bankAccountPurpose': None,
            'branchAddressLine1': None,
            'branchAddressLine2': None,
            'branchCity': None,
            'branchStateProvince': None,
            'branchCountry': None,
            'branchPostalCode': None,
            'wireInstructions': None,
            'intermediaryBankId': None,
            'intermediaryBankName': None,
            'intermediaryBankAccountId': None,
            'intermediaryBankAddressLine1': None,
            'intermediaryBankAddressLine2': None,
            'intermediaryBankCity': None,
            'intermediaryBankStateProvince': None,
            'intermediaryBankCountry': None,
            'intermediaryBankPostalCode': None,
            'shippingMethod': None,
            'isDefaultTransferMethod': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "PaperCheck({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )


class Payment(HyperwalletModel):
    '''
    The Payment Model.

    :param data:
        A dictionary containing the attributes for the Payment.
    '''

    def __init__(self, data):
        '''
        Create a new Payment with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'createdOn': None,
            'programToken': None,
            'clientPaymentId': None,
            'amount': None,
            'currency': None,
            'notes': None,
            'memo': None,
            'purpose': None,
            'releaseOn': None,
            'expiresOn': None,
            'destinationToken': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "Payment({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )


class Balance(HyperwalletModel):
    '''
    The Balance Model.

    :param data:
        A dictionary containing the attributes for the Balance.
    '''

    def __init__(self, data):
        '''
        Create a new Balance with the provided attributes.
        '''

        self.defaults = {
            'currency': None,
            'amount': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "Balance({currency}, {amount})".format(
            currency=self.currency,
            amount=self.amount
        )


class Program(HyperwalletModel):
    '''
    The Program Model.

    :param data:
        A dictionary containing the attributes for the Program.
    '''

    def __init__(self, data):
        '''
        Create a new Program with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'createdOn': None,
            'name': None,
            'parentToken': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "Program({date}, {token})".format(
            date=self.createdOn,
            token=self.token
        )


class Account(HyperwalletModel):
    '''
    The Account Model.

    :param data:
        A dictionary containing the attributes for the Account.
    '''

    def __init__(self, data):
        '''
        Create a new Account with the provided attributes.
        '''

        self.defaults = {
            'token': None,
            'createdOn': None,
            'type': None,
            'email': None
        }

        for (param, default) in self.defaults.items():
            setattr(self, param, data.get(param, default))

    def __repr__(self):
        return "Account({date}, {token})".format(
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
            'PREPAID_CARDS': PrepaidCard,
            'USERS': User
        }

        base, sub = wh_type.split('.')[:2]

        if sub in types:
            return types[sub](wh_object)
        elif base in types:
            return types[base](wh_object)

        return None
