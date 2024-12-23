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

@custom_login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})



@custom_login_required
def product_list(request):
    products = Product.objects.all()  
    return render(request, 'aProducts_page.html', {'products': products})

@custom_login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total_price = sum(item.total_price for item in cart.items.all())
    return render(request, 'aCart_page.html', {'cart': cart, 'total_price': total_price})

@custom_login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

@custom_login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    cart_item.delete()
    return redirect('cart_view')

@custom_login_required
def update_cart(request, product_id):
    cart = Cart.objects.get(user=request.user) 
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    quantity = request.POST.get('quantity')
    if quantity:
        cart_item.quantity = int(quantity)
        cart_item.save()
    
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
def remove_from_wishlist(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get()  
    wishlist.products.remove(product)
    return redirect('wishlist')






