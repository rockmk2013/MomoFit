from django.shortcuts import render
# Create your views here.
from .forms import CustomUserCreationForm,HistoryForm,MenuForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import ItemList, History


def SignUp(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        history_form = HistoryForm(request.POST)
        if all([user_form.is_valid(), history_form.is_valid()]):
            user = user_form.save()
            history = history_form.save(commit=False)
            history.user = user
            history.tdee = 10*history.weight + 6.25*history.height-5*user.age
            if(user.sex==1):
                history.tdee += 5
            else:
                history.tdee -= 161
            if history.actlevel==1:
                history.tdee *= 1.2
            elif history.actlevel==2:
                history.tdee *= 1.375
            elif history.actlevel==3:
                history.tdee *= 1.55
            elif history.actlevel==4:
                history.tdee *= 1.725
            else:
                history.tdee *= 1.9          

            history.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('profile')

    else:
        user_form = CustomUserCreationForm()
        history_form = HistoryForm()

    return render(request, 'signup.html', {
        'user_form': user_form,
        'history_form': history_form,
    })

@login_required(login_url='/') 
def Hello_momo(request):
    if request.user.is_authenticated:
        # print(request.user.kcal)
        history = History.get_history(request.user)
        sex = "生理男性" if request.user.sex==1 else "生理女性"
        #之後有多筆資料的時候可能要去改get_history的query
        context = {
            "name": request.user.username,
            "age": request.user.age,
            "sex": sex,
            "height": history[0][1],
            "weight": history[0][2],
            "fat" : history[0][9],
            "bench_press" :  history[0][3],
            "Dead_lift" : history[0][4],
            "Squat" :  history[0][5],
            "TDEE": history[0][6] #不在user裡面了換到history table裡
        }
    else:
        context = None
    return render(request, 'profile.html', context=context)

@login_required(login_url='/') 
def Menu(request):
    if request.method == 'POST':#insert to menu,insert to menu_item
        menu_form = MenuForm(request.POST)
        items_id = request.POST.getlist('items')
        return redirect('menu')
    else:
        items = ItemList.get_item_list(request.user)
        menu_form = MenuForm(items)
        context={'menu_form':menu_form}
    return render(request, 'menu.html', context=context)