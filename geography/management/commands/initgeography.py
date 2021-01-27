from django.core.management.base import BaseCommand
import csv
from geography.models import Country, City
from decimal import Decimal


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('extra/worldcities.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    self.stdout.write(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    qs = Country.objects.filter(code=row[4])
                    if qs.exists():
                        country = qs.first()
                    else:
                        country = Country.objects.create(title=row[3], code=row[4])
                    City.objects.create(
                        title=row[0],
                        country=country,
                        latitude=Decimal(row[1]),
                        longitude=Decimal(row[2]),
                    )
                    line_count += 1
                    if line_count % 1000 == 0:
                        self.stdout.write(f'Processed {line_count} lines.')
            self.stdout.write(f'Processed {line_count} lines total.')