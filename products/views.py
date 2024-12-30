from django.shortcuts import render, get_object_or_404
from .models import Product
from .models import Cart, CartItem ,Order
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Wishlist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from .models import UserProfile
from django.contrib.auth import logout
import os
import google.generativeai as genai
from .middleware import custom_login_required
from django.views.decorators.http import require_POST


@custom_login_required
def protected_view(request):
    return render(request, 'aMain_page.html')



genai.configure(api_key="")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)


def GenerateResponse(input_text):

    response = model.generate_content([
    "input: What lehengas do you have in pink?",
    "output: We have a variety of pink lehengas! Some popular options are Floral Pink Embroidered Lehenga and Pastel Pink Georgette Lehenga. Would you like to see more details or pictures?",
    "input: Show me lehengas with heavy embroidery.",
    "output: Sure! We have heavily embroidered lehengas in different styles. Some options are Velvet Bridal Lehenga and Designer Zari Work Lehenga. Can I help you choose one?",
    "input: What is the price range for lehengas?",
    "output: Our lehengas range from ₹5,000 to ₹50,000. Do you have a specific budget in mind?",
    "input: Do you have any discounts or offers?",
    "output: Yes! Currently, we are offering up to 20% off on select lehengas. Would you like to explore discounted options?",
    "input: Can I customize the color of the lehenga?",
    "output: Yes, we offer color customization on many lehengas. Let me know which design you like, and we’ll guide you through the options",
    "input: What sizes are available for lehengas?",
    "output: Our lehengas are available in sizes S, M, L, XL, and custom measurements. Would you like assistance with sizing?",
    "input: How long does delivery take?",
    "output: Delivery usually takes 7–10 business days. For customized lehengas, it may take an additional 5 days. Would you like to proceed with an order?",
    "input: What is your return policy?",
    "output: We accept returns within 7 days of delivery for non-customized products in their original condition. Let us know if you need help with a return!",
    "input: Can I talk to a customer care representative?",
    "output: Certainly! Please provide your email or phone number, and our representative will contact you shortly.",
    "input: Do you have matching accessories?",
    "output: No we sell only lehengas here",
    f"input: {input_text}",
    "output: ",
    ])

    return response.text

def chatbot(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "")
        if user_input:
            bot_response = GenerateResponse(user_input)
            return JsonResponse({"response": bot_response})
    return render(request, "chatbot.html")




def main_page(request):
    return render(request, 'aMain_page.html')

def blog_page(request):
    return render(request, 'blog_page.html')

def aboutus_page(request):
    return render(request, 'aboutus_page.html')

def login_page(request):
    return render(request, 'aLogin_page.html')

def register_page(request):
    return render(request, 'aRegister_page.html')

@custom_login_required
def book_appointment(request):
    return render(request, 'book_appointment.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def cancellation_return(request):
    return render(request, 'cancellation_return.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def signup_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['username']  # Should be the email input
        phone_number = request.POST['number']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup_page')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup_page')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken!")
            return redirect('signup_page')

        user = User.objects.create_user(email=username, username=username ,password=password)
        user_profile = UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )

        django_login(request, user)  
        messages.success(request, "Signup successful!")
        return redirect('main_page')

    return render(request, 'aRegister_page.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['emailPassword']
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                django_login(request, user)
                # Migrate guest cart to user cart after successful login
                migrate_guest_cart_to_user(request, user)
                messages.success(request, "Login successful!")
                return redirect('main_page')
            else:
                messages.error(request, "Invalid credentials, please try again.")
                return redirect('login')

        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return redirect('login_page')

    return render(request, 'aLogin_page.html')


@custom_login_required
def logout_user(request):
    logout(request) 
    messages.success(request, "You have successfully logged out.")
    return redirect('login_page')


@custom_login_required
def cancel_order(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'cancel_order_page.html', {
        'product': product,
        'quantity': quantity,
    })

@custom_login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    current_time = timezone.now()
    arrival_date = current_time + timedelta(days=5)

    for item in cart_items:
        Order.objects.create(
            user=request.user,  # Associate the order with the logged-in user
            product=item.product,
            quantity=item.quantity,
            arrival_date=arrival_date
        )

    cart_items.delete()

    return redirect("order_confirmation")


@custom_login_required
def order_confirmation(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders_page.html', {
        'orders': orders
    })


@custom_login_required
def delete_order(request, product_id):
    orders_to_cancel = Order.objects.filter(product_id=product_id)
    
    if orders_to_cancel.exists():
        orders_to_cancel.delete()
        messages.success(request, "Order(s) cancelled successfully.")
    else:
        messages.error(request, "No orders found for the specified product.")
    
    return redirect('order_confirmation')

# views.py
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    is_in_cart = False
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart and cart.items.filter(product=product).exists():
            is_in_cart = True
    else:
        # Check session cart
        guest_cart = request.session.get('guest_cart', {})
        if str(product_id) in guest_cart:
            is_in_cart = True
    
    context = {
        'product': product,
        'is_in_cart': is_in_cart
    }
    return render(request, 'product_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Print the POST data for debugging
    print("POST data:", request.POST)
    
    # Get quantity and ensure it's an integer
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            # Update the quantity instead of adding to it
            cart_item.quantity = quantity  # Changed from += to =
            cart_item.save()
    else:
        guest_cart = request.session.get('guest_cart', {})
        product_id_str = str(product_id)
        # Update the quantity instead of incrementing
        guest_cart[product_id_str] = quantity  # Changed from += 1
        request.session['guest_cart'] = guest_cart
        request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Product added to cart'
        })
    return redirect('cart_view')



def product_list(request):
    products = Product.objects.all()  
    return render(request, 'aProducts_page.html', {'products': products})

def cart_view(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.total_price for item in cart_items)
    else:
        guest_cart = get_or_create_guest_cart(request)
        cart_items = []
        total_price = 0
        
        for product_id, quantity in guest_cart.items():
            product = Product.objects.get(id=int(product_id))
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            })
            total_price += product.price * quantity
    
    return render(request, 'aCart_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'is_authenticated': request.user.is_authenticated
    })



def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
    else:
        guest_cart = get_or_create_guest_cart(request)
        product_id_str = str(product_id)
        if product_id_str in guest_cart:
            del guest_cart[product_id_str]
            request.session['guest_cart'] = guest_cart
            request.session.modified = True
    
    return redirect('cart_view')

def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 0))
    
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    else:
        guest_cart = get_or_create_guest_cart(request)
        product_id_str = str(product_id)
        if quantity > 0:
            guest_cart[product_id_str] = quantity
        else:
            guest_cart.pop(product_id_str, None)
        request.session['guest_cart'] = guest_cart
        request.session.modified = True
    
    return redirect('cart_view')



@custom_login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return HttpResponse(status=204)  # No content, just silently add

@custom_login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'wishlist_page.html', {'wishlist': wishlist})

@custom_login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist = Wishlist.objects.filter(user=request.user).first()

    if wishlist:
        wishlist.products.remove(product)
    
    return redirect('wishlist')





def get_or_create_guest_cart(request):
    """Helper function to get or create a guest cart from session"""
    cart_items = request.session.get('guest_cart', {})
    return cart_items


def migrate_guest_cart_to_user(request, user):
    """Helper function to migrate guest cart to user cart after login"""
    guest_cart = request.session.get('guest_cart', {})
    if guest_cart:
        user_cart, _ = Cart.objects.get_or_create(user=user)
        
        for product_id, quantity in guest_cart.items():
            product = Product.objects.get(id=int(product_id))
            cart_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        
        # Clear guest cart after migration
        del request.session['guest_cart']
        request.session.modified = True

def get_cart_count(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        count = cart.items.count()
    else:
        count = 0
    return JsonResponse({'cart_count': count})
