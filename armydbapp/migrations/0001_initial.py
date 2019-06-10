# Generated by Django 2.1.5 on 2019-02-19 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArmyUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Punishment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Soldier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('soldier_id', models.IntegerField(unique=True)),
                ('service_start_date', models.DateField()),
                ('service_end_date', models.DateField()),
                ('is_at_vacation', models.BooleanField(default=False)),
                ('return_date', models.DateField()),
                ('is_rewarded', models.BooleanField()),
                ('reward_days', models.IntegerField(unique=True)),
                ('is_at_punishment', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SoldierAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SoldierArmyUnits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('army_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='armydbapp.ArmyUnit')),
                ('soldier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='armydbapp.Soldier')),
            ],
        ),
        migrations.CreateModel(
            name='SoldierPunishments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('punishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='armydbapp.Punishment')),
                ('soldier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='armydbapp.Soldier')),
            ],
        ),
    ]
