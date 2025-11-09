from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.http import HttpResponse
from django.shortcuts import render

from .models import Banner, Product, Order
from .serializers import BannerSerializer, ProductSerializer, OrderSerializer


# ✅ Root endpoint check
def index(request):
        return render(request, "readme.html")

# 🖼️ Banner Viewset
class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all().order_by('-created_at')
    serializer_class = BannerSerializer


# 👕 Product Viewset
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    # 🔹 Get all T-Shirts
    @action(detail=False, methods=['get'], url_path='tshirts')
    def get_tshirts(self, request):
        products = Product.objects.filter(category__iexact='tshirt').order_by('-created_at')
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # 🔹 Get all Sweatshirts
    @action(detail=False, methods=['get'], url_path='sweatshirts')
    def get_sweatshirts(self, request):
        products = Product.objects.filter(category__iexact='sweatshirt').order_by('-created_at')
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


# 🧾 Orders (COD + Online)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    # Allow PATCH (for payment verification or status updates)
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    # ✅ COD Order Creation
    @action(detail=False, methods=['post'], url_path='create-cod-order')
    def create_cod_order(self, request):
        """
        Create a Cash on Delivery (COD) order
        """
        data = request.data.copy()
        data["payment_method"] = "COD"

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "✅ COD Order placed successfully!",
                "order_id": serializer.instance.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # # 💳 Online Payment (Razorpay)
    # @action(detail=False, methods=['post'], url_path='create-razorpay-order')
    # def create_razorpay_order(self, request):
    #     """
    #     Create a Razorpay order for online payments.
    #     """
    #     data = request.data
    #
    #     try:
    #         amount = float(data.get("total_amount", 0)) * 100  # Convert to paisa
    #     except (TypeError, ValueError):
    #         return Response({"error": "Invalid amount"}, status=400)
    #
    #     if amount <= 0:
    #         return Response({"error": "Amount must be greater than 0"}, status=400)
    #
    #     # ✅ Initialize Razorpay Client
    #     try:
    #         client = razorpay.Client(
    #             auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    #         )
    #     except Exception as e:
    #         return Response({"error": f"Razorpay init failed: {str(e)}"}, status=500)
    #
    #     # ✅ Create Razorpay Order
    #     try:
    #         razorpay_order = client.order.create({
    #             "amount": int(amount),
    #             "currency": "INR",
    #             "payment_capture": 1
    #         })
    #     except razorpay.errors.BadRequestError as e:
    #         return Response({"error": f"Razorpay Error: {str(e)}"}, status=400)
    #     except Exception as e:
    #         return Response({"error": f"Unexpected Razorpay Error: {str(e)}"}, status=500)
    #
    #     # ✅ Create Pending Order in DB
    #     order = Order.objects.create(
    #         customer_name=data.get("customer_name"),
    #         email=data.get("email"),
    #         phone=data.get("phone"),
    #         address=data.get("address"),
    #         city=data.get("city"),
    #         pincode=data.get("pincode"),
    #         payment_method="ONLINE",
    #         total_amount=amount / 100,
    #         cart_data=data.get("cart_data", []),
    #         status="PENDING"
    #     )
    #
    #     # ✅ Return order info to frontend
    #     return Response({
    #         "message": "✅ Razorpay order created successfully!",
    #         "razorpay_order_id": razorpay_order["id"],
    #         "razorpay_key": settings.RAZORPAY_KEY_ID,  # dynamically sent
    #         "amount": amount,
    #         "currency": "INR",
    #         "order_db_id": order.id
    #     }, status=200)
    #
    # # 🔒 Verify Razorpay Payment
    # @action(detail=False, methods=['post'], url_path='verify-payment')
    # def verify_payment(self, request):
    #     """
    #     Verify payment signature from Razorpay
    #     """
    #     data = request.data
    #     client = razorpay.Client(
    #         auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    #     )
    #
    #     params_dict = {
    #         'razorpay_order_id': data.get('razorpay_order_id'),
    #         'razorpay_payment_id': data.get('razorpay_payment_id'),
    #         'razorpay_signature': data.get('razorpay_signature')
    #     }
    #
    #     try:
    #         # ✅ Verify signature
    #         client.utility.verify_payment_signature(params_dict)
    #
    #         # ✅ Mark order as VERIFIED
    #         order = Order.objects.get(id=data.get("order_db_id"))
    #         order.status = "VERIFIED"
    #         order.save()
    #
    #         return Response({"message": "✅ Payment verified successfully!"})
    #
    #     except razorpay.errors.SignatureVerificationError:
    #         return Response({"error": "Signature verification failed"}, status=400)
    #     except Order.DoesNotExist:
    #         return Response({"error": "Order not found"}, status=404)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=400)
