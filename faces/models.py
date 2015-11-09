from django.db import models

class Face(models.Model):
    year = models.IntegerField(default=0)
    stage_num = models.IntegerField(default=0)
    gradient = models.FloatField(default=0)
    img_name = models.CharField(max_length=200)

    def __str__(self):
        return self.img_name
    
