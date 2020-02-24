from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
...

def login_request(request):
    form = AuthenticationForm()
    return render(request = request,
                  template_name = 'registration/login.html',

                  context={'form':form})