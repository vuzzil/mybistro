from django.db import models


class BistroMenu(models.Model):
    # _id = models.CharField(max_length=24,auto_created=True, primary_key=True)
    menuid = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=2, blank=False, default='')
    title = models.CharField(max_length=20, blank=False, default='')
    price = models.IntegerField()
    desc = models.CharField(max_length=200, blank=False, default='')
    image = models.CharField(max_length=100, blank=False, default='')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['menuid']
