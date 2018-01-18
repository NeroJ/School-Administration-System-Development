# -*- coding: utf-8 -*-
import xlwt
from django.http import HttpResponseRedirect
from django.http import HttpResponse 
from django.shortcuts import render_to_response,RequestContext
from django import forms
from django.contrib import auth
from models import Student,Course,Room,Score,Users,Controler
from system.forms import ChangepwdForm,CourseForm
###########################################login admin###############################################
class UserForm(forms.Form):
    username = forms.CharField(label='用户名：',max_length=100)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())

def login_a(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = Users.objects.filter(username__exact = username,password__exact = password)
            if user:
                return render_to_response('Adminhome.html')
            else:
                return HttpResponseRedirect('/admin_login/')
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf})
    
def logout_a(request):
    return render_to_response('logged_out.html')
####################################################################################################

def Home(request):            
    return render_to_response('home.html')
 
def Contro(request):
    ct= Controler.objects.all()
    ctr = ct[0].CourseContro#选课开关控制项
    f = ctr
    if request.POST:
        if f:
            f = False
            temp = Controler.objects.get(CourseContro = True)
            temp.CourseContro = False
            temp.save()
            return render_to_response('Contro.html',{'f': f})
        else:
            f = True
            temp = Controler.objects.get(CourseContro = False)
            temp.CourseContro = True
            temp.save()
            return render_to_response('Contro.html',{'f': f})            
    return render_to_response('Contro.html',{'f': f})
 
def ScoreF(request):
    p=Student.objects.filter(StudentID=request.user)
    pp = Student.objects.get(StudentID=request.user)
    ScoO = Score.objects.filter(StudentS = pp)
    result_score = ['待定','待定']
    if ScoO:
        for elem in ScoO:
            if elem.Score >= 60:
                elem.Pass = True
                elem.Re = '正考'
                elem.save()
            elif elem.Score > 0 and elem.Score < 60:
                elem.Pass = False
                elem.Re = '补考'
                elem.save()
            else:
                elem.Pass = False
                elem.Re = '待修改'
                elem.save()                
###################################GPA学分绩######################################################
        fff = 0
        temp_s = 0
        temp_m = 0
        GPA_s = 0
        GPA_m = 0
        for i in ScoO:
            GPA_s = GPA_s + float(i.SelectedCourse.CourseScore) * float(i.Score)
            GPA_m = GPA_m + float(i.SelectedCourse.CourseScore)
            if i.SelectedCourse.CourseAttr.encode('utf-8') == '必修':
                temp_s = temp_s + float(i.SelectedCourse.CourseScore) * float(i.Score)
                temp_m = temp_m + float(i.SelectedCourse.CourseScore)
                fff = fff + 1
        if fff == 0:
            temp_m = 1
        result_score[0] = '%.1f'% (temp_s / temp_m)
        result_score[1] = '%.1f'% (((GPA_s/GPA_m)/100)*4.5)
#################################################################################################
    if request.POST:
        obj = request.POST
        if obj['Pass'] =='*':
            ScoO = Score.objects.filter(StudentS = pp,Re = obj['CXBK'] )
            return render_to_response('score.html',{'p': p,'ScoO':ScoO,'r':result_score[0],'GPA':result_score[1]})
        elif obj['CXBK'] =='':
            ScoO = Score.objects.filter(StudentS = pp, Pass = obj['Pass'] )
            return render_to_response('score.html',{'p': p,'ScoO':ScoO,'r':result_score[0],'GPA':result_score[1]})
        else:
            ScoO = Score.objects.filter(StudentS = pp, Pass = obj['Pass'],Re = obj['CXBK'] )
            return render_to_response('score.html',{'p': p,'ScoO':ScoO,'r':result_score[0],'GPA':result_score[1]})
    else:
        return render_to_response('score.html',{'p': p,'ScoO':ScoO,'r':result_score[0],'GPA':result_score[1]})
    
def Room1(request):
    p=Student.objects.filter(StudentID=request.user)
    c = Course.objects.all()
    for item in c:
        temp = item.TimeRange.split('~')
        i = int(temp[0])
        j = int(temp[1])
        for counter in range(i,j+1):
            if item.TXX.encode('utf-8') == '第1,2节':
                form = Room( Semester = '2015秋季学期',
                             Week = '第'+ str(counter) +'周',
                             Date = item.Week,
                             District = item.District,
                             Num = item.Num,
                             ClassID = item.ClassID,
                             T12 = True,
                           )
                if not Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                           Date = item.Week, District = item.District, Num = item.Num,\
                                           ClassID = item.ClassID, T12 = True):
                                               if  Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                           Date = item.Week, District = item.District, Num = item.Num,\
                                                                           ClassID = item.ClassID, T12 = False):
                                                                              dd = Room.objects.get(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                                                   Date = item.Week, District = item.District, Num = item.Num,\
                                                                                                   ClassID = item.ClassID, T12 = False)
                                                                              dd.T12 = True
                                                                              dd.save()
                                                                               
                                               else:                                                   
                                                    form.save()
            if item.TXX.encode('utf-8') == '第3,4节':
                form = Room( Semester = '2015秋季学期',
                             Week = '第'+ str(counter) +'周',
                             Date = item.Week,
                             District = item.District,
                             Num = item.Num,
                             ClassID = item.ClassID,
                             T34 = True,
                           )
                if not Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                           Date = item.Week, District = item.District, Num = item.Num,\
                                           ClassID = item.ClassID, T34 = True):
                                                if  Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                           Date = item.Week, District = item.District, Num = item.Num,\
                                                                           ClassID = item.ClassID, T34 = False):
                                                                              dd = Room.objects.get(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                                                   Date = item.Week, District = item.District, Num = item.Num,\
                                                                                                   ClassID = item.ClassID, T34 = False)
                                                                              dd.T34 = True
                                                                              dd.save()
                                                                               
                                                else:                                                   
                                                     form.save()
            if item.TXX.encode('utf-8') == '第5,6节':
                form = Room( Semester = '2015秋季学期',
                             Week = '第'+ str(counter) +'周',
                             Date = item.Week,
                             District = item.District,
                             Num = item.Num,
                             ClassID = item.ClassID,
                             T56 = True,
                           )
                if not Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                           Date = item.Week, District = item.District, Num = item.Num,\
                                           ClassID = item.ClassID, T56 = True):
                                               if  Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                           Date = item.Week, District = item.District, Num = item.Num,\
                                                                           ClassID = item.ClassID, T56 = False):
                                                                              dd = Room.objects.get(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                                                   Date = item.Week, District = item.District, Num = item.Num,\
                                                                                                   ClassID = item.ClassID, T56 = False)
                                                                              dd.T56 = True
                                                                              dd.save()
                                                                               
                                               else:                                                   
                                                     form.save() 
            if item.TXX.encode('utf-8') == '第7,8节':
                form = Room( Semester = '2015秋季学期',
                             Week = '第'+ str(counter) +'周',
                             Date = item.Week,
                             District = item.District,
                             Num = item.Num,
                             ClassID = item.ClassID,
                             T78 = True,
                           )
                if not Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                           Date = item.Week, District = item.District, Num = item.Num,\
                                           ClassID = item.ClassID, T78 = True):
                                               if  Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                           Date = item.Week, District = item.District, Num = item.Num,\
                                                                           ClassID = item.ClassID, T78 = False):
                                                                              dd = Room.objects.get(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                                                   Date = item.Week, District = item.District, Num = item.Num,\
                                                                                                   ClassID = item.ClassID, T78 = False)
                                                                              dd.T78 = True
                                                                              dd.save()
                                                                               
                                               else:                                                   
                                                     form.save() 
            if item.TXX.encode('utf-8') == '第9,10节':
                form = Room( Semester = '2015秋季学期',
                             Week = '第'+ str(counter) +'周',
                             Date = item.Week,
                             District = item.District,
                             Num = item.Num,
                             ClassID = item.ClassID,
                             T910 = True,
                           )
                if not Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                           Date = item.Week, District = item.District, Num = item.Num,\
                                           ClassID = item.ClassID, T910 = True):
                                               if  Room.objects.filter(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                           Date = item.Week, District = item.District, Num = item.Num,\
                                                                           ClassID = item.ClassID, T910 = False):
                                                                              dd = Room.objects.get(Semester = '2015秋季学期',Week = '第'+ str(counter) +'周',\
                                                                                                   Date = item.Week, District = item.District, Num = item.Num,\
                                                                                                   ClassID = item.ClassID, T910 = False)
                                                                              dd.T910 = True
                                                                              dd.save()
                                                                               
                                               else:                                                   
                                                     form.save()                                               
    ob = Room.objects.all()
    if request.POST:
        obj=request.POST
        ob = ob.filter(Semester=obj['Semester'],Week=obj['ZhouCi'],\
                       Date=obj['XingQi'],District=obj['District'],Num=obj['LouYu'])
        return render_to_response('room1.html',{'p': p,'ob': ob,'S':obj['Semester'],\
                                  'ZC':obj['ZhouCi'],\
                                  'DA':obj['XingQi'],'Dis':obj['District'],\
                                  'LY':obj['LouYu']})
    else:
        return render_to_response('room1.html',{'p': p})

def Management(request):
    p=Student.objects.filter(StudentID=request.user)
    return render_to_response('management.html',{'p': p})

def Arbitrary(request):
    i = 0
    ct= Controler.objects.all()
    ctr = ct[0].CourseContro#选课开关控制项
    Ar=Course.objects.filter(CourseFlag='2')
    p=Student.objects.filter(StudentID=request.user)
    StudentU = Student.objects.get(StudentID=request.user)
    f = StudentU.ArFlag
    Ar_list = []
    for ele in Ar:
        if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
            Ar_list.append(ele)
    if request.GET:
       SOid = request.GET.get('SOid')
       SeleOb = Course.objects.get(id = SOid )
       StudentU.SelectedCourse.add(SeleOb)
       form= Score( Semester = SeleOb.CourseTime,
                    Re = '待修改',
                    StudentS = StudentU,
                    SelectedCourse = SeleOb,
                    Score = 0, 
                  )
       form.save()
################################选择数目限制############################################
       if StudentU.ArNum >= 2:
           StudentU.ArFlag = False
           StudentU.save()
       elif StudentU.ArNum >= 0 and StudentU.ArNum < 2:
           StudentU.ArFlag = True
           t = StudentU.ArNum
           t = t + 1
           if t >= 2:
               StudentU.ArNum = t
               StudentU.ArFlag = False
               f = False
           StudentU.ArNum = t
           StudentU.save()
############################################################################
       temp = SeleOb.AlreadySele
       temp = temp + 1
       SeleOb.AlreadySele = temp
       SeleOb.save()
       Ar_list = []
       for ele in Ar:
           if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
               Ar_list.append(ele)
    if request.POST:
       ob=request.POST
       if ob['Search'] != '':
           Ar = Ar.filter(CourseFlag='2',CourseName = ob['Search'])
           Ar_list = []
           for ele in Ar:
               if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
                   Ar_list.append(ele)
           return render_to_response('arbitrary.html',{'p': p,'Ar': Ar_list,'i': i,'ctr':ctr,'f':f})
       else:
           if ob['Institute'] == '':
               Ar = Ar.filter(CourseFlag='2',District = ob['District'])
               Ar_list = []
               for ele in Ar:
                   if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
                       Ar_list.append(ele)
               return render_to_response('arbitrary.html',{'p': p,'Ar': Ar_list,'i': i,'ctr':ctr,'f':f})
           elif ob['District'] == '':
               Ar = Ar.filter(CourseFlag='2',CourseFacul = ob['Institute'])
               Ar_list = []
               for ele in Ar:
                   if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
                       Ar_list.append(ele)
               return render_to_response('arbitrary.html',{'p': p,'Ar': Ar_list,'i': i,'ctr':ctr,'f':f})
           else:
               Ar = Ar.filter(CourseFlag='2',District = ob['District'],\
                              CourseFacul = ob['Institute'])
               Ar_list = []
               for ele in Ar:
                   if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
                       Ar_list.append(ele)
               return render_to_response('arbitrary.html',{'p': p,'Ar': Ar_list,'i': i,'ctr':ctr,'f':f})
    else:
       return render_to_response('arbitrary.html',{'p': p,'Ar': Ar_list,'i': i,'ctr':ctr,'f':f})

def Socialism(request):
    i = 0
    ct= Controler.objects.all()
    ctr = ct[0].CourseContro#选课开关控制项
    So=Course.objects.filter(CourseFlag='3')
    p=Student.objects.filter(StudentID=request.user)
    StudentU = Student.objects.get(StudentID=request.user)
    f = StudentU.SoFlag
    So_list = [] #实现选一个少一个的功能
    for ele in So:
        if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
            So_list.append(ele)
    if request.GET:
       SOid = request.GET.get('SOid')
       SeleOb = Course.objects.get(id = SOid )
       StudentU.SelectedCourse.add(SeleOb)
       form= Score( Semester = SeleOb.CourseTime,
                    Re = '待修改',
                    StudentS = StudentU,
                    SelectedCourse = SeleOb,
                    Score = 0, 
                  )
       form.save()
################################选择数目限制#############################################
       if StudentU.SoNum >= 1:
           StudentU.SoFlag = False
           StudentU.save()
       elif StudentU.SoNum >= 0 and StudentU.SoNum < 1:
           StudentU.SoFlag = True
           t = StudentU.SoNum
           t = t + 1
           if t >= 1:
               StudentU.SoNum = t
               StudentU.SoFlag = False
               f = False
           StudentU.SoNum = t
           StudentU.save()
#############################################################################
       temp = SeleOb.AlreadySele #实现已选课程数量自增
       temp = temp + 1
       SeleOb.AlreadySele = temp
       SeleOb.save()
       So_list = []
       for ele in So:
           if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
               So_list.append(ele)
    if request.POST:
       ob=request.POST
       if ob['Search'] != '':
           So = So.filter(CourseFlag='3',CourseName = ob['Search'])
           So_list = [] #在索引中实现已选课程不显示的功能
           for ele in So:
               if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
                   So_list.append(ele)
           return render_to_response('socialism.html',{'p': p,'So': So_list,'i': i,'ctr':ctr,'f':f})
       else:
           if ob['Institute'] == '':
               So = So.filter(CourseFlag='3',District = ob['District'])
               So_list = []
               for ele in So:
                   if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
                       So_list.append(ele)
               return render_to_response('socialism.html',{'p': p,'So': So_list,'i': i,'ctr':ctr,'f':f})
           elif ob['District'] == '':
               So = So.filter(CourseFlag='3',CourseFacul = ob['Institute'])
               So_list = []
               for ele in So:
                   if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
                       So_list.append(ele)
               return render_to_response('socialism.html',{'p': p,'So': So_list,'i': i,'ctr':ctr,'f':f})
           else:
               So = So.filter(CourseFlag='3',District = ob['District'],\
                             CourseFacul = ob['Institute'])
               So_list = []
               for ele in So:
                   if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
                       So_list.append(ele)
               return render_to_response('socialism.html',{'p': p,'So': So_list,'i': i,'ctr':ctr,'f':f})
    else:
       return render_to_response('socialism.html',{'p': p,'So': So_list,'i': i,'ctr':ctr,'f':f})

def Compulsory(request):
    i = 0
    ct= Controler.objects.all()
    ctr = ct[0].CourseContro#选课开关控制项
    p=Student.objects.filter(StudentID=request.user) #得到的对象列表
    StudentU = Student.objects.get(StudentID=request.user) #得到的对象
    Co=Course.objects.filter(CourseFlag='1',\
                             CourseFacul=StudentU.BasicInformation.Institute,\
                             Facing=StudentU.BasicInformation.Grade)
    Co_list = []
    for ele in Co:
        if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
            Co_list.append(ele)
    if request.GET:
        Coid = request.GET.get('Coid')
        SCoid = Course.objects.get(id = Coid ) #得到被选课的对象
        StudentU.SelectedCourse.add(SCoid)
        form= Score( Semester = SCoid.CourseTime,
                    Re = '待修改',
                    StudentS = StudentU,
                    SelectedCourse = SCoid,
                    Score = 0, 
                  )
        form.save()
        temp = SCoid.AlreadySele
        temp = temp + 1
        SCoid.AlreadySele = temp
        SCoid.save()
        Co_list = []
        for ele in Co:
            if not Student.objects.filter(StudentID=request.user,SelectedCourse = ele):
                Co_list.append(ele)
    return render_to_response('compulsory.html',{'p': p,'Co': Co_list,'i': i,'ctr':ctr,\
                                                 'Grade':StudentU.BasicInformation.Institute,\
                                                 'Institute':StudentU.BasicInformation.Institute,\
                                                 'Major':StudentU.BasicInformation.Major})

def Result(request):
    ct= Controler.objects.all()
    ctr = ct[0].CourseContro#选课开关控制项
    p=Student.objects.filter(StudentID=request.user)
    pp = Student.objects.get(StudentID=request.user)
    Arp = pp.SelectedCourse.filter(CourseFlag = '2') 
    Sop = pp.SelectedCourse.filter(CourseFlag = '3')
    Cop = pp.SelectedCourse.filter(CourseFlag = '1')
    if request.GET:
       WDid = request.GET.get('WDid')
       WdOb = Course.objects.get(id = WDid )
###############################选择数目限制##############################################
       if WdOb.CourseFlag == '2':
           t = pp.ArNum
           t = t - 1
           if t >= 0 and t < 2:
               pp.ArNum = t
               pp.ArFlag = True
           pp.save()
       if WdOb.CourseFlag == '3':
           t_s = pp.SoNum
           t_s = t_s - 1
           if t_s >= 0 and t_s < 1:
               pp.SoNum = t_s
               pp.SoFlag = True
           pp.save() 
###############################################################################
       temp = WdOb.AlreadySele
       temp = temp - 1
       WdOb.AlreadySele = temp
       WdOb.save()
       ScoO = Score.objects.get(StudentS = pp,SelectedCourse = WdOb)
       pp.SelectedCourse.remove(WdOb)
       ScoO.delete()
    return render_to_response('result.html',{'p': p,'Arp':Arp,'Sop':Sop,'Cop':Cop,'ctr':ctr})

def Page(request):
    SOid = request.GET.get('courseid')
    SeleOb = Course.objects.get(id = SOid)
    return render_to_response('page.html',{'p': SeleOb})

def Timetable(request):
    p=Student.objects.get(StudentID=request.user)
    C_list = p.SelectedCourse.filter()
    timetable = [['','星期一','星期二','星期三','星期四','星期五','星期六','星期日'],\
                 ['第1,2节','','','','','','',''],\
                 ['第3,4节','','','','','','',''],\
                 ['第5,6节','','','','','','',''],\
                 ['第7,8节','','','','','','',''],\
                 ['第9,10节','','','','','','',''],\
                 ['第11,12节','','','','','','','']]
    for course in C_list:
        if course.Week.encode('utf-8') == '星期一' and course.TXX.encode('utf-8') == '第1,2节':
            timetable[1][1] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期二' and course.TXX.encode('utf-8') == '第1,2节':
            timetable[1][2] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期三' and course.TXX.encode('utf-8') == '第1,2节':
            timetable[1][3] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期四' and course.TXX.encode('utf-8') == '第1,2节':
            timetable[1][4] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期五' and course.TXX.encode('utf-8') == '第1,2节':
            timetable[1][5] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期六' and course.TXX.encode('utf-8') == '第1,2节':
            timetable[1][6] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期日' and course.TXX.encode('utf-8') == '第1,2节':
            timetable[1][7] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8') 
#############################################################################################
        if course.Week.encode('utf-8') == '星期一' and course.TXX.encode('utf-8') == '第3,4节':
            timetable[2][1] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8') 
        if course.Week.encode('utf-8') == '星期二' and course.TXX.encode('utf-8') == '第3,4节':
            timetable[2][2] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期三' and course.TXX.encode('utf-8') == '第3,4节':
            timetable[2][3] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期四' and course.TXX.encode('utf-8') == '第3,4节':
            timetable[2][4] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期五' and course.TXX.encode('utf-8') == '第3,4节':
            timetable[2][5] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期六' and course.TXX.encode('utf-8') == '第3,4节':
            timetable[2][6] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期日' and course.TXX.encode('utf-8') == '第3,4节':
            timetable[2][7] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
#############################################################################################
        if course.Week.encode('utf-8') == '星期一' and course.TXX.encode('utf-8') == '第5,6节':
            timetable[3][1] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8') 
        if course.Week.encode('utf-8') == '星期二' and course.TXX.encode('utf-8') == '第5,6节':
            timetable[3][2] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8') 
        if course.Week.encode('utf-8') == '星期三' and course.TXX.encode('utf-8') == '第5,6节':
            timetable[3][3] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8') 
        if course.Week.encode('utf-8') == '星期四' and course.TXX.encode('utf-8') == '第5,6节':
            timetable[3][4] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期五' and course.TXX.encode('utf-8') == '第5,6节':
            timetable[3][5] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期六' and course.TXX.encode('utf-8') == '第5,6节':
            timetable[3][6] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8') 
        if course.Week.encode('utf-8') == '星期日' and course.TXX.encode('utf-8') == '第5,6节':
            timetable[3][7] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
#############################################################################################                        
        if course.Week.encode('utf-8') == '星期一' and course.TXX.encode('utf-8') == '第7,8节':
            timetable[4][1] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期二' and course.TXX.encode('utf-8') == '第7,8节':
            timetable[4][2] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期三' and course.TXX.encode('utf-8') == '第7,8节':
            timetable[4][3] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期四' and course.TXX.encode('utf-8') == '第7,8节':
            timetable[4][4] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期五' and course.TXX.encode('utf-8') == '第7,8节':
            timetable[4][5] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期六' and course.TXX.encode('utf-8') == '第7,8节':
            timetable[4][6] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期日' and course.TXX.encode('utf-8') == '第7,8节':
            timetable[4][7] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
#############################################################################################                              
        if course.Week.encode('utf-8') == '星期一' and course.TXX.encode('utf-8') == '第9,10节':
            timetable[5][1] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期二' and course.TXX.encode('utf-8') == '第9,10节':
            timetable[5][2] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期三' and course.TXX.encode('utf-8') == '第9,10节':
            timetable[5][3] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期四' and course.TXX.encode('utf-8') == '第9,10节':
            timetable[5][4] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期五' and course.TXX.encode('utf-8') == '第9,10节':
            timetable[5][5] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期六' and course.TXX.encode('utf-8') == '第9,10节':
            timetable[5][6] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期日' and course.TXX.encode('utf-8') == '第9,10节':
            timetable[5][7] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
#############################################################################################                              
        if course.Week.encode('utf-8') == '星期一' and course.TXX.encode('utf-8') == '第11,12节':
            timetable[6][1] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期二' and course.TXX.encode('utf-8') == '第11,12节':
            timetable[6][2] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期三' and course.TXX.encode('utf-8') == '第11,12节':
            timetable[6][3] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期四' and course.TXX.encode('utf-8') == '第11,12节':
            timetable[6][4] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')
        if course.Week.encode('utf-8') == '星期五' and course.TXX.encode('utf-8') == '第11,12节':
            timetable[6][5] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')    
        if course.Week.encode('utf-8') == '星期六' and course.TXX.encode('utf-8') == '第11,12节':
            timetable[6][6] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')    
        if course.Week.encode('utf-8') == '星期日' and course.TXX.encode('utf-8') == '第11,12节':
            timetable[6][7] = (course.CourseName +'('+course.CourseID +')'+'\r\n'\
                               +'[' + course.Num + course.ClassID + ']'+'\r\n'\
                               + '[' + course.TimeRange + ']'+ u'周').encode('utf-8')            
    if request.POST:                         
        filename = xlwt.Workbook ()
        sheet = filename.add_sheet('table')
        for iii in range(0,7):
            for jjj in range(0,8):
                sheet.write(iii,jjj,timetable[iii][jjj].decode('utf-8'),style=xlwt.Style.default_style)
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=Schedula.xls'
        filename.save(response)  
        return response                     
    return render_to_response('timetable.html',{'p': p,'c': C_list})

def Changepassword(request):
    p=Student.objects.filter(StudentID=request.user)    
    if request.method == 'GET':
        form = ChangepwdForm()
        return render_to_response('changepassword.html', RequestContext(request,\
                                                                        {'form': form, 'p': p,}))
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return render_to_response('successful.html', RequestContext(request,{'p': p}))
            else:
                return render_to_response('changepassword.html', RequestContext(request, {'form': form, 'p': p, 'oldpassword_is_wrong':True}))
        else:
            return render_to_response('changepassword.html', RequestContext(request, {'form': form, 'p': p, }))

###############################################################Admin#####################################################################
def Adminhome(request):
    return render_to_response('Adminhome.html')

def ScoreA(request):
    error1 = False
    if 'SearchCourse' in request.POST:
        SearchCourse = request.POST['SearchCourse']
        if not SearchCourse:
            error1 = True
        else:
            ScoreCourse = Score.objects.filter(SelectedCourse__CourseName = SearchCourse)
            return render_to_response('ScoreA.html',
                            {'ScoreCourse': ScoreCourse, 'error1': error1})           
    if 'SearchStudent' in request.POST:
        SearchStudent = request.POST['SearchStudent']
        if not SearchStudent:
            error1 = True
        else:
            ScoreStudent = Score.objects.filter(StudentS__StudentID = SearchStudent)
            return render_to_response('ScoreA.html',
                            {'ScoreStudent': ScoreStudent, 'error1': error1})
                            

    return render_to_response('ScoreA.html',
               {'error1': error1})

def ScoreChange(request):
    if 'q' in request.GET:
        q = request.GET['q']
        temp = Score.objects.get(id=q)
        if 'score' in request.POST:
            sco = request.POST.get('score')
            if sco=='':
                render_to_response('ScoreChange.html',
                    {'o': temp})
            else:
                temp.Score = sco
                temp.save()
                return HttpResponseRedirect('/admin_score/')
    return render_to_response('ScoreChange.html',
                    {'o': temp})
def CourseA(request):
    error1 = False
    if 'f' in request.POST:
        f = request.POST['f']
        if not f:
            error1 = True
        else:
            CourseF = Course.objects.filter(CourseFacul = f)
            return render_to_response('CourseA.html',
                            {'CourseF': CourseF, 'error1': error1})        
    
    if 'id' in request.POST:
        id = request.POST['id']
        if not id:
            error1 = True
        else:
            CourseI = Course.objects.filter(CourseID = id)
            return render_to_response('CourseA.html',
                            {'CourseI': CourseI, 'error1': error1})
                            

    return render_to_response('CourseA.html',
               {'error1': error1})

def CourseChange(request):
    if 'q' in request.GET:
        q = request.GET['q']
        temp = Course.objects.get(id=q)
        if request.POST:
            book = CourseForm(request.POST, instance = temp)
            if book.is_valid():
                book.save()
                return HttpResponseRedirect('/admin_course/')
            else:
                book = CourseForm(instance = temp)
                return render_to_response('CourseChange.html',
                        {'o': book})
    book = CourseForm(instance = temp)
    return render_to_response('CourseChange.html',
                    {'o': book})


