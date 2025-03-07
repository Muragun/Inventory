# Generated by Django 4.2.19 on 2025-02-25 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invapp', '0002_remove_itemassociation_child_item_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemAssociation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_associations', to='invapp.inventoryitem', verbose_name='Дочерний предмет')),
                ('parent_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_associations', to='invapp.inventoryitem', verbose_name='Родительский предмет')),
            ],
            options={
                'verbose_name': 'Связь предметов',
                'verbose_name_plural': 'Связи предметов',
                'ordering': ['parent_item', 'child_item'],
                'unique_together': {('parent_item', 'child_item')},
            },
        ),
    ]
