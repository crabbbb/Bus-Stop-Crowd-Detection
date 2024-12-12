from django.db import models

class _TrueFalse (models.IntegerChoices) :
    ACTIVE = 0, 'ACTIVE'
    INACTIVE = 1, 'INACTIVE'