from datetime import date
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Order, Review
from .forms import ReviewForm
from django.shortcuts import get_object_or_404

def home(request):
    reviews = Review.objects.all().order_by("-date")
    return render(request, "home.html", {'reviews': reviews})


@login_required
def user_view(request):
    user = request.user
    orders = Order.objects.filter(user=user)

    for order in orders:
        if order.start_date:
            order.days_diff = (order.start_date - date.today()).days
        else:
            order.days_diff = None 
        
        review = Review.objects.filter(order=order).first()
        if review:
            order.rev_num = review.pk

    return render(request, 'user.html', {'orders': orders, 'user': user})



@login_required
def add_review(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.user.is_authenticated:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)

            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.order = order
                review.user = request.user
                review.does_exists = True
                review.save()

                return redirect('user') 

        else:
            review_form = ReviewForm()
            review_form.fields['date'].initial = timezone.now().date()

        return render(request, 'add_review.html', {
            'review_form': review_form,
            'order': order
        })
    

@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review_form.save()
            return redirect('user')
    else:
        review_form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {
        'review_form': review_form,
        'review': review,
    })
