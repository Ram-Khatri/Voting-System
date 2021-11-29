from django.contrib import admin
from .models import Contest,Post,Vote,storeVote

# Register your models here.
admin.site.register(Contest)
admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(storeVote)

