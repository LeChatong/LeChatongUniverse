from django.conf.urls import url
from beakhub import views

urlpatterns = (
    url(r'^accounts/init/password$', views.init_password),
    url(r'^api/v1/accounts$', views.account_list),
    url(r'^api/v1/accounts/(?P<id>[0-9]+)$', views.account_details),
    url(r'^api/v1/accounts/login$', views.account_login),
    url(r'^api/v1/accounts/init$', views.send_mail_for_init_password),
    url(r'^api/v1/users$', views.user_list),
    url(r'^api/v1/users/(?P<id>[0-9]+)$', views.user_details),
    url(r'^api/v1/categories$', views.category_list),
    url(r'^api/v1/categories/(?P<id>[0-9]+)$', views.category_details),
    url(r'^api/v1/jobs$', views.job_list),
    url(r'^api/v1/jobs/(?P<id>[0-9]+)$', views.job_details),
    url(r'^api/v1/jobs/user/(?P<user_id>[0-9]+)$', views.jobs_by_user),
    url(r'^api/v1/jobs/search$', views.search_job),
    url(r'^api/v1/address$', views.address_list),
    url(r'^api/v1/address/(?P<id>[0-9]+)$', views.address_details),
    url(r'^api/v1/address/job/(?P<job_id>[0-9]+)$', views.address_by_job),
    url(r'^api/v1/comments$', views.comment_add),
    url(r'^api/v1/comments/(?P<id>[0-9]+)$', views.comment_id),
    url(r'^api/v1/comments/job/(?P<job_id>[0-9]+)$', views.comment_job_id),
    url(r'^api/v1/likes/jobs/all$', views.like_all),
    url(r'^api/v1/likes/jobs/details/(?P<like_id>[0-9]+)$', views.like_detail),
    url(r'^api/v1/likes/job/(?P<job_id>[0-9]+)/user/(?P<user_id>[0-9]+)$', views.like_job_user),
    url(r'^api/v1/likes/job/(?P<job_id>[0-9]+)$', views.likes_job),
    url(r'^api/v1/likes/user/(?P<user_id>[0-9]+)$', views.likes_user),
    url(r'^api/v1/events$', views.all_event),
    url(r'^api/v1/events/(?P<id>[0-9]+)$', views.event_by_id),
    url(r'^api/v1/events/user/(?P<user_id>[0-9]+)$', views.events_by_user),
    url(r'^api/v1/events/notsee/user/(?P<user_id>[0-9]+)$', views.events_not_see_by_user),
    url(r'^api/v1/events/view/(?P<id>[0-9]+)$', views.do_event_in_view)
)