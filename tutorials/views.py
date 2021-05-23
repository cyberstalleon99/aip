from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .models import Tutorial
from workforce.models import Department
from .forms import VideoForm
from warehouse.helpers import add_log, change_log

from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag


def tutorial_page_view(request):
    return render(request, 'tutorials/latest_tutorials.html')

class DepartmentTutorialsView(ListView):
    model = Tutorial
    template_name = 'tutorials/department_tutorials.html'
    context_object_name = 'tutorials'

    def get_context_data(self, **kwargs):
        context = super(DepartmentTutorialsView, self).get_context_data(**kwargs)
        context['curr_department'] = Department.objects.get(id=self.kwargs['pk'])
        departments = Department.objects.all()
        context['departments'] = departments
        return context

    def get_queryset(self):
        return self.model.objects.filter(department__in=self.kwargs['pk'])

class LatestTutorailsView(ListView):
    model = Tutorial
    template_name = 'tutorials/latest_tutorials.html'
    context_object_name = 'latest_tutorials'

    # def get_sliced_qs(self, qs):
    #     slice_every = 3
    #     start_at = 0

    #     quotient, remainder = divmod(qs.count / 3)

    #     for i in quotient:
    #         qs[]

    #     return qs[start_at:start_at+3]


    def get_context_data(self, **kwargs):
        context = super(LatestTutorailsView, self).get_context_data(**kwargs)
        departments = Department.objects.all()
        context['departments'] = departments

        # for department in departments:
        #     self.get_sliced_qs(department.tutorials.all)

        return context

class NewTutorialView(LoginRequiredMixin, CreateView):
    model = Tutorial
    template_name = 'tutorials/new_video_form.html'
    form_class = VideoForm

    def form_valid(self, form):
        new_video = form.save(commit=False)
        new_video.slug = slugify(new_video.title)
        new_video.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)

        return reverse_lazy('tutorials:latest')

class UpdateTutorialView(LoginRequiredMixin, UpdateView):
    model = Tutorial
    template_name = 'tutorials/update_video_form.html'
    form_class = VideoForm

    def form_valid(self, form):
        self.form = form
        new_video = form.save(commit=False)
        new_video.slug = slugify(new_video.title)
        new_video.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)

        return reverse_lazy('tutorials:latest')

class DetailTutorialView(DetailView):
    model = Tutorial
    template_name = 'tutorials/search_results.html'
    context_object_name = 'curr_tutorial'

    def get_context_data(self, **kwargs):
        context = super(DetailTutorialView, self).get_context_data(**kwargs)
        departments = Department.objects.all()
        context['departments'] = departments

        q = self.kwargs['q']
        result = self.model.objects.filter(Q(title__icontains=q) | Q(desc__icontains=q) | Q(tags__name=q)).distinct()

        paginator = Paginator(result, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['q_value'] = q
        context['related_videos'] = get_similar_videos(result, self.get_object().tags.similar_objects())
        return context

class SearchResultsView(ListView):
    model = Tutorial
    paginate_by = 10
    template_name = 'tutorials/search_results.html'
    context_object_name = 'tutorials'

    def get_queryset(self):
        q = self.request.GET.get('q')
        result = self.model.objects.filter(Q(title__icontains=q) | Q(desc__icontains=q) | Q(tags__name=q)).distinct()
        return result

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        departments = Department.objects.all()
        context['departments'] = departments
        context['q_value'] = self.request.GET.get('q')

        curr_tutorial = self.get_queryset().first()
        similar_objs = []
        if curr_tutorial:
            similar_objs = curr_tutorial.tags.similar_objects()

        context['curr_tutorial'] = curr_tutorial
        context['related_videos'] = get_similar_videos(self.get_queryset(), similar_objs)
        return context

def get_similar_videos(base, possible_related):

    related_videos = []
    for tuts in possible_related:
        if tuts not in base:
            related_videos.append(tuts)

    return related_videos

def tagged(request, tag_slug, tut_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)

    tutorials = Tutorial.objects.filter(tags=tag)
    possible_related = Tutorial.objects.get(slug=tut_slug).tags.similar_objects()

    departments = Department.objects.all()

    paginator = Paginator(tutorials, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # try:
    #     page_obj = paginator.page(page_number)
    # except PageNotAnInteger:
    #     page_obj = paginator.page(1)
    # except EmptyPage:
    #     page_obj = paginator.page(paginator.num_pages)

    context = {
        'tutorials': tutorials,
        'departments': departments,
        'q_value': tag.name,
        'curr_tutorial': page_obj[0],
        'related_videos': get_similar_videos(tutorials, possible_related),
        'page_obj': page_obj
    }

    return render(request, 'tutorials/search_results.html', context)