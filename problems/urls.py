from django.urls import path
from . import views
from .views import (
    ProblemListView,
    ProblemDetailView,
    ProblemCreateView,
    ProblemUpdateView,
    ProblemDeleteView,
    markdown_preview,
)

app_name = 'problems'

urlpatterns = [
    path('', ProblemListView.as_view(), name='list'),
    path('create/', ProblemCreateView.as_view(), name='create'),
    path('<int:pk>/', ProblemDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ProblemUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ProblemDeleteView.as_view(), name='delete'),

    # 追加: Markdown プレビュー API
    path('preview/', markdown_preview, name='markdown_preview'),
    path('problems/<int:problem_id>/answer/', views.submit_answer, name='submit_answer'),
    path('answers/<int:answer_id>/react/<str:reaction_type>/', views.toggle_reaction, name='toggle_reaction'),
    path('answers/<int:answer_id>/comment/', views.post_comment, name='post_comment'),
]
