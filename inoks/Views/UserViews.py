from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from education.Forms.UserForm import UserForm
from inoks.Forms.ProfileForm import ProfileForm
from inoks.Forms.ProfileUpdateForm import ProfileUpdateForm
from inoks.Forms.ProfileUpdateMemberForm import ProfileUpdateMemberForm
from inoks.Forms.UserUpdateForm import UserUpdateForm
from inoks.models import Profile
from inoks.serializers.profile_serializers import ProfileSerializer
from inoks.services import general_methods
from inoks.services.general_methods import activeUser, passiveUser, reactiveUser


@login_required
def return_add_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    profile_form = ProfileForm()

    if request.method == 'POST':
        x = User.objects.latest('id')

        data = request.POST.copy()
        data['username'] = data['email']
        user_form = UserForm(data)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            group = Group.objects.get(name='Üye')
            user2 = user_form.save()
            password = User.objects.make_random_password()
            user.set_password(password)
            user2.groups.add(group)
            user.is_active = True
            user.save()

            profil = Profile(user=user, tc=profile_form.cleaned_data['tc'],
                             profileImage=profile_form.cleaned_data['profileImage'],
                             address=profile_form.cleaned_data['address'],
                             gender=profile_form.cleaned_data['gender'],
                             job=profile_form.cleaned_data['job'],
                             city=profile_form.cleaned_data['city'],
                             educationLevel=profile_form.cleaned_data['educationLevel'],
                             mobilePhone=profile_form.cleaned_data['mobilePhone'],
                             birthDate=profile_form.cleaned_data['birthDate'],
                             district=profile_form.cleaned_data['district'],
                             sponsor=profile_form.cleaned_data['sponsor'],
                             iban=profile_form.cleaned_data['iban'],
                             ibanAdSoyad=profile_form.cleaned_data['ibanAdSoyad'])
            profil.sponsor = profile_form.cleaned_data['sponsor']
            profil.isContract = profile_form.cleaned_data['isContract']
            profil.isApprove = True
            profil.isActive = True
            #sponsorNumber = Profile.objects.filter(sponsor=profile_form.cleaned_data['sponsor']).count()
            sponsorNumber = Profile.objects.filter(sponsor=profile_form.cleaned_data['sponsor']).filter(isActive=True).count()
            sp_profile = Profile.objects.get(pk=profile_form.cleaned_data['sponsor'].pk)

            if sp_profile.user.groups.all()[0].name == 'Admin':
                limit = 9
            else:
                limit = 2

            if sponsorNumber > limit:
                messages.warning(request, 'Üyeye Sponsor Eklenemez. Sponsor Alanı Dolmuştur.')
                return redirect('inoks:kullanici-ekle')
            else:
                profil.save()

                subject, from_email, to = 'BAVEN Kullanıcı Giriş Bilgileri', 'info@baven.net', user2.email
                text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
                html_content = '<p> <strong>Site adresi:</strong> <a href="https://network.baven.net">network.baven.net</a></p>'
                html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
                html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, 'Üye Başarıyla Kayıt Edilmiştir.')

                return redirect('inoks:kullanici-ekle')

        else:
            isExist = general_methods.existMail(data['email'])
            if isExist:
                messages.warning(request, 'Mail adresi başka bir üyemiz tarafından kullanılmaktadır.')

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-ekle.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def users_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    user = User.objects.get(id=pk)

    user_form = UserUpdateForm(request.POST or None, instance=user)
    profile = Profile.objects.get(user=user)
    profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':

        if user_form.is_valid() and profile_form.is_valid():

            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.username = user_form.cleaned_data['email']
            user.is_active = True
            user.save()
            profile_form.save()

            messages.success(request, 'Profil Bilgileriniz Başarıyla Güncellenmiştir.')
            return redirect('inoks:user-dashboard')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-ekle.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'ilce': profile.district})


@login_required
def users_information(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    user = User.objects.get(pk=pk)

    user_form = UserUpdateForm(request.POST or None, instance=user)
    profile = Profile.objects.get(user=user)
    profile_form = ProfileUpdateMemberForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':

        if user_form.is_valid() and profile_form.is_valid():

            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.is_active = True
            user.save()
            profile_form.save()

            messages.success(request, 'Profil Bilgileriniz Başarıyla Güncellenmiştir.')
            return redirect('inoks:user-dashboard')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-bilgileri.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'ilce': profile.district})


@login_required
def return_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    users = Profile.objects.filter(user__is_active=True).filter(~Q(user__groups__name='Admin'))

    return render(request, 'kullanici/kullanicilar.html', {'users': users})


@login_required
def send_information(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = User.objects.get(pk=pk)
    password = User.objects.make_random_password()
    user.set_password(password)
    user.save()

    subject, from_email, to = 'Baven Kullanıcı Giriş Bilgileri', 'info@baven.net', user.email
    text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
    html_content = '<p> <strong>Site adresi:</strong> <a href="https://network.bavev.net"></a>network.baven.net</p>'
    html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user.username + '</p>'
    html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return render(request, 'kullanici/kullanici-bilgi.html', {'password': password, 'username': user.username})


@login_required
def return_my_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    userprofile = Profile.objects.get(user=current_user)

    users = Profile.objects.filter(sponsor_id=userprofile.id, isApprove=True)

    return render(request, 'kullanici/uyelerim.html', {'users': users})


@login_required
def return_pending_users(request):
    if request.user.groups.all()[0] != Group.objects.get(name="Admin"):
        logout(request)
        return redirect('accounts:login')
    users = Profile.objects.filter(isApprove=False)

    return render(request, 'kullanici/bekleyen-kullanicilar.html', {'users': users})


@api_view()
def getPendingProfile(request, pk):
    profile = Profile.objects.filter(pk=pk)

    data = ProfileSerializer(profile, many=True)

    responseData = {}
    responseData['profile'] = data.data
    responseData['profile'][0]
    return JsonResponse(responseData, safe=True)


@api_view()
def getAllProfile(request, pk):
    profile = Profile.objects.filter(pk=pk)

    data = ProfileSerializer(profile, many=True)

    responseData = {}
    responseData['profile'] = data.data
    responseData['profile'][0]
    return JsonResponse(responseData, safe=True)


@api_view()
def getDeactiveProfile(request, pk):
    profile = Profile.objects.filter(pk=pk)

    data = ProfileSerializer(profile, many=True)

    responseData = {}
    responseData['profile'] = data.data
    responseData['profile'][0]
    return JsonResponse(responseData, safe=True)


@login_required
def profile_active_passive(request):
    if request.POST:
        try:

            user_id = request.POST.get('user_id')

            activeUser(request, int(user_id))

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def profile_reactive(request):
    if request.POST:
        try:

            user_id = request.POST.get('user_id')

            reactiveUser(request, int(user_id))

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def profile_passive(request):
    if request.POST:
        try:

            user_id = request.POST.get('user_id')

            passiveUser(request, int(user_id))

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def pending_profile_delete(request, pk):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Profile.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def return_deactive_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    users = Profile.objects.filter(isActive=False)

    return render(request, 'kullanici/iptal-edilen-kullanicilar.html', {'users': users})
