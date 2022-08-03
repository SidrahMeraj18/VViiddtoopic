from platform import uname_result
from django.shortcuts import redirect, render
from .models import AuthUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from uuid import uuid1
from django.core.mail import send_mail
from django.conf import settings
from icecream import ic
def display_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if "signup" in request.POST:
            if request.POST["name"] not in [i.name for i in AuthUser.objects.all()]:
                if request.POST["email"] not in [i.email for i in AuthUser.objects.all()]:
                    if len(request.POST["password"])>= 8: 
                        USER = User.objects.create_user(
                                    username=request.POST["name"],
                                    password=request.POST["password"],
                                    email=request.POST["email"]
                                )
                        AuthUser.objects.create(
                            name=request.POST["name"],
                            email=request.POST["email"],
                            user = USER
                        )
                        login(request, USER)
                        return redirect("home")
                    else:
                        messages.success(request,"Password should be greater than 8 characters", extra_tags="signup")
                else:
                    messages.success(request,"Email Id already exists", extra_tags="signup")
            else:
                messages.success(request,"Username is already taken by another user ", extra_tags="signup")

        elif "login" in request.POST:
            uname=request.POST["name"]
            password=request.POST["password"]
            user = authenticate(request, username=uname, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.success(request,"Username or Password is incorrect", extra_tags="login")
        return render(request, 'login.html', {})
def logout_view(request):
    logout(request)
    return redirect("home")
verification_code = ""
the_email_id = ""
def set_verif_code(code):
    global verification_code
    verification_code = code
def set_email_id(email):
    global the_email_id
    the_email_id = email
def forgot_pass(request):
    ic(verification_code)
    if "reset-pass" in request.POST:
        emaild_id = request.POST.get("email")
        if emaild_id in [i.email for i in AuthUser.objects.all()]:
            set_verif_code(str(uuid1())[:5])
            set_email_id(request.POST["email"])
            username = [i for i in AuthUser.objects.all() if i.email == request.POST["email"]][0]
            mail_content = f"""Hello {username.name},
    Your VidToPick Password Reset verification Code is {verification_code}


    --
    Regards,
    Team VidToPick

                        """
            messages.success(request,"Password reset link has been sent to your email", extra_tags="password-reset")
            send_mail('VidtoPick Password Reset', mail_content, settings.EMAIL_HOST_USER, [emaild_id])
        else:
            messages.success(request, "There is No Account Associated with this Email Id", extra_tags="no-email")
    elif "verify-code" in request.POST:
        if request.POST["verification-code"] == verification_code:
            messages.success(request, "Verification Code is Correct", extra_tags="correct-code")
        else:
            messages.success(request, "Verification Code is Incorrect", extra_tags="wrong-code")
    elif "reset-password" in request.POST:
        if request.POST["password1"] == request.POST["password2"]:
            username = [i for i in AuthUser.objects.all() if i.email == the_email_id][0]
            user = User.objects.get(username=username.name)
            user.set_password(request.POST["password1"])
            user.save()
            messages.success(request, "Password has been reset", extra_tags="password-reset")
            auth = authenticate(request, username=username.name, password=request.POST["password1"])
            login(request, auth)
            return redirect("home")
        else:
            messages.success(request, "Password and Confirm Password are not same", extra_tags="password-incorrect")
    return render(request, 'forgot_pass.html', {})
def profile_view(request):
    user = request.user.authuser
    return render(request, 'profile.html', {"user":user})
def edit_profile_view(request):
    user = request.user.authuser
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        if username != user.name:
            if username not in [i.name for i in AuthUser.objects.all()]:
                user.name = username
            else:
                messages.success(request,"Username is already taken by another user ", extra_tags="username")
        if email != user.email:
            if email not in [i.email for i in AuthUser.objects.all()]:
                user.email = email
            else:
                messages.success(request,"Email Id already exists", extra_tags="email")
        user.save()
        messages.success(request,"Profile has been updated", extra_tags="edit-profile")
        return render(request, 'edit_profile.html', {"user":user})
    return render(request, "edit_profile.html", {"user":user})
def change_password_view(request):
    user = request.user.authuser
    if request.method == "POST":
        if request.user.check_password(request.POST["old-password"]):
            if request.POST["new-password"] == request.POST["confirm-new-password"]:
                user.user.set_password(request.POST["new-password"])
                user.user.save()
                user.save()
                auth = authenticate(request, username=user.name, password=request.POST["new-password"])
                login(request, auth)
                messages.success(request, "Password has been changed", extra_tags="password-changed")
                return redirect("profile")
            else:
                messages.success(request, "New Password and Confirm Password are not same", extra_tags="password-incorrect2")
        else:
            messages.success(request, "Old Password is incorrect", extra_tags="password-incorrect1")
    return render(request, "change_password.html", {"user":user.name})
def history_view(request):
    objs = request.user.authuser.srtgen_set.all()
    context={"objs":objs}
    return render(request,"history.html",context)
def favourites_view(request):
    objs = request.user.authuser.favourites_set.all()
    context={"objs":objs}
    return render(request,"favourites.html",context)