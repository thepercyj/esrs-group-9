from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import BookForm
from .models import UserBooks, Book, User, UserProfile
from django.contrib import messages

# Create a test user and profile for testing
# test_user = User.objects.create_user("testUser", "testuser@email.com", password="password", first_name="Test", last_name="User")
# test_user_profile = UserProfile.objects.create(user=test_user, primary_location="Brighton", current_location="Brighton",review= 5)

# Selects test user for testing
test_user = User.objects.first()
test_user_profile = UserProfile.objects.first()


# Index Page
def index(request):
    return render(request, 'index.html')


def category(request):
    return render(request, 'category.html')


def about(request):
    return render(request, 'about.html')


def work(request):
    return render(request, 'work.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def profile(request):
    form = BookForm(request.POST or None)
    user_books = UserBooks.objects.filter(owner_book_id=test_user_profile)
    context = {'form': form, 'user_books': user_books}
    return render(request, 'profile_page.html', context)


def addBook(request):
    """Processes the request to add a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            # Adds the book to the userBooks table
            addUserBook(new_book)

            return JsonResponse({'status': 'success', 'message': 'Book added successfully'})
        else:
            # Form validation failed, return error details
            return JsonResponse({'status': 'error', 'message': 'Form validation failed', 'errors': form.errors},
                                status=400)
    else:
        # If the request method is not POST, inform the client appropriately
        # Or render a form for GET requests if that's intended behavior
        return HttpResponse('This endpoint expects a POST request.', status=405)

    # As a last resort, return a generic response for unexpected cases
    # This line should ideally never be reached if all cases are handled correctly above
    return HttpResponse('Unexpected error occurred.', status=500)


def addUserBook(book):
    """Adds a book to the user's library based on the Book Form submitted"""
    new_user_book = UserBooks(
        owner_book_id=test_user_profile,  # Set the current user as the user_id
        currently_with=test_user_profile, # Defaults current user to currently_with on creation
        book_id=book,  # Set the newly created book as the book_id
        availability=True,  # Set available to true by default on creation
        booked='No'
    )

    # Save the new userBooks instance to the database
    new_user_book.save()

def removeBook(request):
    book_id = request.POST.get('book_id')
    try:
        book = UserBooks.objects.get(id=book_id, owner_book_id=test_user_profile)
        book.delete()
        messages.success(request, "Book removed successfully.")
    except UserBooks.DoesNotExist:
        messages.error(request, "Book not found.")
    return redirect('dashboard')



