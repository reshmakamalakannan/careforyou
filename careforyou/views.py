from django.shortcuts import render,redirect
from django.contrib import messages
from passlib.hash import pbkdf2_sha256
from careforyou.models import SignModel,AdminModel,DoctorModel,DHistory,LHistory,HeartHistory,SHistory,FeedbackModel,Appointment
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from .decorators import my_login_required,email_required,admin_login_required
from joblib import load
from django.template.loader import render_to_string
from datetime import datetime
from pytz import timezone 


heartrfc=load('./savedModels/heartrfc.joblib')
diabeteslogre=load('./savedModels/diabeteslogre.joblib')
lungsvm=load('./savedModels/lungsvm.joblib')

def home(request):
    return render(request,"home.html")
def about(request):
    return render(request,"about.html")
def healthy_living(request):
    return render(request,"healthy_living.html")
def stroketips(request):
    return render(request,"stroketips.html")
def visiontips(request):
    return render(request,"visiontips.html")
def menstrualtips(request):
    return render(request,"menstrualtips.html")
def hearttips(request):
    return render(request,"hearttips.html")
def seasontips(request):
    return render(request,"seasontips.html")
def lungtips(request):
    return render(request,"lungtips.html")
def agetips(request):
    return render(request,"agetips.html")
def covidtips(request):
    return render(request,"covidtips.html")
def Diabetestips(request):
    return render(request,"Diabetestips.html")

def adminlogin(request):
    if request.method=="POST":
        if (request.POST.get('adminname') and request.POST.get('adminpass')):
            data=AdminModel.objects.all()
            for result in data:
                if(result.adminname==request.POST.get('adminname') and 
                result.adminpass==request.POST.get('adminpass')):
                    request.session['admin_log']=True
                    return redirect("adminhome")         
            else:
                messages.error(request,"Alert")
    return render(request,"adminlogin.html")

def adminlogout(request):
    try:
        del request.session['admin_log']
		#request.session.flush()
    except:
        return redirect('adminlogin')
    return redirect('adminlogin')

@admin_login_required
def adminhome(request):
    dict={
    'total_users':SignModel.objects.all().count(),
    'total_doctors':DoctorModel.objects.all().count(),
    'total_feedback':FeedbackModel.objects.all().count(),
    'total_appoint':Appointment.objects.all().count(),
    }
    return render(request,"adminhome.html",context=dict)

@admin_login_required
def totalusers(request):
    showall=SignModel.objects.all().order_by('u_id').values()
    return render(request,'totalusers.html',{"data":showall})

@admin_login_required
def totalfeedback(request):
    showall=FeedbackModel.objects.all()
    return render(request,'totalfeedback.html',{"data":showall})

@admin_login_required
def totalappoints(request):
    showall=Appointment.objects.all().order_by('appo_id').values()
    alldates=Appointment.objects.all().order_by('appo_date').values('appo_date').distinct()
    return render(request,'totalappoints.html',{"data":showall,"datas":alldates})

@admin_login_required
def adddoctor(request):
    if request.method=="POST":
        saverecord=DoctorModel()
        saverecord.docname=request.POST.get('docname')
        saverecord.doc_emailid=request.POST.get('doc_emailid')
        saverecord.doc_phno=request.POST.get('doc_phno')
        saverecord.doc_gender=request.POST.get('doc_gender')
        saverecord.doc_addr=request.POST.get('doc_addr')
        saverecord.doc_num=request.POST.get('doc_num')
        saverecord.specialist=request.POST.get('specialist')
        saverecord.doc_expr=request.POST.get('doc_expr')
        saverecord.save()
    return render(request,"adddoctor.html")

@admin_login_required
def viewdoctor(request):
     showall=DoctorModel.objects.all().order_by('doc_id').values()
     return render(request,"viewdoctor.html",{"data":showall})

@admin_login_required
def editdoct(request,id):
    doct = DoctorModel.objects.get(doc_id=id)
    if request.method == "POST":
        doct.docname = request.POST.get('docname')
        doct.doc_gender = request.POST.get('doc_gender')
        doct.specialist = request.POST.get('specialist')
        doct.doc_expr = request.POST.get('doc_expr')
        doct.doc_emailid = request.POST.get('doc_emailid')
        doct.doc_phno = request.POST.get('doc_phno')
        doct.doc_addr = request.POST.get('doc_addr')
        doct.doc_num= request.POST.get('doc_num')
        doct.save()
        return redirect('viewdoctor')
    context = {'doct':doct}
    return render(request, 'editdoct.html', context)
    
def userlogin(request):
    if request.method=="POST":
        if request.POST.get('email_id') and request.POST.get('password'):
            data=SignModel.objects.all()
            for result in data:
                if(result.u_emailid==request.POST.get('email_id') and 
                pbkdf2_sha256.verify(request.POST.get('password'),result.u_password)):
                    request.session['username'] = result.username
                    request.session['u_id'] = result.u_id
                    print(request.session['username'],request.session['u_id'])
                    return redirect("userhome")         
            else:
                messages.error(request,"Alert")
    return render(request,"userlogin.html")

def userlogout(request):
	try:
		del request.session['username']
		del request.session['u_id']
		#request.session.flush()
	except:
		return redirect('userlogin')
	return redirect('userlogin')

def validate_email(request):
    if request.method=="POST":
        u_emailid=request.POST.get('u_emailid')
        if SignModel.objects.filter(u_emailid=u_emailid).first():
            user=SignModel.objects.filter(u_emailid=u_emailid).first()
            html_content = render_to_string("email_template.html",{'user':user})
            text_content=strip_tags(html_content)
            email=EmailMultiAlternatives("CareForYou Reset Password",text_content,"settings.EMAIL_HOST_USER",[u_emailid])
            email.attach_alternative(html_content,"text/html")
            email.fail_silenty=False
            email.send()
            request.session['useremail']=u_emailid
            return redirect('email_sent')
        else:
            messages.error(request,"Alert")
    return render(request,"validate_email.html")

@email_required
def email_sent(request):
    return render(request,"email_sent.html")

@email_required
def reset_password(request):
    if request.method=="POST":
        if((request.POST.get('pass')==request.POST.get('conpass'))):
            #SignModel.objects.filter(pk=result.id).update(u_pass=pbkdf2_sha256.encrypt(request.POST.get('u_pass'),rounds=12000,salt_size=32))
            useremail=request.session['useremail']
            saverecord=SignModel.objects.get(u_emailid=useremail)
            saverecord.u_password=pbkdf2_sha256.encrypt(request.POST.get('pass'),rounds=12000,salt_size=32)
            saverecord.save(update_fields=["u_password"])
            del request.session['useremail']
            print("password reset successful")
            return redirect('successreset')
        else:
            messages.error(request,"Alert")
    return render(request,"reset_password.html")

def successreset(request):
    return render(request,"successreset.html")

def onlyonce(request):
    return render(request,"onlyonce.html")

@my_login_required
def userhome(request):
    if 'username' in request.session:
        current_user = request.session['username']
        param = {'current_user': current_user}
        return render(request, 'userhome.html', param)
    else:
        return redirect('userlogin.html')

@my_login_required
def editprofile(request):
    if 'username' in request.session:
        id=request.session['u_id']
        current_user = request.session['username']
        usr= SignModel.objects.get(u_id=id)
        if request.method == "POST":
            usr.username = request.POST.get('username')
            usr.u_emailid = request.POST.get('u_emailid')
            usr.u_dob = request.POST.get('u_dob')
            usr.u_phno = request.POST.get('u_phno')
            usr.u_gender = request.POST.get('u_gender')
            usr.save()
            request.session['username']=usr.username
    current_user = request.session['username']
    param = {'current_user': current_user,'usr':usr}
    return render(request, 'editprofile.html', param)

def usersign(request):
    if request.method=="POST":
        if SignModel.objects.filter(u_emailid=request.POST.get('u_emailid')).count()>0:
            messages.error(request,"Alert")
            return render(request,"usersign.html")
        else:
            saverecord=SignModel()
            saverecord.username=request.POST.get('username')
            saverecord.u_dob=request.POST.get('u_dob')
            saverecord.u_emailid=request.POST.get('u_emailid')
            enc_password=pbkdf2_sha256.encrypt(request.POST.get('u_password'),rounds=12000,salt_size=32)
            saverecord.u_password=enc_password
            saverecord.u_phno=request.POST.get('u_phno')
            saverecord.u_gender=request.POST.get('u_gender')
            saverecord.save()
            html_content = render_to_string("signup_template.html",{'username':request.POST.get('username')})
            text_content=strip_tags(html_content)
            email=EmailMultiAlternatives("CareForYou",text_content,"settings.EMAIL_HOST_USER",[request.POST.get('u_emailid')])
            email.attach_alternative(html_content,"text/html")
            email.fail_silenty=False
            email.send()
            return redirect("userlogin")
    else:
        return render(request,"usersign.html")

@my_login_required
def delSHist(request,id):
    delSHis=SHistory.objects.get(shis_id=id)
    delSHis.delete()
    return redirect('shistory')

@my_login_required
def shistory(request):
    id=request.session['u_id']
    showall=SHistory.objects.filter(u_id=id).all()
    return render(request,"shistory.html",{"data":showall})

@my_login_required
def strokeresult(request):
    st=pd.read_csv("Datasets/healthcare-dataset-stroke-data.csv")
    st.drop("id",axis=1,inplace=True)
    st["bmi"].fillna(st["bmi"].mean(),inplace=True)
    st.gender.replace({"Male":1,"Female":0,"Other":2},inplace=True)
    st.ever_married.replace({"Yes":1,"No":0},inplace=True)
    st.work_type.replace({"Private":2,"Self-employed":3,"Govt_job":0,"children":4,"Never_worked":1},inplace=True)
    st.Residence_type.replace({"Urban":1,"Rural":0},inplace=True)
    st.smoking_status.replace({"formerly smoked":1,"never smoked":2,"smokes":3,"Unknown":0},inplace=True)
    st_x=st.iloc[:,:-1]
    st_y=st.iloc[:,-1]
    st_x_train, st_x_test, st_y_train, st_y_test=train_test_split(st_x,st_y,test_size=0.2,random_state=101)
    rfc=RandomForestClassifier()
    rfc.fit(st_x_train.values,st_y_train)

    gender=int(request.POST['gender'])
    age=int(request.POST['age'])
    hypertension=int(request.POST['hypertension'])
    heart_disease = int(request.POST['heart_disease'])
    ever_married = int(request.POST['ever_married'])
    work_type = int(request.POST['work_type'])
    Residence_type = int(request.POST['Residence_type'])
    avg_glucose_level = float(request.POST['avg_glucose_level'])
    weight = float(request.POST['weight'])
    height = float(request.POST['height'])
    calculated_bmi = weight / (height/100)**2
    print(calculated_bmi)
    bmi = calculated_bmi
    smoking_status = int(request.POST['smoking_status'])

    pred=rfc.predict([[gender,age,hypertension,heart_disease,ever_married,work_type,Residence_type,
                avg_glucose_level,bmi,smoking_status]])
    result=""
    if pred==[1]:
        result="positive"
    else:
        result="negative"
    saverecord=SHistory()
    saverecord.gender='Female' if(request.POST['gender']=='0') else 'Male' if(request.POST['gender']=='1') else 'Others'
    saverecord.age=request.POST['age']
    saverecord.hypertension='Yes' if (request.POST['hypertension']=='1') else 'No'
    saverecord.heart_disease='Yes' if (request.POST['heart_disease']=='1') else 'No'
    saverecord.ever_married='Married' if (request.POST['ever_married']=='1') else 'Not Married'
    saverecord.work_type='Government Job' if (request.POST['work_type']=='0') else 'Never Worked' if (request.POST['work_type']=='1') else 'Private Job' if (request.POST['work_type']=='2') else 'Self Employed' if (request.POST['work_type']=='3') else 'Children'
    saverecord.residence_type='Urban' if (request.POST['Residence_type']=='1') else 'Rural'
    saverecord.avg_glucose_level=request.POST['avg_glucose_level']
    saverecord.weight=request.POST['weight']
    saverecord.height=request.POST['height']
    saverecord.smoking_status='Unknown' if (request.POST['smoking_status']=='0') else 'Formerly Smoked' if (request.POST['smoking_status']=='1') else 'Never Smoked' if (request.POST['smoking_status']=='2') else 'Smokes'
    saverecord.s_result=result
    saverecord.s_date=datetime.now(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    id=request.session['u_id']
    saverecord.u_id=id
    saverecord.save()
    return render(request,"strokeresult.html",{"result":result})

@my_login_required
def strokepredict(request):
    return render(request,"strokepredict.html")

@my_login_required
def delDHist(request,id):
    delDHis=DHistory.objects.get(dhis_id=id)
    delDHis.delete()
    return redirect('dhistory')

@my_login_required
def dhistory(request):
    id=request.session['u_id']
    showall=DHistory.objects.filter(u_id=id).all()
    return render(request,"dhistory.html",{"data":showall})

@my_login_required
def diabetespredict(request):
    return render(request,"diabetespredict.html")

@my_login_required
def diabetesresult(request):
    Pregnancies=int(request.POST['Pregnancies'])
    Glucose=float(request.POST['Glucose'])
    BloodPressure=int(request.POST['BloodPressure'])
    SkinThickness = float(request.POST['SkinThickness'])
    Insulin = float(request.POST['Insulin'])
    weight = float(request.POST['weight'])
    height = float(request.POST['height'])
    calculated_bmi = weight / (height/100)**2
    print(calculated_bmi)
    BMI = calculated_bmi
    DiabetesPedigreeFunction=int(request.POST['DiabetesPedigreeFunction'])
    Age=int(request.POST['Age'])

    pred=diabeteslogre.predict([[Pregnancies,Glucose,BloodPressure,SkinThickness,
    Insulin,BMI,DiabetesPedigreeFunction,Age]])
    result=""
    if pred==[1]:
        result="positive"
    else:
        result="negative"
    saverecord=DHistory()
    saverecord.preg=request.POST['Pregnancies']
    saverecord.glucose=request.POST['Glucose']
    saverecord.bp=request.POST['BloodPressure']
    saverecord.skinthick=request.POST['SkinThickness']
    saverecord.insulin=request.POST['Insulin']
    saverecord.weight=request.POST['weight']
    saverecord.height=request.POST['height']
    saverecord.pedigree='No Family History' if (request.POST['DiabetesPedigreeFunction']=='0') else 'One parent has diabetes'  if (request.POST['DiabetesPedigreeFunction']=='1') else 'Both parents have diabetes' 
    saverecord.age=request.POST['Age']
    saverecord.d_result=result
    saverecord.d_date=datetime.now(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    id=request.session['u_id']
    saverecord.u_id=id
    saverecord.save()
    return render(request,"diabetesresult.html",{"result":result})

@my_login_required
def delHeartHist(request,id):
    delHeartHis=HeartHistory.objects.get(hhis_id=id)
    delHeartHis.delete()
    return redirect('hearthistory')

@my_login_required
def hearthistory(request):
    id=request.session['u_id']
    showall=HeartHistory.objects.filter(u_id=id).all()
    return render(request,"hearthistory.html",{"data":showall})

@my_login_required
def heartpredict(request):
    return render(request,"heartpredict.html")

@my_login_required
def heartresult(request):
    Age=int(request.POST['Age'])
    Sex=int(request.POST['Sex'])
    ChestPainType=int(request.POST['ChestPainType'])
    RestingBP = int(request.POST['RestingBP'])
    Cholesterol = int(request.POST['Cholesterol'])
    FastingBS = int(request.POST['FastingBS'])
    RestingECG = int(request.POST['RestingECG'])
    MaxHR = int(request.POST['MaxHR'])
    ExerciseAngina = int(request.POST['ExerciseAngina'])
    Oldpeak = float(request.POST['Oldpeak'])
    ST_Slope = int(request.POST['ST_Slope'])

    pred=heartrfc.predict([[Age,Sex,ChestPainType,RestingBP,Cholesterol,FastingBS,RestingECG,MaxHR,ExerciseAngina,Oldpeak,ST_Slope]])
    result=""
    if pred==[1]:
        result="positive"
    else:
        result="negative"
    saverecord=HeartHistory()
    saverecord.age=request.POST['Age']
    saverecord.sex='Male' if(request.POST['Sex']=='0') else 'Female'
    saverecord.chestpaintype='ASY' if (request.POST['ChestPainType']=='0') else 'NAP' if (request.POST['ChestPainType']=='1') else 'ATA' if (request.POST['ChestPainType']=='2') else 'TA'
    saverecord.restingbp=request.POST['RestingBP']
    saverecord.cholesterol=request.POST['Cholesterol']
    saverecord.fastingbs='Yes' if (request.POST['FastingBS']=='1') else 'No'
    saverecord.restingecg='Normal' if (request.POST['RestingECG']=='0') else 'LVH' if (request.POST['RestingECG']=='1') else 'ST'
    saverecord.maxhr=request.POST['MaxHR']
    saverecord.exerciseangina='Yes' if (request.POST['ExerciseAngina']=='1') else 'No'
    saverecord.oldpeak=request.POST['Oldpeak']
    saverecord.st_slope='Flat' if (request.POST['ST_Slope']=='0') else 'Up' if (request.POST['ST_Slope']=='1') else 'Down'
    saverecord.h_result=result
    saverecord.h_date=datetime.now(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    id=request.session['u_id']
    saverecord.u_id=id
    saverecord.save()
    return render(request,"heartresult.html",{"result":result})

@my_login_required
def delLHist(request,id):
    delLHis=LHistory.objects.get(lhis_id=id)
    delLHis.delete()
    return redirect('lhistory')

@my_login_required
def lhistory(request):
    id=request.session['u_id']
    showall=LHistory.objects.filter(u_id=id).all()
    return render(request,"lhistory.html",{"data":showall})

@my_login_required
def lungcancer(request):
    return render(request,"lungcancer.html")

@my_login_required
def lungresult(request):
    gender=int(request.POST['gender'])
    age=int(request.POST['age'])
    smoking=int(request.POST['smoking'])
    yellow_fingers = int(request.POST['yellow_fingers'])
    anxiety = int(request.POST['anxiety'])
    peer_pressure = int(request.POST['peer_pressure'])
    chronic_disease = int(request.POST['chronic_disease'])
    fatigue = int(request.POST['fatigue'])
    allergy = int(request.POST['allergy'])
    wheezing = int(request.POST['wheezing'])
    alcohol = int(request.POST['alcohol'])
    coughing = int(request.POST['coughing'])
    shortness_of_breath= int(request.POST['shortness_of_breath'])
    swallowing_difficulty = int(request.POST['swallowing_difficulty'])
    chest_pain = int(request.POST['chest_pain'])
    pred=lungsvm.predict([[gender,age,smoking,yellow_fingers,anxiety,peer_pressure,
    chronic_disease,fatigue,allergy,wheezing,alcohol,coughing,shortness_of_breath,
    swallowing_difficulty,chest_pain]])
    result=""
    if pred==[2]:
        result="positive"
    else:
        result="negative"
    saverecord=LHistory()
    saverecord.gender='Male' if(request.POST['gender']=='0') else 'Female'
    saverecord.age=request.POST['age']
    saverecord.smoking='Yes' if (request.POST['smoking']=='2') else 'No'
    saverecord.yellow_fingers='Yes' if (request.POST['yellow_fingers']=='2') else 'No'
    saverecord.anxiety='Yes' if (request.POST['anxiety']=='2') else 'No'
    saverecord.peer_pressure='Yes' if (request.POST['peer_pressure']=='2') else 'No'
    saverecord.chronic_disease='Yes' if (request.POST['chronic_disease']=='2') else 'No'
    saverecord.fatigue='Yes' if (request.POST['fatigue']=='2') else 'No'
    saverecord.allergy='Yes' if (request.POST['allergy']=='2') else 'No'
    saverecord.wheezing='Yes' if (request.POST['wheezing']=='2') else 'No'
    saverecord.alcohol='Yes' if (request.POST['alcohol']=='2') else 'No'
    saverecord.coughing='Yes' if (request.POST['coughing']=='2') else 'No'
    saverecord.shortness_of_breath='Yes' if (request.POST['shortness_of_breath']=='2') else 'No'
    saverecord.swallowing_difficulty='Yes' if (request.POST['swallowing_difficulty']=='2') else 'No'
    saverecord.chest_pain='Yes' if (request.POST['chest_pain']=='2') else 'No'
    saverecord.l_result=result
    saverecord.l_date=datetime.now(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    id=request.session['u_id']
    saverecord.u_id=id
    saverecord.save()
    return render(request,"lungresult.html",{"result":result})

@my_login_required
def feedback(request):
    if 'username' in request.session:
        current_user = request.session['username']
        param = {'current_user': current_user}
        if request.method=="POST":
            saverecord=FeedbackModel()
            saverecord.rating=request.POST.get('rate')
            saverecord.f_message=request.POST.get('f_message')
            id=request.session['u_id']
            saverecord.u_id=id
            saverecord.save()
        return render(request, 'feedback.html', param)
    else:
        return render(request,"userlogin.html")

@my_login_required
def bookappoint(request):
    if 'username' in request.session:
        current_user = request.session['username']
        showall=DoctorModel.objects.all().order_by('doc_id').values()
        param = {'current_user': current_user,'data':showall}
        return render(request, 'bookappoint.html', param)
    else:
        return render(request,"userlogin.html")

@my_login_required
def appointpage(request,id):
    if 'username' in request.session:
        current_user = request.session['username']
        doct = DoctorModel.objects.get(doc_id=id)
        param = {'current_user': current_user,'doct':doct}
        if request.method=="POST":
            saverecord=Appointment()
            saverecord.appo_date=request.POST.get('appo_date')
            saverecord.appo_time=request.POST.get('appo_time')
            saverecord.pat_name=request.POST.get('pat_name')
            saverecord.pat_age=request.POST.get('pat_age')
            saverecord.pat_sympt=request.POST.get('pat_sympt')
            saverecord.pat_phno=request.POST.get('pat_phno')
            saverecord.doc_name=doct.docname
            saverecord.doc_specialist=doct.specialist
            saverecord.doc_phno=doct.doc_phno
            saverecord.doc_addr=doct.doc_addr
            saverecord.doc_id=doct.doc_id
            id=request.session['u_id']
            saverecord.u_id=id
            saverecord.save()
            appo=Appointment.objects.filter(u_id=id).last()
            user = SignModel.objects.get(u_id=id)
            can_user=user.username
            u_emailid=user.u_emailid
            html_content = render_to_string("appo_template.html",{'username':can_user,'appo':appo})
            text_content=strip_tags(html_content)
            email=EmailMultiAlternatives("CareForYou Appointment Booked Successfully !!",text_content,"settings.EMAIL_HOST_USER",[u_emailid])
            email.attach_alternative(html_content,"text/html")
            email.fail_silenty=False
            email.send()
            return redirect('myappoints')
        return render(request, 'appointpage.html', param)
    else:
        return render(request,"userlogin.html")

@my_login_required
def myappoints(request):
    if 'username' in request.session:
        current_user = request.session['username']
        id=request.session['u_id']
        showall=Appointment.objects.filter(u_id=id).all()
        param = {'current_user': current_user,'data':showall}
        return render(request, 'myappoints.html', param)
    else:
        return render(request,"userlogin.html")

@my_login_required
def delappoint(request,id):
    delappo=Appointment.objects.get(appo_id=id)
    user = SignModel.objects.get(u_id=delappo.u_id)
    can_date=delappo.appo_date
    can_time=delappo.appo_time
    can_user=user.username
    u_emailid=user.u_emailid
    html_content = render_to_string("cancel_template.html",{'username':can_user,'date':can_date,'time':can_time})
    text_content=strip_tags(html_content)
    email=EmailMultiAlternatives("CareForYou Appointment Cancelled !!",text_content,"settings.EMAIL_HOST_USER",[u_emailid])
    email.attach_alternative(html_content,"text/html")
    email.fail_silenty=False
    email.send()
    delappo.delete()
    return redirect('myappoints')

@my_login_required
def editappoint(request,id):
    if 'username' in request.session:
        current_user = request.session['username']
        appo = Appointment.objects.get(appo_id=id)
        doct = DoctorModel.objects.get(doc_id=appo.doc_id)
        if request.method == "POST":
            appo.appo_date = request.POST.get('appo_date')
            appo.appo_time = request.POST.get('appo_time')
            appo.save(update_fields=["appo_date","appo_time"])
            user = SignModel.objects.get(u_id=appo.u_id)
            can_user=user.username
            u_emailid=user.u_emailid
            html_content = render_to_string("reschedule_template.html",{'username':can_user,'appo':appo})
            text_content=strip_tags(html_content)
            email=EmailMultiAlternatives("CareForYou Appointment Rescheduled Successfully !!",text_content,"settings.EMAIL_HOST_USER",[u_emailid])
            email.attach_alternative(html_content,"text/html")
            email.fail_silenty=False
            email.send()
            return redirect('myappoints')
        context = {'appo':appo,'doct':doct,'current_user':current_user}
        return render(request, 'editappoint.html', context)
    else:
        return render(request,"userlogin.html")
