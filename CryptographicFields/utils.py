from django.db.models.lookups import StartsWith,FieldGetDbPrepValueMixin
class LengthError(Exception):
    def __init__(self,length) -> None:
        super().__init__(f"Length of Encryption Key is '{length}' which is less than '50'")

class StartsWith(FieldGetDbPrepValueMixin,StartsWith):
    pass