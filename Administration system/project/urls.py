from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^admin_login/','system.views.login_a'),
                       url(r'^admin_contro/','system.views.Contro'),
                       url(r'^admin_logout/','system.views.logout_a'),
                       url(r'^admin_home/','system.views.Adminhome',name="Adminhome"),
                       url(r'^admin_score/','system.views.ScoreA',name="ScoreA"),
                       url(r'^admin_score_change/$','system.views.ScoreChange',name="ScoreChange"),
                       url(r'^admin_course/','system.views.CourseA',name="CourseA"),
                       url(r'^admin_course_change/$','system.views.CourseChange',name="CourseChange"),
                       url(r'^login/$',  login),
                       url(r'^accounts/logout/$', logout),
                       url(r'^home/','system.views.Home',name="Home"),
                       url(r'^page/','system.views.Page',name="Page"),
                       url(r'^timetable/','system.views.Timetable',name="Timetable"),
                       url(r'^result/$','system.views.Result',name="Result"),
                       url(r'^compulsory/','system.views.Compulsory',name="Compulsory"),
                       url(r'^socialism/','system.views.Socialism',name="Socialism"),
                       url(r'^arbitrary/$','system.views.Arbitrary',name="Aarbitrary"),
                       url(r'^management/','system.views.Management',name="Introduction"),
                       url(r'^room1/','system.views.Room1',name="Room1"),
                       url(r'^score/','system.views.ScoreF',name="SocreF"),
                       url(r'^medias/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT },name="media"),
                       url(r'^changepassword/','system.views.Changepassword',name="Changepassword"),

    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
