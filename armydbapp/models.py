# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class SoldierAdmin(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Soldier(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, unique = False)
    soldier_img= models.ImageField(null=True, blank=True, unique=False, upload_to="soldiers_imgs/")
    soldier_id = models.IntegerField(null=False, blank=False, unique=True)
    service_start_date = models.DateField(null=False, blank=False, unique = False)
    service_end_date = models.DateField(null=False, blank=False, unique = False)
    current_army_unit = models.CharField(max_length=256, null=True, blank=True, unique = False)
    speciality =  models.CharField(max_length=50, null=True, blank=True, unique = False , default="مراقب جوي")
    adress =  models.CharField(max_length=256, null=True, blank=True, unique = False)
    vacation_choice= models.IntegerField(null=True, blank=True, unique=False, default="1")

    id_tag= models.CharField(max_length=256, null=True, blank=True, unique = False)
    #id_row= models.CharField(max_length=256, null=True, blank=True, unique = False)
    
    is_at_vacation = models.BooleanField(default=False)
    is_at_vacation_sick = models.BooleanField(default=False)
    return_date = models.DateField(null=True, blank=True)
    
    is_rewarded = models.BooleanField(default=False)
    reward_days = models.IntegerField(null=True, blank=True)
    
    
    is_at_punishment = models.BooleanField(default=False)
    current_punishment = models.ForeignKey("SoldierPunishments", null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    is_awaiting_trial = models.BooleanField(default=False)
    reason_awaiting_trial= models.CharField(max_length=1200, null=True, blank=True, unique = False)

    is_out= models.BooleanField(default=False)
    outing_type = models.CharField(max_length=256, null=True, blank=True, unique = False)

    is_absent = models.BooleanField(default=False)
    days_absent= models.CharField(max_length=256, null=True, blank=True, unique = False)
    is_present = models.BooleanField(default=True)
    
    
    is_in_mission = models.BooleanField(default=False)
    mission_type = models.CharField(max_length=256, null=True, blank=True, unique = False)

    work_assigned = models.CharField(max_length=256, null=True, blank=True, unique = False)
    zucchini = models.CharField(max_length=256, null=True, blank=True, unique = False)
    job = models.CharField(max_length=256, null=True, blank=True, unique = False)
    
    remarks = models.CharField(max_length=2560, null=True, blank=True, unique = False)

class Rewards (models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    reward_days = models.IntegerField(null=True, blank=True)
    reward_date = models.DateField(auto_now=True,null=True, blank=True)


class SoldierArmyUnits(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    army_unit = models.CharField(max_length=256, null=True, blank=True, unique = False)
    start_date = models.DateField(null=False, blank=False, unique = False)
    end_date = models.DateField(null=True, blank=True, unique = False, default = None)

class SoldierPunishments(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    punishment = models.CharField(max_length=256, null=False, blank=False, unique = False)
    start_date = models.DateField(null=False, blank=False, unique = False)
    end_date = models.DateField(null=False, blank=False, unique = False)

class Promotion (models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    soldier_rank = models.CharField(max_length=256,null=True, blank=True , default = "جندي")
    promotion_date = models.DateField(null=True, blank=True, default = None)

class Vacations(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True , unique = False, default = None)
    end_date = models.DateField(null=True, blank=True, unique = False, default = None)