from django.core.management.base import BaseCommand
from store.models import Product

PRODUCTS = [
    {
        "name": "Classic White Sneakers",
        "slug": "classic-white-sneakers",
        "description": "Clean everyday sneakers with a comfortable sole and minimal design.",
        "price": "2499.00",
        "category": "Fashion",
        "stock": 20,
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Wireless Headphones",
        "slug": "wireless-headphones",
        "description": "Comfortable wireless headphones with immersive sound and a long-lasting battery.",
        "price": "3999.00",
        "category": "Electronics",
        "stock": 15,
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Smart Watch",
        "slug": "smart-watch",
        "description": "Modern smartwatch for notifications, fitness tracking and everyday convenience.",
        "price": "5499.00",
        "category": "Electronics",
        "stock": 12,
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Travel Backpack",
        "slug": "travel-backpack",
        "description": "Spacious backpack with laptop compartment and multiple organizer pockets.",
        "price": "1899.00",
        "category": "Accessories",
        "stock": 25,
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Minimal Desk Lamp",
        "slug": "minimal-desk-lamp",
        "description": "Elegant desk lamp that gives your workspace a warm, focused glow.",
        "price": "1299.00",
        "category": "Home",
        "stock": 18,
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Ceramic Coffee Mug",
        "slug": "ceramic-coffee-mug",
        "description": "Simple ceramic mug for coffee, tea and your favorite hot drinks.",
        "price": "499.00",
        "category": "Home",
        "stock": 40,
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Classic Sunglasses",
        "slug": "classic-sunglasses",
        "description": "Timeless sunglasses with a lightweight frame for everyday wear.",
        "price": "999.00",
        "category": "Accessories",
        "stock": 30,
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Cotton Hoodie",
        "slug": "cotton-hoodie",
        "description": "Soft cotton-blend hoodie designed for comfortable casual wear.",
        "price": "1599.00",
        "category": "Fashion",
        "stock": 22,
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=900&q=80",
    },
]

class Command(BaseCommand):
    help = "Create or update demo products."

    def handle(self, *args, **options):
        for data in PRODUCTS:
            slug = data.pop("slug")
            Product.objects.update_or_create(slug=slug, defaults=data)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(PRODUCTS)} products."))
