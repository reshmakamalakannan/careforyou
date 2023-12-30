from django.db import models
class SignModel(models.Model):
    u_id=models.AutoField(primary_key=True,auto_created=True)
    username=models.CharField(max_length=50)
    u_dob=models.DateField()
    u_emailid=models.EmailField(max_length=60)
    u_password=models.CharField(max_length=256)
    u_phno=models.CharField(max_length=10)
    u_gender=models.CharField(max_length=10)
    class Meta:
        db_table="signup"
class AdminModel(models.Model):
    adminname=models.CharField(max_length=50)
    adminpass=models.CharField(max_length=50)
    class Meta:
        db_table="admin"
class DoctorModel(models.Model):
    doc_id=models.AutoField(primary_key=True,auto_created=True)
    docname=models.CharField(max_length=50)
    specialist=models.CharField(max_length=50)
    doc_emailid=models.EmailField(max_length=60)
    doc_addr=models.CharField(max_length=50)
    doc_phno=models.CharField(max_length=10)
    doc_gender=models.CharField(max_length=10)
    doc_num=models.CharField(max_length=5)
    doc_expr=models.IntegerField()
    class Meta:
        db_table="doctor"
class DHistory(models.Model):
    dhis_id=models.AutoField(primary_key=True,auto_created=True)
    preg=models.IntegerField()
    glucose=models.IntegerField()
    bp=models.IntegerField()
    skinthick=models.IntegerField()
    insulin=models.IntegerField()
    weight=models.FloatField()
    height=models.FloatField()
    pedigree=models.CharField(max_length=50)
    age=models.IntegerField()
    d_result=models.CharField(max_length=15)
    u_id=models.IntegerField()
    d_date=models.DateTimeField()
    class Meta:
        db_table="dhistory"
class LHistory(models.Model):
    lhis_id=models.AutoField(primary_key=True,auto_created=True)
    gender=models.CharField(max_length=10)
    age=models.IntegerField()
    smoking=models.CharField(max_length=5)
    yellow_fingers=models.CharField(max_length=5)
    anxiety =models.CharField(max_length=5)
    peer_pressure = models.CharField(max_length=5)
    chronic_disease = models.CharField(max_length=5)
    fatigue = models.CharField(max_length=5)
    allergy = models.CharField(max_length=5)
    wheezing = models.CharField(max_length=5)
    alcohol = models.CharField(max_length=5)
    coughing = models.CharField(max_length=5)
    shortness_of_breath= models.CharField(max_length=5)
    swallowing_difficulty = models.CharField(max_length=5)
    chest_pain = models.CharField(max_length=5)
    l_result=models.CharField(max_length=15)
    u_id=models.IntegerField()
    l_date=models.DateTimeField()
    class Meta:
        db_table="lhistory"
class HeartHistory(models.Model):
    hhis_id=models.AutoField(primary_key=True,auto_created=True)
    age=models.IntegerField()
    sex=models.CharField(max_length=10)
    chestpaintype=models.CharField(max_length=10)
    restingbp=models.IntegerField()
    cholesterol=models.IntegerField()
    fastingbs=models.CharField(max_length=5)
    restingecg=models.CharField(max_length=10)
    maxhr=models.IntegerField()
    exerciseangina=models.CharField(max_length=5)
    oldpeak=models.FloatField()
    st_slope=models.CharField(max_length=10)
    h_result=models.CharField(max_length=15)
    u_id=models.IntegerField()
    h_date=models.DateTimeField()
    class Meta:
        db_table="hearthistory"
class SHistory(models.Model):
    shis_id=models.AutoField(primary_key=True,auto_created=True)
    gender=models.CharField(max_length=10)
    age=models.IntegerField()
    hypertension=models.CharField(max_length=5)
    heart_disease=models.CharField(max_length=5)
    ever_married=models.CharField(max_length=15)
    work_type=models.CharField(max_length=20)
    residence_type=models.CharField(max_length=10)
    avg_glucose_level=models.FloatField()
    weight=models.FloatField()
    height=models.FloatField()
    smoking_status=models.CharField(max_length=20)
    s_result=models.CharField(max_length=15)
    u_id=models.IntegerField()
    s_date=models.DateTimeField()
    class Meta:
        db_table="shistory"
class FeedbackModel(models.Model):
    f_id=models.AutoField(primary_key=True,auto_created=True)
    rating=models.IntegerField()
    f_message=models.CharField(max_length=300)
    u_id=models.IntegerField()
    class Meta:
        db_table="feedback"
class Appointment(models.Model):
    appo_id=models.AutoField(primary_key=True,auto_created=True)
    appo_date=models.DateField()
    appo_time=models.TimeField()
    u_id=models.IntegerField()
    pat_name=models.CharField(max_length=50)
    pat_age=models.IntegerField()
    pat_sympt=models.CharField(max_length=50)
    pat_phno=models.CharField(max_length=10)
    doc_id=models.IntegerField()
    doc_name=models.CharField(max_length=50)
    doc_specialist=models.CharField(max_length=50)
    doc_phno=models.CharField(max_length=10)
    doc_addr=models.CharField(max_length=50)
    class Meta:
        db_table="appointment"