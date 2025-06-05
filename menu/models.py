from django.db import models
from django.contrib.auth.models import User

class Size(models.Model):
    name = models.CharField(max_length=20) #small, med , large , extra large

    def __str__(self):
        return f"{self.name}"


class Topping(models.Model):
        name = models.CharField(max_length=20)
        size = models.ForeignKey(Size, on_delete=models.CASCADE)
        price = models.DecimalField(max_digits=5, decimal_places=2)

        def __str__(self):
            return f"{self.name} - {str(self.price)}"

    
class Pizza(models.Model):
    name = models.CharField(max_length = 50)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.size.name}) - {self.price}"


class Drink(models.Model):
    name = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - {str(self.price)} - {self.size}"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    topping = models.ManyToManyField(Topping)
    drink = models.ManyToManyField(Drink, blank=True)  
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        toppings = ", ".join([t.name for t in self.topping.all()])
        drinks = ", ".join([d.name for d in self.drink.all()])
        return f"{self.pizza.name} - {self.size.name} - {self.created_at} - Toppings: {toppings} - Drinks: {drinks}"



