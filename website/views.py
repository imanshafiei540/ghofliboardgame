from django.shortcuts import render
from website.models import *
import requests, json
from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect


def index(request):
    user = {}
    user["has_user"] = 0
    if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
        username = request.session['username']
        user["has_user"] = 1
        user["username"] = username
    strategy_top = Rank.objects.filter(rank_name="Strategy ").order_by('rank_value')[:10]
    thematic_top = Rank.objects.filter(rank_name="Thematic").order_by('rank_value')[:10]
    family_top = Rank.objects.filter(rank_name="Family ").order_by('rank_value')[:10]
    return render(request, "search.html", {"user": user, "strategy_bg": strategy_top, 'thematic': thematic_top, "family_top": family_top})


def search(request):
    user = {}
    user["has_user"] = 0
    if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
        username = request.session['username']
        user["has_user"] = 1
        user["username"] = username
    if request.GET:
        search_word = request.GET['q']
        all_bgs = Boardgame.objects.filter(name__icontains=search_word)
        print(user)
        return render(request, "seachresult.html", {"boardgames": all_bgs, "user": user})


def show_boardgame(request, bgg_code):
    user = {}
    user["has_user"] = 0
    if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
        username = request.session['username']
        user["has_user"] = 1
        user["username"] = username
    boardgame = Boardgame.objects.get(bgg_code=bgg_code)
    images = Image.objects.filter(boardgame=boardgame).order_by("id")[:12]
    videos = Video.objects.filter(boardgame=boardgame).order_by("id")
    forums = Forum.objects.filter(boardgame=boardgame).order_by("id")
    mycredits = Credit.objects.filter(boardgame=boardgame).order_by("id")
    designer = []
    artist = []
    publisher = []
    for credit in mycredits:
        if credit.credit_kind == "DESIGNER":
            designer.append({"name": credit.credit_title, "objectid": credit.credit_bgg_id})
        if credit.credit_kind == "ARTIST":
            artist.append({"name": credit.credit_title, "objectid": credit.credit_bgg_id})
        if credit.credit_kind == "PUBLISHER":
            publisher.append({"name": credit.credit_title, "objectid": credit.credit_bgg_id})
    expansions = Expansion.objects.filter(boardgame=boardgame).order_by("id")
    files = File.objects.filter(boardgame=boardgame).order_by("id")
    files_show = []
    for file in files:
        ext_list = file.file_name.split(".")
        ext = ext_list[len(ext_list) - 1]
        files_show.append({"file": file, "ext": ext})
    types = []
    bg_types = TypeToBoardgame.objects.filter(boardgame=boardgame)
    for type in bg_types:
        types.append({"name": type.type.name, "href": type.type.href})

    mechs = []
    bg_mechs = MechanicToBoardgame.objects.filter(boardgame=boardgame)
    for mech in bg_mechs:
        mechs.append({"name": mech.mechanic.name, "href": mech.mechanic.href})

    families = []
    bg_families = FamilyToBoardgame.objects.filter(boardgame=boardgame)
    for fam in bg_families:
        families.append({"name": fam.family.name, "href": fam.family.href})

    bg_rank = Rank.objects.filter(boardgame=boardgame)
    ranks = []
    overall = 0
    desc = boardgame.description
    desc = desc.replace("\\", "")
    for rank in bg_rank:
        if rank.rank_name == "Overall":
            ranks.append({"name": "کلی", "val": rank.rank_value})
            overall_real = rank.average
            overall = round(rank.average, 1)
        elif rank.rank_name == "Strategy ":
            ranks.append({"name": "استراتژی", "val": rank.rank_value})
        elif rank.rank_name == "Thematic":
            ranks.append({"name": "تماتیک", "val": rank.rank_value})
        elif rank.rank_name == "War":
            ranks.append({"name": "جنگ", "val": rank.rank_value})
        elif rank.rank_name == "Family ":
            ranks.append({"name": "خانواده", "val": rank.rank_value})
        elif rank.rank_name == "Abstract ":
            ranks.append({"name": "استراتژی انتزاعی", "val": rank.rank_value})
        elif rank.rank_name == "Party ":
            ranks.append({"name": "مهمانی", "val": rank.rank_value})
        elif "Children" in rank.rank_name:
            ranks.append({"name": "کودکان", "val": rank.rank_value})
        else:
            ranks.append({"name": rank.rank_name, "val": rank.rank_value})
    return render(request, "index.html",
                  {"boardgame": boardgame, "ranks": ranks, 'overallval': overall, 'overallvalreal': overall_real,
                   "bg_desc": desc, "types": types,
                   "mechs": mechs, "families": families, "images": images, "files": files_show, "videos": videos,
                   "expansions": expansions, "forums": forums, "designers": designer, "artists": artist,
                   "publishers": publisher, "user": user})


def bgg_enter_items(request):
    try:
        for j in range(57, 101):
            print("Page: " + str(j))
            url = "https://boardgamegeek.com/browse/boardgame/page/" + str(j)
            bgg_site_content = requests.get(url).content
            soup = BeautifulSoup(bgg_site_content, 'html.parser')
            table_content = soup.find("table", {"id": "collectionitems"})
            items = table_content.find_all("tr")
            for i in range(1, len(items)):
                print("starting")
                item_td = items[i].find("td", {"class": "collection_thumbnail"})
                bgg_url = "https://boardgamegeek.com/" + item_td.find("a")['href']
                bgg_code = item_td.find("a")['href'].split("/")[2]
                bgg_content = requests.get(bgg_url, timeout=30).content
                bgg_soup = BeautifulSoup(bgg_content, 'html.parser')
                game_content = bgg_soup.find("script")
                if not game_content:
                    bgg_code = item_td.find("a")['href'].split("/")[2]
                    bgg_content = requests.get(bgg_url, timeout=10).content
                    bgg_soup = BeautifulSoup(bgg_content, 'html.parser')
                    game_content = bgg_soup.find("script")

                game_data = game_content.text[
                            game_content.text.find("GEEK.geekitemPreload"):game_content.text.find(
                                "GEEK.geekitemSettings") - 3]
                game_data = game_data.replace("GEEK.geekitemPreload = ", "")
                game_data = game_data.replace("true", "True")
                game_data = game_data.replace("false", "False")
                game_data = game_data.replace("null", "'null'")
                game_json_data = eval(game_data)
                # print(json.dumps(game_json_data['item'], indent=4, sort_keys=True))
                min_player = game_json_data['item']['minplayers']
                max_player = game_json_data['item']['maxplayers']
                max_play_time = game_json_data['item']['maxplaytime']
                min_play_time = game_json_data['item']['minplaytime']
                min_age = game_json_data['item']['minage']
                avg_weight = game_json_data['item']['stats']['avgweight']
                stddev = game_json_data['item']['stats']['stddev']
                users_rated = game_json_data['item']['stats']['usersrated']
                fans = game_json_data['item']['stats']['numfans']
                num_owned = game_json_data['item']['stats']['numowned']
                num_plays = game_json_data['item']['stats']['numplays']
                num_wish = game_json_data['item']['stats']['numwish']
                sub_type = game_json_data['item']['subtype']
                bg_name = game_json_data['item']['name']
                if game_json_data['item']['polls']['userplayers']['best']:
                    min_best_player = game_json_data['item']['polls']['userplayers']['best'][0]['min']
                    max_best_player = game_json_data['item']['polls']['userplayers']['best'][0]['max']
                    if min_best_player == 'null':
                        min_best_player = 0
                    if max_best_player == 'null':
                        max_best_player = 1000
                else:
                    min_best_player = 0
                    max_best_player = 0
                rank_point = game_json_data['item']['rankinfo'][0]['baverage']
                description = game_json_data['item']['description']
                image_url = game_json_data['item']['imageurl'].replace("\\", "/")
                image_url = image_url.replace("//", "/")
                image_url = image_url.replace("https", "http")
                bg_name = bg_name.replace("\\", "")
                bg_name = bg_name.replace("/", " and ")
                filename = bg_name.replace(" ", "") + ".jpg"
                r = requests.get(image_url, timeout=30)
                if r.status_code == 200:
                    with open("/Users/impala69/PycharmProjects/ghofliboardgame/public/media/" + filename, 'wb') as f:
                        f.write(r.content)

                new_bg = Boardgame(name=bg_name, min_players=int(min_player), max_players=int(max_player),
                                   min_best_players=int(min_best_player), max_best_players=int(max_best_player),
                                   min_age=int(min_age),
                                   weight=avg_weight, min_play_time=min_play_time, max_play_time=max_play_time,
                                   bg_image="./" + filename, description=description, bgg_code=int(bgg_code),
                                   stddev=float(stddev),
                                   users_rated=int(users_rated), fans=int(fans), num_owned=int(num_owned),
                                   num_plays=int(num_plays),
                                   num_wish=int(num_wish), sub_type=sub_type)
                new_bg.save()

                for bg_sub in game_json_data['item']['links']['boardgamesubdomain']:
                    bg_sub_name = bg_sub['name'].replace("\\", "")
                    # print(bg_sub_name)
                    our_type = Type.objects.get(name=bg_sub_name)
                    type_to_bg = TypeToBoardgame(type=our_type, boardgame=new_bg)
                    type_to_bg.save()

                for bg_cat in game_json_data['item']['links']['boardgamecategory']:
                    bg_cat_name = bg_cat['name'].replace("\\", "")
                    our_cat = Category.objects.get(name=bg_cat_name)
                    cat_to_bg = CategoryToBoardgame(category=our_cat, boardgame=new_bg)
                    cat_to_bg.save()

                for bg_mech in game_json_data['item']['links']['boardgamemechanic']:
                    bg_mech_name = bg_mech['name'].replace("\\", "")
                    our_mech = Mechanic.objects.get(name=bg_mech_name)
                    mech_to_bg = MechanicToBoardgame(mechanic=our_mech, boardgame=new_bg)
                    mech_to_bg.save()

                for bg_family in game_json_data['item']['links']['boardgamefamily']:
                    bg_family_name = bg_family['name'].replace("\\", "")
                    our_family = Family.objects.get(name=bg_family_name)
                    family_to_bg = FamilyToBoardgame(family=our_family, boardgame=new_bg)
                    family_to_bg.save()

                for bg_rank in game_json_data['item']['rankinfo']:
                    bg_rank_name = bg_rank['veryshortprettyname']
                    bg_rank_value = bg_rank['rank']
                    bg_rank_avg = bg_rank['baverage']
                    new_rank = Rank(rank_value=bg_rank_value, average=bg_rank_avg, rank_name=bg_rank_name,
                                    boardgame=new_bg)
                    new_rank.save()

                print(str(bgg_code) + " : " + str(bg_name))
    except Exception as e:
        print("Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrooooooooooooooooooooooooooooooorrrrrr: " + str(bgg_code))
        print(e)
    return HttpResponse("100 Done")


def enter_bgg_category(request):
    url = "https://boardgamegeek.com/browse/boardgamecategory"
    bgg_site_content = requests.get(url).content
    soup = BeautifulSoup(bgg_site_content, 'html.parser')
    table_content = soup.find("table", {"class": "forum_table"})
    items = table_content.find_all("tr")
    counter = 0
    for item in items:
        links = item.find_all("td")
        for link in links:
            cat = link.find("a")
            name = cat.text
            href = cat['href']
            counter += 1
            # new_cat = Category(name=name, href=href)
            # new_cat.save()
    return HttpResponse(counter)


def enter_bgg_mechanics(request):
    url = "https://boardgamegeek.com/browse/boardgamemechanic"
    bgg_site_content = requests.get(url).content
    soup = BeautifulSoup(bgg_site_content, 'html.parser')
    table_content = soup.find("table", {"class": "forum_table"})
    items = table_content.find_all("tr")
    counter = 0
    for item in items:
        links = item.find_all("td")
        for link in links:
            mech = link.find("a")
            if mech:
                name = mech.text
                href = mech['href']
                counter += 1
                # new_mech = Mechanic(name=name, href=href)
                # new_mech.save()
    return HttpResponse(counter)


def enter_bgg_family(request):
    counter = 0
    for i in range(1, 30):
        url = "https://boardgamegeek.com/browse/boardgamefamily/page/" + str(i)
        bgg_site_content = requests.get(url).content
        soup = BeautifulSoup(bgg_site_content, 'html.parser')
        table_content = soup.find("table", {"class": "forum_table"})
        items = table_content.find_all("tr")
        for item in items:
            links = item.find_all("td")
            for link in links:
                family = link.find_all("a")[1]
                if family:
                    name = family.text
                    href = family['href']
                    counter += 1
                    # new_family = Family(name=name, href=href)
                    # new_family.save()
        print(counter)
    return HttpResponse(counter)


def save_image(request):
    try:
        boardgames = Boardgame.objects.all().order_by("id")
        for i in range(8, len(boardgames)):
            boardgame = boardgames[i]
            print(boardgame)
            print("starting: " + str(i) + ": " + boardgame.name)
            bgg_content = requests.get(
                "https://api.geekdo.com/api/images?ajax=1&gallery=all&nosession=1&objectid=%s&objecttype=thing&pageid=%s&showcount=16&size=thumb&sort=hot" % (
                    str(boardgame.bgg_code), "1"),
                timeout=30)
            for image in bgg_content.json()['images']:
                image_id = image['imageid']
                image_url = image['imageurl_lg']
                image_cap = image['caption']
                filename = str(image_id) + ".jpg"
                new_img = Image(image="./" + filename, bgg_image_id=image_id, img_caption=image_cap,
                                boardgame=boardgame)
                r = requests.get(image_url, timeout=30)
                if r.status_code == 200:
                    with open("/Users/impala69/PycharmProjects/ghofliboardgame/public/media/" + filename, 'wb') as f:
                        f.write(r.content)
                        new_img.save()
                        print("Image Done: " + str(image_id))
                else:
                    print("Image Faiiiiiiiiiiiiiiiiiiiiiiiiiiiild: " + str(image_id))


    except Exception as e:
        print("Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrooooooooooooooooooooooooooooooorrrrrr: " + str(
            boardgame.bgg_code))
        print(e)
    return HttpResponse("100 Done")


def save_file(request):
    try:
        boardgames = Boardgame.objects.all().order_by("id")
        for i in range(0, len(boardgames)):
            boardgame = boardgames[i]
            print("starting: " + str(i) + ": " + boardgame.name)
            bgg_content = requests.get(
                "https://api.geekdo.com/api/files?ajax=1&languageid=0&nosession=1&objectid=%s&objecttype=thing&pageid=%s&showcount=25&sort=hot" % (
                    str(boardgame.bgg_code), "1"),
                timeout=30)
            for file in bgg_content.json()['files']:
                file_page_id = file['filepageid']
                file_id = file['fileid']
                file_desc = file['description']['rendered']
                file_title = file['title']
                file_name = file['filename']
                new_file = File(file_title=file_title, bgg_file_id=file_id, bgg_file_page_id=file_page_id,
                                file_desc=file_desc,
                                boardgame=boardgame, file_name=file_name)
                new_file.save()
                print("File Done: " + str(file_id))

    except Exception as e:
        print("Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrooooooooooooooooooooooooooooooorrrrrr: " + str(
            boardgame.bgg_code))
        print(e)
    return HttpResponse("100 Done")


def save_video(request):
    try:
        boardgames = Boardgame.objects.all().order_by("id")
        for i in range(0, len(boardgames)):
            boardgame = boardgames[i]
            print("starting: " + str(i) + ": " + boardgame.name)
            bgg_content = requests.get(
                "https://api.geekdo.com/api/videos?ajax=1&gallery=all&nosession=1&objectid=%s&objecttype=thing&pageid=%s&showcount=50&sort=recent" % (
                    str(boardgame.bgg_code), "1"),
                timeout=30)
            for video in bgg_content.json()['videos']:
                video_id = video['videoid']
                video_title = video['title']
                video_post_date = video['postdate']
                youtube_id = video['extvideoid']
                video_category = video['gallery']
                new_video = Video(video_title=video_title, bgg_video_id=video_id,
                                  video_category=video_category, youtube_video_id=youtube_id,
                                  boardgame=boardgame, video_post_date=video_post_date)
                new_video.save()
                print("video Done: " + str(video_id))

    except Exception as e:
        print("Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrooooooooooooooooooooooooooooooorrrrrr: " + str(
            boardgame.bgg_code))
        print(e)
    return HttpResponse("100 Done")


def save_expansion(request):
    try:
        boardgames = Boardgame.objects.all().order_by("id")
        for i in range(4, len(boardgames)):
            boardgame = boardgames[i]
            print("starting: " + str(i) + ": " + boardgame.name)
            bgg_content = requests.get(
                "https://api.geekdo.com/api/geekitem/linkeditems?ajax=1&linkdata_index=boardgameexpansion&nosession=1&objectid=%s&objecttype=thing&pageid=%s&showcount=25&sort=yearpublished&subtype=boardgameexpansion" % (
                    str(boardgame.bgg_code), "1"),
                timeout=30)
            for expansion in bgg_content.json()['items']:
                exp_id = expansion['objectid']
                exp_name = expansion['name']
                exp_image_url = expansion['images']['previewthumb']
                exp_image_name = str(exp_id) + ".jpg"
                new_exp = Expansion(expansion_name=exp_name, expansion_image="./" + exp_image_name,
                                    expansion_bgg_id=exp_id, boardgame=boardgame)
                r = requests.get(exp_image_url, timeout=30)
                if r.status_code == 200:
                    with open("/Users/impala69/PycharmProjects/ghofliboardgame/public/media/" + exp_image_name,
                              'wb') as f:
                        f.write(r.content)
                        new_exp.save()
                        print("Expansion Done: " + str(exp_id))

    except Exception as e:
        print("Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrooooooooooooooooooooooooooooooorrrrrr: " + str(
            boardgame.bgg_code))
        print(e)
    return HttpResponse("100 Done")


def save_forum(request):
    try:
        boardgames = Boardgame.objects.all().order_by("id")
        for i in range(0, len(boardgames)):
            boardgame = boardgames[i]
            print("starting: " + str(i) + ": " + boardgame.name)
            bgg_content = requests.get(
                "https://api.geekdo.com/api/forums/threads?ajax=1&filterforums=194&forumid=0&nosession=1&objectid=%s&objecttype=thing&pageid=%s&showcount=100&sort=hot" % (
                    str(boardgame.bgg_code), "1"),
                timeout=30)
            for forum in bgg_content.json()['threads']:
                forum_id = forum['threadid']
                forum_title = forum['subject']
                forum_cat = forum['forumtitle']
                new_forum = Forum(forum_title=forum_title, bgg_forum_id=forum_id, forum_category=forum_cat,
                                  boardgame=boardgame)
                new_forum.save()
                print("Forum Done: " + str(forum_id))

    except Exception as e:
        print("Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrooooooooooooooooooooooooooooooorrrrrr: " + str(
            boardgame.bgg_code))
        print(e)
    return HttpResponse("100 Done")


def save_credits(request):
    try:
        boardgames = Boardgame.objects.all().order_by("id")
        for i in range(0, len(boardgames)):
            boardgame = boardgames[i]
            print("starting: " + str(i) + ": " + boardgame.name)
            bgg_content = requests.get(
                "https://api.geekdo.com/api/geekitems?nosession=1&objectid=%s&objecttype=thing&subtype=boardgame" % (
                    str(boardgame.bgg_code)),
                timeout=30)
            year = bgg_content.json()['item']['yearpublished']
            for designer in bgg_content.json()['item']['links']['boardgamedesigner']:
                designer_name = designer['name']
                designer_code = designer['objectid']
                new_designer = Credit(credit_bgg_id=designer_code, credit_kind="DESIGNER", credit_title=designer_name,
                                      boardgame=boardgame)
                new_designer.save()
                print("Designer Done: " + str())

            for artist in bgg_content.json()['item']['links']['boardgameartist']:
                artist_name = artist['name']
                artist_code = artist['objectid']
                new_artist = Credit(credit_bgg_id=artist_code, credit_kind="ARTIST", credit_title=artist_name,
                                    boardgame=boardgame)
                new_artist.save()
                print("Artist Done: " + str())

            for pub in bgg_content.json()['item']['links']['boardgamepublisher']:
                pub_name = pub['name']
                pub_code = pub['objectid']
                new_pub = Credit(credit_bgg_id=pub_code, credit_kind="PUBLISHER", credit_title=pub_name,
                                 boardgame=boardgame)
                new_pub.save()
                print("Publisher Done: " + str())

            boardgame.year_published = year
            boardgame.save()
            break
    except Exception as e:
        print("Errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrooooooooooooooooooooooooooooooorrrrrr: " + str(
            boardgame.bgg_code))
        print(e)
    return HttpResponse("100 Done")


def register(request):
    if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
        return redirect("/")
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['repassword']
        if re_password == password:
            password_hashed = make_password(password)
            new_user = User(username=username, email=email, password=password_hashed)
            new_user.save()

    return render(request, "register.html")


def login(request):
    if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
        return redirect("/")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        my_user_username = User.objects.filter(username=username)
        my_user_email = User.objects.filter(email=username)
        if my_user_email.count() == 1:
            password_real = my_user_email[0].password
            if check_password(password, password_real):
                return redirect("/")
            else:
                return HttpResponse("Wrong Pass or Email")
        elif my_user_username.count() == 1:
            password_real = my_user_username[0].password
            if check_password(password, password_real):
                request.session['is_logged_in'] = True
                request.session['username'] = username
                return redirect("/")
            else:
                return HttpResponse("Wrong Pass or Username")
        else:
            return HttpResponse("Wrong Pass or Username")
    return render(request, "login.html")


def logout(request):
    if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
        request.session['is_logged_in'] = False
        request.session['username'] = 0
        return redirect("/login")
    return redirect("/login")


def get_current_user(request):
    if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
        username = request.session['username']
        user = {"username": username}
        return JsonResponse(user)
    return JsonResponse({"username": 0})


def get_bg_likes(request):
    if request.method == "GET":
        bgg_code = request.GET['bgg_code']
        boardgame = Boardgame.objects.get(bgg_code=bgg_code)
        bg_likes = UserLikes.objects.filter(boardgame=boardgame).count()
        return JsonResponse({"bg_likes": bg_likes})


def like_bg(request):
    if request.method == "GET":
        bgg_code = request.GET['bgg_code']
        boardgame = Boardgame.objects.get(bgg_code=bgg_code)
        if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
            username_session = request.session['username']
            username = User.objects.get(username=username_session)
            old_like = UserLikes.objects.filter(boardgame=boardgame, username=username)
            if old_like.count() == 0:
                user_like = UserLikes(boardgame=boardgame, username=username)
                user_like.save()
                return JsonResponse({"success": 1})
            else:
                old_like.delete()

    return JsonResponse({"success": 0})


def get_user_bg_data(request):
    if request.method == "GET":
        bgg_code = request.GET['bgg_code']
        boardgame = Boardgame.objects.get(bgg_code=bgg_code)
        if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
            username_session = request.session['username']
            username = User.objects.get(username=username_session)
            is_old_like = UserLikes.objects.filter(boardgame=boardgame, username=username).count()
            is_old_wish = UserWishes.objects.filter(boardgame=boardgame, username=username).count()
            is_old_has = UserHas.objects.filter(boardgame=boardgame, username=username).count()
            user_rate = UserRates.objects.filter(boardgame=boardgame, username=username)
            if user_rate.count() == 0:
                user_rate_num = 0
            else:
                user_rate_num = user_rate[0].rate
            return JsonResponse(
                {"is_user_like_bg": is_old_like, "is_user_wish_bg": is_old_wish, "is_user_has_bg": is_old_has,
                 'bg_rate_from_user': user_rate_num, 'success': 1})
        else:
            return JsonResponse({'success': 0})


def wish_bg(request):
    if request.method == "GET":
        bgg_code = request.GET['bgg_code']
        boardgame = Boardgame.objects.get(bgg_code=bgg_code)
        if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
            username_session = request.session['username']
            username = User.objects.get(username=username_session)
            old_wish = UserWishes.objects.filter(boardgame=boardgame, username=username)
            if old_wish.count() == 0:
                user_wish = UserWishes(boardgame=boardgame, username=username)
                user_wish.save()
                return JsonResponse({"success": 1})
            else:
                old_wish.delete()

    return JsonResponse({"success": 0})


def has_bg(request):
    if request.method == "GET":
        bgg_code = request.GET['bgg_code']
        boardgame = Boardgame.objects.get(bgg_code=bgg_code)
        if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
            username_session = request.session['username']
            username = User.objects.get(username=username_session)
            old_has = UserHas.objects.filter(boardgame=boardgame, username=username)
            if old_has.count() == 0:
                user_has = UserHas(boardgame=boardgame, username=username)
                user_has.save()
                return JsonResponse({"success": 1})
            else:
                old_has.delete()

    return JsonResponse({"success": 0})


def rate_bg(request):
    if request.method == "GET":
        bgg_code = request.GET['bgg_code']
        rate_number = request.GET['rate']
        boardgame = Boardgame.objects.get(bgg_code=bgg_code)
        if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
            username_session = request.session['username']
            username = User.objects.get(username=username_session)
            old_rate = UserRates.objects.filter(boardgame=boardgame, username=username)
            print(old_rate)
            if old_rate.count() == 0:
                user_rate = UserRates(boardgame=boardgame, username=username, rate=int(rate_number))
                user_rate.save()
                return JsonResponse({"success": 1})
            else:
                old_rate_obj = UserRates.objects.get(boardgame=boardgame, username=username)
                old_rate_obj.rate = int(rate_number)
                old_rate_obj.save()

    return JsonResponse({"success": 0})


def profile(request):
    if request.session.has_key("is_logged_in") and request.session['is_logged_in']:
        username_session = request.session['username']
        username = User.objects.get(username=username_session)
        user_wishes = UserWishes.objects.filter(username=username)
        user_hases = UserHas.objects.filter(username=username)
        user_likes = UserLikes.objects.filter(username=username)
        user_rates = UserRates.objects.filter(username=username).order_by("-rate")
        user_data = {"wishes": user_wishes, "likes": user_likes, "hases": user_hases, "rates": user_rates}
        return render(request, "profile.html", {"userdata": user_data})
    else:
        return redirect("/login")