from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_region_category_image_alter_category_name_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('region', models.ForeignKey(on_delete=models.CASCADE, to='products.region')),
            ],
        ),
    ]
