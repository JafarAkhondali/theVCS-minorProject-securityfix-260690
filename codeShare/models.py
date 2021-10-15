from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.utils import timezone

# data related to codes
class Code(models.Model):
    codeId = models.TextField(primary_key=True)
    codeName = models.CharField(max_length=10, default="untitled")
    codeSettings = models.JSONField()
    dateOfCreation = models.DateTimeField(default=datetime.now(tz=timezone.utc))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    lastEditTime = models.DateTimeField(default=datetime.now(tz=timezone.utc))
    driveId = models.TextField(unique=True)

    @classmethod
    def create(cls, pkey, codeName, codeSettings, owner, driveId):
        code = cls(codeId=pkey, codeName=codeName, codeSettings=codeSettings, owner=owner, driveId=driveId)
        code.save()
        return code
    
    def __str__(self):
        return self.codeName

