from django.core.management.base import BaseCommand
import csv
from geography.models import Country, City
from decimal import Decimal


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('docs/worldcities.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    self.stdout.write(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    country = Country.objects.filter(code=row[4]).first()
                    if country is None:
                        country = Country.objects.create(name=row[3], code=row[4])
                    City.objects.create(
                        name=row[0],
                        country=country,
                        latitude=Decimal(row[1]),
                        longitude=Decimal(row[2]),
                    )
                    line_count += 1
                    if line_count % 1000 == 0:
                        self.stdout.write(f'Processed {line_count} lines.')
            self.stdout.write(f'Processed {line_count} lines total.')
