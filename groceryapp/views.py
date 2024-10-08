from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Category,Product,Customer,Order,Notification,Charge
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
import random
import re
from django.contrib import messages
# Create your views here.
def index(request):
    
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    order = Order.objects.filter(Customer_id = customer_id,active=True)
    if order:
        messages.success(request, 'Hooray!🎉🎉Your order is now being packed!')

    cart = request.session.get('cart', [])
    cartlen=len(cart)


    category = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
            product= Product.objects.filter(category = category_id, active=True).order_by('?')
            paginator = Paginator(product, 21)  # Show 10 products per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
    else:
        product = Product.objects.filter(active=True).order_by('?')
        paginator = Paginator(product, 21)  # Show 10 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    paras={'category':category,'product':page_obj,'customer':customer,'cartlen':cartlen}
    return render(request, 'index.html',paras)

def about(request):
    cart = request.session.get('cart', [])
    cartlen=len(cart)

    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    paras={'customer':customer,'cartlen':cartlen}
    return render(request, 'about.html',paras)

def contact(request):
    cart = request.session.get('cart', [])
    cartlen=len(cart)
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    if request.method == 'POST':
         fname = request.POST.get('fname')
         lname = request.POST.get('lname')
         email = request.POST.get('email')
         contactnumber=request.POST.get('contactnumber')
         message=request.POST.get('message')
         ordermail=Notification.objects.filter(active=True)
         for ix in ordermail:
                send_mail('Contact Mail', f'Name: {fname} {lname}\n \n Email: {email}\n \n Contact: {contactnumber} \n \n Message:{message}', settings.EMAIL_HOST_USER, [ ix.email], fail_silently=False)
         return redirect(contact)
    paras={'customer':customer,'cartlen':cartlen}
    return render(request, 'contact.html',paras)


def product_view(request, product_id):
    cart = request.session.get('cart', [])
    cartlen=len(cart)
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    product = get_object_or_404(Product, pk=product_id)
   
    paras={'customer':customer,'product': product}
    cart = request.session.get('cart', [])  # Retrieve cart from session or an empty list if not present
   
    if request.method == 'POST':
        cart_quantity = float(request.POST.get('cart_quantity'))
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

        return redirect(carts)

    similar_category=Product.objects.filter(category=product.category)
    paras = {'customer': customer, 'product': product, 'cart': cart,'similar_category':similar_category, 'cartlen':cartlen}

    return render(request, 'productview.html', paras)


def loginc(request):
    cart = request.session.get('cart', [])
    cartlen=len(cart)
    paras={'cartlen':cartlen}
    if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                customer = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                # Handle case where email doesn't exist
                messages.error(request, 'E-mail not matched. Please try again.')
                return render(request, 'login.html')

            if password == customer.password:
                # Passwords match, login successful
                # You might want to set session variables or use Django's built-in authentication system here
                request.session['email'] = email
                request.session['customer_id'] = customer.id
                return redirect(index)  # Replace 'index' with the name of your home page URL pattern
            else:
                # Passwords don't match
                messages.error(request, 'Incorrect email or password. Please try again.')
                return render(request, 'login.html')
    return render(request, 'login.html',paras)



def resetpassword(request):
    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST.get('email')
            try:
                user = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return render(request, 'reset.html', {'error': 'Email not found.', 'step': 1})
            
            # Generate and send OTP
            otp = random.randint(10000, 99999)
      
            
            send_mail('Password Reset OTP',f'Your OTP is: {otp}' , settings.EMAIL_HOST_USER, [email], fail_silently=False)
            # Store OTP and email in session
            request.session['otp'] = otp
            request.session['email'] = email
            
            return render(request, 'reset.html', {'step': 2})
        
        elif 'otp' in request.POST:
            otp_input = request.POST.get('otp')
            otp_session = request.session.get('otp')
            
            if otp_input and int(otp_input) == otp_session:
                return render(request, 'reset.html', {'step': 3})
            else:
                return render(request, 'reset.html', {'error': 'Invalid OTP', 'step': 2})
        
        elif 'new_password' in request.POST:
            new_password = request.POST.get('new_password')
            email = request.session.get('email')
            
            try:
                user = get_object_or_404(Customer, email=email)
                user.password = new_password
                user.save()
                return redirect(loginc)
            except Customer.DoesNotExist:
                return render(request, 'reset.html', {'error': 'Error resetting password', 'step': 3})
    
    return render(request, 'reset.html', {'step': 1})

def validate_password(password):
     # Check for minimum length of 8 characters
    if len(password) <= 6:
        return "Password must be at least 6 characters long."
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    
    # Check for at least one symbol
    # if not re.search(r'[\W_]', password):
    #     return "Password must contain at least one symbol."
    
    # Check for at least one numeric digit
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one numeric digit."
    
    return "Password is valid."



def signup(request):
    cart = request.session.get('cart', [])
    cartlen=len(cart)
    paras={'cartlen':cartlen}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        mobile_number = request.POST.get('mobile_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        context = {
            'email': email,
            'mobile_number': mobile_number,
            'first_name': first_name,
            'last_name': last_name
        }


        # Check if email already exists
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'email already exist ')
            return render(request,'signup.html', context)
        if password != password1:
            messages.error(request, 'Confirm password not matched')
            return render(request, 'signup.html', context)
         # Validate password
        password_validation_message = validate_password(password)
        if password_validation_message != "Password is valid.":
            messages.error(request, password_validation_message)
            return render(request, 'signup.html', context)
        
        if len(mobile_number) != 10:
            messages.error(request, 'Confirm phone Number')
            return render(request, 'signup.html', context)
            # Create a new Customer object and save it
        customer = Customer.objects.create(
                email=email,
                password=password,
                mobile_number=mobile_number,
                first_name=first_name,
                last_name=last_name,
            )
        customer.save()
        return redirect(loginc)

  
    return render(request, 'signup.html',paras)

def logout(request):
    request.session.clear()
    return redirect(loginc)

def carts(request):
    # Get customer info if logged in
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.get(id=customer_id) if customer_id else None
    
    # Initialize cart-related variables
    cart = request.session.get('cart', [])
    cartlen = len(cart)
    products = []
    order_details = {
        'product_ids': [],
        'names': [],
        'quantities': [],
        'subtotals': []
    }
    total = 0.0

    # Process each item in the cart
    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        quantity = item['quantity']
        price = float(product.price)
        subtotal = price * quantity
        
        order_details['product_ids'].append(product.id)
        order_details['names'].append(product.title)
        order_details['quantities'].append(quantity)
        order_details['subtotals'].append(subtotal)
        
        products.append([product, quantity, subtotal])
        total += subtotal

    # Calculate final amount including extra charges
    extra_amount = sum(float(charge.amount) for charge in Charge.objects.all())
    final_amount = total + extra_amount

    if request.method == 'POST':
        if 'product_id' in request.POST:
            # Remove product from cart
            product_id_to_remove = int(request.POST.get('product_id'))
            cart = [item for item in cart if item['product_id'] != product_id_to_remove]
            request.session['cart'] = cart
            return redirect(carts)
        
        elif 'payment' in request.POST:
            return redirect(payment)
        
        else:
            # Place the order
            fullname = f"{customer.first_name} {customer.last_name}"
            order_id_prefix = "JJ"
            order_date = datetime.datetime.now().strftime("%d%m%Y")
            orderplacedid = f"{order_id_prefix}{order_date}{customer_id}"
            
            for i in range(len(order_details['product_ids'])):
                Order.objects.create(
                    Orderplacedid=orderplacedid,
                    Customer_id=customer_id,
                    name=fullname,
                    email=customer.email,
                    mobile_number=customer.mobile_number,
                    address=customer.address,
                    product_id=order_details['product_ids'][i],
                    product_name=order_details['names'][i],
                    quantity=order_details['quantities'][i],
                    product_sub_price=order_details['subtotals'][i],
                    payment_mode='COD'
                )
            
            send_mail(
                f'Order Confirm #{orderplacedid}',
                f'\n\nThank you for your purchase. Your order has been successfully placed.'
                f'\n\nCustomer Name: {fullname}\n\nOrder id: #{orderplacedid}'
                f'\n\nPayment Mode: COD\n\nProduct amount {total} + Extra Charges {extra_amount} = ₹{final_amount}'
                f'\n\nView order: https://www.jewajiadamji.com/order/',
                settings.EMAIL_HOST_USER,
                [customer.email],
                fail_silently=False
            )

            for notification in Notification.objects.filter(active=True):
                send_mail(
                    'Order Mail',
                    f'New Order received\n\nCustomer Name: {customer.first_name}\n\nOrder id: #{orderplacedid}'
                    f'\n\nEmail: {customer.email}\n\nPayment Mode: COD\n\nProduct amount {total} + Extra Charges {extra_amount} = {final_amount}'
                    f'\n\nView order: https://www.jewajiadamji.com/dsearch/?query={orderplacedid}',
                    settings.EMAIL_HOST_USER,
                    [notification.email],
                    fail_silently=False
                )

            # Clear cart after order is placed
            del request.session['cart']
            return redirect('order')

    paras = {
        'charge': Charge.objects.all(),
        'customer': customer,
        'cart': cart,
        'products': products,
        'total': total,
        'final_amount': final_amount,
        'cartlen': cartlen
    }
    return render(request, 'cart.html', paras)

def account(request):
    cart = request.session.get('cart', [])
    cartlen=len(cart)
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None

    user = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.mobile_number = request.POST.get('mobile_number')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.address=request.POST.get('address')
        user.save()
        return redirect(index)
    
    paras={'customer':customer,'cartlen':cartlen}
    return render(request, 'account.html',paras)


def order(request):
    cart = request.session.get('cart', [])
    cartlen=len(cart)
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    order = Order.objects.filter(Customer_id = customer_id,active=True)
    total=0
    Orderplacedid=""
    date=""
    address=customer.address
    for i in order:
        total+=float(i.product_sub_price)
        Orderplacedid=i.Orderplacedid
        date=i.my_date
    deleivered=Order.objects.filter(Customer_id = customer_id,active=False)
    paras = {'cartlen':cartlen,'customer': customer,'order':order,'Orderplacedid':Orderplacedid,"date":date,'address':address ,'total':total,'deleivered':deleivered }
    return render(request,'order.html',paras)

def product_search(request):
    cart = request.session.get('cart', [])
    cartlen=len(cart)
    query = request.GET.get('query', '')  # Get the search term from GET request
    results = []
    if query:  # Ensure the query is not empty
        results = Product.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query)| Q(description__icontains=query))

    return render(request, 'search.html', {
        'query': query,
        'results': results
    })




import qrcode
import base64
from io import BytesIO
def payment(request):
    cart = request.session.get('cart', [])
    cartlen=len(cart)
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.get(id=customer_id)
    else:
        customer = None

    cart = request.session.get('cart', [])
    total = []
    order_product = []
    order_name = []
    order_qty = []
    order_subtotal = []

    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        order_product.append(product.id)
        order_name.append(product.title)
        order_qty.append(item['quantity'])
        p=float(product.price)
        subtotal=float(p*item['quantity'])
        order_subtotal.append(subtotal)
        total.append(subtotal)

    total = sum(total)
    charge=Charge.objects.all()
    extra_amount=float(0)
    for i in charge:
        extra_amount+=float(i.amount)
    final_amount=total+extra_amount


    fullname = customer.first_name + " " + customer.last_name if customer else "Guest"
    show_qr = False
    img_tag = ""

    if request.method == 'POST':
        upid = request.POST.get('upiid')
        x = datetime.datetime.now()
        y = x.strftime("%d%m%Y")
        orderplacedid = f"JJ{y}{customer_id}"

        for i in range(len(order_product)):
            order = Order(Orderplacedid=orderplacedid, Customer_id=customer_id, name=fullname, email=customer.email, mobile_number=customer.mobile_number, address=customer.address, product_id=order_product[i], product_name=order_name[i], quantity=order_qty[i], product_sub_price=order_subtotal[i],online_payment=True, upiId=upid, payment_mode='online')
            order.save()
            send_mail(f'Order Confirm #{orderplacedid}', f'\n\n Thank you for your purchase. Your order has been successfully placed. \n\n Customer Name: {fullname}\n\n Order id: #{orderplacedid} \n \n  Payment Mode: Online \n \n Upi Id: {upid} \n\n Product amount {total} + Extra Charges {extra_amount} = ₹{final_amount}  \n \n View order: https://www.jewajiadamji.com/order/ \n\n We will verify the receipt of your payment prior to proceeding with your order for delivery. Should you have any additional questions or require further assistance, please feel free to contact us: https://www.jewajiadamji.com/contact/', settings.EMAIL_HOST_USER, 
                        [customer.email], fail_silently=False)

        ordermail = Notification.objects.filter(active=True)
        for ix in ordermail:
            send_mail('Order Mail', f'New Order received from Customer Name: {customer.first_name} Order id: #{orderplacedid} \n \n Email: {customer.email} \n \n Payment Mode: Online \n \n Upi Id: {upid}\n\n Product amount {total} + Extra Charges {extra_amount} = {final_amount}  \n \n View order: https://www.jewajiadamji.com/dsearch/?query={orderplacedid}' , settings.EMAIL_HOST_USER, [ix.email], fail_silently=False)

        # QR Code generation happens after form submission
        upi_link = f"upi://pay?pa=9829623144@okbizaxis&pn=JewajiAdamJi&tr={orderplacedid}&am={final_amount}&cu=INR"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(upi_link)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_img_base64 = base64.b64encode(buffer.getvalue()).decode()
        img_tag = f'<img src="data:image/png;base64,{qr_img_base64}" alt="QR Code">'
        show_qr = True
        del request.session['cart']
        return render(request, 'payment.html', {'cartlen':cartlen,'customer': customer,'show_qr': show_qr, 'img_tag': img_tag,'orderplacedid':orderplacedid,'total':total})

    return render(request, 'payment.html', {'cartlen':cartlen,'customer': customer,'show_qr': show_qr, 'img_tag': img_tag})
# admin
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(dashboard)  # Redirect to a success page.
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'logindashboard.html')

def logout_view(request):
    logout(request)
    return redirect(index)

@login_required
def dashboard_search(request):
    query = request.GET.get('query', '')  # Get the search term from GET request
    results = []
    if query:  # Ensure the query is not empty
        results = Order.objects.filter( Q(Orderplacedid__icontains=query),active=True)

    if request.method == 'POST':
        order_id=request.POST.get('order_id')
        o = get_object_or_404(Order, id=order_id)
        o.active=False
        o.save()
    return render(request, 'dashboard_search.html', {
        'query': query,
        'results': results
    })

@login_required
def dashboard(request):
    order=Order.objects.filter(active=True)
    
    if request.method == 'POST':
        order_id=request.POST.get('order_id')
        o = get_object_or_404(Order, id=order_id)
        o.active=False
        o.save()
    return render(request, 'dashboard.html', {'order': order})

@login_required
def codorder(request):
    order=Order.objects.filter(active=True,online_payment=False)
    
    if request.method == 'POST':
        order_id=request.POST.get('order_id')
        o = get_object_or_404(Order, id=order_id)
        o.active=False
        o.save()
    return render(request, 'codorder.html', {'order': order})

@login_required
def onlinepayment(request):
    order=Order.objects.filter(active=True,online_payment=True) 
    if request.method == 'POST':
        order_id=request.POST.get('order_id')
        o = get_object_or_404(Order, id=order_id)
        o.active=False
        o.save()
    return render(request,'prepaidorder.html',{'order': order})

@login_required
def pastorderdashboard(request):
    order=Order.objects.filter(active=False)
    return render(request, 'pastorder.html', {'order': order})


def privacy(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    paras={'customer':customer}
    return render(request, 'privacy.html', {'paras': paras})


def terms(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    paras={'customer':customer}
    return render(request, 'terms&condition.html', {'paras': paras})

