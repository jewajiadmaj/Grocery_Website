from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Category,Product,Customer,Order,Notification
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def index(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None


    category = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
            product= Product.objects.filter(category = category_id, active=True)
    else:
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

        return redirect(carts)

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

def carts(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.get(id=customer_id)
    else:
        customer = None
    cart = request.session.get('cart', [])
    products = []
    total=[]
    order_product=[]
    order_name=[]
    order_qty=[]
    order_subtotal=[]
    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        order_product.append(product.id)
        order_name.append(product.title)
        order_qty.append(item['quantity'])
        subtotal=float(product.price*item['quantity'])
        order_subtotal.append(subtotal)
        products.append([product,item['quantity'],subtotal])
        total.append(float(subtotal))
    
    total=sum(total)

    if request.method == 'POST':
        if 'product_id' in request.POST:
            product_id_to_remove = int(request.POST.get('product_id'))  # Get the product_id to remove from the form submission
            cart = request.session.get('cart', [])
        
            # Remove the product from the cart
            updated_cart = [item for item in cart if item['product_id'] != product_id_to_remove]
        
            request.session['cart'] = updated_cart  # Update cart in session
            return redirect(carts)  # Redirect to the cart page after removing the product

    
        else:
            fullname=customer.first_name+" "+customer.last_name
            x = datetime.datetime.now()
            y=x.strftime("%d""%m""%Y")
            orderplacedid=f"JJ{y}{customer_id}"
            for i in range(len(order_product)):
                order=Order(Orderplacedid=orderplacedid,Customer_id=customer_id,name=fullname,email=customer.email,mobile_number=customer.mobile_number,address=customer.address,product_id=order_product[i],product_name=order_name[i]
                       ,quantity=order_qty[i] ,product_sub_price=order_subtotal[i])
                print(fullname)
                order.save()
            ordermail=Notification.objects.filter(active=True)
            for ix in ordermail:
                send_mail('Order Mail', f'New Oreder recived from Customer Name: {customer.first_name} Order id: #{orderplacedid} \n \n Email: {customer.email} \n \n', settings.EMAIL_HOST_USER, [
                  ix.email], fail_silently=False)
            return redirect('order')
  

    paras = {'customer': customer, 'cart': cart, 'products': products,'total':total}
    return render(request, 'cart.html', paras)  

def account(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None

    user = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')
        user.mobile_number = request.POST.get('mobile_number')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.address=request.POST.get('address')
        user.save()
        return redirect(index)
    
    paras={'customer':customer}
    return render(request, 'account.html',paras)


def order(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer=Customer.objects.get(id=customer_id)
    else:
        customer=None
    print(customer_id)
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
    paras = {'customer': customer,'order':order,'Orderplacedid':Orderplacedid,"date":date,'address':address ,'total':total,'deleivered':deleivered }
    return render(request,'order.html',paras)

def product_search(request):
    query = request.GET.get('query', '')  # Get the search term from GET request
    results = []
    if query:  # Ensure the query is not empty
        results = Product.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query))

    return render(request, 'search.html', {
        'query': query,
        'results': results
    })

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
def dashboard(request):
    order=Order.objects.filter(active=True)
    
    if request.method == 'POST':
        order_id=request.POST.get('order_id')
        o = get_object_or_404(Order, id=order_id)
        o.active=False
        o.save()
    return render(request, 'dashboard.html', {'order': order})

@login_required
def pastorderdashboard(request):
    order=Order.objects.filter(active=False)
    return render(request, 'pastorder.html', {'order': order})