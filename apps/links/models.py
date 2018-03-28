from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=120, null=False, blank=False)
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title


class Link(models.Model):
    category = models.ForeignKey(
        'Category', related_name='links', null=False, blank=False,
        on_delete=models.CASCADE)
    display_text = models.CharField(max_length=120, null=False, blank=False)
    external_link = models.CharField(max_length=400, null=False, blank=False)
    active = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('added_at',)

    def __str__(self):
        return '{}: {}'.format(self.category.title, self.display_text)
