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


class Webhook(HyperwalletModel):

    def __init__(self, data):
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
            type=self.type,
            date=self.createdOn
        )
