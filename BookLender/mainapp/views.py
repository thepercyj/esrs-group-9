from io import BytesIO
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .forms import BookForm, UserRegisterForm, ProfilePicForm
from .models import UserBook, User, UserProfile, Book, Conversation, Message
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.core.files.base import ContentFile
from django.db.models import Q
from django.db import transaction
from django.utils.timezone import now
from django.http import HttpResponseBadRequest
from BookLender import settings


# test_user2 = User.objects.get(username='TestUser2')
# test_user_2_profile = UserProfile.objects.get(user=test_user2)


def login_required_message(function):
    """
    Decorator to display a message if the user is not logged in
    """

    def wrap(request, *args, **kwargs):
        # If the user is logged in, call the function
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)

        # If the user is not logged in, display an error message and redirect to the login page
        else:
            messages.error(request, "You need to be logged in to view this page.")
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # Retains the docstring and name of the original function
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# test page
def test(request):
    if request.method == "POST":
        searchquery = request.POST.get('searchquery')  # Retrieve the value of searchquery from POST data
        user_profiles = UserProfile.objects.filter(user__username=searchquery)  # Filter user profiles based on username

        return render(request, 'test.html', {'searchquery': searchquery,
                                             'user_profiles': user_profiles})  # Pass the filtered user profiles to the template
    else:
        return render(request, 'about.html')


# Index Page
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def lend(request):
    return render(request, 'lend.html')


def forgetpass(request):
    return render(request, 'forgetpass.html')


def new_home(request):
    return render(request, 'newhome.html')


def chat(request):
    return render(request, 'chat.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.save_profile()
            return redirect('login_view')  # Redirect to login page
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                # Handle the case where authentication fails
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    # Prepare the context
    token = {'form_log': form}
    # No need to manually add the CSRF token in Django templates, {% csrf_token %} does this
    return render(request, 'login.html', token)


@login_required_message
def profile(request):
    form = BookForm(request.POST or None)
    user = request.user
    library = Book.objects.all()
    user_profile = UserProfile.objects.get(user=user)
    user_books = UserBook.objects.filter(owner_book_id=user_profile)
    books_count = user_books.count()  # Count the number of books
    context = {'bookform': form, 'user_books': user_books, 'user_profile': user_profile, 'user': user,
               'user_book_count': books_count, 'library': library}
    return render(request, 'profile_page.html', context)


@login_required_message
def addBook(request):
    """Processes the request to add a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            # Adds the book to the userBooks table
            addUserBook(request, new_book)
            return redirect('profile')
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


@login_required_message
def addUserBook(request, book):
    user_profile = UserProfile.objects.get(user=request.user)
    """Adds a book to the user's library based on the Book Form submitted"""
    new_user_book = UserBook(
        owner_book_id=user_profile,  # Set the current user as the user_id
        currently_with=user_profile,  # Defaults current user to currently_with on creation
        book_id=book,  # Set the newly created book as the book_id
        availability=True,  # Set available to true by default on creation
        booked='No'
    )

    # Save the new userBooks instance to the database
    new_user_book.save()


@login_required_message
def library(request):
    # Fetch all Book records without prefetch_related
    library = Book.objects.all()

    # Debug output to check the books
    for book in library:
        print(f"Book: {book.book_title}, Added by: {book.added_by}")

    # Filter out books added by the current user
    library = library.exclude(added_by=request.user)

    # Debug output to check the filtered books
    for book in library:
        print(f"Filtered Book: {book.book_title}, Added by: {book.added_by}")

    # Pass the result to the template
    return render(request, 'library.html', {'library': library})


@login_required_message
def removeBook(request):
    user_profile = UserProfile.objects.get(user=request.user)
    book_id = request.POST.get('book_id')
    try:
        book = UserBook.objects.get(id=book_id, owner_book_id=user_profile)
        book.delete()
        messages.success(request, "Book removed successfully.")
    except UserBook.DoesNotExist:
        messages.error(request, "Book not found.")
    return HttpResponseRedirect(reverse('profile') + '?remove=true')


@login_required_message
def updateProfile(request):
    if request.method == 'POST':
        user = request.user
        user_profile = UserProfile.objects.get(user=user)  # Adjust based on your UserProfile model relation

        user.username = request.POST.get('inputUserName')
        user.first_name = request.POST.get('inputFirstName')
        user.last_name = request.POST.get('inputLastName')
        user.email = request.POST.get('inputEmailAddress')
        user.save()

        user_profile.primary_location = request.POST.get('inputLocation')
        user_profile.phone_number = request.POST.get('inputPhone')
        user_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile_page')
    else:
        # Handle non-POST request
        return render(request, 'profile_page.html')


@login_required_message
def img_upload(request):
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if the user is authenticated
            if request.user.is_authenticated:
                image_file = form.cleaned_data['profile_pic']

                # Check file size
                if image_file.size > 2 * 1024 * 1024:  # 2 MB limit
                    return JsonResponse({'error': "File size exceeds the limit of 2 MB."})

                # Image compression
                img = Image.open(image_file)
                img = img.convert('RGB')
                img.thumbnail((1024, 1024))  # Resize to maximum dimensions of 1024x1024
                img_io = BytesIO()

                # Save in JPEG format
                img.save(img_io, format='JPEG', quality=70)  # Adjust quality as needed
                img_io.seek(0)
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.profile_pic.save(image_file.name + '.jpg', ContentFile(img_io.getvalue()), save=True)

                # Save in PNG format if the uploaded file is not already PNG
                if image_file.name.lower().endswith('.png'):
                    img_io = BytesIO()
                    img.save(img_io, format='PNG', optimize=True)
                    img_io.seek(0)
                    user_profile.profile_pic.save(image_file.name, ContentFile(img_io.getvalue()), save=True)

                # Save in WebP format if the uploaded file is not already WebP
                if image_file.name.lower().endswith('.webp'):
                    img_io = BytesIO()
                    img.save(img_io, format='WEBP', quality=70)
                    img_io.seek(0)
                    user_profile.profile_pic.save(image_file.name, ContentFile(img_io.getvalue()), save=True)

                return JsonResponse({'success': True})  # Indicate success
            else:
                # Handle case where user is not authenticated
                return JsonResponse({'error': "User not authenticated"}, status=401)
    else:
        form = ProfilePicForm()
    return render(request, 'profile_page.html', {'uploadpic': form})


@login_required_message
def display_pic(request):
    # Assuming you have a UserProfile instance associated with the currently logged-in user
    user_profile = request.user.profile
    library = Book.objects.all()

    return render(request, 'profile_page.html', {'user_profile': user_profile})


@login_required_message
def search(request):
    if request.method == "POST":
        searchquery = request.POST.get('searchquery')  # Retrieve the value of searchquery from POST data
        user_profiles = UserProfile.objects.filter(user__username=searchquery)  # Filter user profiles based on username

        return render(request, 'search.html', {'searchquery': searchquery,
                                               'user_profiles': user_profiles})  # Pass the filtered user profiles to the template
    else:
        # Handle GET request
        # return render(request, 'search.html')
        user_profiles = UserProfile.objects.all()
        return render(request, 'search.html', {'user_profiles': user_profiles})


def user_profile(request, profile_id):
    # Fetch the UserProfile object based on the provided profile_id
    user_profile = get_object_or_404(UserProfile, pk=profile_id)

    # Access the user associated with the user_profile
    users = user_profile.user

    if request.method == 'POST':
        selected_owner_profile_id = request.POST.get('owner_id')

        if selected_owner_profile_id:
            selected_owner = get_object_or_404(UserProfile, pk=selected_owner_profile_id)

            try:
                with transaction.atomic():
                    existing_conversation = Conversation.objects.filter(
                        (Q(id_1=user_profile) & Q(id_2=selected_owner)) |
                        (Q(id_2=user_profile) & Q(id_1=selected_owner))
                    ).first()

                    if existing_conversation:
                        # If conversation already exists, redirect to conversation
                        return redirect('conversation', conversation_id=existing_conversation.id)
                    else:
                        # If conversation doesn't exist, create a new one
                        new_conversation_object = Conversation(id_1=user_profile, id_2=selected_owner)
                        new_conversation_object.save()
                        # Create a pre-message to notify both parties
                        pre_message_content = f"{users.username} wants to connect with you."
                        new_message = Message(
                            from_user=user_profile,
                            to_user=selected_owner,
                            details=pre_message_content,
                            request_type=1,  # Assuming 1 represents a simple message
                            request_value='Simple Message',
                            created_on=now(),
                            modified_on=now(),
                            notification_status=1,
                            conversation=new_conversation_object
                        )
                        new_message.save()
                        # Display a popup alert to both parties
                        messages.success(request, pre_message_content)
                        return redirect('new_conversation')  # Redirect to new conversation page
            except Exception as e:
                messages.error(request, 'An error occurred.')
                return redirect('search')
        else:
            messages.error(request, 'Please select an owner.')
            return redirect('user_profile', profile_id=profile_id)

    return render(request, 'users_profiles.html', {'user_profiles': user_profile, 'users': users})


@login_required_message
def borrow(request, book_id):
    """
    View function to initiate a borrow request for a book.
    """
    book = get_object_or_404(Book, id=book_id)
    user_books = book.user_books_book.all()

    if request.method == 'POST':
        selected_owner_username = request.POST.get('owner')

        if selected_owner_username:
            selected_owner = get_object_or_404(UserProfile, user__username=selected_owner_username)
            our_profile = UserProfile.objects.get(user=request.user)

            try:
                with transaction.atomic():
                    existing_conversation = Conversation.objects.filter(
                        (Q(id_1=our_profile) & Q(id_2=selected_owner)) |
                        (Q(id_2=our_profile) & Q(id_1=selected_owner))
                    ).first()

                    if existing_conversation:
                        # If conversation already exists, redirect to conversation
                        return redirect('conversation', conversation_id=existing_conversation.id)
                    else:
                        # If conversation doesn't exist, create a new one
                        new_conversation_object = Conversation(id_1=our_profile, id_2=selected_owner)
                        new_conversation_object.save()
                        # Create a pre-message to notify both parties
                        pre_message_content = f"{request.user.username} wants to borrow a book from you."
                        new_message = Message(
                            from_user=our_profile,
                            to_user=selected_owner,
                            details=pre_message_content,
                            request_type=2,  # Assuming 2 represents borrow request
                            request_value='Borrow Request',
                            created_on=now(),
                            modified_on=now(),
                            notification_status=1,
                            conversation=new_conversation_object
                        )
                        new_message.save()
                        # Display a popup alert to both parties
                        messages.success(request, pre_message_content)
                        return redirect('new_conversation')  # Redirect to new conversation page
            except Exception as e:
                messages.error(request, 'An error occurred.')
                return redirect('library')
        else:
            messages.error(request, 'Please select an owner.')
            return redirect('borrow', book_id=book_id)

    return render(request, 'borrow.html', {'book': book, 'user_books': user_books})
