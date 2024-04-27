from django.contrib import admin
from .models import User, Room, Booking, Payment, Service, BookingService, Discount, Review

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Service)
admin.site.register(BookingService)
admin.site.register(Discount)
admin.site.register(Review)

