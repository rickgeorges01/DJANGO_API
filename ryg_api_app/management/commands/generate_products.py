from django.core.management.base import BaseCommand
from ryg_api_app.models import Product
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Génère 1000 produits aléatoires dans la base de données'

    def handle(self, *args, **kwargs):
        fake = Faker()
        produits = []

        for _ in range(5000):
            name = fake.word().capitalize() + " " + fake.word().capitalize()
            price = round(random.uniform(10, 2000), 2)
            description = fake.sentence()

            produit = Product(name=name, price=price, description=description)
            produits.append(produit)

        Product.objects.bulk_create(produits)
        self.stdout.write(self.style.SUCCESS('5000 produits ajoutés avec succès !'))
