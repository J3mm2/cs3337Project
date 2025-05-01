from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
from .models import MainMenu, Book, Favorite, Comment
from .forms import BookForm, CommentForm


from django.http import HttpResponseRedirect

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse


def index(request):
    item_list = MainMenu.objects.all()  # Just fetch the menu items from the database

    return render(request, 'bookMng/index.html', {'item_list': item_list})


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  template_name='bookMng/postbook.html',
                  context={
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })


def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  template_name='bookMng/displaybooks.html',
                  context={
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.pic_path = book.picture.url[14:]
    comments = Comment.objects.filter(book=book).order_by('-created_date')

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()

    # Handle comment form
    comment_form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.book = book
                new_comment.user = request.user
                new_comment.save()
                return redirect('book_detail', book_id=book_id)
        else:
            comment_form = CommentForm()

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'is_favorite': is_favorite,
                      'comments': comments,
                      'comment_form': comment_form
                  })


@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    favorite = Favorite.objects.filter(user=request.user, book=book)

    if favorite.exists():
        favorite.delete()
    else:
        Favorite.objects.create(user=request.user, book=book)

    return redirect('book_detail', book_id=book_id)


@login_required(login_url='/accounts/login/')
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('book')
    books = [fav.book for fav in favorites]
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/my_favorites.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()

    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

@login_required(login_url='/accounts/login/')
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


def about_us(request):
    return render(request,
                  'bookMng/about_us.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })