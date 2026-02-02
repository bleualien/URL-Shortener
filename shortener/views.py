from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import ShortURL

#User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'shortener/register.html', {'form': form})

# Management & Analytics
@login_required
def dashboard(request):
    if request.method == "POST":
        original = request.POST.get('original_url')
        custom_key = request.POST.get('custom_key') # Bonus: Custom URL
        
        if original:
            # Check if custom key is unique
            if custom_key and not ShortURL.objects.filter(short_key=custom_key).exists():
                ShortURL.objects.create(original_url=original, short_key=custom_key, user=request.user)
            else:
                ShortURL.objects.create(original_url=original, user=request.user)
        return redirect('dashboard')
    
    urls = ShortURL.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shortener/dashboard.html', {'urls': urls})

# Redirection & Click Tracking
def redirect_url(request, short_key):
    url_entry = get_object_or_404(ShortURL, short_key=short_key)
    url_entry.clicks += 1  
    url_entry.save()
    return redirect(url_entry.original_url)

#URL Management (Edit)
@login_required
def edit_url(request, pk):
    url_entry = get_object_or_404(ShortURL, pk=pk, user=request.user)
    if request.method == "POST":
        new_url = request.POST.get('original_url')
        if new_url:
            url_entry.original_url = new_url
            url_entry.save()
            return redirect('dashboard')
    return render(request, 'shortener/edit.html', {'url': url_entry})

# URL Management (Delete)
@login_required
def delete_url(request, pk):
    url = get_object_or_404(ShortURL, pk=pk, user=request.user)
    url.delete()
    return redirect('dashboard')