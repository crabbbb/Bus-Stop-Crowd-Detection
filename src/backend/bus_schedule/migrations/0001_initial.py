# Generated by Django 3.1.12 on 2024-12-12 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AssignmentId', models.CharField(blank=True, max_length=5, null=True)),
                ('Time', models.TimeField()),
                ('DayOfWeek', models.IntegerField(choices=[(0, 'SUNDAY'), (1, 'MONDAY'), (2, 'TUESDAY'), (3, 'WEDNESDAY'), (4, 'THURSDAY'), (5, 'FRIDAY'), (6, 'SATURDAY')])),
                ('BusId', models.CharField(max_length=5)),
                ('RouteId', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'Assignment',
            },
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BusId', models.CharField(blank=True, max_length=5, null=True)),
                ('CarPlateNo', models.CharField(max_length=7)),
                ('Capacity', models.IntegerField()),
                ('IsActive', models.IntegerField(choices=[(0, 'ACTIVE'), (1, 'INACTIVE')], default=0)),
            ],
            options={
                'db_table': 'Bus',
            },
        ),
        migrations.CreateModel(
            name='BusStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StationId', models.CharField(blank=True, max_length=5, null=True)),
                ('StationName', models.CharField(max_length=255)),
                ('IsActive', models.BooleanField()),
            ],
            options={
                'db_table': 'BusStation',
            },
        ),
        migrations.CreateModel(
            name='BusTrackingLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ArrivalDateTime', models.DateTimeField(blank=True, null=True)),
                ('AssignmentId', models.CharField(max_length=5)),
                ('BusStatus', models.CharField(choices=[('HA', 'HAVENT ARRIVE'), ('A', 'ARRIVE'), ('D', 'DROPING'), ('R', 'RESTING'), ('W', 'WAITING')], max_length=5)),
                ('BusCapacityEstimate', models.CharField(blank=True, choices=[('E', 'EMPTY'), ('L', 'LOW'), ('M', 'MODERATE'), ('AF', 'ALMOST FULL'), ('F', 'FULL')], max_length=5, null=True)),
            ],
            options={
                'db_table': 'BusTrackingLog',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RouteId', models.CharField(blank=True, max_length=5, null=True)),
                ('RouteDescription', models.TextField(blank=True, null=True)),
                ('RouteDuration', models.IntegerField()),
                ('FromCampus', models.BooleanField()),
                ('IsActive', models.BooleanField()),
            ],
            options={
                'db_table': 'Route',
            },
        ),
        migrations.CreateModel(
            name='RouteStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StationId', models.CharField(max_length=5)),
                ('RouteId', models.CharField(max_length=5)),
                ('RouteOrder', models.IntegerField()),
            ],
            options={
                'db_table': 'RouteStation',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ScheduleId', models.CharField(blank=True, max_length=5, null=True)),
                ('IsActive', models.BooleanField()),
                ('CreateAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Schedule',
            },
        ),
        migrations.CreateModel(
            name='ScheduleAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ScheduleId', models.CharField(max_length=5)),
                ('AssignmentId', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'ScheduleAssignment',
            },
        ),
    ]
