from django.db import transaction
from django.db.models import Sum, Avg, Q, F

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Room, Booking, Payment, Service, BookingService, Discount, Review

from .serializers import UserSerializer, RoomSerializer, BookingSerializer, PaymentSerializer, ServiceSerializer, BookingServiceSerializer, DiscountSerializer, ReviewSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from datetime import datetime


class StatisticsView(APIView):
    def get(self, request):
        total_users = User.objects.count()
        total_bookings = Booking.objects.count()
        total_payments = Payment.objects.aggregate(total_amount=Sum('amount'))['total_amount']
        average_room_price = Room.objects.aggregate(average_price=Avg('price'))['average_price']
        total_services = Service.objects.count()
        total_booking_services = BookingService.objects.count()
        total_discounts = Discount.objects.count()
        total_reviews = Review.objects.count()
        average_rating = Review.objects.aggregate(average_rating=Avg('rating'))['average_rating']

        statistics = {
            'total_users': total_users,
            'total_bookings': total_bookings,
            'total_payments': total_payments,
            'average_room_price': average_room_price,
            'total_services': total_services,
            'total_booking_services': total_booking_services,
            'total_discounts': total_discounts,
            'total_reviews': total_reviews,
            'average_rating': average_rating,
        }
        return Response(statistics)


class RoomFilterView(APIView):
    def get(self, request):
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        search_term = request.GET.get('search_term', '')

        filters = Q()

        if min_price:
            filters &= Q(price__gte=min_price)

        if max_price:
            filters &= Q(price__lte=max_price)

        if search_term:
            filters &= Q(room_number__icontains=search_term) | Q(room_type__icontains=search_term)

        rooms = Room.objects.filter(filters)

        room_list = [{
            'room_id': room.room_id,
            'room_number': room.room_number,
            'room_type': room.room_type,
            'price': room.price,
            'availability': room.availability
        } for room in rooms]

        return Response(room_list)


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()


        user_id = request.query_params.get('user_id')
        if user_id:
            users = users.filter(user_id=user_id)


        email = request.query_params.get('email')
        if email:
            users = users.filter(email=email)


        surname = request.query_params.get('surname')
        if surname:
            users = users.filter(surname__icontains=surname)


        name = request.query_params.get('name')
        if name:
            users = users.filter(name__icontains=name)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, user_id):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateRoomAvailabilityAPIView(APIView):
    def post(self, request):
        try:
            booking_id = request.data.get('booking_id')

            # Знайти кількість заброньованих кімнат за заданим ідентифікатором бронювання
            booked_rooms_count = BookingService.objects.filter(booking_id=booking_id).count()

            # Оновити кількість доступних кімнат за допомогою F-виразу
            Room.objects.update(availability=F('availability') - booked_rooms_count)

            return Response("Кількість доступних кімнат оновлена успішно", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Помилка під час оновлення кількості доступних кімнат: {str(e)}",
                            status=status.HTTP_400_BAD_REQUEST)


class RoomListView(APIView):
    def get(self, request):
        rooms = Room.objects.all()

        room_number = request.query_params.get('room_number')
        if room_number:
            rooms = rooms.filter(room_number=room_number)


        room_type = request.query_params.get('room_type')
        if room_type:
            rooms = rooms.filter(room_type=room_type)


        price_lte = request.query_params.get('price_lte')
        if price_lte:
            rooms = rooms.filter(price__lte=price_lte)


        price_gte = request.query_params.get('price_gte')
        if price_gte:
            rooms = rooms.filter(price__gte=price_gte)


        availability = request.query_params.get('availability')
        if availability is not None:
            rooms = rooms.filter(availability=availability)

        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class RoomDetailView(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(room_id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def post(self, request, room_id):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, room_id):
        try:
            room = Room.objects.get(room_id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomCreateView(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateBookingView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            room_id = request.data.get('room_id')
            amount = request.data.get('amount')
            payment_method = request.data.get('payment_method')

            # Створення нового бронювання
            booking = Booking(
                booking_date=datetime.now(),
                check_in_date=request.data.get('check_in_date'),
                check_out_date=request.data.get('check_out_date'),
                user_id=user_id,
                room_id=room_id
            )
            booking.save()

            # Створення платежу для цього бронювання
            payment = Payment(
                amount=amount,
                date=datetime.now(),
                payment_method=payment_method,
                booking=booking
            )
            payment.save()

            return Response({'message': 'Booking and payment created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookingListView(APIView):
    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request):
        bookings = Booking.objects.all()


        booking_date = request.query_params.get('booking_date')
        if booking_date:
            bookings = bookings.filter(booking_date=booking_date)


        check_in_date = request.query_params.get('check_in_date')
        if check_in_date:
            bookings = bookings.filter(check_in_date=check_in_date)


        check_out_date = request.query_params.get('check_out_date')
        if check_out_date:
            bookings = bookings.filter(check_out_date=check_out_date)


        user_id = request.query_params.get('user_id')
        if user_id:
            bookings = bookings.filter(user_id=user_id)


        room_id = request.query_params.get('room_id')
        if room_id:
            bookings = bookings.filter(room_id=room_id)

        bookings = bookings.select_related('user', 'room')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class BookingDetailView(APIView):
    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def post(self, request, booking_id):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, booking_id):
        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PaymentListView(APIView):
    def get(self, request):
        payments = Payment.objects.all()


        amount = request.query_params.get('amount')
        if amount:
            payments = payments.filter(amount=amount)


        date = request.query_params.get('date')
        if date:
            payments = payments.filter(date=date)


        payment_method = request.query_params.get('payment_method')
        if payment_method:
            payments = payments.filter(payment_method=payment_method)


        booking_id = request.query_params.get('booking_id')
        if booking_id:
            payments = payments.filter(booking_id=booking_id)

        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class PaymentDetailView(APIView):
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(payment_id=payment_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    def post(self, request, payment_id):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, payment_id):
        try:
            payment = Payment.objects.get(payment_id=payment_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()


        name = request.query_params.get('name')
        if name:
            services = services.filter(name__icontains=name)


        price = request.query_params.get('price')
        if price:
            services = services.filter(price=price)

        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class ServiceDetailView(APIView):
    def get(self, request, service_id):
        try:
            service = Service.objects.get(service_id=service_id)
        except Service.DoesNotExist:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def post(self, request, service_id):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_id):
        try:
            service = Service.objects.get(service_id=service_id)
        except Service.DoesNotExist:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookingServiceListView(APIView):
    def get(self, request):
        booking_services = BookingService.objects.all()


        booking_id = request.query_params.get('booking_id')
        if booking_id:
            booking_services = booking_services.filter(booking_id=booking_id)


        service_id = request.query_params.get('service_id')
        if service_id:
            booking_services = booking_services.filter(service_id=service_id)


        quantity = request.query_params.get('quantity')
        if quantity:
            booking_services = booking_services.filter(quantity=quantity)


        date_time = request.query_params.get('date_time')
        if date_time:
            booking_services = booking_services.filter(date_time=date_time)

        serializer = BookingServiceSerializer(booking_services, many=True)
        return Response(serializer.data)


class BookingServiceDetailView(APIView):
    def get(self, request, booking_service_id):
        try:
            booking_service = BookingService.objects.get(booking_service_id=booking_service_id)
        except BookingService.DoesNotExist:
            return Response({"error": "Booking Service not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingServiceSerializer(booking_service)
        return Response(serializer.data)

    def post(self, request, booking_service_id):
        serializer = BookingServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, booking_service_id):
        try:
            booking_service = BookingService.objects.get(booking_service_id=booking_service_id)
        except BookingService.DoesNotExist:
            return Response({"error": "Booking Service not found"}, status=status.HTTP_404_NOT_FOUND)
        booking_service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DiscountListView(APIView):
    def get(self, request):
        discounts = Discount.objects.all()


        name = request.query_params.get('name')
        if name:
            discounts = discounts.filter(name__icontains=name)


        description = request.query_params.get('description')
        if description:
            discounts = discounts.filter(description__icontains=description)


        percentage = request.query_params.get('percentage')
        if percentage:
            discounts = discounts.filter(percentage=percentage)


        service_name = request.query_params.get('service_name')
        if service_name:
            discounts = discounts.filter(services__name__icontains=service_name)


        discounts = discounts.prefetch_related('services')
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)


class DiscountDetailView(APIView):
    def get(self, request, discount_id):
        try:
            discount = Discount.objects.get(discount_id=discount_id)
        except Discount.DoesNotExist:
            return Response({"error": "Discount not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiscountSerializer(discount)
        return Response(serializer.data)

    def post(self, request, discount_id):
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, discount_id):
        try:
            discount = Discount.objects.get(discount_id=discount_id)
        except Discount.DoesNotExist:
            return Response({"error": "Discount not found"}, status=status.HTTP_404_NOT_FOUND)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListView(APIView):
    def get(self, request):
        reviews = Review.objects.all()


        rating = request.query_params.get('rating')
        if rating:
            reviews = reviews.filter(rating=rating)


        user_id = request.query_params.get('user_id')
        if user_id:
            reviews = reviews.filter(user_id=user_id)


        booking_id = request.query_params.get('booking_id')
        if booking_id:
            reviews = reviews.filter(booking_id=booking_id)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewDetailView(APIView):
    def get(self, request, review_id):
        try:
            review = Review.objects.get(review_id=review_id)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def post(self, request, review_id):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(review_id=review_id)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)