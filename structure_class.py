import copy as _copy

# Define struct class
class struct (dict):
    """
    A class to implement MATLAB-like structures
    """

    def __repr__(self):
        """
        String representation of the struct
        """
        return "struct({})".format(super().__repr__())


    def __getattr__(self, field):
        """
        Gets value of a field
        """
        if field not in dir(self):
            if field in self.keys():
                return self[field]
            else:
                return None
        else:
            return None


    def __setattr__(self, field, value):
        """
        Sets value of a field
        """
        if field not in dir(self):
            self[field] = value
        else:
            return super().__setattr__(field, value)


    def fields(self):
        """
        Gets the list of defined fields of the struct
        """
        return list(self.keys())


    def remove_field(self, field):
        """
        Removes a field from the struct
        """
        if field in self.keys():
            del self[field]


    def add_field(self, field, value = None):
        """
        Adds a new field to the struct
        """
        if field not in self.keys():
            self[field] = value


    def copy(self):
        """
        Creates a shallow copy of the struct
        """
        self_copy = struct()
        for field in self.keys():
            if isinstance(self[field], struct):
                self_copy[field] = self[field].copy()
            else:
                self_copy[field] = _copy.copy(self[field])

        return self_copy


    def deepcopy(self):
        """
        Creates a deep copy of the struct
        """
        self_copy = struct()
        for field in self.keys():
            if isinstance(self[field], struct):
                self_copy[field] = self[field].deepcopy()
            else:
                self_copy[field] = _copy.deepcopy(self[field])

        return self_copy


    def repeat(self, n):
        """
        Repeats/replicates the struct to create an array of structs (eg. for initialization)
        """
        return [self.deepcopy() for i in range(n)]

