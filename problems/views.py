from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Problem, Answer, AnswerReaction
from .forms import ProblemForm  # カスタムフォームを作る場合
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import markdown
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm

class ProblemListView(ListView):
    model = Problem
    template_name = 'problems/problem_list.html'
    context_object_name = 'problems'
    paginate_by = 20

def get_queryset(self):
    queryset = Problem.objects.select_related('author').order_by('-created_at')
    query = self.request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(answer__icontains=query)
        )
    return queryset

class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'problems/problem_detail.html'
    context_object_name = 'problem'

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
            return redirect('problem_detail', pk=problem_id)
    else:
        form = AnswerForm()

    return render(request, 'problems/submit_answer.html', {'form': form, 'problem': problem})

@login_required
def toggle_reaction(request, answer_id, reaction_type):
    """
    ユーザーが回答に👍👎リアクションするビュー
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    reaction, created = AnswerReaction.objects.get_or_create(
        user=request.user,
        answer=answer,
        defaults={'reaction_type': reaction_type}
    )

    if not created:
        if reaction.reaction_type == reaction_type:
            reaction.delete()  # 同じ反応を2回押すと取り消し
        else:
            reaction.reaction_type = reaction_type
            reaction.save()

    return redirect('problem_detail', pk=answer.problem.id)