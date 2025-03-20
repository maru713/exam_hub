from django.urls import path
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
]
