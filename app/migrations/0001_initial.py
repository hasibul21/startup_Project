# Generated by Django 4.0 on 2022-01-03 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Investorinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('logo', models.ImageField(null=True, upload_to='images/')),
                ('establish_year', models.IntegerField(blank=True, null=True)),
                ('investor_type', models.CharField(blank=True, max_length=10, null=True)),
                ('employee_range', models.CharField(blank=True, max_length=10, null=True)),
                ('market_presence', models.CharField(blank=True, max_length=100, null=True)),
                ('lokking_at', models.CharField(blank=True, max_length=100, null=True)),
                ('tags', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('videos', models.FileField(null=True, upload_to='videos/')),
                ('weblink', models.URLField(blank=True, unique=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('team_member1', models.ImageField(null=True, upload_to='images/')),
                ('team_member2', models.ImageField(null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='StartupInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('logo', models.ImageField(null=True, upload_to='images/')),
                ('establish_year', models.IntegerField(blank=True, null=True)),
                ('business_model', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_range', models.CharField(blank=True, max_length=100, null=True)),
                ('market_presence', models.CharField(blank=True, max_length=100, null=True)),
                ('lokking_at', models.CharField(blank=True, max_length=100, null=True)),
                ('sector', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('videofile', models.FileField(null=True, upload_to='videos/')),
                ('weblink', models.URLField(blank=True, unique=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('team_member1', models.ImageField(null=True, upload_to='images/')),
                ('team_member2', models.ImageField(null=True, upload_to='images/')),
            ],
        ),
    ]
