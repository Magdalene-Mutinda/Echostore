from products.models import Region, City


region_cities = {
    "Nairobi": ["Westlands", "Kasarani", "Langata", "Embakasi", "Dagoretti"],
    "Mombasa": ["Nyali", "Likoni", "Changamwe", "Kisauni"],
    "Kisumu": ["Kisumu Central", "Kisumu East", "Kisumu West"],
    "Nakuru": ["Nakuru Town East", "Nakuru Town West", "Naivasha"],
    "Kiambu": ["Thika", "Ruiru", "Limuru", "Githunguri"],
    "Machakos": ["Machakos Town", "Kangundo", "Mwala"],
    "Kajiado": ["Kajiado Town", "Kitengela", "Ngong"],
    "Uasin Gishu": ["Eldoret East", "Eldoret West", "Turbo"],
    "Kericho": ["Kericho Town", "Litein", "Kipkelion"],
    "Nyeri": ["Nyeri Town", "Othaya", "Karatina"],
}

for region_name, cities in region_cities.items():
    try:
        region = Region.objects.get(name=region_name)  # exact match
        for city_name in cities:
            city, created = City.objects.get_or_create(name=city_name, region=region)
            if created:
                print(f"Added city '{city_name}' to region '{region_name}'")
            else:
                print(f"City '{city_name}' already exists in '{region_name}'")
    except Region.DoesNotExist:
        print(f"Region '{region_name}' not found in database.")

print("\nCity seeding completed!")
