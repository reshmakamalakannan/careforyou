"""careforyou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name="home"),
    path("about",views.about,name="about"),
    path("healthy_living",views.healthy_living,name="healthy_living"),

    path("adminlogin",views.adminlogin,name="adminlogin"),
    path("adminlogout",views.adminlogout,name="adminlogout"),
    path("adminhome",views.adminhome,name="adminhome"),
    path("adddoctor",views.adddoctor,name="adddoctor"),
    path("viewdoctor",views.viewdoctor,name="viewdoctor"),
    path("editdoct/<int:id>",views.editdoct,name="editdoct"),
    path("totalusers",views.totalusers,name="totalusers"),
    path("totalfeedback",views.totalfeedback,name="totalfeedback"),
    path("totalappoints",views.totalappoints,name="totalappoints"),

    path("stroketips",views.stroketips,name="stroketips"),
    path("visiontips",views.visiontips,name="visiontips"),
    path("menstrualtips",views.menstrualtips,name="menstrualtips"),
    path("hearttips",views.hearttips,name="hearttips"),
    path("seasontips",views.seasontips,name="seasontips"),
    path("lungtips",views.lungtips,name="lungtips"),
    path("agetips",views.agetips,name="agetips"),
    path("covidtips",views.covidtips,name="covidtips"),
    path("Diabetestips",views.Diabetestips,name="Diabetestips"),


    path("validate_email",views.validate_email,name="validate_email"),
    path("email_sent",views.email_sent,name="email_sent"),
    path("reset_password",views.reset_password,name="reset_password"),
    path("successreset",views.successreset,name="successreset"),
    path("onlyonce",views.onlyonce,name="onlyonce"),


    path("userlogin",views.userlogin,name="userlogin"),
    path('userlogout/', views.userlogout, name='userlogout'),
    path("userhome",views.userhome,name="userhome"),
    path("usersign",views.usersign,name="usersign"),
    path("editprofile",views.editprofile,name="editprofile"),
    path("feedback",views.feedback,name="feedback"),

    path("bookappoint",views.bookappoint,name="bookappoint"),
    path("appointpage/<int:id>",views.appointpage,name="appointpage"),
    path("myappoints",views.myappoints,name="myappoints"),
    path("delappoint/<int:id>",views.delappoint,name="delappoint"),
    path("editappoint/<int:id>",views.editappoint,name="editappoint"),
   
    path("dhistory",views.dhistory,name="dhistory"),
    path("delDHist/<int:id>",views.delDHist,name="delDHist"),
    path("lhistory",views.lhistory,name="lhistory"),
    path("delLHist/<int:id>",views.delLHist,name="delLHist"),
    path("hearthistory",views.hearthistory,name="hearthistory"),
    path("delHeartHist/<int:id>",views.delHeartHist,name="delHeartHist"),
    path("shistory",views.shistory,name="shistory"),
    path("delSHist/<int:id>",views.delSHist,name="delSHist"),

    path("strokepredict/",views.strokepredict,name="strokepredict"),
    path("strokepredict/strokeresult",views.strokeresult),
    path("diabetespredict/",views.diabetespredict,name="diabetespredict"),
    path("diabetespredict/diabetesresult",views.diabetesresult),
    path("heartpredict/",views.heartpredict,name="heartpredict"),
    path("heartpredict/heartresult",views.heartresult),
    path("lungcancer/",views.lungcancer,name="lungcancer"),
    path("lungcancer/lungresult",views.lungresult),
]
