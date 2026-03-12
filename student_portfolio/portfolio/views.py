from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Profile, Project, Skill, Education, Experience
from .forms import ProjectForm, SkillForm, EducationForm, ExperienceForm
from .utils import render_to_pdf


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


# ─── Resume ───────────────────────────────────────────────────────────────────

RESUME_TEMPLATES = [
    'modern', 'classic', 'minimal', 'creative', 
    'professional', 'compact', 'academic', 'twocolumn'
]

@login_required
def resume_selection(request):
    return render(request, 'portfolio/resume_selection.html', {'templates': RESUME_TEMPLATES})

@login_required
def resume_preview(request, template_name):
    if template_name not in RESUME_TEMPLATES:
        raise Http404("Template not found.")
    
    profile = request.user.profile
    context = {
        'profile': profile,
        'user': request.user,
        'skills': Skill.objects.filter(user=request.user),
        'education': Education.objects.filter(user=request.user),
        'experiences': Experience.objects.filter(user=request.user),
        'projects': Project.objects.filter(owner=request.user, is_public=True),
    }
    return render(request, f'portfolio/resume_templates/{template_name}.html', context)


@login_required
def resume_download(request, template_name):
    if template_name not in RESUME_TEMPLATES:
        raise Http404("Template not found.")

    profile = request.user.profile
    context = {
        'profile': profile,
        'user': request.user,
        'skills': Skill.objects.filter(user=request.user),
        'education': Education.objects.filter(user=request.user),
        'experiences': Experience.objects.filter(user=request.user),
        'projects': Project.objects.filter(owner=request.user, is_public=True),
    }
    pdf = render_to_pdf(f'portfolio/resume_templates/{template_name}.html', context)
    if pdf:
        return pdf
    messages.error(request, 'Error generating PDF.')
    return redirect('resume_selection')