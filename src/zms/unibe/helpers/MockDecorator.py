class MockDecorator:
    def __call__(self, func):
        return func

    def apply(self, *args, **kwargs):
        return lambda func: func