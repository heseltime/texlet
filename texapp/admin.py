from django.contrib import admin

from texapp.models import Letter, ProfileUser, ProfileAddressee

# separate lines, like this:

admin.site.register(Letter)
admin.site.register(ProfileUser)
admin.site.register(ProfileAddressee)


