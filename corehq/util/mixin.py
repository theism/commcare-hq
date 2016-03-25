import uuid


class UUIDGeneratorException(Exception):
    pass


class UUIDGeneratorMixin(object):
    """
    Automatically generates uuids on __init__ if not generated yet.

    To use: Add this mixin to your model as the left-most class being inherited from
    and list all field names in UUIDS_TO_GENERATE to generate uuids for.

    NOTE: Where possible, a UUIDField should be used instead of this mixin. But
    this is needed in cases where migrating a char field to a UUIDField is
    not possible because some of the existing uuids don't match the
    UUIDField format constraints.
    """

    def __init__(self, *args, **kwargs):
        super(UUIDGeneratorMixin, self).__init__(*args, **kwargs)

        field_names = getattr(self, 'UUIDS_TO_GENERATE', [])
        if not field_names:
            raise UUIDGeneratorException("Expected UUIDS_TO_GENERATE to not be empty")

        for field_name in field_names:
            value = getattr(self, field_name)
            if not value:
                setattr(self, field_name, uuid.uuid4().hex)