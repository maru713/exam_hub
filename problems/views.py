from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Problem
from .forms import ProblemForm  # カスタムフォームを作る場合

class ProblemListView(ListView):
    model = Problem
    template_name = 'problems/problem_list.html'
    context_object_name = 'problems'
    paginate_by = 20

    def get_queryset(self):
        return Problem.objects.select_related('category').order_by('-created_at')

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

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('problems:list')
        return super().dispatch(request, *args, **kwargs)

class ProblemDeleteView(LoginRequiredMixin, DeleteView):
    model = Problem
    template_name = 'problems/problem_confirm_delete.html'
    success_url = reverse_lazy('problems:list')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('problems:list')
        return super().dispatch(request, *args, **kwargs)

