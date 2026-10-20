from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user, empty in v1 Stage A.

    Declared from day one (SD-4/SA-3) so swapping behaviour later never needs a
    painful user-table migration. Roles (admin vs owner/family) are added as
    groups in Slice B0; no extra fields are needed in v1.
    """

    pass
