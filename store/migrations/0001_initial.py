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
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("image_url", models.URLField(blank=True)),
                ("stock", models.PositiveIntegerField(default=10)),
                ("category", models.CharField(blank=True, max_length=100)),
                ("featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-featured", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=30)),
                ("address", models.TextField()),
                ("city", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=20)),
                ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("processing", "Processing"), ("shipped", "Shipped"), ("delivered", "Delivered"), ("cancelled", "Cancelled")], default="pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=200)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="store.order")),
                ("product", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="store.product")),
            ],
        ),
    ]
