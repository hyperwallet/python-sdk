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
        return "User({token}, {date}, {id})".format(
            token=self.token,
            date=self.createdOn,
            id=self.clientUserId
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

    def __repr__(self):
        return "Webhook({token}, {date}, {type})".format(
            token=self.token,
            date=self.createdOn,
            type=self.type
        )
