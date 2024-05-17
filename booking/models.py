from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.surname}, {self.name}, {self.phone}"

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=50, unique=True, db_index=True)
    room_type = models.CharField(max_length=50, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField()

    def __str__(self):
        return f"Room {self.room_number}, price: {self.price}"

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateTimeField(db_index=True)
    check_in_date = models.DateTimeField(db_index=True)
    check_out_date = models.DateTimeField(db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, db_index=True)


    def __str__(self):
        return f"Booking ID: {self.booking_id}, User: {self.user}, Room: {self.room}"

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    payment_method = models.CharField(max_length=255)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment ID: {self.payment_id}, payment method: {self.payment_method}, date: {self.date}"

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Service ID: {self.service_id}, name: {self.name}, price: {self.price}"

class BookingService(models.Model):
    booking_service_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_time = models.DateTimeField()

    def __str__(self):
        return f"Booking Service ID: {self.booking_service_id}"

class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(db_index=True)
    percentage = models.FloatField()
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    rating = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review ID: {self.review_id}, rating: {self.rating}, user: {self.user}"


