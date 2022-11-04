from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect

from .tools import ipfs_upload
from .contractcalls import add_user, add_club, add_post

from .models import Club, User, Post, Comment

# Create your views here.


def connection_check(request):
    return HttpResponse("Working.")


@api_view(["POST"])
def check_club_name(request):
    club_name = request.data["name"]
    if Club.objects.filter(name=club_name).exists():
        club = Club.objects.filter(name=club_name).first()
        club_data = model_to_dict(club)
        return Response({"status": "Success", "data": club_data})
    else:
        return Response({"status": "Failed"})


@api_view(["POST"])
def create_club(request):
    print(request)
    name = request.data["name"]
    description = request.data["description"]
    category = request.data["category"]
    profilepic = request.data["profilepic"]
    admin = request.data["admin"]
    profilepic_url = ipfs_upload(profilepic)
    if Club.objects.filter(name=name).exists():
        club = Club.objects.filter(name=name).first()
        club_data = model_to_dict(club)
        return Response({"status": "Failed", "data": club_data})
    else:
        add_club(
            name,
            description,
            profilepic_url,
            category,
            admin
        )
        Club.objects.create(name=name,
                            description=description,
                            profilepic=profilepic_url,
                            category=category,
                            members=1, admin=admin)
        club = Club.objects.filter(name=name).first()
        club_data = model_to_dict(club)
        return Response({"status": "Success", "data": club_data})


@api_view(['POST'])
def get_user_data(request):
    account = request.data['account']
    if not User.objects.filter(account=account).exists():
        default_pic = "https://s.yimg.com/ny/api/res/1.2/W_MhFStkWMQrj6QSq3.D3A--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTY0MA--/https://s.yimg.com/uu/api/res/1.2/jvHNRMbOHkjVvCfisU_GVw--~B/aD04MDA7dz04MDA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/accesswire.ca/a8c86bdb6bb6d08e3f525f2d56816f55"
        add_user(account, 'Unnamed', "No description", default_pic)
        User.objects.create(account=account, name="Unnamed",
                            description="No description", profilepic=default_pic)

    user = User.objects.filter(account=account).first()
    user_data = model_to_dict(user)
    return Response({"status": "Success", "data": user_data})


@api_view(['POST'])
def edit_user_data(request):
    name = request.data['name']
    account = request.data['account']
    description = request.data['description']
    profilepic = request.data['profilepic']
    profilepic_url = ipfs_upload(profilepic)
    if not User.objects.filter(account=account).exists():
        add_user(account, name, description, profilepic_url)
        User.objects.create(account=account, name=name,
                            description=description, profilepic=profilepic_url)
    else:
        user = User.objects.filter(account=account).first()
        user.name = name
        user.description = description
        user.profilepic = profilepic_url
        add_user(account, name, description, profilepic_url)
        user.save()
    return Response({"status": "Success"})


@api_view(['POST'])
def get_clubs(request):
    myClubs = Club.objects.all()
    myclubsdata = []
    for club in myClubs:
        thisclub = model_to_dict(club)
        myclubsdata.append(thisclub)
    return Response({"status": "Success", "data": myclubsdata})


@api_view(["POST"])
def get_clubs_number(request):
    response_data = {
        "🌐 Web3": Club.objects.filter(category="🌐 Web3").count(),
        "🪐 Metaverse": Club.objects.filter(category="🪐 Metaverse").count(),
        "🏦 DeFi": Club.objects.filter(category="🏦 DeFi").count(),
        "🎮 GameFi": Club.objects.filter(category="🎮 GameFi").count(),
        "💖 SocialFi": Club.objects.filter(category="💖 SocialFi").count(),
        "🖼 NFT": Club.objects.filter(category="🖼 NFT").count(),
        "🗳️ DAO": Club.objects.filter(category="🗳️ DAO").count(),
        "⚡ Layer2": Club.objects.filter(category="⚡ Layer2").count(),
        "🔐 Crypto": Club.objects.filter(category="🔐 Crypto").count(),
        "💩 Meme": Club.objects.filter(category="💩 Meme").count(),
        "🏷️ Others": Club.objects.filter(category="🏷️ Others").count(),
    }
    return Response({"status": "Success", "data": response_data})


@api_view(["POST"])
def get_club_data(request):
    clubId = request.data["clubId"]
    club = Club.objects.get(pk=clubId)
    club_data = model_to_dict(club)
    return Response({"status": "Success", "data": club_data})


@api_view(["POST"])
def get_club_posts(request):
    clubId = request.data["clubId"]
    posts = list(Post.objects.filter(club=clubId))
    post_data = []
    for post in posts:
        mypost = model_to_dict(post)
        post_data.append(mypost)
    return Response({"status": "Success", "data": post_data})


@api_view(["POST"])
def create_post(request):
    content = request.data["content"]
    clubId = int(request.data["clubId"])
    posted_by = request.data["postedBy"]
    add_post(content,
             clubId,
             posted_by)
    Post.objects.create(content=content, club=clubId, posted_by=posted_by)
    return Response({"status": "Success"})


@api_view(["POST"])
def get_my_posts(request):
    account = request.data["account"]
    myposts = []
    posts = list(Post.objects.filter(posted_by=account))
    for post in posts:
        myposts.append(model_to_dict(post))
    return Response({"status": "Success", "data": myposts})


@api_view(["POST"])
def get_my_clubs(request):
    account = request.data["account"]
    myclubs = []
    clubs = list(Club.objects.filter(admin=account))
    for club in clubs:
        myclubs.append(model_to_dict(club))
    return Response({"status": "Success", "data": myclubs})


@api_view(["POST"])
def create_comment(request):
    clubId = int(request.data["clubId"])
    postId = int(request.data["postId"])
    commented_by = request.data["commented_by"]
    comment = request.data['comment']
    Comment.objects.create(club=clubId, postId=postId,
                           commented_by=commented_by, comment=comment)
    return Response({"status": "Success"})


@api_view(["POST"])
def get_post_comments(request):
    clubId = request.data["clubId"]
    postId = request.data["postId"]
    comments = list(comments.objects.filter(clubId=clubId, postId=postId))

    comment_data = []

    for comment in comments:
        mycomment = model_to_dict(comment)
        comment_data.append(mycomment)
    return Response({"status": "Success", "data": comment_data})


def PostLike(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return Response({"status": "Success"})