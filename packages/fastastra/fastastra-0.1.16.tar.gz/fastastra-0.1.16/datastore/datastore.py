from abc import ABC, abstractmethod


class DataStore(ABC):
    @abstractmethod
    def setupEndpoints(self, app):
        """
        Sets up the app endpoints given existing tables available in the datastore.
        """
        raise NotImplementedError


    def setupSession(self, token, dbid):
        """
        Sets up the datastore session given a token.
        """
        raise NotImplementedError

    def getSubApp(self):
        """
        Sets up the datastore session given a token.
        """
        raise NotImplementedError
