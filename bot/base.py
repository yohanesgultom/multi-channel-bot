from abc import ABC, abstractmethod

class Base:
    @abstractmethod
    def reply(self, msg, user_id=None):
        """
        Get a reply for a message from given user_id
        Ideally user_id is used to identify unique session
        """
        pass

    def get_predicate(self, key, user_id=None):
        """
        Get a predicate (stored value) for given key in user_id session
        """
        pass

    def set_predicate(self, key, val, user_id=None):
        """
        Set a predicate (stored value) for given key with given value in user_id session
        """
        pass