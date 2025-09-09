from django.shortcuts import render
from .models import ContactMessage

def contact_submit(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email',''),
            message=request.POST.get('message')
        )
        return render(request, 'contacts/thankyou.html')
    return render(request, 'contacts/contact_form.html')
