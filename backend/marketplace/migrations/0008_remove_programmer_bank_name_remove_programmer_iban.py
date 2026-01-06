from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0007_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programmer',
            name='bank_name',
        ),
        migrations.RemoveField(
            model_name='programmer',
            name='iban',
        ),
    ]
