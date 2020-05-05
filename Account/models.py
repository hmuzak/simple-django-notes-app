from django.db import models

# Create your models here.

class Note(models.Model):
    user    = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="notes")
    title   = models.CharField(max_length=40, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    hour    = models.TimeField(verbose_name="Hour", auto_now_add=True)
    date    = models.DateField(verbose_name="Date", auto_now_add=True)

    def __str__(self):
        return self.title
