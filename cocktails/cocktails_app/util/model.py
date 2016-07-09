class RealInstanceProvider(object):
    def get_actual_instance(self):
        # Check the cache
        if hasattr(self, '_actual_instance'):
            return self._actual_instance

        subclasses = self.__class__.__subclasses__()

        # If no subclasses, it is its own actual instance
        if not subclasses:
            self._actual_instance = getattr(self, self.__class__.__name__,
                                            self)
            return self._actual_instance

        else:
            subclasses_names = [sc.__name__.lower() for sc in subclasses]

            for subclass_name in subclasses_names:
                if hasattr(self, subclass_name):
                    self._actual_instance = getattr(
                        self, subclass_name, self).get_actual_instance()

                    return self._actual_instance

            self._actual_instance = self

            return self
