from django.http import HttpResponse
from django.views import generic
from django.db.models.functions import Lower
from django.http import JsonResponse
from .models import *
from .forms import SearchDishForm
from django.shortcuts import render, redirect
from django.conf import settings

from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import pdb
import json
from django.utils import timezone

def SignupView(request):
    A={
        'Минимальная активность':'Min',
        'Слабая активность':'W',
        'Средняя активность':'Med',
        'Высокая активность':'H',
        'Экстра-активность':'E',
    }
    S={
        'Мужской':'M',
        'Женский':'W',
    }
    D={
        'Потеря веса':'L',
        'Поддержание веса': 'K',
        'Набор веса':'I',
    }


    if request.POST.get('submit') is not None:
        username=request.POST.get('name')
        password=request.POST.get('password')
        email=request.POST.get('email')
        current_user=User.objects.create_user(username,email,password)
        current_user.save()
        current_user_profile = UserProfile(user = current_user)
        current_user_profile.height=int(request.POST.get('height'))
        current_user_profile.wish_weight=int(request.POST.get('wish_weight'))
        current_user_profile.age=int(request.POST.get('age'))
        current_user_profile.sex=S[request.POST.get('sex')]
        current_user_profile.diet=D[request.POST.get('diet')]
        current_user_profile.activity=A[request.POST.get('activity')]
        current_user_profile.save()
        w=UserWeight(user=current_user_profile, date=timezone.now().date(),weight=int(request.POST.get('weight')))
        w.save()
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'calorimetr/signup.html')


def BaseView(request):
    current_user = request.user
    if not current_user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:

        current_user_profile = UserProfile.objects.get(user = current_user)
        return render(request,'calorimetr/base.html')
def CalendarView(request):
    current_user = request.user
    if not current_user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    month_list=['Январь',
                'Февраль',
                'Март',
                'Апрель',
                'Май',
                'Июнь',
                'Июль',
                'Август',
                'Сентябрь',
                'Октябрь',
                'Ноябрь',
                'Декабрь',
                ]
    current_month_ind = int(timezone.now().month)-1
    if request.GET.get('submit') is not None:
        current_month=request.GET.get('month')
        current_month_ind = month_list.index(current_month)
    current_user = request.user
    current_user_profile = UserProfile.objects.get(user = current_user)
    rsk=current_user_profile.get_rsk()

    eatings = list(Eating.objects.filter(date__month=current_month_ind+1, date__year=timezone.now().year).order_by('date').all())
    eating_days={}
    for e in eatings:
        day = str(e.date.strftime("%d/%m/%Y"))
        if eating_days.get(day) is None:
            c=e.get_calorie()
            eating_days[day]=(c,floor(c*100/rsk))
        else:
            c=eating_days[day][0]+e.get_calorie()
            eating_days[day]=(c,floor(c*100/rsk))


    return render(request,
                'calorimetr/calendar.html',
                {'current_month': month_list[current_month_ind] ,
                'month_list':month_list,
                'eatings':eating_days,
                }
                )


def WeightView(request):
    current_user = request.user
    if not current_user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    current_user_profile = UserProfile.objects.get(user = current_user)

    if request.POST.get('curr_weight_edit') is not None:
        w=UserWeight.objects.filter(date=timezone.now().date())
        if not w:
            w=UserWeight(user=current_user_profile, date=timezone.now().date(),weight=int(request.POST.get('weight')))
        else:
            w=w[0]
            w.weight=int(request.POST.get('weight'))
        w.save()

    if request.POST.get('wish_weight_edit') is not None:
        current_user_profile.wish_weight=int(request.POST.get('wish_weight'))
        current_user_profile.save()

    weight_list=list(current_user_profile.userweight_set.all().order_by('date'))
    weight_list_weight = []
    weight_list_year = []
    weight_list_month = []
    weight_list_day = []
    for w in weight_list:
        weight_list_weight.append(w.weight)
        weight_list_year.append(w.date.year)
        weight_list_month.append(w.date.month)
        weight_list_day.append(w.date.day)

    return render(request, 'calorimetr/weight_graph.html',
                {
                'current_user_profile': current_user_profile,
                'start_weight': weight_list[0].weight,
                'weight_list_year': weight_list_year,
                'weight_list_month': weight_list_month,
                'weight_list_day':weight_list_day,
                'weight_list_weight': weight_list_weight
                }
                )

def RSKView(request):
    current_user = request.user
    if not current_user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    A={
        'Минимальная активность':'Min',
        'Слабая активность':'W',
        'Средняя активность':'Med',
        'Высокая активность':'H',
        'Экстра-активность':'E',
    }
    S={
        'Мужской':'M',
        'Женский':'W',
    }
    D={
        'Потеря веса':'L',
        'Поддержание веса': 'K',
        'Набор веса':'I',
    }

    current_user_profile = UserProfile.objects.get(user = current_user)
    if request.POST.get('submit') is not None:
         current_user_profile.height=int(request.POST.get('height'))
         w=current_user_profile.userweight_set.filter(date=timezone.now().date())
         if not w:
             w=UserWeight(user=current_user_profile, date=timezone.now().date(),weight=int(request.POST.get('weight')))
         else:
             w.weight=int(request.POST.get('weight'))
         w.save()
         current_user_profile.wish_weight=int(request.POST.get('wish_weight'))
         current_user_profile.age=int(request.POST.get('age'))
         current_user_profile.sex=S[request.POST.get('sex')]
         current_user_profile.diet=D[request.POST.get('diet')]
         current_user_profile.activity=A[request.POST.get('activity')]

         current_user_profile.save()


    return render(request, 'calorimetr/rsk.html',{'current_user': current_user_profile})

def IndexView(request):
    current_user = request.user
    if not current_user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.POST.get('submit') is not None:
        e_name=request.POST.get('eating')
        e_b=Eating.objects.filter(name=e_name)
        if e_name and not e_b:
            current_user = request.user
            current_user_profile = UserProfile.objects.get(user = current_user)
            e=Eating(name=e_name,date=timezone.now(),user=current_user_profile)
            e.save()

    if  request.POST.get('del_dishes') is not None:
        param = request.POST.get('del_dishes').split('-')

        return del_dish(request,param[0],param[1])
    ind=request.POST.get('delete_eating')
    if ind is not None:
        Eating.objects.filter(pk=ind).delete()

    return render(request, 'calorimetr/index.html',{'latest_eating_list':Eating.objects.all().order_by('date')})

def SearchView(request, eating_id):
    # Получаем не отфильтрованный кверисет всех моделей
    queryset = Dish.objects.all()
    q = request.GET.get("q")
    if q:
    # Если 'q' в GET запросе, фильтруем кверисет по данным из 'q'
        queryset = Dish.objects.filter(name__icontains=q)
    return render(request, 'calorimetr/search_form.html',{'dish_list':queryset, 'eating_id':eating_id, 'product_name':q})


def add(request, eating_id):

    dish_id=request.POST.getlist('dishes')
    dish_portions=request.POST.getlist('portions')
    e=Eating.objects.get(pk=eating_id)

    for str in dish_id:
        arr_str=str.split('-')
        id_d=arr_str[1]
        id_p=arr_str[0]
        d=Dish.objects.get(pk=int(id_d))
        d.eating.add(e)
        d.save()

        port_list=d.portion_set.filter(eating=e)

        if not port_list:
            port=Portion(val=dish_portions[int(id_p)-1],dish=d,eating=e)
            port.save()

        else:
            port=port_list[0]
            port.val=dish_portions[int(id_p)-1]
            port.save()


    return HttpResponseRedirect(reverse('diary'))

def del_dish(request, eating_id, dish_id):


    e=Eating.objects.get(pk=eating_id)

    d=Dish.objects.get(pk=dish_id)
    arr=list(d.eating.all())
    arr.remove(e)
    d.eating=arr
    d.save()
    Portion.objects.filter(eating=e,dish=d).delete()

    return HttpResponseRedirect(reverse('diary'))

def AddProduct(request, eating_id):
    if request.POST.get('add_prod') :
        product_name = request.POST.get('add_prod')
        return render(request, 'calorimetr/add_product.html',{'product_name':product_name, 'eating_id':eating_id})

    if request.POST.get('add_in_database') :

        n=request.POST.get('name')
        c=request.POST.get('calorie')
        f=request.POST.get('fat')
        p=request.POST.get('protein')
        carbo=request.POST.get('carbo')
        portion=request.POST.get('portion')

        dish_list=Dish.objects.filter(name=n)
        d=None
        if not dish_list:
            d=Dish(name=n,calorie=c,fat=f,protein=p,carbohydrates=carbo)
            d.save()
        else:
            d=dish_list[0]
            d.name=n
            d.calorie=c
            d.fat=f
            d.protein=p
            d.carbohydrates=carbo
        e=Eating.objects.filter(pk=eating_id)[0]
        e_list=list(d.eating.all())
        e_list.append(e)
        d.eating =e_list
        d.save()
        port_list=d.portion_set.filter(eating=e)

        if not port_list:
            port=Portion(val=portion,dish=d,eating=e)
            port.save()
        else:
            port=port_list[0]
            port.val=portion
            port.save()
        return HttpResponseRedirect(reverse('diary'))
