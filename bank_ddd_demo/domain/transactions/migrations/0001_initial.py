# Generated by Django 3.1.6 on 2021-02-06 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('client_id', models.UUIDField()),
                ('submission_datetime', models.DateTimeField()),
                ('transaction_type', models.CharField(choices=[('D', 'Deposit'), ('W', 'Withdrawal')], max_length=1)),
                ('amount', models.DecimalField(decimal_places=20, max_digits=40)),
            ],
        ),
    ]
