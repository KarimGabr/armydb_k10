from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from armydbapp.models import *
from django.core.validators import URLValidator, ValidationError
from django.db import IntegrityError
from hashlib import md5
import datetime
import queue
import io
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage


today = datetime.datetime.now()
today = datetime.date(today.year,today.month,today.day)             
def home(request):
    if request.method == "GET":
            if request.user.is_authenticated:
                return redirect ("armydbapp:index")
            return render(request, "armydbapp/home.html")
    else:
            return HttpResponse(status=500)

def login_view(request):
    if request.user.is_authenticated:
        return redirect ("armydbapp:index")
        
    return render(request, 'armydbapp/login.html')

def login_user(request):
    if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            if not username or not password:
                    return render(request, "armydbapp/login.html", {"error":"Enter all required fields"})
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    login(request, user)
                    return redirect("armydbapp:index")
                    
            else:
                    return render(request, "armydbapp/login.html", {"error":"Wrong username or password"})
    else:
            return redirect("armydbapp:index")
            

def logout_user(request):
    logout(request)
    return redirect("armydbapp:login")

def index(request):
    if request.method == "GET":
        user = request.user
        names=[]
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.is_absent == True:
                        return_date = soldier.return_date 
                        days_absent = daysBetweenDates(return_date.year, return_date.month, return_date.day, today.year, today.month, today.day)
                        days_absent = str(days_absent)
                        Soldier.objects.filter(soldier_id = soldier.soldier_id).update(days_absent = days_absent)
        if not request.user.is_authenticated:
                return redirect("armydbapp:home")
        

        dof3at, radif_specialities, dof3a_number_of_specialities = dof3at_radif()
        awaiting_trial,sum_number_of_specialities, number_of_specialities, specialities, number_of_at_vacation_sick, number_late_unit, number_late_vacation, number_punished, number_of_soldiers, number_of_at_vacation, number_prisioned, number_out, number_absent, number_mission,number_here, number_returning = numbering()
        number_of_at_vacation_sick_k10_head, number_of_soldiers_k10_head, number_of_at_vacation_k10_head, number_prisioned_k10_head, number_out_k10_head, number_absent_k10_head, number_mission_k10_head, number_here_k10_head = numbering_k10_head()
        number_of_at_vacation_sick_s1_head, number_of_soldiers_s1_head, number_of_at_vacation_s1_head, number_prisioned_s1_head, number_out_s1_head, number_absent_s1_head, number_mission_s1_head, number_here_s1_head = numbering_s1_head()
        number_of_at_vacation_sick_s2_head, number_of_soldiers_s2_head, number_of_at_vacation_s2_head, number_prisioned_s2_head, number_out_s2_head, number_absent_s2_head, number_mission_s2_head, number_here_s2_head = numbering_s2_head()
        number_of_at_vacation_sick_s3_head, number_of_soldiers_s3_head, number_of_at_vacation_s3_head, number_prisioned_s3_head, number_out_s3_head, number_absent_s3_head, number_mission_s3_head, number_here_s3_head = numbering_s3_head()
        return render(request, "armydbapp/index.html", {"user":user,
                        "names":names,
                        "number_punished":number_punished,
                        "number_of_soldiers":number_of_soldiers,
                        "number_of_soldiers":number_of_soldiers,
                        "number_of_at_vacation":number_of_at_vacation,
                        "number_prisioned":number_prisioned,
                        "number_out":number_out,
                        "number_absent":number_absent,
                        "number_mission":number_mission,
                        "number_here":number_here,
                        "number_returning":number_returning,
                        "number_late_vacation":number_late_vacation,
                        "number_late_unit":number_late_unit,
                        "number_of_at_vacation_sick":number_of_at_vacation_sick,
                        "number_of_at_vacation_sick_k10_head":number_of_at_vacation_sick_k10_head,
                        "number_of_soldiers_k10_head":number_of_soldiers_k10_head, 
                        "number_of_at_vacation_k10_head":number_of_at_vacation_k10_head, 
                        "number_prisioned_k10_head":number_prisioned_k10_head, 
                        "number_out_k10_head":number_out_k10_head, 
                        "number_absent_k10_head":number_absent_k10_head, 
                        "number_mission_k10_head":number_mission_k10_head, 
                        "number_here_k10_head":number_here_k10_head,
                        "number_of_at_vacation_sick_s1_head":number_of_at_vacation_sick_s1_head,
                        "number_of_soldiers_s1_head":number_of_soldiers_s1_head, 
                        "number_of_at_vacation_s1_head":number_of_at_vacation_s1_head, 
                        "number_prisioned_s1_head":number_prisioned_s1_head, 
                        "number_out_s1_head":number_out_s1_head, 
                        "number_absent_s1_head":number_absent_s1_head, 
                        "number_mission_s1_head":number_mission_s1_head, 
                        "number_here_s1_head":number_here_s1_head,
                        "number_of_at_vacation_sick_s2_head":number_of_at_vacation_sick_s2_head,
                        "number_of_soldiers_s2_head":number_of_soldiers_s2_head, 
                        "number_of_at_vacation_s2_head":number_of_at_vacation_s2_head, 
                        "number_prisioned_s2_head":number_prisioned_s2_head, 
                        "number_out_s2_head":number_out_s2_head, 
                        "number_absent_s2_head":number_absent_s2_head, 
                        "number_mission_s2_head":number_mission_s2_head, 
                        "number_here_s2_head":number_here_s2_head,
                        "number_of_at_vacation_sick_s3_head":number_of_at_vacation_sick_s3_head,
                        "number_of_soldiers_s3_head":number_of_soldiers_s3_head, 
                        "number_of_at_vacation_s3_head":number_of_at_vacation_s3_head, 
                        "number_prisioned_s3_head":number_prisioned_s3_head, 
                        "number_out_s3_head":number_out_s3_head, 
                        "number_absent_s3_head":number_absent_s3_head, 
                        "number_mission_s3_head":number_mission_s3_head, 
                        "number_here_s3_head":number_here_s3_head,
                        "number_of_specialities":number_of_specialities, 
                        "specialities":specialities,
                        "sum_number_of_specialities":sum_number_of_specialities,
                        "awaiting_trial":awaiting_trial,
                        "dof3at":dof3at,
                        "radif_specialities":radif_specialities,
                        "dof3a_number_of_specialities":dof3a_number_of_specialities,
                        },)

def soldier_list(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        names=[]
        dof3at=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                return_date = soldier.return_date
                present = soldier.is_present


                

                if soldier.is_at_vacation == False and present == True and soldier.is_absent == False:
                      pass
                else:        
                        if return_date:
                                if today < return_date:
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation=True)
                                elif today == return_date:
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation=True)
                                
                                elif today > return_date :
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation = False)
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation_sick = False)
                                        if present == True :
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_absent=False)
                                        elif present == False:
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_absent=True)
                
                if soldier.is_at_punishment == False :
                        pass
                else:

                        for punishment in soldiers_punishments:
                                if punishment.soldier.soldier_id == soldier.soldier_id:
                                        if today < punishment.end_date :
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(current_punishment=punishment)
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_punishment=True)
                                        elif today > punishment.end_date:
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_punishment=False)
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(current_punishment=None)

                
                                        
        
                
        
        for soldier in soldier_list:
                if soldier.service_end_date in dof3at:
                        pass
                else:
                        dof3at.append(soldier.service_end_date)
        dof3at.sort()
        

        return render(request, "armydbapp/soldier_list.html",{"soldier_list":soldier_list,"soldiers_punishments": soldiers_punishments,"dof3at": dof3at, "names": names},)

def soldier_search(request):
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        if request.method == "POST":
                query = request.POST.get('q')
                soldier_list = []
                soldier_list1 = Soldier.objects.filter(name__istartswith=query)
                soldier_list1 = soldier_list1.order_by("name")
                soldier_list2 = Soldier.objects.filter(name__icontains=query)
                soldier_list2 = soldier_list2.order_by("name")
                for soldier in soldier_list1:
                        soldier_list.append(soldier)
                for soldier in soldier_list2:
                        if soldier in soldier_list:
                                pass
                        else:
                                soldier_list.append(soldier)

                soldiers_punishments = SoldierPunishments.objects.all()
                
        return render(request, "armydbapp/soldier_list.html",{"soldier_list":soldier_list,"soldiers_punishments": soldiers_punishments,"names":names,},)



def add_soldier(request):
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_soldier.html",{"names":names,},)

def submit_soldier(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        if request.method == "POST":
                soldier_name = request.POST.get('soldier-name')
                soldier_img = request.FILES.get('soldier-img')
                soldier_id = request.POST.get('soldier-id')
                soldier_army_unit_name = request.POST.get('soldier-army-unit-name')
                soldier_army_unit_number = request.POST.get('soldier-army-unit-number')
                soldier_current_army_unit = soldier_army_unit_number + " " + soldier_army_unit_name
                soldier_service_start_date = request.POST.get('soldier-service-start-date')
                soldier_service_end_date = request.POST.get('soldier-service-end-date')
                soldier_speciality= request.POST.get('soldier-speciality')
                soldier_adress= request.POST.get('soldier-adress')
                id_tag= "S"+str(soldier_id)
                new_soldier = Soldier(  name=soldier_name,
                                        soldier_img=soldier_img, 
                                        soldier_id=soldier_id, 
                                        service_start_date=soldier_service_start_date, 
                                        service_end_date=soldier_service_end_date,
                                        current_army_unit=soldier_current_army_unit,
                                        speciality =soldier_speciality,
                                        adress = soldier_adress,
                                        id_tag= id_tag,
                                        
                                        )
                
                new_soldier.save()

                soldier_unit = SoldierArmyUnits(soldier = new_soldier, 
                                                army_unit = soldier_current_army_unit, 
                                                start_date = today, 
                                                )

                soldier_unit.save()
                return redirect("armydbapp:soldier_list")

def add_img(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_img.html",{"soldier_id":soldier_id,"names":names,},)

def submit_add_img(request):
        if request.method == "POST":
                soldier_img = request.FILES.get('soldier-img')
                soldier_number = request.POST.get('soldier_number')
                soldier =  Soldier.objects.filter(soldier_id=soldier_number).get()
                soldier.update(soldier_img=soldier_img)
                return redirect("armydbapp:soldier_list")

def add_reward(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_reward.html",{"soldier_id":soldier_id,"names":names,},)

def submit_reward(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                rewarded_soldier = get_object_or_404(Soldier, soldier_id=soldier_number)
                days_rewarded = request.POST.get('days_rewarded')
                Soldier.objects.filter(soldier_id=soldier_number).update(reward_days=days_rewarded)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_rewarded=True)

                new_reward = Rewards (soldier = rewarded_soldier, reward_days = days_rewarded)
                
                new_reward.save()

                return redirect("armydbapp:soldier_list")

def add_zucchini(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_zucchini.html",{"soldier_id":soldier_id,"names":names,},)

def submit_zucchini(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                soldier = get_object_or_404(Soldier, soldier_id=soldier_number)
                zucchini = request.POST.get('zucchini')
                soldier.zucchini = zucchini
                soldier.save()

                return redirect("armydbapp:soldier_list")

def add_work_assigned(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_work_assigned.html",{"soldier_id":soldier_id,"names":names,},)

def submit_work_assigned(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                soldier = get_object_or_404(Soldier, soldier_id=soldier_number)
                work_assigned = request.POST.get('work_assigned')
                soldier.work_assigned = work_assigned
                soldier.save()

                return redirect("armydbapp:soldier_list")

def add_job(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_job.html",{"soldier_id":soldier_id,"names":names,},)

def submit_job(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                soldier = get_object_or_404(Soldier, soldier_id=soldier_number)
                job = request.POST.get('job')
                soldier.job = job
                soldier.save()

                return redirect("armydbapp:soldier_list")

'''def submit_remark(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                soldier = get_object_or_404(Soldier, soldier_id=soldier_number)
                remarks = request.POST.get('remarks')
                soldier.remarks = remarks
                soldier.save()
                soldier_number = str(soldier_number)
                url = "armydbapp:soldier_information" + "?" + "soldier_id=" + soldier_number
        return redirect(url)'''
        

def add_vacation(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_vacation.html",{"soldier_id":soldier_id,"names":names,},)



def submit_vacation(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                date_of_return = request.POST.get('date_of_return')
                Soldier.objects.filter(soldier_id=soldier_number).update(return_date=date_of_return)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_at_vacation=True)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_present=False)
                soldier = Soldier.objects.filter(soldier_id=soldier_number).get()
                vacation = Vacations(soldier=soldier,start_date=today,end_date=date_of_return)
                vacation.save()
                             
                return_date = soldier.return_date
                present = soldier.is_present
                               
                if soldier.is_at_vacation == False and present == True and soldier.is_absent == False:
                      pass
                else:        
                        if return_date:
                                if today < return_date:
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation=True)
                                elif today == return_date:
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation=True)
                                
                                elif today > return_date :
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation = False)
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation_sick = False)
                                        if present == True :
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_absent=False)
                                        elif present == False:
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_absent=True)
                
                return redirect("armydbapp:soldier_list")

def add_vacation_sick(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_vacation_sick.html",{"soldier_id":soldier_id,"names":names,},)

def submit_vacation_sick(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                date_of_return = request.POST.get('date_of_return')
                Soldier.objects.filter(soldier_id=soldier_number).update(return_date=date_of_return)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_at_vacation_sick=True)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_at_vacation=True)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_present=False)

                soldier =  Soldier.objects.filter(soldier_id=soldier_number).get()
                
                return_date = soldier.return_date
                present = soldier.is_present
                               
                if soldier.is_at_vacation == False and present == True and soldier.is_absent == False:
                      pass
                else:        
                        if return_date:
                                if today < return_date:
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation=True)
                                elif today == return_date:
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation=True)
                                
                                elif today > return_date :
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation = False)
                                        Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_at_vacation_sick = False)
                                        if present == True :
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_absent=False)
                                        elif present == False:
                                                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_absent=True)
                return redirect("armydbapp:soldier_list")

def add_punishment(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_punishment.html",{"soldier_id":soldier_id,"names":names,},)

def submit_punishment(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                punished_soldier = get_object_or_404(Soldier, soldier_id=soldier_number)
                type_of_punishment = request.POST.get('punishment_type')
                start_date_punishment = request.POST.get('punishment_start_date')
                end_date_punishment = request.POST.get('punishment_end_date')

                soldier_punishment = SoldierPunishments(soldier=punished_soldier, 
                                                        punishment=type_of_punishment, 
                                                        start_date=start_date_punishment, 
                                                        end_date=end_date_punishment)
                
                soldier_punishment.save()
                Soldier.objects.filter(soldier_id=soldier_number).update(current_punishment = soldier_punishment)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_at_punishment=True)
                return redirect("armydbapp:soldier_list")

def soldier_information(request):
        soldier_id = request.GET.get('soldier_id')
        
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        
        for soldier in soldier_list:
                names.append(soldier.name)
        
        soldier = Soldier.objects.filter(soldier_id=soldier_id).get()
        info={"soldier":soldier,"names":names,}
        punishement_list = SoldierPunishments.objects.filter(soldier = soldier)
        if punishement_list: 
                info.update({"punishement_list":punishement_list})
        
        units_list = SoldierArmyUnits.objects.filter(soldier = soldier)
        if units_list:
                info.update({"units_list":units_list})
        
        vacations = Vacations.objects.filter(soldier = soldier)
        if vacations:
                info.update({"vacations":vacations})
        
        rewards = Rewards.objects.filter(soldier = soldier)
        if rewards:
                info.update({"rewards":rewards})
        promotions = Promotion.objects.filter(soldier = soldier)
        if promotions:
                info.update({"promotions":promotions})
        
        
        return render(request, "armydbapp/soldier_information.html",info,)



def delete_soldier(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/delete_soldier.html",{"soldier_id":soldier_id,"names":names,},)

def submit_delete_soldier(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                Soldier.objects.filter(soldier_id=soldier_number).delete()
                return redirect("armydbapp:soldier_list")


def dont_delete_soldier(request):
        if request.method == "POST":
                return redirect("armydbapp:soldier_list")

def add_promotion(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/add_promotion.html",{"soldier_id":soldier_id,"names":names,},)

def submit_promotion(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                promoted_soldier = get_object_or_404(Soldier, soldier_id=soldier_number)
                soldier_rank = request.POST.get('rank')
                soldier_promotion = Promotion(soldier=promoted_soldier, 
                                                        soldier_rank=soldier_rank, 
                                                        promotion_date=today,)
                soldier_promotion.save()                                        
        return redirect("armydbapp:soldier_list")

def awaiting_trial(request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                
        return render(request, "armydbapp/awaiting_trial.html",{"soldier_id":soldier_id,"names":names,},)

def submit_awaiting_trial(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                reason = request.POST.get('reason-awaiting-trial')
                Soldier.objects.filter(soldier_id=soldier_number).update(is_awaiting_trial=True)
                Soldier.objects.filter(soldier_id=soldier_number).update(reason_awaiting_trial= reason)     
                return redirect("armydbapp:soldier_list")
                
def dont_awaiting_trial(request):
        if request.method == "POST":
                return redirect("armydbapp:soldier_list")


def trial_done (request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                
        return render(request, "armydbapp/trial_done.html",{"soldier_id":soldier_id,"names":names,},)


def submit_trial_done(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                Soldier.objects.filter(soldier_id=soldier_number).update(is_awaiting_trial=False)               
                return redirect("armydbapp:soldier_list")

def dont_trial_done(request):
        if request.method == "POST":
                return redirect("armydbapp:soldier_list")

def reward_consumed (request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        
        return render(request, "armydbapp/reward_consumed.html",{"soldier_id":soldier_id,"names":names,},)


def submit_reward_consumed(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                Soldier.objects.filter(soldier_id=soldier_number).update(is_rewarded=False)               
                return redirect("armydbapp:soldier_list")

def dont_reward_consumed(request):
        if request.method == "POST":
                return redirect("armydbapp:soldier_list")

def absent (request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/absent.html",{"soldier_id":soldier_id,"names":names,},)


def submit_absent(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                Soldier.objects.filter(soldier_id=soldier_number).update(is_absent=True)               
                return redirect("armydbapp:soldier_list")

def dont_absent(request):
        if request.method == "POST":
                return redirect("armydbapp:soldier_list")

def present (request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/present.html",{"soldier_id":soldier_id,"names":names,},)


def submit_present(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                Soldier.objects.filter(soldier_id=soldier_number).update(is_absent=False)    
                Soldier.objects.filter(soldier_id=soldier_number).update(is_present=True)  
                Soldier.objects.filter(soldier_id=soldier_number).update(is_at_vacation=False)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_at_vacation_sick=False)          
                return redirect("armydbapp:soldier_list")

def dont_present(request):
        if request.method == "POST":
                return redirect("armydbapp:soldier_list")

def outing (request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/outing.html",{"soldier_id":soldier_id,"names":names,},)

def submit_outing(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                type_of_outing = request.POST.get('type_of_outing')
                Soldier.objects.filter(soldier_id=soldier_number).update(outing_type=type_of_outing)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_out=True)
                return redirect("armydbapp:soldier_list")

def no_outing (request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/no_outing.html",{"soldier_id":soldier_id,"names":names,},)

def submit_no_outing(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                Soldier.objects.filter(soldier_id=soldier_number).update(outing_type=None)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_out=False)
                return redirect("armydbapp:soldier_list")

def dont_no_outing(request):
        if request.method == "POST":
                return redirect("armydbapp:soldier_list")    


def mission (request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/mission.html",{"soldier_id":soldier_id,"names":names,},)

def submit_mission(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                type_of_mission = request.POST.get('type_of_mission')
                Soldier.objects.filter(soldier_id=soldier_number).update(mission_type=type_of_mission)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_in_mission=True)
                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_present=False)
                return redirect("armydbapp:soldier_list")

def no_mission (request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/no_mission.html",{"soldier_id":soldier_id,"names":names,},)

def submit_no_mission(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                Soldier.objects.filter(soldier_id=soldier_number).update(mission_type=None)
                Soldier.objects.filter(soldier_id=soldier_number).update(is_in_mission=False)
                Soldier.objects.filter(soldier_id=soldier.soldier_id).update(is_present=True)
                return redirect("armydbapp:soldier_list")

def dont_no_mission(request):
        if request.method == "POST":
                return redirect("armydbapp:soldier_list")    

def change_army_unit (request):
        soldier_id = request.GET.get('soldier_id')
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/change_army_unit.html",{"soldier_id":soldier_id,"names":names,},)

def submit_change_army_unit(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                soldier =  Soldier.objects.filter(soldier_id=soldier_number)
                soldier_army_unit_name = request.POST.get('soldier-army-unit-name')
                soldier_army_unit_number = request.POST.get('soldier-army-unit-number')
                soldier_current_army_unit = soldier_army_unit_number + " " + soldier_army_unit_name
                start_date_unit = today
                soldier_last_unit = Soldier.objects.get(soldier_id=soldier_number).current_army_unit
                
                last_unit =  SoldierArmyUnits.objects.filter(soldier= Soldier.objects.get(soldier_id=soldier_number), army_unit = soldier_last_unit)
                last_unit.update(end_date = today)
                
                

                soldier_unit = SoldierArmyUnits(soldier = Soldier.objects.get(soldier_id=soldier_number), 
                                                army_unit = soldier_current_army_unit, 
                                                start_date = start_date_unit, 
                                                )
                
                soldier.update(current_army_unit=soldier_current_army_unit)
                soldier_unit.save()

                return redirect("armydbapp:soldier_list")

def dont_change_army_unit(request):
        if request.method == "POST":
                return redirect("armydbapp:soldier_list")  

def numbering ():
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        number_of_soldiers = 0 
        number_of_at_vacation = 0
        number_of_at_vacation_sick = 0
        number_prisioned = 0
        number_out = 0 
        number_absent = 0
        number_mission = 0
        number_here = 0
        number_punished = 0
        number_returning = 0
        number_late_vacation = 0
        number_late_unit = 0 
        specialities=[]
        soldiers = Soldier.objects.all()
        awaiting_trial = 0 
        for soldier in soldiers:
                number_of_soldiers += 1 
                if soldier.is_awaiting_trial == True:
                        awaiting_trial +=1 
                if soldier.is_at_vacation:
                        number_of_at_vacation += 1
                if soldier.is_at_vacation_sick:
                        number_of_at_vacation_sick += 1
                if soldier.is_at_punishment: 
                        number_punished +=1
                        current_punishment = SoldierPunishments.objects.filter(soldier= soldier).get()
                        current_punishment = current_punishment.punishment
                        if current_punishment == "حبس":
                                number_prisioned += 1 
                if soldier.is_out:
                        number_out += 1
                if soldier.is_absent:
                        number_absent += 1
                if soldier.is_in_mission:
                        number_mission += 1
                if soldier.return_date == today:
                        number_returning += 1
                if soldier.return_date != None:
                        if daysBetweenDates(soldier.return_date.year, soldier.return_date.month, soldier.return_date.day, today.year, today.month, today.day) >= 31: 
                                number_late_vacation +=1

                if soldier.current_army_unit == "قيادة الكتيبة":
                        pass
                else:
                      
                    try:
                                                                
                        last_unit = SoldierArmyUnits.objects.get(soldier= soldier , army_unit = soldier.current_army_unit)
                        if last_unit.start_date != None:
                            if daysBetweenDates(last_unit.start_date.year, last_unit.start_date.month, last_unit.start_date.day, today.year, today.month, today.day) >= 90: 
                                    number_late_unit +=1
                    
                    except:
                        pass
                
                if soldier.speciality:
                        if soldier.speciality not in specialities:
                                specialities.append(soldier.speciality)

        number_of_specialities = [0] * len(specialities)
        for soldier in soldiers:
                for speciality in specialities:

                        if soldier.speciality == speciality:
                                number_of_specialities[specialities.index(speciality)] += 1 

        sum_number_of_specialities = str(sum(number_of_specialities))

        j=0
        for i in number_of_specialities:
                number_of_specialities[j]= str(i)
                j += 1 
        
        
        number_here = number_of_soldiers - (number_of_at_vacation + number_prisioned + number_out + number_absent + number_mission) 
        
        return  str(awaiting_trial),sum_number_of_specialities , number_of_specialities, specialities, str(number_of_at_vacation_sick), str(number_late_unit) , str(number_late_vacation), str(number_punished), str(number_of_soldiers), str(number_of_at_vacation), str(number_prisioned), str(number_out), str(number_absent), str(number_mission), str(number_here), str(number_returning)

def dof3at_radif():
        specialities=[]
        soldiers = Soldier.objects.all()
        dof3at = []
        
        for soldier in soldiers:
                if soldier.speciality:
                        if soldier.speciality not in specialities:
                                specialities.append(soldier.speciality)
                if soldier.service_end_date not in dof3at:
                        dof3at.append(soldier.service_end_date)

        
        dof3at.sort() 
        

        number_of_specialities = [0] * len(specialities)
        dof3a_number_of_specialities = [0] * len(dof3at)

        for i in range(0,len(dof3at)):
                dof3a_number_of_specialities[i] = [0] * len(specialities)
        
        for soldier in soldiers:
                for speciality in specialities:
                        if soldier.speciality == speciality:
                                dof3a_number_of_specialities[dof3at.index(soldier.service_end_date)][specialities.index(speciality)] += 1

        
        for i in range(0,(len(dof3at))):
                for j in range (0,(len(specialities))):
                        x = dof3a_number_of_specialities[i][j]
                        x = str(x)
                        dof3a_number_of_specialities[i][j]= x
                        
       
        
        
        j=0 
        for i in dof3at:
                dof3at[j] = str(i.year) + "/" + str(i.month) + "/" + str(i.day)
                j+=1 

        # lessa el vertical_sum = [] 
        #horizontal_sum 
        '''for i in range(0,(len(dof3at))):
                for x in dof3a_number_of_specialities[i]:
                        dof3a_number_of_specialities[i].append(dof3a_number_of_specialities[i])
        
        
        specialities.append("الاجمالي")'''
                            
        return dof3at, specialities, dof3a_number_of_specialities


def reward_list(request):
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/reward_list.html",{"soldier_list":soldier_list,"soldiers_punishments": soldiers_punishments,"names":names,},)

def punished_list(request):
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
        return render(request, "armydbapp/punished_list.html",{"soldier_list":soldier_list,"soldiers_punishments": soldiers_punishments,"names":names,},)


daysOfMonths = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def isLeapYear(year): #funtion returns true if the year is a leap year, false if the year is a common year 
    if year%4 != 0:
        return False
    elif year%100 != 0:
        return True
    elif year%400 !=0:
        return False 
    else:
        return True 

def daysOfMonth(month):
    return daysOfMonths[month-1]

def isDateBefore(y1, m1, d1, y2, m2, d2):
    if y1 < y2 :
        return True
    elif y1 == y2:
        if m1 < m2 :
            return True
        elif m1 == m2:
            return d1 < d2
    else:
        return False

def dayAfter (y, m, d):
    if isLeapYear(y):
        daysOfMonths[1]=29
    else:
        daysOfMonths[1]=28
        
    if d < daysOfMonth(m):
        return y,m,d+1
    if m < 12:
        return y, m+1 ,1
    else:
        return y+1 ,1,1
        

    
def daysBetweenDates(y1, m1, d1, y2, m2, d2):
    if isDateBefore(y1, m1, d1, y2, m2, d2) == False:
            return 0 
    days = 0
    while isDateBefore(y1, m1, d1, y2, m2, d2):
        y1,m1,d1=dayAfter(y1,m1,d1)
        days +=1 
    return days

def late_vacation_list(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]

                
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.return_date != None:
                        if daysBetweenDates(soldier.return_date.year, soldier.return_date.month, soldier.return_date.day, today.year, today.month, today.day) >= 31: 
                                soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/late_vacation_list.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)


def return_today_list(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.return_date == today:
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/return_today_list.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def late_unit_list(request):
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "قيادة الكتيبة":
                        pass
                else:
                    try:
                        last_unit =  SoldierArmyUnits.objects.get(soldier= soldier , army_unit = soldier.current_army_unit)
                        if last_unit.start_date != None:
                                if daysBetweenDates(last_unit.start_date.year, last_unit.start_date.month, last_unit.start_date.day, today.year, today.month, today.day) >= 90: 
                                        soldier_list_filtered.append(soldier)
                    except:
                        pass
        return render(request, "armydbapp/late_unit_list.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def absent_list(request):      
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.is_absent == True:
                        soldier_list_filtered.append(soldier)
                        return_date = soldier.return_date 
                        days_absent = daysBetweenDates(return_date.year, return_date.month, return_date.day, today.year, today.month, today.day)
                        days_absent = str(days_absent)
                        Soldier.objects.filter(soldier_id = soldier.soldier_id).update(days_absent = days_absent)

        return render(request, "armydbapp/absent_list.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def awaiting_trial_list(request):      
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.is_awaiting_trial == True:
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/awaiting_trial_list.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def vacation_choice(request):
        if request.method == "POST":
                soldier_number = request.POST.get('soldier_number')
                soldier = Soldier.objects.get(soldier_id=soldier_number)
                value = request.POST.get(soldier.id_tag)
                soldier.vacation_choice= value
                soldier.save()  
                        
        return redirect("armydbapp:soldier_list") 


def katiba_headquart(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "قيادة الكتيبة":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def s1_headquart(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "قيادة السرية الأولي":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_1(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "1 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_2(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "2 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_3(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "3 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_4(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "4 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_5(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "5 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_6(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "6 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_7(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "7 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_8(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "8 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_1(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "1 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_2(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "2 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_3(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "3 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_4(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "4 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_5(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "5 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_6(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "6 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_7(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "7 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_8(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "8 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def nahas(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "4 نحاس":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def s2_headquart(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "قيادة السرية الثانية":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_9(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "9 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_10(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "10 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_11(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "11 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def tagar_12(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "12 تاجر":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)


def ahmed_9(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "9 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_10(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "10 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_11(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "11 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def ahmed_12(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "12 أحمد":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_1(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "1 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_2(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "2 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_3(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "3 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_4(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "4 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_5(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "5 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_6(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "6 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_7(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "7 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_8(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "8 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_9(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "9 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_10(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "10 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_11(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "11 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def badi3_12(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "12 بديع":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)
def hisham_1(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "1 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_2(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "2 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_3(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "3 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_4(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "4 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_5(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "5 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_6(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "6 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_7(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "7 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_8(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "8 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_9(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "9 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_10(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "10 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_11(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "11 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def hisham_12(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "12 هشام":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)


def s3_headquart(request):
               
        soldier_list = Soldier.objects.all()
        soldier_list = soldier_list.order_by("name")
        soldiers_punishments = SoldierPunishments.objects.all()
        soldier_list_filtered = []
        names=[]
        for soldier in soldier_list:
                names.append(soldier.name)
                if soldier.current_army_unit == "قيادة السرية الثالثة":
                        soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def dof3a_radif(request):
        if request.method == "POST":
                dof3a = request.POST.get('dof3a')
                dof3a = datetime.datetime.strptime(dof3a, "%Y-%m-%d")
                soldier_list = Soldier.objects.all()
                soldier_list = soldier_list.order_by("name")
                soldiers_punishments = SoldierPunishments.objects.all()
                soldier_list_filtered = []
                names=[]
                for soldier in soldier_list:
                        names.append(soldier.name)
                        if soldier.service_end_date.year == dof3a.year:
                                if soldier.service_end_date.month == dof3a.month:
                                        if soldier.service_end_date.day == dof3a.day:
                                                soldier_list_filtered.append(soldier)

        return render(request, "armydbapp/soldier_list_filter.html",{"soldier_list_filtered":soldier_list_filtered,"soldiers_punishments": soldiers_punishments,"names":names,},)

def numbering_k10_head ():
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        number_of_soldiers_k10_head = 0 
        number_of_at_vacation_k10_head = 0
        number_of_at_vacation_sick_k10_head = 0
        number_prisioned_k10_head = 0
        number_out_k10_head = 0 
        number_absent_k10_head = 0
        number_mission_k10_head = 0
        number_here_k10_head = 0
        number_punished_k10_head = 0
        number_returning_k10_head = 0
        number_late_vacation_k10_head = 0
        number_late_unit_k10_head = 0 
        soldiers = Soldier.objects.all()
        
        for soldier in soldiers:
                if soldier.current_army_unit == "قيادة الكتيبة":
                        number_of_soldiers_k10_head += 1 
                        if soldier.is_at_vacation:
                                number_of_at_vacation_k10_head += 1
                        if soldier.is_at_vacation_sick:
                                number_of_at_vacation_sick_k10_head += 1
                        if soldier.is_at_punishment: 
                                number_punished_k10_head +=1
                                current_punishment = SoldierPunishments.objects.filter(soldier= soldier).get()
                                current_punishment = current_punishment.punishment
                                if current_punishment == "حبس":
                                        number_prisioned_k10_head += 1 
                        if soldier.is_out:
                                number_out_k10_head += 1
                        if soldier.is_absent:
                                number_absent_k10_head += 1
                        if soldier.is_in_mission:
                                number_mission_k10_head += 1
                        

        number_here_k10_head = number_of_soldiers_k10_head - (number_of_at_vacation_k10_head + number_prisioned_k10_head + number_out_k10_head + number_absent_k10_head + number_mission_k10_head) 
        
        return str(number_of_at_vacation_sick_k10_head), str(number_of_soldiers_k10_head), str(number_of_at_vacation_k10_head), str(number_prisioned_k10_head), str(number_out_k10_head), str(number_absent_k10_head), str(number_mission_k10_head), str(number_here_k10_head)


def numbering_s1_head ():
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        number_of_soldiers_s1_head = 0 
        number_of_at_vacation_s1_head = 0
        number_of_at_vacation_sick_s1_head = 0
        number_prisioned_s1_head = 0
        number_out_s1_head = 0 
        number_absent_s1_head = 0
        number_mission_s1_head = 0
        number_here_s1_head = 0
        number_punished_s1_head = 0
        number_returning_s1_head = 0
        number_late_vacation_s1_head = 0
        number_late_unit_s1_head = 0 
        soldiers = Soldier.objects.all()
        s1 = ["قيادة السرية الأولي","1 تاجر","2 تاجر","3 تاجر","4 تاجر","5 تاجر","6 تاجر","7 تاجر","8 تاجر","1 أحمد","2 أحمد","3 أحمد","4 أحمد","5 أحمد","6 أحمد","7 أحمد","8 أحمد","4 نحاس"]
        for soldier in soldiers:
                if soldier.current_army_unit in s1:
                        number_of_soldiers_s1_head += 1 
                        if soldier.is_at_vacation:
                                number_of_at_vacation_s1_head += 1
                        if soldier.is_at_vacation_sick:
                                number_of_at_vacation_sick_s1_head += 1
                        if soldier.is_at_punishment: 
                                number_punished_s1_head +=1
                                current_punishment = SoldierPunishments.objects.filter(soldier= soldier).get()
                                current_punishment = current_punishment.punishment
                                if current_punishment == "حبس":
                                        number_prisioned_s1_head += 1 
                        if soldier.is_out:
                                number_out_s1_head += 1
                        if soldier.is_absent:
                                number_absent_s1_head += 1
                        if soldier.is_in_mission:
                                number_mission_s1_head += 1
                        

        number_here_s1_head = number_of_soldiers_s1_head - (number_of_at_vacation_s1_head + number_prisioned_s1_head + number_out_s1_head + number_absent_s1_head + number_mission_s1_head) 
        
        return str(number_of_at_vacation_sick_s1_head), str(number_of_soldiers_s1_head), str(number_of_at_vacation_s1_head), str(number_prisioned_s1_head), str(number_out_s1_head), str(number_absent_s1_head), str(number_mission_s1_head), str(number_here_s1_head)

def numbering_s2_head ():
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        number_of_soldiers_s2_head = 0 
        number_of_at_vacation_s2_head = 0
        number_of_at_vacation_sick_s2_head = 0
        number_prisioned_s2_head = 0
        number_out_s2_head = 0 
        number_absent_s2_head = 0
        number_mission_s2_head = 0
        number_here_s2_head = 0
        number_punished_s2_head = 0
        number_returning_s2_head = 0
        number_late_vacation_s2_head = 0
        number_late_unit_s2_head = 0 
        soldiers = Soldier.objects.all()
        s2 = ["قيادة السرية الثانية","9 تاجر","10 تاجر","11 تاجر","12 تاجر","11 أحمد","12 أحمد","10 أحمد","9 أحمد","1 بديع","2 بديع","3 بديع", "4 بديع", "1 هشام","2 هشام","3 هشام", "4 هشام",]
        for soldier in soldiers:
                if soldier.current_army_unit in s2:
                        number_of_soldiers_s2_head += 1 
                        if soldier.is_at_vacation:
                                number_of_at_vacation_s2_head += 1
                        if soldier.is_at_vacation_sick:
                                number_of_at_vacation_sick_s2_head += 1
                        if soldier.is_at_punishment: 
                                number_punished_s2_head +=1
                                current_punishment = SoldierPunishments.objects.filter(soldier= soldier).get()
                                current_punishment = current_punishment.punishment
                                if current_punishment == "حبس":
                                        number_prisioned_s2_head += 1 
                        if soldier.is_out:
                                number_out_s2_head += 1
                        if soldier.is_absent:
                                number_absent_s2_head += 1
                        if soldier.is_in_mission:
                                number_mission_s2_head += 1
                        

        number_here_s2_head = number_of_soldiers_s2_head - (number_of_at_vacation_s2_head + number_prisioned_s2_head + number_out_s2_head + number_absent_s2_head + number_mission_s2_head) 
        
        return str(number_of_at_vacation_sick_s2_head), str(number_of_soldiers_s2_head), str(number_of_at_vacation_s2_head), str(number_prisioned_s2_head), str(number_out_s2_head), str(number_absent_s2_head), str(number_mission_s2_head), str(number_here_s2_head)


def numbering_s3_head ():
        today = datetime.datetime.now()
        today = datetime.date(today.year,today.month,today.day)
        number_of_soldiers_s3_head = 0 
        number_of_at_vacation_s3_head = 0
        number_of_at_vacation_sick_s3_head = 0
        number_prisioned_s3_head = 0
        number_out_s3_head = 0 
        number_absent_s3_head = 0
        number_mission_s3_head = 0
        number_here_s3_head = 0
        number_punished_s3_head = 0
        number_returning_s3_head = 0
        number_late_vacation_s3_head = 0
        number_late_unit_s3_head = 0 
        soldiers = Soldier.objects.all()
        s3 = ["قيادة السرية الثالثة","5 بديع","6 بديع","7 بديع","8 بديع","9 بديع","10 بديع","11 بديع","12 بديع","5 هشام","6 هشام","7 هشام","8 هشام","9 هشام","10 هشام","11 هشام","12 هشام",]
        for soldier in soldiers:
                if soldier.current_army_unit in s3:
                        number_of_soldiers_s3_head += 1 
                        if soldier.is_at_vacation:
                                number_of_at_vacation_s3_head += 1
                        if soldier.is_at_vacation_sick:
                                number_of_at_vacation_sick_s3_head += 1
                        if soldier.is_at_punishment: 
                                number_punished_s3_head +=1
                                current_punishment = SoldierPunishments.objects.filter(soldier= soldier).get()
                                current_punishment = current_punishment.punishment
                                if current_punishment == "حبس":
                                        number_prisioned_s3_head += 1 
                        if soldier.is_out:
                                number_out_s3_head += 1
                        if soldier.is_absent:
                                number_absent_s3_head += 1
                        if soldier.is_in_mission:
                                number_mission_s3_head += 1
                        

        number_here_s3_head = number_of_soldiers_s3_head - (number_of_at_vacation_s3_head + number_prisioned_s3_head + number_out_s3_head + number_absent_s3_head + number_mission_s3_head) 
        
        return str(number_of_at_vacation_sick_s3_head), str(number_of_soldiers_s3_head), str(number_of_at_vacation_s3_head), str(number_prisioned_s3_head), str(number_out_s3_head), str(number_absent_s3_head), str(number_mission_s3_head), str(number_here_s3_head)



def gen_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    return FileResponse(buffer, as_attachment=True, filename='قاعدة البيانات.pdf')

