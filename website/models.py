from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=255, null=False)
    href = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, null=False)
    href = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.name


class Mechanic(models.Model):
    name = models.CharField(max_length=255, null=False)
    href = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.name


class Family(models.Model):
    name = models.CharField(max_length=255, null=False)
    href = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.name


class Boardgame(models.Model):
    name = models.CharField(max_length=255, null=False)
    min_players = models.IntegerField(null=False)
    max_players = models.IntegerField(null=False)
    min_best_players = models.IntegerField(null=False)
    max_best_players = models.IntegerField(null=False)
    min_age = models.IntegerField(null=False)
    weight = models.FloatField(null=False)
    min_play_time = models.IntegerField(null=False)
    max_play_time = models.IntegerField(null=False)
    bg_image = models.ImageField(null=False)
    description = models.TextField()
    bgg_code = models.IntegerField(null=False)
    stddev = models.FloatField(null=False)
    users_rated = models.IntegerField(null=False)
    fans = models.IntegerField(null=False)
    num_owned = models.IntegerField(null=False)
    year_published = models.IntegerField(null=False)
    num_plays = models.IntegerField(null=False)
    num_wish = models.IntegerField(null=False)
    sub_type = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class TypeToBoardgame(models.Model):
    type = models.ForeignKey(to=Type, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class CategoryToBoardgame(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, default=0)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class MechanicToBoardgame(models.Model):
    mechanic = models.ForeignKey(to=Mechanic, on_delete=models.CASCADE, default=0)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class FamilyToBoardgame(models.Model):
    family = models.ForeignKey(to=Family, on_delete=models.CASCADE, default=0)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class Rank(models.Model):
    rank_value = models.IntegerField(null=False)
    average = models.FloatField(null=False)
    rank_name = models.CharField(max_length=255, null=False)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField(null=False)
    bgg_image_id = models.IntegerField(null=False)
    img_caption = models.TextField(null=False)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class File(models.Model):
    file_title = models.CharField(max_length=500, null=False)
    bgg_file_page_id = models.IntegerField(null=False)
    bgg_file_id = models.IntegerField(null=False)
    file_desc = models.TextField(null=False)
    file_name = models.CharField(max_length=500, null=False)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class Forum(models.Model):
    forum_title = models.CharField(max_length=500, null=False)
    forum_category = models.CharField(max_length=500, null=False)
    bgg_forum_id = models.IntegerField(null=False)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class Video(models.Model):
    video_title = models.CharField(max_length=500, null=False)
    bgg_video_id = models.IntegerField(null=False)
    video_category = models.CharField(max_length=250, null=False)
    youtube_video_id = models.CharField(max_length=50, null=False)
    video_post_date = models.CharField(max_length=250, null=False)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class Expansion(models.Model):
    expansion_bgg_id = models.IntegerField(null=False)
    expansion_name = models.CharField(max_length=500, null=False)
    expansion_image = models.ImageField(null=False)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE, related_name="base_bg")


class Credit(models.Model):
    credit_bgg_id = models.IntegerField(null=False)
    credit_kind = models.CharField(max_length=200, null=False)
    credit_title = models.CharField(max_length=500, null=False)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE, related_name="credit_bg")


class User(models.Model):
    username = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=250, null=False)
    password = models.CharField(max_length=500, null=False)
    def __str__(self):
        return self.username


class UserLikes(models.Model):
    username = models.ForeignKey(to=User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class UserWishes(models.Model):
    username = models.ForeignKey(to=User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class UserHas(models.Model):
    username = models.ForeignKey(to=User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)


class UserRates(models.Model):
    rate = models.IntegerField(null=False)
    username = models.ForeignKey(to=User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(to=Boardgame, on_delete=models.CASCADE)




