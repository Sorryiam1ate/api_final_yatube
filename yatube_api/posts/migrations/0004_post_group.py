import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='posts.group'),
            preserve_default=False,
        ),
    ]
