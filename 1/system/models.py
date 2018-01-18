# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Controler(models.Model):
    CourseContro = models.BooleanField(blank=True) #选课开关
    
class Users(models.Model):
    username = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=100,blank=True)
    def __unicode__(self):
        return self.username
class Room(models.Model):
    Semester = models.CharField(max_length=100,blank=True)#2015年秋季学期
    Week = models.CharField(max_length=100,blank=True)#第几周
    Date = models.CharField(max_length=100,blank=True)#星期几
    District = models.CharField(max_length=100,blank=True)#校区
    Num = models.CharField(max_length=100,blank=True)#楼宇
    ClassID = models.CharField(max_length=100,blank=True)#教室编号
    T12 = models.BooleanField(blank=True)#12节课是否被占用
    T34 = models.BooleanField(blank=True)
    T56 = models.BooleanField(blank=True)
    T78 = models.BooleanField(blank=True)
    T910 = models.BooleanField(blank=True)#9,10节课是否被占用 
    def __unicode__(self):
        return self.ClassID
class Information(models.Model):
    Name = models.CharField(max_length=100,blank=True)
    StudentID = models.CharField(max_length=100,blank=True)
    Faculty = models.CharField(max_length=100,blank=True)
    Grade = models.CharField(max_length=100,blank=True)
    Nation = models.CharField(max_length=100,blank=True)#民族
    BirthDate = models.CharField(max_length=100,blank=True)
    EntranceDate = models.CharField(max_length=100,blank=True)
    StatusID = models.CharField(max_length=100,blank=True)
    Province = models.CharField(max_length=100,blank=True)
    Sex = models.CharField(max_length=100,blank=True)
    Institute = models.CharField(max_length=100,blank=True)
    Major = models.CharField(max_length=100,blank=True)
    ClassID = models.CharField(max_length=100,blank=True)
    Origin = models.CharField(max_length=100,blank=True)#籍贯
    PoliticStatus = models.CharField(max_length=100,blank=True)#政治面貌
    Phone = models.CharField(max_length=100,blank=True)
    Nationality = models.CharField(max_length=100,blank=True)#国家
    GraduatedHighSchool = models.CharField(max_length=100,blank=True)
    def __unicode__(self):
        return self.Name
class Course(models.Model):
    CourseFlag = models.CharField(max_length=20,blank=True)#必修1，全校任选2，人文社科3
    CourseTime = models.CharField(max_length=100,blank=True)#学年学期
    CourseID = models.CharField(max_length=100,blank=True)#课程编码
    CourseName = models.CharField(max_length=100,blank=True)
    PreCourse = models.CharField(max_length=200,blank=True)#前置课程
    Facing = models.CharField(max_length=100,blank=True)#面向对象
    District = models.CharField(max_length=100,blank=True)#开课校区
    Intro = models.CharField(max_length=200,blank=True)#课程介绍
    CourseAttr = models.CharField(max_length=100,blank=True)#课程属性，必修等
    CourseFacul = models.CharField(max_length=100,blank=True)#开课院系
    CourseScore = models.CharField(max_length=20,blank=True)#课程学分
    AlreadySele = models.IntegerField(max_length=100,blank=True)#已选数量
    Capasity = models.IntegerField(max_length=100,blank=True)#课程容量
    Week = models.CharField(max_length=100,blank=True)#课表显示，星期几
    TXX = models.CharField(max_length=100,blank=True)#课表显示，第几节课
    Num = models.CharField(max_length=100,blank=True)#楼宇
    ClassID = models.CharField(max_length=100,blank=True)#教室编号    
    TimeRange = models.CharField(max_length=100,blank=True)#课程持续的周次，例如[1~17]周
    CourseFlagCon = models.BooleanField(blank=True)
    def __unicode__(self):
        return self.CourseName
class Student(models.Model):
    StudentID = models.CharField(max_length=100,blank=True)
    SelectedCourse = models.ManyToManyField(Course,blank=True)
    BasicInformation = models.OneToOneField(Information,blank=True)
    ArNum = models.IntegerField(max_length=100,blank=True)
    ArFlag = models.BooleanField(blank=True)
    SoNum = models.IntegerField(max_length=100,blank=True)
    SoFlag = models.BooleanField(blank=True)
    def __unicode__(self):
       return self.BasicInformation.Name
class Score(models.Model) :
    Semester = models.CharField(max_length=100) #学年学期
    Re = models.CharField(blank=True,max_length=100) #重修补考
    Pass = models.BooleanField(blank=True)#是否通过
    SelectedCourse = models.ForeignKey(Course,blank=True)#已选课程
    Score = models.IntegerField(blank=True,max_length=100)
    StudentS = models.ForeignKey(Student,blank=True)
    def __unicode__(self):
        return self.SelectedCourse.CourseName
    
admin.site.register(Information)
admin.site.register(Room)
admin.site.register(Course)
admin.site.register(Score)
admin.site.register(Student)
admin.site.register(User)
admin.site.register(Users)
admin.site.register(Controler)