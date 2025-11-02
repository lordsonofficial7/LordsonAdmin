from django.contrib import admin
from django import forms

from .models import Banner, Product, ProductImage, Order


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')


class ProductForm(forms.ModelForm):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2X Large'),
    ]

    sizes = forms.MultipleChoiceField(
        choices=SIZE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('title', 'category', 'price', 'discount', 'final_price', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    readonly_fields = ('final_price',)
    inlines = [ProductImageInline]

#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ("id", "customer_name", "phone", "total_amount", "payment_method", "status", "created_at")
#     list_filter = ("status", "payment_method", "created_at")
#     search_fields = ("customer_name", "phone", "email")
#
#     # allows admin to update order status easily
#     list_editable = ("status",)



# admin.py
from django.contrib import admin
from .models import Order
from openpyxl import Workbook
from django.http import HttpResponse
import datetime
import json


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "phone",
        "total_amount",
        "payment_method",
        "status",
        "created_at",
    )
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("customer_name", "phone", "email")
    list_editable = ("status",)

    actions = ["export_to_excel"]

    def export_to_excel(self, request, queryset):
        """
        Export selected orders to an Excel file
        """
        wb = Workbook()
        ws = wb.active
        ws.title = "Orders"

        # Define Excel headers
        headers = [
            "Order ID",
            "Customer Name",
            "Email",
            "Phone",
            "Address",
            "City",
            "Pincode",
            "Payment Method",
            "Total Amount",
            "Status",
            "Created At",
            "Products",
        ]
        ws.append(headers)

        # Add data rows
        for order in queryset:
            # Format cart data (product details)
            products_text = ""
            try:
                for item in order.cart_data:
                    title = item.get("title") or item.get("product_title") or "Unknown"
                    qty = item.get("qty", 1)
                    price = item.get("final_price", item.get("price", 0))
                    products_text += f"{title} (x{qty}) - ₹{price}\n"
            except Exception:
                products_text = json.dumps(order.cart_data, indent=2)

            ws.append([
                order.id,
                order.customer_name,
                order.email or "",
                order.phone,
                order.address,
                order.city,
                order.pincode,
                order.payment_method,
                float(order.total_amount),
                order.status,
                order.created_at.strftime("%Y-%m-%d %H:%M"),
                products_text.strip(),
            ])

        # Prepare HTTP response
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        filename = f"Orders_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response["Content-Disposition"] = f"attachment; filename={filename}"

        wb.save(response)
        return response

    export_to_excel.short_description = "📥 Download selected orders as Excel"
