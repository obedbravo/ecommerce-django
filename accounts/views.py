from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
import requests

from carts.views import _cart_id
from carts.models import Cart, CartItem
# Create your views here.

def register(request):

     form = RegistrationForm()

     if request.method == 'POST':
          form = RegistrationForm(request.POST)
          if  form.is_valid():
               first_name = form.cleaned_data['first_name']
               last_name = form.cleaned_data['last_name']
               email = form.cleaned_data['email']
               phone_number = form.cleaned_data['phone_number']
               password = form.cleaned_data['password']
               #vaxi.drez@gmail.com
               username = email.split("@")[0]
               user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
               user.phone_number = phone_number
               user.save()

               # proceso para mandar el email para que confirme el usuario activacion de cuenta
               current_site = get_current_site(request)
               mail_subject = 'Por favor activa tu cuenta en Joyeria Bravo'
               body = render_to_string('accounts/account_verification_email.html', {
                    'user': user,
                    'domain':current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)), #covierte a coleccion de caracteres
                    'token': default_token_generator.make_token(user),

               })

               to_email = email
               send_email = EmailMessage(mail_subject, body, to=[to_email])
               send_email.send()


             #  messages.success(request, 'Se registro el usuario correctamente')
               return redirect('/accounts/login/?command=verification&email='+email)
     

     context = {
            'form': form
     }

     return render(request, 'accounts/register.html', context) 


#--------------------------------------------LOGIN------------------------------------------------
def login(request):

     if request.method == 'POST':
          email = request.POST['email']
          password = request.POST['password']

          user = auth.authenticate(email=email, password=password)

          if user is not None:
               try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exist:
                         cart_item = CartItem.objects.filter(cart=cart)

                         product_variation = []
                         for item in  cart_item:
                              variation = item.variation.all()
                              product_variation.append(list(variation))
                         
                         cart_item = CartItem.objects.filter(user=user)
                         ex_var_list = []
                         id =[]
                         for item in cart_item:
                              existing_variation = item.variation.all()
                              ex_var_list.append(existing_variation)
                              id.append(item.id)
                         
                         #comparacion si hay variations igualitos entra user y id inicio de sesio y no
                         for pr in ex_var_list:
                              if pr in product_variation:
                                   index = product_variation.index[pr]
                                   item_id = id[index]
                                   item = CartItem.objects.get(id=item_id)
                                   item.quantity += 1
                                   item.user = user
                                   item.save()
                              else:
                                   cart_item = CartItem.objects.filter(cart=cart)
                                   for item in cart_item:          
                                        item.user = user
                                        item.save()
               except:
                    pass
            
               auth.login(request, user)
               messages.success(request, 'Entro en sesion con exito!')

               url = request.META.get('HTTP_REFERER')  #-->  http://localhost:8000/accounts/login/?next=/cart/checkout/
               try:
                    query = requests.utils.urlparse(url).query  #----> ?next=/cart/checkout/

                    params = dict(x.split('=') for x in query.split('&')) 
                    if 'next' in params:
                         nextPage = params['next']
                         return redirect(nextPage)
                    
               except:
                  return redirect('dashboard')
          else:
               messages.error(request, 'Las credenciales son incorrectas')
               return redirect('login')


     return render(request, 'accounts/login.html')

#-------------------------------LOGOUT------------------------------------------------------------

@login_required(login_url='login') #esta funcion solo es activa cuando el usuario esta en sesion.
def logout(request):
     auth.logout(request)
     messages.success(request, 'Has salido de la sesion')
     return redirect('login')

#------------------------------------CUENTA ACTIVADA-----------------------------

def activate(request, uidb64, token):
     try:
          uid = urlsafe_base64_decode(uidb64).decode()
          user = Account._default_manager.get(pk=uid)
     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

     if user is not None and  default_token_generator.check_token(user, token):
          user.is_active = True
          user.save()
          messages.success(request, 'Felicidades, tu cuenta esta activa!')
          return redirect('login')
     else:
          messages.error(request, 'La actividad es invalida')
          return redirect('register')



#--------------------------------DASHBOARD----------------------------------
@login_required(login_url='login') 
def dashboard(request):
     return render(request, 'accounts/dashboard.html')

#-------------------------------RECUPERAR CONTRASEÑA--------------------------------------------

def forgotPassword(request):
     if request.method == 'POST':
          email = request.POST['email']
          if Account.objects.filter(email=email):
               user = Account.objects.get(email__exact=email)

               current_site = get_current_site(request)
               mail_subject = 'Resetear Contraseña'
               body = render_to_string('accounts/reset_password_email.html', {
                    'user': user,
                    'domain':current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
               })
               to_email = email
               send_email = EmailMessage(mail_subject, body, to=[to_email])
               send_email.send()

               messages.success(request, 'Un email fue enviado a tu bandeja de entrada para resetar tu password')
               return redirect('login')
          else:
               messages.error(request, 'La cuenta de ususario no existe')
               return redirect('forgotPassword')
     
     return render(request, 'accounts/forgotPassword.html')

#-------------------------------------RESETPASSWORD_VALIDATE-------------------------------------

def resetpassword_validate(request, uidb64, token):
     try:
          uid = urlsafe_base64_decode(uidb64).decode()
          user = Account._default_manager.get(pk=uid)
     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
          user=None
     
     if user is not None and default_token_generator.check_token(user, token):
          request.session['uid'] = uid
          messages.success(request, 'Por favor  resetea  tu password')
          return redirect('resetPassword')
     else:
          messages.error(request, 'El link ha expirado')
          return redirect('login')
#-------------------------------------resetPassword------------------------------------------------

def resetPassword(request):
     if request.method == 'POST':
          password = request.POST['password']
          confirm_password = request.POST['confirm_password']

          if password == confirm_password:
               uid = request.session.get('uid')
               user = Account.objects.get(pk=uid)
               user.set_password(password)
               user.save()
               messages.success(request, 'El password se reseteo correctamente')
               return redirect('login')
          else:
               messages.error(request, 'El password de confirmacion no concuerda ')
               return redirect('resetPassword')
     else:
          return render(request, 'accounts/resetPassword.html')
