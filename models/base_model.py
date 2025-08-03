""" model layer """
import uuid

def constructor(self, *args, **kwargs):
    """ constructor for all models """
    # Set object instance defaults
    self.id = str(uuid.uuid4())

    # Note that setattr will call the setters for attribs in the list
    if kwargs:
        for key, value in kwargs.items():
            if key in self.can_init:
                setattr(self, key, value)
