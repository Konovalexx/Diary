from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Entry
from .forms import EntryForm, SearchForm


class IndexView(ListView):
    """Представление для отображения публичных записей."""

    model = Entry
    template_name = "diary/index.html"
    context_object_name = "entries"

    def get_queryset(self):
        """Получаем только публичные записи, отсортированные по дате создания."""
        return Entry.objects.filter(is_public=True).order_by("-created_at")

    def get_context_data(self, **kwargs):
        """Добавляем текущий год в контекст для футера."""
        context = super().get_context_data(**kwargs)
        context["current_year"] = timezone.now().year  # Добавляем текущий год
        return context


class MyDiaryView(LoginRequiredMixin, ListView):
    """Представление для отображения личного дневника пользователя."""

    model = Entry
    template_name = "diary/my_diary.html"
    context_object_name = "entries"

    def get_queryset(self):
        """Получаем записи, принадлежащие текущему пользователю."""
        return Entry.objects.filter(author=self.request.user).order_by("-created_at")


class SearchView(ListView):
    """Представление для поиска записей по запросу."""

    model = Entry
    template_name = "diary/index.html"  # Используем тот же шаблон, что и для отображения публичных записей
    context_object_name = "entries"

    def get_queryset(self):
        """Фильтруем записи по запросу."""
        query = self.request.GET.get("query", "")
        is_public = self.request.GET.get(
            "is_public", ""
        )  # Добавляем фильтрацию по публичности
        author = self.request.GET.get("author", "")

        # Базовый queryset: только публичные записи
        queryset = Entry.objects.filter(is_public=True).order_by("-created_at")

        # Фильтрация по запросу
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        # Фильтрация по публичности (если указано)
        if is_public:
            queryset = queryset.filter(is_public=True)

        # Фильтрация по автору (если указан)
        if author:
            queryset = queryset.filter(author__email__icontains=author)

        return queryset

    def get_context_data(self, **kwargs):
        """Добавляем форму поиска в контекст."""
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        context["current_year"] = timezone.now().year  # Добавляем текущий год
        return context


class EntryCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания новой записи."""

    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_url = reverse_lazy("diary:my_diary")

    def form_valid(self, form):
        """Заполняем автора записи текущим пользователем перед сохранением."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Добавляем дополнительные данные для шаблона."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Новая запись"
        return context


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования записи."""

    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_url = reverse_lazy("diary:my_diary")

    def get_object(self, queryset=None):
        """Проверяем, что пользователь является автором записи, иначе выбрасываем исключение."""
        entry = get_object_or_404(Entry, pk=self.kwargs["pk"])
        if entry.author != self.request.user:
            raise PermissionDenied("У вас нет прав на редактирование этой записи.")
        return entry

    def get_context_data(self, **kwargs):
        """Добавляем дополнительные данные для шаблона."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактировать запись"
        return context


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления записи."""

    model = Entry
    template_name = "diary/entry_confirm_delete.html"
    success_url = reverse_lazy("diary:my_diary")

    def get_object(self, queryset=None):
        """Проверяем, что только автор записи может её удалить."""
        entry = get_object_or_404(Entry, pk=self.kwargs["pk"])
        if entry.author != self.request.user:
            raise PermissionDenied("У вас нет прав на удаление этой записи.")
        return entry


class EntryDetailView(DetailView):
    """Представление для просмотра подробной записи."""

    model = Entry
    template_name = "diary/entry_detail.html"
    context_object_name = "entry"

    def get_context_data(self, **kwargs):
        """Добавляем текущий год для футера."""
        context = super().get_context_data(**kwargs)
        context["current_year"] = timezone.now().year
        return context
