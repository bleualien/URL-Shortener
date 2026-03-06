from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import ShortURL

# --- User Registration ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Send success message to the login page
            messages.success(request, "Registration successful! Please log in with your new credentials.")
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'shortener/register.html', {'form': form})

# --- Management & Analytics (Dashboard) ---
@login_required
def dashboard(request):
    if request.method == "POST":
        original = request.POST.get('original_url', '').strip()
        custom_key = request.POST.get('custom_key', '').strip()
        
        if original:
            # FIX: Ensure the URL is absolute so redirect() doesn't stay on your domain
            if not original.startswith(('http://', 'https://')):
                original = 'https://' + original

            # Handle Custom Keys
            if custom_key:
                if not ShortURL.objects.filter(short_key=custom_key).exists():
                    ShortURL.objects.create(original_url=original, short_key=custom_key, user=request.user)
                    messages.success(request, f"Shortened to your custom link: {custom_key}")
                else:
                    messages.error(request, f"The custom key '{custom_key}' is already in use. Please try another.")
            else:
                # Create with auto-generated key (handled by model save() or logic)
                ShortURL.objects.create(original_url=original, user=request.user)
            
            return redirect('dashboard')
    
    urls = ShortURL.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shortener/dashboard.html', {'urls': urls})

# --- Redirection & Click Tracking ---
def redirect_url(request, short_key):
    # get_object_or_404 handles the "Link not found" error automatically
    url_entry = get_object_or_404(ShortURL, short_key=short_key)
    url_entry.clicks += 1  
    url_entry.save()
    return redirect(url_entry.original_url)

# --- URL Management (Edit) ---
@login_required
def edit_url(request, pk):
    url_entry = get_object_or_404(ShortURL, pk=pk, user=request.user)
    
    if request.method == "POST":
        new_url = request.POST.get('original_url', '').strip()
        new_key = request.POST.get('short_key', '').strip()
        
        if new_url and new_key:
            # Add protocol if missing
            if not new_url.startswith(('http://', 'https://')):
                new_url = 'https://' + new_url
            
            # Check if the key was changed and if the new key already exists
            if new_key != url_entry.short_key and ShortURL.objects.filter(short_key=new_key).exists():
                messages.error(request, f"The name '{new_key}' is already taken. Try another.")
            else:
                url_entry.original_url = new_url
                url_entry.short_key = new_key
                url_entry.save()
                messages.success(request, "Link updated successfully!")
                return redirect('dashboard')
                
    return render(request, 'shortener/edit.html', {'url': url_entry})

# --- URL Management (Delete) ---
@login_required
def delete_url(request, pk):
    url = get_object_or_404(ShortURL, pk=pk, user=request.user)
    url.delete()
    messages.info(request, "Link deleted.")
    return redirect('dashboard')

# --- Staff Only: Global History ---
def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def global_history(request):
    # select_related avoids the "N+1" query problem when fetching user data for each link
    all_urls = ShortURL.objects.select_related('user').all().order_by('-created_at')
    
    context = {
        'urls': all_urls,
        'total_links': all_urls.count(),
        'total_clicks': sum(url.clicks for url in all_urls)
    }
    return render(request, 'shortener/global_history.html', context)