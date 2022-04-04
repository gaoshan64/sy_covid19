# Generated by Django 4.0.3 on 2022-04-03 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ann', '0005_alter_article_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_now', models.CharField(max_length=30, verbose_name='现在住址')),
                ('article_relatived', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='about_patient', to='ann.article', verbose_name='相关报告')),
            ],
        ),
    ]