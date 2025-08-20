from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from apps.blog.models import Blog, BlogCategory, Tag
from apps.settings.models import SiteSettings
from apps.core.models import Service
from django.db.models import Q
from django.db.models import Count


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        # Base queryset with related optimizations
        queryset = (
            Blog.objects.filter(deleted_at__isnull=True)
            .select_related('category')
            .prefetch_related('tags')
        )

        # 🔎 Search filter (title & content)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by tag
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        if not queryset.exists():
            self.extra_context = {'no_blogs': True}

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Site settings (singleton)
        site_settings = SiteSettings.objects.first()

        # Limit services to 3 with prefetch features
        services = Service.objects.prefetch_related('features').all()[:3]
        context['categories'] = BlogCategory.objects.all()
        context['tags'] = Tag.objects.all()
        # Add extra context
        context.update({
            'site_settings': site_settings,
            'services': services,
            'title': site_settings.site_title if site_settings else 'Blogs',
            'meta_description': site_settings.meta_description if site_settings else 'Latest blogs and updates',
            'meta_keywords': site_settings.meta_keywords if site_settings else 'blogs, articles, updates',
        })

        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        # Join category and tags in single query
        queryset = Blog.objects.filter(deleted_at__isnull=True)\
                               .select_related('category')\
                               .prefetch_related('tags')
        obj = get_object_or_404(queryset, slug=self.kwargs.get(self.slug_url_kwarg))
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()

        # Prefetch categories and tags
        context['tags'] = blog.tags.all()
        
        # Categories with count of published blogs
        context['categories'] = BlogCategory.objects.annotate(
            blog_count=Count('blogs')  # use 'blogs', the correct related_name
        )

        context['category'] = blog.category
        return context
