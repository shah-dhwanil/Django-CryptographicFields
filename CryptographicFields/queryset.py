class CryptographicQuerySet():
    def __init__(self,queryset) -> None:
        self.queryset=queryset
        return None
    def __iter__(self):
        return iter(self.queryset)
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.queryset)