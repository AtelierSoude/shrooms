from rest_framework import mixins

class AltSerializerMixin(mixins.RetrieveModelMixin):
    serializer_class = None
    alt_serializer_class = None

    def retrieve(self, request, *args, **kwargs):
        """
        Override this method to define the logic to choose 
        between serializer and alt_serializer
        """
        return super(AltSerializerMixin, self).retrieve(request, *args, **kwargs)

    def get_alt_serializer(self, *args, **kwargs):
        """
        Return the **alternative** serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_alt_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_alt_serializer_class(self):
        """
        Return the class to use for the alternative serializer.
        Defaults to using `self.alt_serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.alt_serializer_class is not None, (
            "'%s' should either include a `alt_serializer_class` attribute, "
            "or override the `get_alt_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.alt_serializer_class
