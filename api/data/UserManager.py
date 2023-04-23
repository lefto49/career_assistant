from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create(self, email, password, **validated_data):
        user = self.model(email=self.normalize_email(email), **validated_data)
        user.set_password(password)

        user.save()
        return user