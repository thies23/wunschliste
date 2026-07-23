from django.db import models
from django.utils import timezone


class Wish(models.Model):
    name = models.CharField("Name des Schenkers", max_length=100, blank=True, null=True)
    title = models.CharField("Bezeichnung", max_length=200)
    description = models.TextField("Beschreibung", blank=True, null=True)
    link = models.URLField("Link", blank=True, null=True)
    image = models.ImageField("Bild", upload_to='wish_images/', blank=True, null=True, 
                             help_text="Produktbild hochladen")
    image_url = models.URLField("Bild-URL", blank=True, null=True, 
                               help_text="Alternativ: URL zum Produktbild")
    price = models.DecimalField("Preis", max_digits=10, decimal_places=2, 
                               default=0.00)
    urgency = models.IntegerField("Dringlichkeit", 
                                 choices=[(i, i) for i in range(1, 6)],
                                 default=3,
                                 help_text="1 = nicht so dringend, 5 = sehr dringend")
    is_available = models.BooleanField("Verfügbar", default=True)
    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    gifted_at = models.DateTimeField("Geschenkt am", blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Wunsch"
        verbose_name_plural = "Wünsche"
    
    def __str__(self):
        return self.title


class GiftTransaction(models.Model):
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE, related_name='transactions')
    giver_name = models.CharField("Name des Schenkers", max_length=100)
    gifted_at = models.DateTimeField("Geschenkt am", auto_now_add=True)
    is_reversed = models.BooleanField("Rückgängig gemacht", default=False)
    
    class Meta:
        ordering = ['-gifted_at']
        verbose_name = "Schenk-Transaktion"
        verbose_name_plural = "Schenk-Transaktionen"
    
    def __str__(self):
        return f"{self.giver_name} -> {self.wish.title}"