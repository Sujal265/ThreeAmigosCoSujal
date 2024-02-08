from django.test import TestCase, Client
from django.urls import reverse
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductReview, wishlist_model, Address
from django.contrib.auth.models import User
from userauths.models import User

class ModelTests(TestCase):
    def setUp(self):
        # Create test instances for models
        self.category = Category.objects.create(title="Test Category")
        self.vendor = Vendor.objects.create(title="Test Vendor")
        self.product = Product.objects.create(
            title="Test Product",
            category=self.category,
            vendor=self.vendor,
            vendor_price=10.00
        )
        # Use the custom User model
        self.user = User.objects.create(username="testuser")
        self.order = CartOrder.objects.create(user=self.user, price=20.00)
        self.order_item = CartOrderItems.objects.create(
            order=self.order,
            item="Test Item",
            price=10.00,
            total=20.00
        )
        self.review = ProductReview.objects.create(
            user=self.user,
            product=self.product,
            review="Test Review",
            rating=5
        )
        self.wishlist_item = wishlist_model.objects.create(
            user=self.user,
            product=self.product
        )
        self.address = Address.objects.create(
            user=self.user,
            mobile="1234567890",
            address="Test Address",
            status=True
        )

    def test_category_model(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_vendor_model(self):
        self.assertEqual(str(self.vendor), "Test Vendor")

    def test_product_model(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_user_model(self):
        self.assertEqual(str(self.user), "testuser")

    def test_order_model(self):
        self.assertEqual(str(self.order), f"Cart Order - {self.order.id}")

    def test_order_item_model(self):
        self.assertEqual(str(self.order_item), "Test Item")

    def test_review_model(self):
        self.assertEqual(str(self.review), "Test Product - Test Review")

    def test_wishlist_model(self):
        self.assertEqual(str(self.wishlist_item), "Test Product - testuser Wishlist")

    def test_address_model(self):
        self.assertEqual(str(self.address), "Test Address")


class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(title="Test Product")

    def test_index_view(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)

    def test_product_list_view(self):
        response = self.client.get(reverse("core:product_list"))
        self.assertEqual(response.status_code, 200)

    def test_category_list_view(self):
        response = self.client.get(reverse("core:category_list"))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        response = self.client.get(reverse("core:product-detail", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_category_product_list_view(self):
        category = Category.objects.create(title="TestCategory")
        response = self.client.get(reverse("core:category-product-list", args=[category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestCategory Products")

    def test_vendor_detail_view(self):
        vendor = Vendor.objects.create(title="TestVendor")
        response = self.client.get(reverse("core:vendor_detail", args=[vendor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestVendor Products")

    def test_search_view(self):
        response = self.client.get(reverse("core:search_view"), {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search results for 'test'")

    def test_checkout_view(self):
        response = self.client.get(reverse("core:checkout"))
        self.assertEqual(response.status_code, 200)

        # Check if the page contains the expected content
        self.assertContains(response, "Checkout")  # Assuming there's a title "Checkout" on the page

        # Check if the form is present on the page
        self.assertContains(response, "<form")  # Check for the presence of a form tag

        # Check if the cart items are displayed
        self.assertContains(response, "Cart Items")  # Assuming there's a section with cart items

        # Check if the total amount is shown
        self.assertContains(response, "Total Amount")  # Assuming there's a section with the total amount

        # Add more specific checks based on your implementation

        # Example: Check if the "Place Order" button is present
        self.assertContains(response, '<button type="submit">Place Order</button>')

        # Example: Check if the user's address is displayed
        self.assertContains(response, "User Address: Test Address")  # Adjust based on your user's address

        # Example: Check if there's a form field for adding a new address
        self.assertContains(response, '<input type="text" name="address">')

        # Example: Check if the payment options are displayed
        self.assertContains(response, "Payment Options")  # Assuming there's a section for payment options

        # Example: Check if there's a field for selecting payment method
        self.assertContains(response, '<select name="payment_method">')

        # Example: Check if the order summary is displayed
        self.assertContains(response, "Order Summary")  # Assuming there's a section for order summary

        # Example: Check if the order items and their prices are listed
        self.assertContains(response, "Test Item - $10.00")  # Adjust based on your actual order items

        # Example: Check if there's a field for applying a discount code
        self.assertContains(response, '<input type="text" name="discount_code">')


    def test_wishlist_view(self):
        response = self.client.get(reverse("core:wishlist_view"))
        self.assertEqual(response.status_code, 200)