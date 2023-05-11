from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpRequest

from api.views import *


def home(request):
    return HttpResponse("<h1>Hey this is a home page</h1>")


def search_paper(request):

    papers = {}
    if request.method == "POST":  # if the search button clicked
        database = request.POST.get("database")
        query = request.POST.get("search_paper")
        rows = request.POST.get("rows")
        search_request = HttpRequest()
        search_request.method = 'POST'
        search_request.user = request.user
        search_request.META = request.META
        search_request.session = request.session
        search_request.GET.update({"title": query, "rows": rows})
        if database == "semantic_scholar":
            response = semantic_scholar(search_request)
        elif database == "eric_papers":
            response = eric_papers(search_request)
        elif database == "zenodo":
            response = zenodo(search_request)
        elif database == "doaj":
            response = doaj_get(search_request)
        elif database == "google_scholar":
            response = google_scholar(search_request)
        elif database == "core":
            response = core_get(search_request)
        papers = json.loads(response.content.decode()).get('results')
    context = {'page': 'Search Paper', 'warning': "","papers": papers}
    return render(request, "pages/search_paper.html", context)


def search_user(request):
    context = {'page': 'Search User'}
    return render(request, "pages/search_user.html", context)

def sign_up(request):
    # warning will be used to warn the user if the credentials are invalid or for any other warning
    context = {'page': 'Sign Up', 'warning': ""}

    if request.user.is_authenticated:  # if the user is authenticated, then redirect to search paper page
        return redirect("/search_paper/")

    if request.method == "POST":  # if the sign in button clicked
        username = request.POST.get("user_name")
        password = request.POST.get("password")

        #create a request to call user_registration
        signup_request = HttpRequest()
        signup_request.method = 'POST'
        signup_request.user = request.user
        signup_request.META = request.META
        signup_request.session = request.session
        signup_request.headers = {"username": username, "password": password}
        signup_response = user_registration(signup_request)

        if signup_response.status_code == 200:  # if the user is created, redirect to  sign in page
            return redirect("/sign_in/")
        else:
            context["warning"] = "Invalid credentials!"  # if not registered
    return render(request, "pages/sign_up.html", context)

def sign_in(request):
    # uncomment below and get sign_in page before testing.
    # this is necessary until a user is created
    # after the user is created, comment them again
    """r_username = "omari"
    r_password = "123456"
    User.objects.create_user(
        username=r_username, password=r_password, first_name="nam", last_name="surname")"""

    # warning will bi used to warn the user if the credentials are invaild or for any other warning
    context = {'page': 'Sign In', 'warning': ""}
    if request.user.is_authenticated:  # if the user is authenticated, then redirect to search paper page
        return redirect("/search_paper/")

    if request.method == "POST":  # if the sign in button clicked
        username = request.POST.get("user_name")
        password = request.POST.get("password")

        login_request = HttpRequest()
        login_request.method = 'POST'
        login_request.user = request.user
        login_request.META = request.META
        login_request.session = request.session
        login_request.headers = {"username": username, "password": password}
        login_response = log_in(login_request)

        if login_response.status_code == 200:  # if the user is registered, redirect to search paper page
            return redirect("/search_paper/")
        else:
            context["warning"] = "Invalid credentials!"  # if not registered

    return render(request, "pages/sign_in.html", context)


def profile_page(request):
    context = {'page': 'Profile Page'}
    return render(request, "pages/profile_page.html", context)


def my_lists(request):
    papers = [
        {'title': '<PAPER TITLE1>', 'abstract': "<ABSTRACT1>", 'year': 2000},
        {'title': '<PAPER TITLE2>', 'abstract': "<ABSTRACT2>", 'year': 2001},
        {'title': '<PAPER TITLE3>', 'abstract': "<ABSTRACT3>", 'year': 2002},
        {'title': '<PAPER TITLE4>', 'abstract': "<ABSTRACT4>", 'year': 2003},
    ]
    context = {'page': 'My Lists', "papers": papers}
    return render(request, "pages/my_lists.html", context)


def following_lists(request):
    lists = [
        'list1',
        'list2',
        'list3',
        'list4',
    ]
    context = {'page': 'Following Lists', 'lists': lists}
    return render(request, "pages/following_lists.html", context)


def list_content(request):
    context = {'page': 'List Content'}
    return render(request, "pages/list_content.html", context)


def paper_content(request):
    context = {'page': 'Paper content'}
    return render(request, "pages/paper_content.html", context)


def follow_requests(request):
    reqs = [
        {'sender': 'NAME1'},
        {'sender': 'NAME2'},
        {'sender': 'NAME3'},
        {'sender': 'NAME4'}
    ]
    context = {'page': 'Follow Requests', 'follow_requests': reqs}
    return render(request, "pages/follow_requests.html", context)
