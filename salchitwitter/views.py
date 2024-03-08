from django.shortcuts import render, redirect
from .models import Profile, Salchitweet
from .forms import TweetForm

def dashboard(request):
    form = TweetForm(request.POST or None)
    # we add the functionality after pressing the button in the html form in dashboard
    if request.method == 'POST':
        # if the info comes from GET method it will jump to form = TweeForm and to render
        # we will fill the TweetForm in models with the data coming with POST request
        # or None is to avoid that if it is bigger than 140 the message will fail. To send the bound form to the
        # template if a validation error occurs we need or None. Or is a short circuit operator. Only evaluates the
        # second arguement if the first one is False
        if form.is_valid():
            tweet = form.save(commit=False)  # we are preventing to commit to the database yet, because is left the user entry
            tweet.user = request.user  # we pick the current logged user
            tweet.save()  # it will do the commit to the database
            return redirect("salchitwitter:dashboard")  # to prevent sending again if in cache, meaning app: url path
    
    followed_tweets = Salchitweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()).order_by("-created_at")
    """.filte() on Salchitweet object, which allows us to pick particular tweet object from the table depending on field lookups.
        We save the output of this call to followed_tweets.
        First we define the queryset field lookup (line 19), which is Django ORM syntax for the main part of an SQL WHERE clasue.
        We can follow through database relations with a double-underscore syntax(__) specific to Django ORM. We write
        user__profile__ in to access the profile of a user and see whether that profile is in a collection that we will
        pass as the value to your field lookup keyword argument.
        In the second part of the line we provide the field lookup. Needs to be a queryset object containing profile objects.
        we can fetch the relevant profiles from our database by accessing all profile objects in. follows of the currently
        logged-in user's profile (request.user.profile)
    """
    
    return render(request, "salchitwitter/dashboard.html", {"form": form, "tweets":followed_tweets}, )
    # the dictionary is to pass the info to the html file under the key form
    # the new part of the dictionary pass the followed_tweets cotaining a queryset object of all the tweets of all the
    # profiles the current user follows, ordered by the newest tweet first. We're passing it to our template under the 
    # key name tweets.

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    # it is uesed django's object-relational mapper(ORM) to retrieve objects from our profile table and
    # store them in profiles. We want to get all user profiles except for our own, which we accomplish with
    # .exclude()
    return render(request, "salchitwitter/profile_list.html", {"profiles": profiles})
    # we render a context dictionary that contains 'profiles', we will get them from the db.sqlite3
    
    
def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        # The arguments are an object and a string. The result is True if the string is the name of one of the
        # object's attributes, False if not.
        # When you call the profile view, you first check whether request.user contains profile with hasattr().
        # If the profile is missing, then you create a profile for your user before proceeding.
        missing_profile = Profile(user=request.user)
        missing_profile.save()
        
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile # using the user attribute form Django's request object, which
        # refers to the current_user_profile.
        data = request.POST
        # we get the user-submitted data from the request.POST dictionary and sotre it in data.
        action = data.get("follow")
        # we retrieve the data 
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "salchitwitter/profile.html", {"profile": profile})