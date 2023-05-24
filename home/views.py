from django.shortcuts import redirect, render


from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Author, Book, BookReview, Message

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def home(request):
    books = Book.objects.all()
    abouts = Author.objects.all()[:1]
    reviews = BookReview.objects.all()
    best_selling_books = Book.best_selling()[:1]
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save the message to the database
        message_obj = Message.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('home')
        
        # # Send email notification
        # subject = 'New Message Received'
        # context = {'name': name, 'email': email, 'message': message}
        # html_message = render_to_string('email_template.html', context)
        # plain_message = strip_tags(html_message)
        # from_email = 'centdam101@gmail.com'  # Replace with your email address
        # to_email = [email]  # Replace with the recipient's email address
        
        # send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
        
    ctx = {
        'books': books,
        'best_selling_books': best_selling_books,
        'abouts': abouts,
        'reviews': reviews
    }
    return render(request, 'home.html', ctx)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'book_detail.html', {'book': book})
