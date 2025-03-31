from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Problem, Answer, AnswerReaction, Grade, Subject, Topic
from .forms import ProblemForm, AnswerCommentForm  # カスタムフォームを作る場合
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import markdown
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm
from django.db.models import Count, Q

class ProblemListView(ListView):
    model = Problem
    template_name = 'problems/problem_list.html'
    context_object_name = 'problems'
    paginate_by = 20

    def get_queryset(self):
        queryset = Problem.objects.select_related('author')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(answer__icontains=query)
            )
        # 🔽 フィルタ追加
        grade = self.request.GET.get('grade')
        subject = self.request.GET.get('subject')
        topic = self.request.GET.get('topic')

        if grade:
            queryset = queryset.filter(grade_id=grade)
        if subject:
            queryset = queryset.filter(subject_id=subject)
        if topic:
            queryset = queryset.filter(topic_id=topic)

        # 🔽 ソート追加
        sort = self.request.GET.get('sort')
        if sort == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'difficulty_high':
            queryset = queryset.order_by('-difficulty')
        elif sort == 'difficulty_low':
            queryset = queryset.order_by('difficulty')
        elif sort == 'most_answers':
            queryset = queryset.annotate(answer_count=Count('answers')).order_by('-answer_count')
        elif sort == 'most_good':
            queryset = queryset.annotate(
                good_count=Count('answers__reactions', filter=Q(answers__reactions__is_good=True))
            ).order_by('-good_count')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = Grade.objects.all()
        context['subjects'] = Subject.objects.all()
        context['topics'] = Topic.objects.all()
        return context

class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'problems/problem_detail.html'
    context_object_name = 'problem'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'answers__purposes', 'answers__reactions', 'answers__comments'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problem = self.get_object()
        user = self.request.user
        answer_reactions = {}
        if user.is_authenticated:
            for answer in problem.answers.all():
                reaction = answer.reactions.filter(user=user).first()
                if reaction:
                    answer_reactions[answer.id] = 'good' if reaction.is_good else 'bad'
        context['answer_reactions'] = answer_reactions

        # 🔽 追加: 各回答に対するコメントフォームを用意
        comment_forms = {
            answer.id: AnswerCommentForm()
            for answer in problem.answers.all()
        }
        context['comment_forms'] = comment_forms

        return context

from django.contrib.auth.mixins import LoginRequiredMixin

class ProblemCreateView(LoginRequiredMixin, CreateView):
    model = Problem
    form_class = ProblemForm
    template_name = 'problems/problem_form.html'
    success_url = reverse_lazy('problems:list')

    def form_valid(self, form):
        form.instance.author = self.request.user  # 作成者をセット
        return super().form_valid(form)


class ProblemUpdateView(LoginRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemForm
    template_name = 'problems/problem_form.html'
    success_url = reverse_lazy('problems:list')
    # 自分の作成した問題のみ編集・削除できるように制限
    def get_queryset(self):
        return Problem.objects.filter(author=self.request.user)  # 自分の問題のみ取得

class ProblemDeleteView(LoginRequiredMixin, DeleteView):
    model = Problem
    template_name = 'problems/problem_confirm_delete.html'
    success_url = reverse_lazy('problems:list')

    def get_queryset(self):
        return Problem.objects.filter(author=self.request.user)  # 自分の問題のみ削除可能


@csrf_exempt
def markdown_preview(request):
    """ユーザーが入力した Markdown を HTML に変換する API"""
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        markdown_text = data.get("content", "")
        html = markdown.markdown(markdown_text)
        return JsonResponse({"markdown": html})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def submit_answer(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.problem = problem
            answer.save()
            form.save_m2m()  # 🔥 多対多フィールドを保存（←これ重要！）
            return redirect('problems:detail', pk=answer.problem.id)
    else:
        form = AnswerForm()

    return render(request, 'problems/submit_answer.html', {'form': form, 'problem': problem})

@login_required
def toggle_reaction(request, answer_id, reaction_type):
    answer = get_object_or_404(Answer, pk=answer_id)
    is_good = reaction_type == 'good'

    reaction, created = AnswerReaction.objects.get_or_create(
        user=request.user,
        answer=answer,
        defaults={'is_good': is_good}
    )

    if not created:
        if reaction.is_good == is_good:
            reaction.delete()
        else:
            reaction.is_good = is_good
            reaction.save()

    return redirect('problems:detail', pk=answer.problem.id)

@login_required
def post_comment(request, answer_id):
    """コメントの投稿処理"""
    answer = get_object_or_404(Answer, id=answer_id)
    if request.method == 'POST':
        form = AnswerCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.answer = answer
            comment.save()
    return redirect('problems:detail', pk=answer.problem.id)