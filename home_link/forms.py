from django import forms

YEAR_CHOICES = (
    ("#/", "请选择年份"),
    ('https://www.ynpxrz.com/n1456209c1599.aspx', '2016年'),
    ('http://www.zizzs.com/c/201706/17861.html', '2017年'),
    ('http://www.gaosan.com/gaokao/217808.html', '2018年'),
    ('https://www.gjw.cn/GaoKaoZiXun/964809-2.html', '2019年'),
    ('http://www.gaosan.com/gaokao/64218.html', '2020年'))


class GradeChoiceForm(forms.Form):
    url = forms.CharField(label="", widget=forms.Select(choices=YEAR_CHOICES))

class Grade(forms.Form):
    yc = forms.CharField(min_length=1, max_length=3, label="")