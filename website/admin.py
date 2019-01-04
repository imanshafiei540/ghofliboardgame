from django.contrib import admin
from website.models import *

admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Mechanic)
admin.site.register(Family)
admin.site.register(Boardgame)
admin.site.register(TypeToBoardgame)
admin.site.register(CategoryToBoardgame)
admin.site.register(MechanicToBoardgame)
admin.site.register(FamilyToBoardgame)
admin.site.register(Rank)
admin.site.register(Image)
admin.site.register(File)
admin.site.register(Credit)
admin.site.register(User)
admin.site.register(Expansion)
admin.site.register(UserLikes)
admin.site.register(UserWishes)
admin.site.register(UserHas)
admin.site.register(UserRates)



