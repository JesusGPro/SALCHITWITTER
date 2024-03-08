from django.contrib import admin

from django.contrib.auth.models import Group, User

from .models import Profile, Salchitweet

class ProfileInline(admin.StackedInline):
    model = Profile
    # The admin interface has the ability to edit models on the same page as a parent model. These are called
    # inlines. 

class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the 'username' field
    fields = ["username"]
    inlines = [ProfileInline]
    
    

admin.site.unregister(User)  # se quita el usuario que viene por defecto
admin.site.register(User, UserAdmin)  # de registra el usuarion, pasando el customizado UserAdmin class que
                                    # que se ha creado, con el campo llamado username, "salchi_admin"
admin.site.unregister(Group)  # se quita el campo Group

# admin.site.register(Profile)  # registramos Profile

admin.site.register(Salchitweet)
