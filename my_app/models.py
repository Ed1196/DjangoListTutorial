from django.db import models


# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search)

    def contains_kw_python(self):
        if 'python' in self.search:
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = "Searches"
