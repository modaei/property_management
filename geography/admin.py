from django.contrib import admin
from .models import Country, City


class CityAdmin(admin.ModelAdmin):
    model = City
    # list_display = (
    #     'title', 'origin_country', 'origin_city', 'destination_country', 'destination_city', 'create_date')
    # list_filter = ('validation_type',)
    search_fields = ('country__title',)
    # ordering = ('create_date',)
    # fields = (
    #     'id', 'slug', 'title', 'user', 'origin_country', 'origin_city', 'destination_country', 'destination_city',
    #     'payment_method', 'delivery_method', 'create_date', 'contact_methods', 'description')
    # inlines = ()
    # readonly_fields = ('id', 'create_date', 'update_date')


admin.site.register(Country)
admin.site.register(City, CityAdmin)
