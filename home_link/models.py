from django.db import models

# Create your models here.

class GradeInfo(models.Model):
    name = models.CharField(max_length=100)

    subsection = models.CharField(max_length=15, verbose_name='分段')
    sec_num = models.CharField(max_length=15, verbose_name='段内人数')
    sum = models.CharField(max_length=15, verbose_name='累计人数')

    add_date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")

    def __str__(self):
        return "{}-{}-{}".format(self.subsection, self.sec_num, self.sum)

    class Meta:
        verbose_name = "黑龙江省高考理科成绩一分一段表"


#class Grade(models.Model):
 #   name = models.CharField(max_length=20)
  #  rank = models.CharField(max_length=15, verbose_name='排名')
