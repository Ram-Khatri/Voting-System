from django.contrib import admin
from .models import User

# Register your models here.
admin.site.site_header="Voting System Administration"
admin.site.site_title="Admin panel"
admin.site.index_title="Welcome Home Admin"
admin.site.register(User)