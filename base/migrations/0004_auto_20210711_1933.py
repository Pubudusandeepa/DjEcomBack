# Generated by Django 3.0.5 on 2021-07-11 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, default='/placeholder.png', max_length=200, null=True),
        ),
    ]
