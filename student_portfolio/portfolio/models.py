from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    headline = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    portfolio_visibility = models.CharField(
        max_length=10,
        choices=[('public', 'Public'), ('private', 'Private')],
        default='public'
    )
    THEME_CHOICES = [
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
        ('developer', 'Developer Theme'),
    ]
    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default='light'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Profile.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    tech_stack = models.CharField(max_length=300, blank=True, help_text="Comma-separated technologies")
    github_link = models.URLField(blank=True)
    live_demo = models.URLField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def tech_list(self):
        """Return tech stack as a list."""
        if self.tech_stack:
            return [t.strip() for t in self.tech_stack.split(',') if t.strip()]
        return []

    def __str__(self):
        return self.title


class Skill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=3,
        help_text="1=Beginner, 5=Expert"
    )

    class Meta:
        ordering = ['-proficiency', 'name']

    def __str__(self):
        return f"{self.name} ({self.proficiency}/5)"


class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = 'Education'

    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Experience(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} at {self.company}"


class Achievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_earned = models.DateField(blank=True, null=True)
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)
    certificate_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-date_earned']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='contact_messages')
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender_name} to {self.profile.user.username}"