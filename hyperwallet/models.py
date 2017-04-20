class HyperwalletModel(object):
    '''
    The base Hyperwallet Model from which all other models will inherit.

    :param data: The username of this API user. **REQUIRED**
    '''

    def __init__(self, data):
        '''
        Create an instance of the base HyperwalletModel.
        '''
        for key in data:
            setattr(self, key, data.get(key))


class Webhook(HyperwalletModel):

    def __repr__(self):
        return "Webhook(token={token}, \
                        type={type}, \
                        createdOn='{createdOn}')".format(
                            token=self.token,
                            type=self.type,
                            createdOn=self.createdOn
                        )
