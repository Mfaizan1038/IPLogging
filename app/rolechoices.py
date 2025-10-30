from django.db.models import TextChoices

class RoleChoice(TextChoices):
    Gold_user="Gold user"
    Bronze_user="Bronze user"
    Silver_user="Silver user"
    Unauthenticated_user="Unauthenticated user"
