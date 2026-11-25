from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ProjectForm, SignUpForm
from .models import Project


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("project_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "註冊成功，歡迎使用！")
        return response


class OwnerQuerysetMixin(LoginRequiredMixin):
    """每個使用者只能看到、修改自己的案件。"""

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectListView(OwnerQuerysetMixin, ListView):
    model = Project
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(client_name__icontains=q))
        if status in Project.Status.values:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        mine = Project.objects.filter(owner=self.request.user)
        stats = mine.aggregate(
            total=Count("id"),
            in_progress=Count("id", filter=Q(status=Project.Status.IN_PROGRESS)),
            done_budget=Sum("budget", filter=Q(status=Project.Status.DONE)),
            pipeline_budget=Sum("budget", filter=~Q(status=Project.Status.DONE)),
        )
        ctx["stats"] = stats
        ctx["status_choices"] = Project.Status.choices
        ctx["q"] = self.request.GET.get("q", "")
        ctx["current_status"] = self.request.GET.get("status", "")
        return ctx


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "已新增案件。")
        return super().form_valid(form)


class ProjectUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        messages.success(self.request, "已更新案件。")
        return super().form_valid(form)


class ProjectDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("project_list")

    def form_valid(self, form):
        messages.success(self.request, f"已刪除「{self.object.title}」。")
        return super().form_valid(form)
