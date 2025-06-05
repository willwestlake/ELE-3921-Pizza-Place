from django.contrib import admin
from .models import Size, Topping, Pizza, Drink, Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pizza', 'size', 'created_at', 'get_toppings', 'get_drinks')
    list_filter = ('created_at',)
    search_fields = ('id', 'user__username', 'pizza__name')

    def get_toppings(self, obj):
        return ", ".join([t.name for t in obj.topping.all()])
    get_toppings.short_description = "Toppings"
 
    def get_drinks(self, obj):
        return ", ".join([d.name for d in obj.drink.all()])
    get_drinks.short_description = "Drinks"

admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Drink)
