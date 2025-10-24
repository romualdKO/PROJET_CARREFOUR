# Generated manually to fix Vente model references
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CarrefourApp', '0016_merge_20251023_0853'),
    ]

    operations = [
        # Cette migration ne fait rien mais force Django à recharger les références
        migrations.AlterField(
            model_name='utilisationcoupon',
            name='vente',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='CarrefourApp.Vente'  # Majuscule correct
            ),
        ),
        migrations.AlterField(
            model_name='lignevente',
            name='vente',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='lignes',
                to='CarrefourApp.Vente'  # Majuscule correct
            ),
        ),
    ]
