from django.db import models

class Test(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text