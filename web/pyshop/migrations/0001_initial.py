# Generated by Django 3.0.5 on 2020-07-25 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('category', models.CharField(choices=[('s', 'shirt'), ('sw', 'sportswear'), ('ow', 'outwear')], max_length=2)),
                ('photo', models.ImageField(upload_to='images')),
                ('price_is', models.FloatField()),
                ('describtion', models.TextField()),
                ('price_was', models.FloatField()),
            ],
        ),
    ]
