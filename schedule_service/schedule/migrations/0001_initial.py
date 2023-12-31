# Generated by Django 4.2.2 on 2023-08-01 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Airport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("airport_name", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=45)),
                ("status", models.CharField(default="Active", max_length=45)),
            ],
            options={"db_table": "airport",},
        ),
        migrations.CreateModel(
            name="Flight",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("flight_number", models.IntegerField()),
                ("seating_capacity", models.IntegerField()),
                ("status", models.CharField(default="Active", max_length=45)),
            ],
            options={"db_table": "flight",},
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("arrival_time", models.DateTimeField()),
                ("departure_time", models.DateTimeField()),
                ("available_seats", models.IntegerField()),
                ("base_price", models.FloatField()),
                ("status", models.CharField(default="Active", max_length=45)),
                (
                    "destination_airport",
                    models.ForeignKey(
                        db_column="destination_airport",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="destination_schedules",
                        to="schedule.airport",
                    ),
                ),
                (
                    "flight",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="schedule.flight",
                    ),
                ),
                (
                    "source_airport",
                    models.ForeignKey(
                        db_column="source_airport",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="source_schedules",
                        to="schedule.airport",
                    ),
                ),
            ],
            options={"db_table": "schedule",},
        ),
    ]
