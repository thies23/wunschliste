from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import Wish, GiftTransaction
from .forms import PublicPasswordForm, GiverNameForm, WishForm
from .decorators import simple_auth_required


def public_view_login(request):
    form = PublicPasswordForm()
    
    if request.method == 'POST':
        form = PublicPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if password == settings.PUBLIC_VIEW_PASSWORD:
                request.session['public_view_authenticated'] = True
                return redirect('public_wishes')
            else:
                messages.error(request, 'Falsches Passwort!')
    
    context = {
        'form': form,
        'help_text': settings.PUBLIC_VIEW_HELP_TEXT,
        'contact_email': settings.CONTACT_EMAIL,
    }
    return render(request, 'wunschliste/login.html', context)


def public_wishes(request):
    if not request.session.get('public_view_authenticated'):
        return redirect('public_view_login')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        wishes = Wish.objects.filter(is_available=True)
        sort_by = request.GET.get('sort', 'urgency')
        
        if sort_by == 'price':
            wishes = wishes.order_by('price')
        elif sort_by == 'shop':
            wishes = wishes.order_by('link')
        elif sort_by == 'alphabet':
            wishes = wishes.order_by('title')
        elif sort_by == 'urgency':
            wishes = wishes.order_by('-urgency')
        else:
            wishes = wishes.order_by('-urgency')
        
        data = {
            'wishes': [
                {
                    'id': w.id,
                    'title': w.title,
                    'link': w.link,
                    'image': w.image.url if w.image else (w.image_url or ''),
                    'price': str(w.price),
                    'urgency': w.urgency,
                    'is_available': w.is_available,
                }
                for w in wishes
            ]
        }
        return JsonResponse(data)
    
    sort_by = request.GET.get('sort', 'urgency')
    
    wishes = Wish.objects.filter(is_available=True)
    
    if sort_by == 'price':
        wishes = wishes.order_by('price')
    elif sort_by == 'shop':
        wishes = wishes.order_by('link')
    elif sort_by == 'alphabet':
        wishes = wishes.order_by('title')
    elif sort_by == 'urgency':
        wishes = wishes.order_by('-urgency')
    else:
        wishes = wishes.order_by('-urgency')
    
    context = {
        'wishes': wishes,
        'sort_by': sort_by,
        'contact_email': settings.CONTACT_EMAIL,
    }
    return render(request, 'wunschliste/public_wishes.html', context)


@require_http_methods(["POST"])
def gift_wish(request, wish_id):
    if not request.session.get('public_view_authenticated'):
        return JsonResponse({'error': 'Nicht autorisiert'}, status=403)
    
    wish = get_object_or_404(Wish, id=wish_id)
    
    if not wish.is_available:
        return JsonResponse({'error': 'Dieser Gegenstand ist nicht mehr verfügbar'}, status=400)
    
    form = GiverNameForm(request.POST)
    if form.is_valid():
        giver_name = form.cleaned_data['giver_name']
        
        wish.is_available = False
        wish.gifted_at = timezone.now()
        wish.name = giver_name
        wish.save()
        
        GiftTransaction.objects.create(
            wish=wish,
            giver_name=giver_name
        )
        
        return JsonResponse({
            'success': True,
            'message': f'{giver_name} hat "{wish.title}" geschenkt!'
        })
    
    return JsonResponse({'error': 'Ungültige Daten'}, status=400)


@simple_auth_required(
    'CREATE_WISH_USERNAME',
    'CREATE_WISH_PASSWORD',
    'create_wish_login'
)
def create_wish(request):
    
    if request.method == 'POST':
        form = WishForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wunsch erfolgreich erstellt!')
            return redirect('create_wish')
    else:
        form = WishForm()
    
    wishes = Wish.objects.all()
    
    context = {
        'form': form,
        'wishes': wishes,
    }
    return render(request, 'wunschliste/create_wish.html', context)



@simple_auth_required(
    'CREATE_WISH_USERNAME',
    'CREATE_WISH_PASSWORD',
    'create_wish_login'
)
def edit_wish(request, wish_id):
    wish = get_object_or_404(Wish, id=wish_id)
    
    if request.method == 'POST':
        form = WishForm(request.POST, request.FILES, instance=wish)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wunsch erfolgreich bearbeitet!')
            return redirect('create_wish')
    else:
        form = WishForm(instance=wish)
    
    context = {
        'form': form,
        'wish': wish,
        'editing': True,
    }
    return render(request, 'wunschliste/edit_wish.html', context)


@simple_auth_required(
    'CREATE_WISH_USERNAME',
    'CREATE_WISH_PASSWORD',
    'create_wish_login'
)
def delete_wish(request, wish_id):
    wish = get_object_or_404(Wish, id=wish_id)
    
    if request.method == 'POST':
        wish.delete()
        messages.success(request, 'Wunsch erfolgreich gelöscht!')
        return redirect('create_wish')
    
    context = {
        'wish': wish,
    }
    return render(request, 'wunschliste/delete_wish.html', context)



def create_wish_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if (username == settings.CREATE_WISH_USERNAME and 
            password == settings.CREATE_WISH_PASSWORD):
            request.session['auth_CREATE_WISH_USERNAME'] = True
            return redirect('create_wish')
        else:
            messages.error(request, 'Falsche Zugangsdaten!')
    
    return render(request, 'wunschliste/login.html', {
        'view_title': 'Wünsche erstellen',
        'contact_email': settings.CONTACT_EMAIL,
    })



@simple_auth_required(
    'GIFT_HISTORY_USERNAME',
    'GIFT_HISTORY_PASSWORD',
    'gift_history_login'
)
def gift_history(request):
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            transaction_id = request.POST.get('transaction_id')
            transaction = get_object_or_404(GiftTransaction, id=transaction_id)
            
            if not transaction.is_reversed:
                transaction.is_reversed = True
                transaction.save()
                
                wish = transaction.wish
                wish.is_available = True
                wish.name = None
                wish.gifted_at = None
                wish.save()
                
                return JsonResponse({'success': True})
        
        return JsonResponse({'error': 'Ungültige Anfrage'}, status=400)
    
    transactions = GiftTransaction.objects.select_related('wish').all()
    
    context = {
        'transactions': transactions,
    }
    return render(request, 'wunschliste/gift_history.html', context)


def gift_history_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if (username == settings.GIFT_HISTORY_USERNAME and 
            password == settings.GIFT_HISTORY_PASSWORD):
            request.session['auth_GIFT_HISTORY_USERNAME'] = True
            return redirect('gift_history')
        else:
            messages.error(request, 'Falsche Zugangsdaten!')
    
    return render(request, 'wunschliste/login.html', {
        'view_title': 'Schenk-Historie',
        'contact_email': settings.CONTACT_EMAIL,
    })