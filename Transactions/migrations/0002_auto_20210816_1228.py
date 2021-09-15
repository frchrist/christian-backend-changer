# Generated by Django 3.2.4 on 2021-08-16 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Currencies', '0002_auto_20210815_2058'),
        ('Transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='reference',
            field=models.CharField(default='AS-8374', max_length=20, unique=True, verbose_name='reference'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exchange',
            name='currencie',
            field=models.ForeignKey(help_text='designant whether client currencie is', on_delete=django.db.models.deletion.CASCADE, related_name='currencie', to='Currencies.currencies'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='devise',
            field=models.ForeignKey(help_text='designante whether this currencie which client want to buy', on_delete=django.db.models.deletion.CASCADE, related_name='devise', to='Currencies.currencies'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='recieve_amount',
            field=models.DecimalField(decimal_places=4, max_digits=6, verbose_name='recieve amount'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='send_amount',
            field=models.DecimalField(decimal_places=4, max_digits=6, verbose_name='send amount'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='state',
            field=models.CharField(choices=[('done', 'done'), ('pending', 'pending'), ('failed', 'failed')], help_text='Designante the status of current transaction', max_length=9, verbose_name='transaction status'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='to_wallet_address',
            field=models.CharField(max_length=100, verbose_name='reciever wallet address'),
        ),
    ]