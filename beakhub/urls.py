from django.conf.urls import url
from beakhub import views

urlpatterns = (
    url(r'^accounts$', views.account_list),
    url(r'^accounts/(?P<id>[0-9]+)$', views.account_details),
    url(r'^accounts/login$', views.account_login),
    url(r'^users$', views.user_list),
    url(r'^users/(?P<id>[0-9]+)$', views.user_details),
    url(r'^categories$', views.category_list),
    url(r'^categories/(?P<id>[0-9]+)$', views.category_details),
    url(r'^jobs$', views.job_list),
    url(r'^jobs/(?P<id>[0-9]+)$', views.job_details),
    url(r'^jobs/user/(?P<user_id>[0-9]+)$', views.jobs_by_user),
    url(r'^jobs/search$', views.search_job),
    url(r'^address$', views.address_list),
    url(r'^address/(?P<id>[0-9]+)$', views.address_details),
    url(r'^address/job/(?P<job_id>[0-9]+)$', views.address_by_job),
    url(r'^comments$', views.comment_add),
    url(r'^comments/(?P<id>[0-9]+)$', views.comment_id),
    url(r'^comments/job/(?P<job_id>[0-9]+)$', views.comment_job_id),
    url(r'^likes/jobs/all$', views.like_all),
    url(r'^likes/jobs/details/(?P<like_id>[0-9]+)$', views.like_detail),
    url(r'^likes/job/(?P<job_id>[0-9]+)/user/(?P<user_id>[0-9]+)$', views.like_job_user),
    url(r'^likes/job/(?P<job_id>[0-9]+)$', views.likes_job),
    url(r'^likes/user/(?P<user_id>[0-9]+)$', views.likes_user),
    url(r'^events/all$', views.all_event),
    url(r'^events/user/(?P<user_id>[0-9]+)$', views.events_by_user),
    url(r'^events/view/(?P<id>[0-9]+)$', views.do_event_in_view)
)