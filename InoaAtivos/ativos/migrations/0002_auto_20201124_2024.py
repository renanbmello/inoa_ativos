# Generated by Django 3.1.3 on 2020-11-24 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ativos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='ativo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
