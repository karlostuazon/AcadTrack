from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100) 
    
    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name

class Task(models.Model):
    CAT = (
        ('Project', 'Project'),
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
        ('Exam', 'Exam'),
        ('Other', 'Other')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name="Task Description") 
    #category = models.ForeignKey(Category, on_delete=models.CASCADE, default="Others", null=True, blank=True)
    category = models.CharField(choices=CAT, max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name="Notes")
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    files = models.FileField(null=True, blank=True)

    # -- Saves category as title so def __str__(self) can return something 
    # def save(self, *args, **kwargs):
    #     self.title = str(self.category)
    #     super(Task, self).save(*args, **kwargs)

    def due_int(self):
        due = due|timeuntil
        return int(due)

    def __str__(self):
        return str(self.title)


    class Meta:
        order_with_respect_to = 'user'


 