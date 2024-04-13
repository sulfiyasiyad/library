from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from vookeys.models import Category,Book,Usermember,Cart,Order,OrderItem,Contact,Rent,Requestbook,Issue,Lost,Paydetails,Payment,Bookfine
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
import os
import math
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
import random
from django.core import mail
from django.utils import timezone
import datetime


    
# Create your views here.

def home(request):
   
        book=Book.objects.all()
        total=0
        tot=Cart.objects.filter(user_id=request.user.id)
        total=tot
        paginator=Paginator(book,8)
        page_number=request.GET.get('page')
        final=paginator.get_page(page_number)
        return render(request,'home.html',{'book':book,"total":total,'final':final})
   

def signin(request):
    return render(request,'signin.html')
def add_signin(request):
    if request.method=='POST':
        username=request.POST['username'] 
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('adminhome')
            else:
                auth.login(request,user)
                messages.info(request, f'welcome {username}')
                return redirect('userhome')
        else:
            messages.info(request,'invalid username or password ')
            return redirect('signin')
    else:
        return redirect('signin')


def signup(request):
        return render(request,'signup.html')
def add_signup(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        number=request.POST['number']
        email=request.POST['email']
        image=request.FILES.get('file')
        if username==username:
            if email==email:
                if User.objects.filter(email=email).exists():
                    messages.info(request,"This Email Already Exists!!")
                else:
                    if User.objects.filter(username=username).exists():
                        messages.info(request,"This  Username Already Exists!!")
                    else:
                        use=User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email)
                        use.save()
                        user1=Usermember(number=number,uImage=image,user=use)
                        user1.user=use
                        user1.save()
                        messages.info(request,'Successfully registered wait for admin approval')
                        return redirect('signup')
        return redirect('signup')

@login_required(login_url='signin')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('home')
@login_required(login_url='signin')
def search(request):
        total=0
        cart_item=Cart.objects.filter(user=request.user)
        total=sum(item.quantity for item in cart_item)
    
        if request.method=='GET':
            query= request.GET.get('q')
            submitbutton= request.GET.get('submit')
            if query is not None:
                lookups= Q(book_name=query) | Q(auther_name=query)
                results= Book.objects.filter(lookups).distinct()
                context={'results': results,'submitbutton': submitbutton,'total':total}
                return render(request,'search.html', context)
            else:
                return render(request,'search.html')
        else:
            return render(request,'search.html')

def add_contact(request):
    if request.method=='POST':

        name=request.POST['name'] 
        email=request.POST['email']
        msg=request.POST['message']
        send=Contact.objects.create(user=request.user,name=name,email=email,Message=msg)
        send.save()
        subject="user query mail"
        message="hai"+name+"email:"+email+"message"+msg
        recepient="sulfiyacs16@gmail.com"
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
    return redirect('userhome')



###########################################admin###########################################################################
@login_required(login_url='signin')

def adminhome(request):
    total=Usermember.objects.all().filter(status=0).count()
    user=Usermember.objects.all().filter(status=1).count()
    book=Book.objects.all().count() 
    rent=Requestbook.objects.all().filter(issued=True).count()
    count=Order.objects.all().count()
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()



    return render(request,'admin.html',{'total':total,'user':user,'book':book,'rent':rent,'count':count,'b':b})

def admin_request(request):
    data=Usermember.objects.all().filter(status=0)
    total=0
    total=Usermember.objects.all().filter(status=0).count()
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    return render(request,'admin_request.html',{'data':data,'total':total,'b':b})

@login_required(login_url='signin')
def approve(request,pk):
        user1=Usermember.objects.get(id=pk)
        user1.status=1
        user1.save()
        email=user1.user.email
        status=0
        username=user1.user.username
        p=str(random.randint(100000,999999))
        
        user=User.objects.get(id=user1.user_id)
        user.set_password(p)
        user.save()
        subject="congragulation you are sucessfully registered .your login credentials"
        message= "password:"+" "+p+ "\n" +"username:" +username
        recipient=email
    
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
        return redirect('admin_request')
@login_required(login_url='signin')
def disapprove(request,pk):
        user1=Usermember.objects.get(id=pk)
        user2=User.objects.get(id=user1.user_id)
        user1.delete()
        user2.delete()
        return redirect('admin_request')
@login_required(login_url='signin')
def show_user(request):
        show=Usermember.objects.all().filter(status=1)
        total=Usermember.objects.all().filter(status=0).count()
        b=0
        b=Requestbook.objects.all().filter(issued=True,returned=False).count()
        return render(request,'show_user.html',{'show':show,'total':total,'b':b})
def delete_user(request,pk):
        member=Usermember.objects.get(id=pk)
        member.delete()
        member.user.delete()
        return redirect('show_user')
@login_required(login_url='signin')
def category(request):
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    total=0
    total=Usermember.objects.all().filter(status=0).count()
    return render(request,'category.html',{'total':total,'b':b})

@login_required(login_url='signin')
def add_category(request):
        if request.method=='POST':
            category=request.POST['category']
            if(category==category):
                if Category.objects.filter(category=category).exists():
                    messages.info(request,"This category Already Exists!!")
                else:
                    category1=Category(category=category)
                    category1.save()
                    messages.info(request,'Category Added Sucessfully')
            return redirect('category')

@login_required(login_url='signin')
def book( request):
    category1=Category.objects.all()
    total=0
    total=Usermember.objects.all().filter(status=0).count()
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    return render(request,'book.html',{'category':category1,'total':total,'b':b})
@login_required(login_url='signin')
def add_book(request):
        if request.method=='POST':
            bname=request.POST['bname']
            description=request.POST['des']
            auther_name=request.POST['aname']
            sel=request.POST['sel']
            scategory=Category.objects.get(id=sel)
            book_stock=request.POST['stock']
            price=request.POST['price']
            book_rent=request.POST['book_rent']
            image=request.FILES.get('file')
            isbn=request.POST['isbn']
            if(bname==bname):
                if Book.objects.filter(book_name=bname).exists():
                    messages.info(request,"Book Already Exists!!")
                    print('allready exist')
                else:
                    book1=Book(book_name=bname,book_description=description,auther_name=auther_name,book_stock=book_stock,book_price=price,Image=image,category=scategory,isbn=isbn,book_rent=book_rent)
                    book1.save()
                    messages.info(request,'Book added Sucessfully')
            return redirect('book')


@login_required(login_url='signin')
def show_book(request):
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    book2=Book.objects.all()
    total=0
    total=Usermember.objects.all().filter(status=0).count()
    return render(request,'show_book.html',{'book':book2 ,'total':total,'b':b})
@login_required(login_url='signin')
def edit_book(request,pk):
        b=Requestbook.objects.all().filter(issued=True,returned=False).count()
        book3=Book.objects.get(id=pk)
        category3=Category.objects.all()
        total=0
        total=Usermember.objects.all().filter(status=0).count()
    
        return render(request,'edit_book.html',{'book3':book3,'category3':category3,'total':total,'b':b})
@login_required(login_url='signin')
def book_edit(request,pk):
        if request.method=='POST':
            book4=Book.objects.get(id=pk)
            book4.book_name=request.POST['bname']
            book4.book_description=request.POST['des']
            book4.auther_name=request.POST['aname']
            sel=request.POST['sel']
            scourse=Category.objects.get(id=sel)
            book4.book_stock=request.POST['stock']
            book4.book_price=request.POST['price']
            book4.book_rent=request.POST['book_rent']
    
            # book4.Image=request.FILES.get('file')
            if len(request.FILES)!=0:
                if len(book4.Image)>0:
                    os .remove( book4.Image.path)
                    book4.Image=request.FILES.get('file')
        
            book4.save()
            book4.category=scourse
            book4.save()
            return redirect('show_book')

def delete_book(request,pk):
        book4=Book.objects.get(id=pk)
        book4.delete()
        return redirect('show_book')
#####################################userhome###################################################################################
def userhome(request):
        book=Book.objects.all()
        total=0
        cart_item=Cart.objects.filter(user=request.user)
        total=sum(item.quantity for item in cart_item)
        user=User.objects.all()
        paginator=Paginator(book,8)
        page_number=request.GET.get('page')
        final=paginator.get_page(page_number) 
        return render(request,'userhome.html',{'book':book,"total":total,'user':user,'final':final})
@login_required(login_url='signin')
def add_cart(request,pk):
    book=Book.objects.get(id=pk)
    cart_items = Cart.objects.filter(book=book)
    # Check if the product is already in the cart
    if cart_items.exists():
        cart_item = cart_items.first()
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If the product is not in the cart, create a new entry
        a=Cart.objects.create(book=book,user=request.user)
        a.quantity += 1
        a.save()
    return redirect('userhome')

@login_required(login_url='signin')
def cart(request):
    total=0
    cart=Cart.objects.filter(user_id=request.user.id)
    total=sum(item.quantity for item in cart)
    cart_items=Cart.objects.filter(user=request.user)
    total_price=sum(item.book.book_price * item.quantity for item in cart_items)
    return render(request, 'cartone.html',{'cart_items': cart_items,'total_price':total_price,"total":total})

@login_required(login_url='signin')
def remove_cart(request,pk):
        cart_item = Cart.objects.get(id=pk)
        cart_item.delete()
        return redirect('cart')
@login_required(login_url='signin')
def increase_cart(request,pk):
        cart_item=Cart.objects.get(id=pk)
        if (cart_item.quantity >=1):
            cart_item.quantity +=1
            cart_item.save()
        
        return redirect('cart')
@login_required(login_url='signin')
def decrease_cart(request,pk):
      
        cart_item=Cart.objects.get(id=pk)
        if (cart_item.quantity >=1):
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
@login_required(login_url='signin')
def user_profile(request):
         user=request.user.id
         user1=Usermember.objects.get(user=user)
         return render(request,'userprofile.html',{'usermember':user1})
@login_required(login_url='signin')
def user_edit(request):
        user=request.user.id
        usermember1=Usermember.objects.get(user=user)
        return render(request,'edit_user.html',{'usermember1':usermember1})
    
@login_required(login_url='signin')
def user_editdetails(request):
        if request.method=='POST':
            user=request.user.id
            user1=User.objects.get(id=user)
            usermember=Usermember.objects.get(user=user)
            user1.first_name=request.POST.get('first_name')
            user1.last_name=request.POST.get('last_name')
            user1.username=request.POST.get('username')
            user1.email=request.POST.get('email')
            usermember.number=request.POST.get('number')
            # usermember.uImage=request.FILES.get('file')
            if len(request.FILES)!=0:
                if len(usermember.uImage)>0:
                    os .remove(usermember.uImage.path)
                usermember.uImage=request.FILES.get('file')
            if  User.objects.filter(email=user1.email).exclude(username=request.user.username).exists():
                messages.info(request, 'This email is already in use. Please choose a different one.')
            
            elif User.objects.filter(username=user1.username).exclude(email=request.user.email).exists():
                messages.info(request, 'This username is already in use. Please choose a different one.')
           
           
            else:
                 user1.save()
                 usermember.save()
                #  messages.info(request,'Your profile was updated sucessfully')
                 return redirect('user_profile')
        
          


                 
                        
                          

                             
            
            return redirect('user_edit')
@login_required(login_url='signin')
def change_password(request):
        total=0
        cart_item=Cart.objects.filter(user=request.user)
        total=sum(item.quantity for item in cart_item)

    
        if request.method=='POST':
            password=request.POST['oldpassword']
            password2=request.POST['password']
            password3=request.POST['re-password']
            user=request.user.id
            user=User.objects.get(id=user)
            if(password==password2):
                if(password==password3):
                     messages.info(request,"already exist")
            elif(password2==password3):
                user.set_password(password2)
                user.save()
                # messages.info(request,"password changes sucessfully")
                return redirect('signin')
            
            else:
                messages.info(request,"password are not matching")
                      
            
                 
                 
        
           
        return render(request,'change_password.html',{'total':total})
        # return redirect('userhome')
@login_required(login_url='signin')
def checkout(request):
        usermember1=Usermember.objects.get(user=request.user)
        rawcart=Cart.objects.filter(user=request.user)
        order=Order.objects.filter(user=request.user)
        for item in rawcart:
            if item.quantity > item.book.book_stock:
                a=Cart.objects.get(id=item.id)
                a.delete()
        cartitems=Cart.objects.filter(user=request.user)
        total_price=0
        for item in cartitems:
            total_price=total_price+item.book.book_price*item.quantity
        print(total_price)
        
        return render(request,'checkout.html',{'cartitems':cartitems,'total_price':total_price,'usermember1':usermember1})
@login_required(login_url='signin')
def placeorder(request):
        if request.method=='POST':
            neworder=Order()
            neworder.user=request.user
            neworder.fname=request.POST['n1']
            neworder.lname=request.POST['n2']
            neworder.Email=request.POST['n3']
            neworder.Address=request.POST['n4']
            neworder.phone=request.POST['n5']
            neworder.city=request.POST['n6']
            neworder.State=request.POST['n7']
            neworder.country=request.POST['n8']
            neworder.pincode=request.POST['n11']
            neworder.payment_mode=request.POST['n10']
            neworder.payment_id=request.POST['n11']
    
            cart=Cart.objects.filter(user=request.user)
            cart_total_price=0 
            for item in cart:
                cart_total_price=cart_total_price+item.book.book_price*item.quantity
                neworder.total_price=cart_total_price
            sentMail(neworder.Email,neworder.fname,neworder.lname,neworder.Address,cart,neworder.total_price)
    
    
            
            
            tractno='abc'+str(random.randint(1111111,9999999))
            
            while Order.objects.filter(tracking_no=tractno) is None:
                tractno='abc'+str(random.randint(1111111,9999999))
            neworder.tracking_no=tractno
            neworder.save()
            neworderitems=Cart.objects.filter(user=request.user)
            for item in neworderitems:
             
                OrderItem.objects.create(user=request.user,order=neworder,book=item.book,price=item.book.book_price,quantity=item.quantity)
                orderbook = Book.objects.filter(id=item.book.id).first()
                orderbook.book_stock= orderbook.book_stock-item.quantity
                orderbook.save()
    
                
           
            
            Cart.objects.filter(user=request.user).delete()
    
            messages.success(request,'your order has been placed sucessfully')
            
          
    
        return redirect('checkout')
def sentMail(email, fname,lname,Address, orderItem, total_price):
        print(orderItem)
        print(email)
        print(fname)
        print(lname)
        print(Address)
        print(total_price)
        print(email)
       
    
    
    
    
        subject = 'Order Confirmed'
        html_message = render_to_string('mail_template.html', { 'email' : email, 'first_name':fname, 'last_name':lname, 'address':Address, 'orderItem': orderItem, 'totalPrice': total_price})
        plain_message = strip_tags(html_message)
        to = email
        mail.send_mail(subject, plain_message,settings.EMAIL_HOST_USER, [to], html_message=html_message)
def product(request,pk):
    total=0
    cart=Cart.objects.filter(user_id=request.user.id)
    total=sum(item.quantity for item in cart)
    # requestedbooks,issuedbooks=getmybooks(request.user)
    if(Book.objects.filter(id=pk)):
        book=Book.objects.filter(id=pk).first
        context={'book':book,'total':total}
    else:
        messages.info("No such item")
        return redirect('userhome')

    return render(request,'product_view.html',context)

def user_ordedproduct(request):
    total=0
    cart_item=Cart.objects.filter(user=request.user)
    total=sum(item.quantity for item in cart_item)

    user=Usermember.objects.filter(user_id=request.user.id)
    if user:
        a= OrderItem.objects.all().filter(user=request.user)
        return render(request,'user_ordedproduct.html',{'a':a,'total':total})
     
def rent(request,pk):
    user=Usermember.objects.filter(user_id=request.user)
    if user:
        book=Book.objects.get(id=pk)
        issue=Rent.objects.create(book=book,user=request.user)
        issue.quantity +=1
        issue.status=1
        issue.save()
    return redirect('Issue1')
def Issue1(request):
  
    total=0
    cart=Cart.objects.filter(user_id=request.user.id)
    total=sum(item.quantity for item in cart)
    user=Usermember.objects.filter(user_id=request.user)
    if user:
         rent=Rent.objects.all().filter(user_id=request.user)  
    return render(request,'rent.html',{'book':rent,'total':total})
def add_issue(request,pk):
    neworderitems=Rent.objects.filter(id=pk)
    if request.method=='POST':
        Issuedate=request.POST['n1']
        returndate=request.POST['n2']
    for item in neworderitems:
        a=Requestbook.objects.create(user=request.user,book=item.book,quantity=item.quantity,Issuedate=Issuedate,returndate=returndate)
        a.save()
        neworderitems.delete()
        messages.info(request,'Your request was sended sucessfully')
    return redirect('Issue1')
def issue_book(request,issueID):
    issue=Requestbook.objects.get(id=issueID)
    issue.issued=True
    issue.status=True
    if(issue.issued==True and issue.returned==False):
        y,m,d=str(timezone.now().date()).split('-')
        today=datetime.date(int(y),int(m),int(d))
        
        y2,m2,d2=str(issue.returndate).split('-')
        lastdate=datetime.date(int(y2),int(m2),int(d2))
        
        
        if(today>lastdate):
            diff=today-lastdate 
            issue.calc=True

    
            issue.diff=diff.days
            
            if not issue.paid:
                issue.amount=diff.days*10
                issue.save()
            else:
                print('fine paid')
        else:
            a='no fine'
            print(a)
    else:
        print('no fine')
  

  



    orderbook=Book.objects.filter(id=issue.book.id).first()
    orderbook.book_stock= orderbook.book_stock-issue.quantity
    orderbook.save()
    issue.save()
    
    
    return redirect('requestedissues')

def requestedissues(request):
    totalbook=0
    iss=Requestbook.objects.filter(user_id=request.user.id)
    totalbook=sum(item.quantity for item in iss)
    
    total=Usermember.objects.all().filter(status=0).count()
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    if request.GET.get('user_id') is not None and request.GET.get('user_id') != '':
        try:
            user= User.objects.get(username=request.GET.get('user_id'))
            student=Usermember.objects.filter(user_id=user)
            if student:
                user=user[0]
                issues=Requestbook.objects.filter(user=user,issued=False)
                return render(request,'allissues.html',{'issues':issues,'totalbook':totalbook,'b':b})
            messages.error(request,'No Student found')
            return redirect('allissues') 
        except User.DoesNotExist:
            messages.error(request,'user not found')
            return redirect('allissues')

    else:
        issues=Requestbook.objects.filter(issued=False)
        return render(request,'allissues.html',{'issues':issues,'total':total,'totalbook':totalbook,'b':b})
def view_issuebook(request):
    total=0
    cart=Cart.objects.filter(user_id=request.user.id)
    total=sum(item.quantity for item in cart)
    if Usermember.objects.filter(user_id=request.user):
        issues=Requestbook.objects.filter(user=request.user,issued=True)
    else:
         issues=Requestbook.objects.filter(user=request.user)

    return render(request,'myissues.html',{'issues':issues,'total':total})
    
def view_notissue(request):
    total=0
    cart=Cart.objects.filter(user_id=request.user.id)
    total=sum(item.quantity for item in cart)
    if Usermember.objects.filter(user_id=request.user):
        issues=Requestbook.objects.filter(user=request.user,issued=False)
    return render(request,'notissue.html',{'issues':issues,'total':total})
    
     



def main_return(request):
    total=0
    cart_item=Cart.objects.filter(user=request.user)
    total=sum(item.quantity for item in cart_item)
    if Usermember.objects.filter(user_id=request.user):
        issues=Requestbook.objects.filter(user=request.user,issued=True)

    else:
        issues=Requestbook.objects.filter(user=request.user)
    return render(request,'return_book.html',{'issues':issues,'total':total})
        
    messages.error(request,'You are Not a user !')
def return_book(request,issueID):
    issue=Requestbook.objects.get(id=issueID)
    calcFine(issue)
    issue.returned=True

    orderbook=Book.objects.filter(id=issue.book.id).first()
    orderbook.book_stock= orderbook.book_stock+issue.quantity
    orderbook.save()
    issue.save()
    return redirect('main_return')
    # return render(request,'return_book.html',{'issue':issue})
def calcFine(issue):
    "Calculate fines of each issue if any"
    if(issue.issued==True and issue.returned==False):
        y,m,d=str(timezone.now().date()).split('-')
        today=datetime.date(int(y),int(m),int(d))
        
        y2,m2,d2=str(issue.returndate).split('-')
        lastdate=datetime.date(int(y2),int(m2),int(d2))
        
        fine,created=Bookfine.objects.get_or_create(requestbook=issue,user=issue.user)
        if(today>lastdate):
            diff=today-lastdate 
    
            fine.diff=diff.days
            fine.status=1
            
            if not fine.paid:
                fine.amount=diff.days*10
                fine.save()
            else:
                print('fine paid')
        else:
            a='no fine'
            print(a)
    else:
        print('no fine')

# def sentMails(email,lost):
#         print(lost)
        
#         print(email)
        
       
    
    
    
    
        





def lost(request):
    total=0
    cart=Cart.objects.filter(user_id=request.user.id)
    total=sum(item.quantity for item in cart)
    if Usermember.objects.filter(user_id=request.user):
        issues=Requestbook.objects.filter(user=request.user,issued=True,returned=False)
        
        return render(request,'lost.html',{'issues':issues,'total':total})
def lost_send(request,pk):
    neworderitems=Requestbook.objects.filter(id=pk)
    pen=Requestbook.objects.get(id=pk)
    penaltyamount=100
   
    for item in neworderitems:
        penaltyadd=(item.book.book_price +item.amount+item.book.book_rent+penaltyamount)* item.quantity
        print(item.book.book_price)
        print(item.amount)
        print(item.book.book_rent)
        print(penaltyamount)
        a=Lost(book=item.book,user=request.user,quantity=item.quantity,subtotal=penaltyadd,penalty=penaltyamount,bookfine=item.amount)
        a.save()
       
        neworderitems.delete()
    return redirect('pay_fine')
def admin_lost(request):
    a=Lost.objects.all().filter(status=0)
    
    return render(request,'admin_lost.html',{'lost':a})
def lost_fine(request,pk):
    order2=Lost.objects.all().filter(id=pk)
    return render(request,'lost_fine.html',{'order1':order2})
def add_fine(request,pk):
    newone=Lost.objects.get(id=pk)
    newone.status=True
    if request.method=='POST':
        newone.fine=request.POST['n1']
        newone.damage=request.POST['n2']
        newone.save()
        newone.subtotal=(newone.book.book_price + int(newone.fine))*newone.quantity
        newone.save()
    return redirect('admin_lost')


def pay_fine(request):
    total=0
    cart=Cart.objects.filter(user_id=request.user.id)
    total=sum(item.quantity for item in cart)
    total1=0
    cart_item=Lost.objects.filter(user=request.user)
    total1=sum(item.quantity for item in cart_item)
    cartitem=Lost.objects.all().filter(user=request.user)
    for item in cartitem:
         if item.quantity >item.book.book_stock:
              a=Lost.objects.get(id=item.id)
    rawcart=Lost.objects.filter(user=request.user)
    total_price=0
    for item in rawcart:
         total_price=total_price+item.bookfine*item.quantity+item.book.book_price+item.book.book_rent+item.penalty
         



    return render(request,'viewlost_fine.html',{'a':rawcart,'total_price':total_price,'total1':total1,'total':total})
   




def checkout_pay(request):
    usermember1=Usermember.objects.get(user=request.user)
    rawcart=Lost.objects.filter(user=request.user)
    order=Paydetails.objects.filter(user=request.user)
    for item in rawcart:
        if item.quantity > item.book.book_stock:
            a=Lost.objects.get(id=item.id)
            a.delete()
    cartitems=Lost.objects.filter(user=request.user)
    total_price=0
    for item in cartitems:
        total_price=total_price+item.bookfine*item.quantity+item.book.book_price+item.book.book_rent+item.penalty     
    return render(request,'pay.html',{'cartitems':cartitems,'total_price':total_price,'usermember1':usermember1})
     
     
def paydetails(request):
    if request.method=='POST':
            neworder=Paydetails()
            neworder.user=request.user
            neworder.fname=request.POST['n1']
            neworder.lname=request.POST['n2']
            neworder.Email=request.POST['n3'] 
            neworder.phone=request.POST['n5']
            cart=Lost.objects.filter(user=request.user)
            cart_total_price=0 
            for item in cart:
                cart_total_price=cart_total_price+item.bookfine*item.quantity+item.book.book_price+item.book.book_rent+item.penalty   
                neworder.total_price=cart_total_price
            neworder.save()
            neworderitems=Lost.objects.filter(user=request.user)
            for item in neworderitems:
             
                Payment.objects.create(paydetails=neworder,book=item.book,quantity=item.quantity)
                orderbook = Book.objects.filter(id=item.book.id).first()
              
                orderbook.save()
            Lost.objects.filter(user=request.user).delete()
            
    
            messages.success(request,' Thanku payment was done sucessfully')
    return redirect('checkout_pay')
def myfines(request):
    total=0
    cart=Cart.objects.filter(user_id=request.user.id)
    total=sum(item.quantity for item in cart)
    if Usermember.objects.filter(user_id=request.user):
        student=Usermember.objects.filter(user_id=request.user)[0]
        issues=Requestbook.objects.filter(user=request.user)
        for issue in issues:
            calcFine(issue)
        fines=Bookfine.objects.filter(user=request.user,status=1)
        total_price=0
        for item in fines:
            total_price=total_price+item.amount
             
             

        return render(request,'myfine.html',{'fines':fines,'total':total,'total_price':total_price})
    messages.error(request,'You are Not a user !')
    return redirect('/')
def pay(request,pk):
    fine=Requestbook.objects.get(id=pk)
    fine.paid=True
    fine.diff=False

    fine.save()
    return redirect('main_return')


def rent_adminhistory(request):
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    rent=Requestbook.objects.all().filter(issued=True)
    total=Usermember.objects.all().filter(status=0).count()
    return render(request,'rent_adminhistory.html',{'rent':rent,'total':total,'b':b})

def admin_buy_history(request):
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    history2=Order.objects.all()
    total=Usermember.objects.all().filter(status=0).count()
    return render(request,'admin_buy_history.html',{'history2':history2,'total':total,'b':b})
def show(request,pk):
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
 
    order2=OrderItem.objects.all().filter(order_id=pk)
    order1=OrderItem.objects.all()
   
    return render(request,'show.html',{'history1':order2,'history2':order1,'b':b})
def rentfine(request):
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    fine=Requestbook.objects.all()
    total=0
    total=Usermember.objects.all().filter(status=0).count()
    return render(request,'rent_paid.html',{'fine':fine,'b':b,'total':total})
def lostpenalty(request):
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    total=0
    cart=Cart.objects.filter(user_id=request.user.id)
    total=sum(item.quantity for item in cart)
    a= Paydetails.objects.all()
    return render(request,'lostpenalty.html',{'a':a,'total':total,'b':b})
def lostpenalty_product(request,pk):
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    a=Payment.objects.all().filter(paydetails_id=pk)
    return render(request,'lostpenalty_product.html',{'a':a,'b':b})

def return_history(request):
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    a=Requestbook.objects.all().filter(returned=True)
    return render(request,'return_history.html',{'a':a,'b':b})
def notification(request):
    a=Requestbook.objects.all().filter(issued=True,returned=False)
    b=0
    b=Requestbook.objects.all().filter(issued=True,returned=False).count()
    total=0
    total=Usermember.objects.all().filter(status=0).count()
    return render(request,'notification.html',{'a':a,'b':b,'total':total})

     



        
     








          
          
          
     

        
     
     

          
     
     
     





   
         
   
    
     



    
    
        


    




           
