from mongoengine import Document, EmailField, StringField, BooleanField, DateTimeField
from datetime import datetime
from bcrypt import checkpw


class BistroUser(Document):
    """
    Customize Bistro  user 
    """
    email = EmailField(verbose_name='email address', max_length=255, unique=True)
    username = StringField(verbose_name='username', blank=False, max_length=150)
    password = StringField(verbose_name='password', blank=False, max_length=128)
    theme = StringField(blank=True, max_length=20)
    staff = BooleanField(blank=False, default=False)  # a admin user; non super-user
    admin = BooleanField(blank=False, default=False)  # a superuser
    date_joined = DateTimeField(default=datetime.now(), verbose_name='date joined')
    last_login = DateTimeField(blank=True, verbose_name='last login')
    is_authenticated = BooleanField(blank=False, default=False)

    # meta = {
    #     'db_alias': 'bistrodb',
    # }

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_active(self):
        "Is the user active"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_json(self):
        return {
            "id": str(self.pk),
            "email": self.email,
            "username": self.username,
            "theme": self.theme,
            "staff": self.staff,
            "admin": self.admin,
            "last_login": self.last_login.strftime("%Y/%m/%d %H:%M:%S"),
        }
