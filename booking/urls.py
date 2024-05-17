from django.urls import path, include
from .views import UserListView, RoomListView, BookingListView, PaymentListView, ServiceListView, \
    BookingServiceListView, DiscountListView, ReviewListView, UserDetailView, RoomDetailView, BookingDetailView, \
    PaymentDetailView, ServiceDetailView, BookingServiceDetailView, DiscountDetailView, ReviewDetailView, \
    RoomCreateView, StatisticsView, RoomFilterView, CreateBookingView, UpdateRoomAvailabilityAPIView

urlpatterns = [

    #statistics
    path('statistic/', StatisticsView.as_view(), name='statistics'),

    path('rooms/filter/', RoomFilterView.as_view(), name='room_filter'),

    #Використання Silk
    path('silk/', include('silk.urls', namespace='silk')),


    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),


    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:room_id>/', RoomDetailView.as_view(), name='room-detail'),
    path('room/', RoomCreateView.as_view(), name='room_create'),
    path('update_room_availability/', UpdateRoomAvailabilityAPIView.as_view(), name='update_room_availability'),

    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:booking_id>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/create/', CreateBookingView.as_view(), name='create_booking'),


    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/<int:payment_id>/', PaymentDetailView.as_view(), name='payment-detail'),


    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:service_id>/', ServiceDetailView.as_view(), name='service-detail'),


    path('booking-services/', BookingServiceListView.as_view(), name='booking-services-list'),
    path('booking-services/<int:booking_service_id>/', BookingServiceDetailView.as_view(),
         name='booking-service-detail'),


    path('discounts/', DiscountListView.as_view(), name='discount-list'),
    path('discounts/<int:discount_id>/', DiscountDetailView.as_view(), name='discount-detail'),



    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
]