from django.shortcuts import render, redirect
from .forms import ProjectForm

def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()

    return render(request, 'portfolio/add_project.html', {'form': form})
from django.shortcuts import render
from .models import Project

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'portfolio/projects.html', {'projects': projects})