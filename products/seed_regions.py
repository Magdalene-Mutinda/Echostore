from products.models import Region

regions = [
    "Nairobi",
    "Mombasa",
    "Kisumu",
    "Nakuru",
    "Kiambu",
    "Machakos",
    "Kajiado",
    "Uasin Gishu",
    "Kericho",
    "Nyeri"
]

for name in regions:
    Region.objects.get_or_create(name=name)

print("✅ Regions added successfully!")
