from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Category,Product,Customer
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
def index(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None


    category = Category.objects.all()
    product=Product.objects.filter(active=True)
    paras={'category':category,'product':product,'customer':customer}
    return render(request, 'index.html',paras)

def about(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    paras={'customer':customer}
    return render(request, 'about.html',paras)
def product_view(request, product_id):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    product = get_object_or_404(Product, pk=product_id)
   
    paras={'customer':customer,'product': product}
    cart = request.session.get('cart', [])  # Retrieve cart from session or an empty list if not present
    if request.method == 'POST':
        cart_quantity = int(request.POST.get('cart_quantity'))
        updated = False

        # Check if the product is already in the cart
        for item in cart:
            if item['product_id'] == product_id:
                item['quantity'] = cart_quantity
                updated = True
                break

        # If the product is not already in the cart, add it
        if not updated:
            cart.append({'product_id': product_id, 'quantity': cart_quantity})

        request.session['cart'] = cart  # Update cart in session

    paras = {'customer': customer, 'product': product, 'cart': cart}

    return render(request, 'productview.html', paras)

def sign(request):  
    if request.method == 'POST':
        if 'first_name' in request.POST:
            print('baa')
            email = request.POST.get('email')
            password = request.POST.get('password')
            mobile_number = request.POST.get('mobile_number')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            # Check if email already exists
            if Customer.objects.filter(email=email).exists():
                return HttpResponse("Email already exists")  # Handle this case as needed
            
            # Create a new Customer object and save it
            customer = Customer.objects.create(
                email=email,
                password=password,
                mobile_number=mobile_number,
                first_name=first_name,
                last_name=last_name,
            )
            customer.save()

            return HttpResponse("Sign Up successful")  # You may want to redirect here instead
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                customer = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                # Handle case where email doesn't exist
                messages.error(request, 'Incorrect email or password. Please try again.')
                return render(request, 'sign.html')

            if password == customer.password:
                # Passwords match, login successful
                # You might want to set session variables or use Django's built-in authentication system here
                request.session['email'] = email
                request.session['customer_id'] = customer.id
                return redirect(index)  # Replace 'index' with the name of your home page URL pattern
            else:
                # Passwords don't match
                messages.error(request, 'Incorrect email or password. Please try again.')
                return render(request, 'sign.html')
                    
    return render(request, 'sign.html')
def logout(request):
    request.session.clear()
    return redirect(sign)

def cart(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.get(id=customer_id)
    else:
        customer = None

    if request.method == 'POST':
        product_id_to_remove = int(request.POST.get('product_id'))  # Get the product_id to remove from the form submission
        cart = request.session.get('cart', [])
        
        # Remove the product from the cart
        updated_cart = [item for item in cart if item['product_id'] != product_id_to_remove]
        
        request.session['cart'] = updated_cart  # Update cart in session
        return redirect('cart')  # Redirect to the cart page after removing the product

    cart = request.session.get('cart', [])
    products = []
    total=[]
    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        subtotal=product.price*item['quantity']
        products.append([product,item['quantity'],subtotal])
        total.append(float(subtotal))
    
    total=sum(total)

    paras = {'customer': customer, 'cart': cart, 'products': products,'total':total}
    return render(request, 'cart.html', paras)  