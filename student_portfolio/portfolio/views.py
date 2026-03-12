from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from .models import Profile, Project, Skill, Education, Experience
from .forms import ProjectForm, SkillForm, EducationForm, ExperienceForm
from .utils import render_to_pdf
import json


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    profile = request.user.profile
    projects = Project.objects.filter(owner=request.user)
    skills = Skill.objects.filter(user=request.user)
    education = Education.objects.filter(user=request.user)
    experiences = Experience.objects.filter(user=request.user)
    context = {
        'profile': profile,
        'projects': projects,
        'skills': skills,
        'education': education,
        'experiences': experiences,
    }
    return render(request, 'portfolio/dashboard.html', context)


# ─── Public Portfolio ─────────────────────────────────────────────────────────

def public_portfolio(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    if profile.portfolio_visibility == 'private':
        if not request.user.is_authenticated or request.user != profile.user:
            raise Http404("This portfolio is private.")
    projects = Project.objects.filter(owner=profile.user, is_public=True)
    skills = Skill.objects.filter(user=profile.user)
    education = Education.objects.filter(user=profile.user)
    experiences = Experience.objects.filter(user=profile.user)
    blog_posts = profile.user.blog_posts.filter(status='published')
    context = {
        'profile': profile,
        'portfolio_user': profile.user,
        'projects': projects,
        'skills': skills,
        'education': education,
        'experiences': experiences,
        'blog_posts': blog_posts,
    }
    return render(request, 'portfolio/public_portfolio.html', context)


# ─── Project CRUD ─────────────────────────────────────────────────────────────

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Project added!')
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'portfolio/project_form.html', {'form': form, 'title': 'Add Project'})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not project.is_public and request.user != project.owner:
        raise Http404
    return render(request, 'portfolio/project_detail.html', {'project': project})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated!')
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'portfolio/project_form.html', {'form': form, 'title': 'Edit Project'})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('dashboard')
    return render(request, 'portfolio/confirm_delete.html', {'object': project, 'type': 'project'})


# ─── Skill CRUD ───────────────────────────────────────────────────────────────

@login_required
def skill_create(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill added!')
            return redirect('dashboard')
    else:
        form = SkillForm()
    return render(request, 'portfolio/generic_form.html', {'form': form, 'title': 'Add Skill'})


@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated!')
            return redirect('dashboard')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'portfolio/generic_form.html', {'form': form, 'title': 'Edit Skill'})


@login_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted.')
        return redirect('dashboard')
    return render(request, 'portfolio/confirm_delete.html', {'object': skill, 'type': 'skill'})


# ─── Education CRUD ──────────────────────────────────────────────────────────

@login_required
def education_create(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.user = request.user
            edu.save()
            messages.success(request, 'Education added!')
            return redirect('dashboard')
    else:
        form = EducationForm()
    return render(request, 'portfolio/generic_form.html', {'form': form, 'title': 'Add Education'})


@login_required
def education_edit(request, pk):
    edu = get_object_or_404(Education, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=edu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Education updated!')
            return redirect('dashboard')
    else:
        form = EducationForm(instance=edu)
    return render(request, 'portfolio/generic_form.html', {'form': form, 'title': 'Edit Education'})


@login_required
def education_delete(request, pk):
    edu = get_object_or_404(Education, pk=pk, user=request.user)
    if request.method == 'POST':
        edu.delete()
        messages.success(request, 'Education entry deleted.')
        return redirect('dashboard')
    return render(request, 'portfolio/confirm_delete.html', {'object': edu, 'type': 'education'})


# ─── Experience CRUD ─────────────────────────────────────────────────────────

@login_required
def experience_create(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            messages.success(request, 'Experience added!')
            return redirect('dashboard')
    else:
        form = ExperienceForm()
    return render(request, 'portfolio/generic_form.html', {'form': form, 'title': 'Add Experience'})


@login_required
def experience_edit(request, pk):
    exp = get_object_or_404(Experience, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experience updated!')
            return redirect('dashboard')
    else:
        form = ExperienceForm(instance=exp)
    return render(request, 'portfolio/generic_form.html', {'form': form, 'title': 'Edit Experience'})


@login_required
def experience_delete(request, pk):
    exp = get_object_or_404(Experience, pk=pk, user=request.user)
    if request.method == 'POST':
        exp.delete()
        messages.success(request, 'Experience entry deleted.')
        return redirect('dashboard')
    return render(request, 'portfolio/confirm_delete.html', {'object': exp, 'type': 'experience'})


# ─── Resume Template System ──────────────────────────────────────────────────

# Template metadata with display info for the gallery cards
RESUME_TEMPLATES = {
    'modern': {
        'name': 'Modern',
        'description': 'Clean lines with blue accents and a sleek header layout.',
        'icon': '🔷',
        'accent': '#0056b3',
        'preview_bg': 'linear-gradient(135deg, #e8f0fe, #ffffff)',
        'font': 'Helvetica Neue',
        'category': 'Professional',
    },
    'classic': {
        'name': 'Classic',
        'description': 'Timeless serif design with traditional resume formatting.',
        'icon': '📜',
        'accent': '#333333',
        'preview_bg': 'linear-gradient(135deg, #f5f0e8, #ffffff)',
        'font': 'Times New Roman',
        'category': 'Traditional',
    },
    'minimal': {
        'name': 'Minimal',
        'description': 'Ultra-clean with bold typography and maximum whitespace.',
        'icon': '✨',
        'accent': '#111111',
        'preview_bg': 'linear-gradient(135deg, #f8f8f8, #ffffff)',
        'font': 'Segoe UI',
        'category': 'Modern',
    },
    'creative': {
        'name': 'Creative',
        'description': 'Vibrant coral header with card-based sections and rounded pills.',
        'icon': '🎨',
        'accent': '#ff6b6b',
        'preview_bg': 'linear-gradient(135deg, #ffe3e3, #fafaef)',
        'font': 'Montserrat',
        'category': 'Creative',
    },
    'professional': {
        'name': 'Professional',
        'description': 'Corporate-ready with structured layout and bold headings.',
        'icon': '💼',
        'accent': '#222222',
        'preview_bg': 'linear-gradient(135deg, #f0f0f0, #ffffff)',
        'font': 'Arial',
        'category': 'Professional',
    },
    'twocolumn': {
        'name': 'Two-Column',
        'description': 'Dark sidebar with contact & skills, main area for experience.',
        'icon': '📊',
        'accent': '#3498db',
        'preview_bg': 'linear-gradient(135deg, #2c3e50 33%, #ecf0f1 33%)',
        'font': 'Open Sans',
        'category': 'Modern',
    },
    'academic': {
        'name': 'Academic',
        'description': 'Traditional CV style with centered headings and serif fonts.',
        'icon': '🎓',
        'accent': '#000000',
        'preview_bg': 'linear-gradient(135deg, #f9f6f0, #ffffff)',
        'font': 'Garamond',
        'category': 'Academic',
    },
    'compact': {
        'name': 'Compact',
        'description': 'Information-dense layout with grey section bars and side dates.',
        'icon': '📋',
        'accent': '#1a1a1a',
        'preview_bg': 'linear-gradient(135deg, #e6e6e6, #ffffff)',
        'font': 'Helvetica',
        'category': 'Professional',
    },
    'dark': {
        'name': 'Dark Theme',
        'description': 'Sleek dark design with gradient header and neon accent highlights.',
        'icon': '🌙',
        'accent': '#e94560',
        'preview_bg': 'linear-gradient(135deg, #1a1a2e, #16213e)',
        'font': 'Helvetica Neue',
        'category': 'Creative',
    },
}

# Font options available for customization
FONT_OPTIONS = [
    ('Helvetica, Arial, sans-serif', 'Helvetica'),
    ("'Times New Roman', Times, serif", 'Times New Roman'),
    ("'Georgia', serif", 'Georgia'),
    ("'Courier New', Courier, monospace", 'Courier New'),
    ("'Verdana', Geneva, sans-serif", 'Verdana'),
    ("'Trebuchet MS', sans-serif", 'Trebuchet MS'),
    ("'Garamond', serif", 'Garamond'),
    ("'Palatino Linotype', serif", 'Palatino'),
    ("-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", 'System UI'),
    ("'Lucida Console', Monaco, monospace", 'Lucida Console'),
]

# Color theme presets
COLOR_THEMES = [
    ('#0056b3', 'Royal Blue'),
    ('#e94560', 'Vibrant Rose'),
    ('#2ecc71', 'Emerald Green'),
    ('#e67e22', 'Sunset Orange'),
    ('#9b59b6', 'Amethyst Purple'),
    ('#1abc9c', 'Turquoise'),
    ('#e74c3c', 'Crimson Red'),
    ('#34495e', 'Charcoal'),
    ('#f39c12', 'Golden Yellow'),
    ('#2980b9', 'Ocean Blue'),
    ('#8e44ad', 'Deep Purple'),
    ('#d35400', 'Pumpkin'),
]

FONT_SIZES = [
    (8, '8pt — Extra Small'),
    (9, '9pt — Small'),
    (10, '10pt — Default'),
    (11, '11pt — Medium'),
    (12, '12pt — Large'),
    (13, '13pt — Extra Large'),
    (14, '14pt — Huge'),
]


@login_required
def resume_selection(request):
    """Render the resume template gallery page."""
    context = {
        'templates': RESUME_TEMPLATES,
        'templates_json': json.dumps(RESUME_TEMPLATES),
        'font_options': FONT_OPTIONS,
        'color_themes': COLOR_THEMES,
        'font_sizes': FONT_SIZES,
    }
    return render(request, 'portfolio/resume_gallery.html', context)


@login_required
def resume_preview(request, template_name):
    """Render a preview of a specific resume template (HTML)."""
    if template_name not in RESUME_TEMPLATES:
        raise Http404("Template not found.")

    # Extract customization params from GET
    font_family = request.GET.get('font', '')
    font_size = request.GET.get('size', '')
    accent_color = request.GET.get('color', '')

    profile = request.user.profile
    context = {
        'profile': profile,
        'user': request.user,
        'skills': Skill.objects.filter(user=request.user),
        'education': Education.objects.filter(user=request.user),
        'experiences': Experience.objects.filter(user=request.user),
        'projects': Project.objects.filter(owner=request.user, is_public=True),
        'template_name': template_name,
        'font_family': font_family,
        'font_size': font_size,
        'accent_color': accent_color,
    }
    return render(request, f'portfolio/resume_templates/{template_name}.html', context)


@login_required
def resume_preview_ajax(request, template_name):
    """Return rendered HTML of a resume template for AJAX live preview."""
    if template_name not in RESUME_TEMPLATES:
        return JsonResponse({'error': 'Template not found'}, status=404)

    font_family = request.GET.get('font', '')
    font_size = request.GET.get('size', '')
    accent_color = request.GET.get('color', '')

    profile = request.user.profile
    context = {
        'profile': profile,
        'user': request.user,
        'skills': Skill.objects.filter(user=request.user),
        'education': Education.objects.filter(user=request.user),
        'experiences': Experience.objects.filter(user=request.user),
        'projects': Project.objects.filter(owner=request.user, is_public=True),
        'font_family': font_family,
        'font_size': font_size,
        'accent_color': accent_color,
    }
    html = render_to_string(f'portfolio/resume_templates/{template_name}.html', context, request=request)
    return JsonResponse({'html': html})


@login_required
def resume_download(request, template_name):
    """Download resume as PDF with optional customization."""
    if template_name not in RESUME_TEMPLATES:
        raise Http404("Template not found.")

    font_family = request.GET.get('font', '')
    font_size = request.GET.get('size', '')
    accent_color = request.GET.get('color', '')

    profile = request.user.profile
    context = {
        'profile': profile,
        'user': request.user,
        'skills': Skill.objects.filter(user=request.user),
        'education': Education.objects.filter(user=request.user),
        'experiences': Experience.objects.filter(user=request.user),
        'projects': Project.objects.filter(owner=request.user, is_public=True),
        'font_family': font_family,
        'font_size': font_size,
        'accent_color': accent_color,
    }
    template_info = RESUME_TEMPLATES[template_name]
    filename = f"resume_{template_info['name'].lower().replace(' ', '_')}.pdf"
    pdf = render_to_pdf(f'portfolio/resume_templates/{template_name}.html', context, filename=filename)
    if pdf:
        return pdf
    messages.error(request, 'Error generating PDF. Please make sure xhtml2pdf is installed.')
    return redirect('resume_selection')