from django.db import models
import django_tables2 as tables

class Details(models.Model):
    company = models.TextField(db_column='Company', null=True,
                               verbose_name = 'API Company')
    provider = models.TextField(db_column='Provider', null=True,
                                verbose_name = 'API Provider Page')
    homepage = models.TextField(db_column='Homepage', null=True,
                                verbose_name = 'API Homepage')
    category = models.CharField(max_length=50, db_column='Category', null=True,
                                verbose_name='Primary Category')

    def __str__(self):
        return "%s, %s, %s, %s" % (self.company, self.provider, self.homepage,
                                   self.category)

class DetailsTable(tables.Table):
    homepage = tables.TemplateColumn('<a href="{{record.homepage}}">{{record.homepage}}</a>')
    provider = tables.TemplateColumn('<a href="{{record.provider}}">{{record.provider}}</a>')
    class Meta:
        model = Details
        fields = ('company', 'provider', 'homepage', 'category')