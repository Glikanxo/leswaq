from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from account.models import *
from core.models import *
from django.http import JsonResponse
import string
import random
from datetime import date

def registration_view(request):
	context = {}

	if request.user.is_authenticated:
		return redirect('core:index')
	if request.POST:
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(username=username, password=raw_password)
			login(request,account)
			return redirect('core:index')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'register.html', context)

def child_registration_view(request):
	context = {}

	if not request.user.is_authenticated:
		return redirect('core:index')
	if request.POST:
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			Enfant.objects.create(parent=request.user,child=Account.objects.get(username=username))
			MiseANiveau.objects.create(attributed=True,
											account=Account.objects.get(username=username),
											mode='kid',
											duree='1',
											date_attribution=date.today())
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(username=username, password=raw_password)
			login(request,account)
			return redirect('core:index')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'child_registration.html', context)

def logout_view(request):
	logout(request)
	return redirect('core:index')

def login_view(request):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect('core:index')
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			try:
				user = authenticate(username=Account.objects.get(email=username),password=password)
			except:
				user = authenticate(username=username,password=password)
			if user:
				login(request,user)
				return redirect('core:index')
	else:
		form = AccountAuthenticationForm()
	context['login_form'] = form
	return render(request,'login.html', context)

def profile(request):
	if request.user.is_authenticated:
		template = 'profil.html'
		account = Account.objects.get(username=request.user.username)
		mode = 'aucun'
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			mode = MiseANiveau.objects.filter(attributed=True,account=request.user)[0].mode
		if 'editpp' in request.POST:
			account.profile_pic = request.FILES.get('imgco')
			account.save()
			return redirect('account:profil')

		if mode == 'aucun':
			securite = 'moyenne'
			if Signal.objects.filter(post__creator=request.user,decision='accepté'):
				if Signal.objects.filter(post__creator=request.user,decision='accepté').count() >= 3 :
					securite = 'faible'
		else:
			securite = 'forte'
			if Signal.objects.filter(post__creator=request.user,decision='accepté'):
				if Signal.objects.filter(post__creator=request.user,decision='accepté').count() >= 3 :
					securite = 'moyenne' 
				elif Signal.objects.filter(post__creator=request.user,decision='accepté').count() >= 5 :
					securite = 'faible' 

		ventes = Annonce.objects.filter(creator=request.user,typeannonce='vente')
		achats = Annonce.objects.filter(creator=request.user,typeannonce='achat')
		urgences = Annonce.objects.filter(creator=request.user,typeannonce='urgence')
		if request.user.is_authenticated:
			if mode == "ado":
				ventes =ventes.filter(price__lte=99999)
				achats = achats.filter(price__lte=99999)
				urgences = urgences.filter(price__lte=99999)

		rating = 0
		for i in Rating.objects.filter(account=request.user):
			if i.rating=='p':
				rating+=1
			elif i.rating=='n':
				rating-=1
		vente_count = 0
		achat_count = 0
		for i in Annonce.objects.filter(creator=request.user,typeannonce='vente'):
			if i.buyer != '':
				vente_count += 1
			
		for i in Annonce.objects.filter(creator=request.user,typeannonce='achat'):
			if i.buyer != '':
				achat_count += 1

		for i in HistoryItem.objects.filter(buyer=request.user):
			if i.post.typeannonce == 'vente':
				achat_count += 1
			elif i.post.typeannonce == 'achat':
				vente_count += 1

		context = {
			'user': request.user,
			'ventes':ventes,
			'achats':achats,
			'urgences':urgences,
			'securite': securite,
			'rating':rating,
			'vente_count':vente_count,
			'achat_count':achat_count,
			'mode':mode
		}
		return render(request,template,context)
	else:
		return redirect('core:index')

def userprofile(request,user):
	if request.user.is_authenticated:
		template = 'profil.html'
		user = get_object_or_404(Account, username=user)
		mode = 'aucun'
		if MiseANiveau.objects.filter(attributed=True,account=user).exists():
			mode = MiseANiveau.objects.filter(attributed=True,account=user)[0].mode
		if request.user.is_authenticated:
			if subscriptions.objects.filter(subscriber=request.user,subscribed_to=Account.objects.filter(username=user)[0]).exists():
				subscription = True
			else:
				subscription = False
		else:
			subscription = False

		if mode == 'aucun':
			securite = 'moyenne'
			if Signal.objects.filter(post__creator=user,decision='accepté'):
				if Signal.objects.filter(post__creator=user,decision='accepté').count() >= 3 :
					securite = 'faible'
		else:
			securite = 'forte'
			if Signal.objects.filter(post__creator=user,decision='accepté'):
				if Signal.objects.filter(post__creator=user,decision='accepté').count() >= 3 :
					securite = 'moyenne' 
				elif Signal.objects.filter(post__creator=user,decision='accepté').count() >= 5 :
					securite = 'faible' 

		if request.POST:
			if request.POST.get('action') == 'subscribe':
				if request.user.is_authenticated:
					if subscription == False:
						subscriptions.objects.create(subscriber=request.user,subscribed_to=Account.objects.filter(username=user)[0])
			elif request.POST.get('action') == 'unsubscribe':
				if request.user.is_authenticated:
					if subscription == True:
						subscriptions.objects.filter(subscriber=request.user,subscribed_to=Account.objects.filter(username=user)[0])[0].delete()
		
		ventes = Annonce.objects.filter(creator=user,typeannonce='vente')
		achats = Annonce.objects.filter(creator=user,typeannonce='achat')
		urgences = Annonce.objects.filter(creator=user,typeannonce='urgence')
		if request.user.is_authenticated:
			if mode == "ado":
				ventes =ventes.filter(price__lte=99999)
				achats = achats.filter(price__lte=99999)
				urgences = urgences.filter(price__lte=99999)
		state = 'neutral'
		if request.user.is_authenticated:
			if Rating.objects.filter(voter=request.user,
											account=user
											,rating='n').exists():
				state = 'down'
			elif Rating.objects.filter(voter=request.user,
											account=user,
											rating='p').exists():
				state = 'up'
			else:
				state = 'neutral'

		rating = 0
		for i in Rating.objects.filter(account=user):
			if i.rating=='p':
				rating+=1
			elif i.rating=='n':
				rating-=1

		vente_count = 0
		achat_count = 0
		for i in Annonce.objects.filter(creator=user,typeannonce='vente'):
			if i.buyer != '':
				vente_count += 1
			
		for i in Annonce.objects.filter(creator=user,typeannonce='achat'):
			if i.buyer != '':
				achat_count += 1

		for i in HistoryItem.objects.filter(buyer=user):
			if i.post.typeannonce == 'vente':
				achat_count += 1
			elif i.post.typeannonce == 'achat':
				vente_count += 1

		context = {
			'user':user,
			'subscription':subscription,
			'securite': securite,
			'ventes':ventes,
			'achats':achats,
			'urgences':urgences,
			'state': state,
			'rating':rating,
			'vente_count':vente_count,
			'achat_count':achat_count,
			'mode':mode
		}
		return render(request,template,context)
	else:
		return redirect('account:login')

def saved(request):
	if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
		template = 'profil.html'
		saved = SavedItem.objects.filter(creator=request.user)
		mode = 'aucun'
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			mode = MiseANiveau.objects.filter(attributed=True,account=request.user)[0].mode

		if mode == 'aucun':
			securite = 'moyenne'
			if Signal.objects.filter(creator=request.user,decision='accepté'):
				if Signal.objects.filter(creator=request.user,decision='accepté').count() >= 3 :
					securite = 'faible'
		else:
			securite = 'forte'
			if Signal.objects.filter(creator=request.user,decision='accepté'):
				if Signal.objects.filter(creator=request.user,decision='accepté').count() >= 3 :
					securite = 'moyenne' 
				elif Signal.objects.filter(creator=request.user,decision='accepté').count() >= 5 :
					securite = 'faible' 
		context = {
			'page': 'saved',
			'user': request.user,
			'saved':saved,
			'securite':securite
		}
		return render(request, template, context)
	else:
		return redirect('core:index')


def upgrade(request):
	template='upgrade.html'
	if request.POST.get('action') == 'check':
		if request.POST.get('nin')[2:5] == str(request.user.birth_date)[1:4]:
			return JsonResponse({'status':'success'})
		else:
			return JsonResponse({'status':'fail'})
	elif request.POST.get('action') == 'submit':
		if request.POST.get('nin')[2:5] == str(request.user.birth_date)[1:4]:
			code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
			mise = MiseANiveau.objects.create(account=request.user,
											attachement=request.FILES.get('attachement'),
											mode=request.POST.get('mode'),
											NIN=request.POST.get('nin'),
											adresse=request.POST.get('adresse'),
											code_confirmation=code)
			return redirect('core:index')
		else:
			return JsonResponse({'status':'fail'})


	context={}
	return render(request,template,context)

def confirmcode(request):
	if request.user.is_authenticated:
		if MiseANiveau.objects.filter(account=request.user).exists():
			if not request.user.identite_confirme:
				template='confirmcode.html'
				if request.POST.get('action') == 'confirm':
					if request.POST.get("code").upper() == MiseANiveau.objects.filter(account=request.user,attributed=False)[0].code_confirmation:
						user = Account.objects.filter(username=request.user.username)[0]
						user.identite_confirme = True
						user.save()
						return JsonResponse({'stat':'success'})
					else:
						return JsonResponse({'stat':'fail'})

				context={}
				return render(request,template,context)

def down(request):
	if request.POST:
		if request.POST.get('action') == 'down':
			if Rating.objects.filter(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='p').exists():
				Rating.objects.filter(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='p')[0].delete()
				Rating.objects.create(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='n')
				return JsonResponse({'stat':'down'})
			elif Rating.objects.filter(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='n').exists():
				Rating.objects.filter(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='n')[0].delete()
				return JsonResponse({'stat':'neutral'})
			else:
				Rating.objects.create(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='n')
				return JsonResponse({'stat':'down'})


	return JsonResponse({})

def up(request):
	if request.POST:
		if request.POST.get('action') == 'up':
			if Rating.objects.filter(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='n').exists():
				Rating.objects.filter(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='n')[0].delete()
				Rating.objects.create(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='p')
				return JsonResponse({'stat':'up'})
			elif Rating.objects.filter(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='p').exists():
				Rating.objects.filter(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='p')[0].delete()
				return JsonResponse({'stat':'neutral'})
			else:
				Rating.objects.create(voter=request.user,
									account=Account.objects.filter(username=request.POST.get('account'))[0],
									rating='p')
				return JsonResponse({'stat':'up'})


	return JsonResponse({})

def history(request):
	template = 'history.html'

	history = HistoryItem.objects.filter(buyer=request.user)

	context = {
		'historyitems':history
	}
	return render(request, template,context)
