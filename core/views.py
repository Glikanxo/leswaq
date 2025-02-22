from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from account.models import *
from django.db.models import Q
from datetime import datetime, timedelta,date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now


# Create your views here.

def age(request):
	age = 0
	if request.user.is_authenticated:
		today = date.today()
		age=int((today-request.user.birth_date).days/365.25)
	return age

def index(request):
	template = 'index2.html'
	if request.user.is_authenticated:
		if age(request) < 18 and age(request) >= 16:
			if not MiseANiveau.objects.filter(attributed=True,account=request.user,mode='ado').exists():
				MiseANiveau.objects.create(attributed=True,
											account=request.user,
											mode='ado',
											duree='1',
											date_attribution=date.today())
		elif age(request) < 16:
			if not MiseANiveau.objects.filter(attributed=True,account=request.user,mode='kid').exists():
				MiseANiveau.objects.create(attributed=True,
											account=request.user,
											mode='ado',
											duree='1',
											date_attribution=date.today())
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			mise = MiseANiveau.objects.filter(attributed=True,account=request.user)[0]
			if date.today() > (mise.date_attribution + timedelta(days=(30*int(mise.duree)))):
				mise.attributed=False
				mise.save()
		for i in DeleteRequest.objects.filter(attributed=False):
			if (datetime.today() - i.created.replace(tzinfo=None)).days == 2:
				product = i.post
				archive = AnnonceArchive.objects.create(creator=product.creator,
								slug= product.slug,
								title=product.title,
								description=product.description,
								prix=product.prix,
								categorie=product.categorie,
								sous_categorie=product.sous_categorie,
								typeannonce=product.typeannonce,
								notice=product.notice,
								sexe = product.sexe,
								age_min = product.age_min,
								age_max = product.age_max,
								wilaya =product.wilaya)
				for i in product.images.all():
					archive.images.add(i)
				archive.save() 
				product.delete()
				i.delete()
	context = {
		'urgences': Annonce.objects.filter(typeannonce="urgence")[0:16],
		'vendeur': Annonce.objects.filter(vendeur_en_ligne=True)[0:16],
		'divers': Annonce.objects.all().order_by('?').exclude(typeannonce="covoiturage")[0:26],
	}
	return render(request, template, context)

def get_mode():
	mode = 'aucun'
	if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
		mise = MiseANiveau.objects.filter(attributed=True,account=request.user)[0]
		mode = mise.mode
	return mode

def newpost(request):
	template = 'new_post.html'
	if request.user.is_authenticated:
		mode = 'aucun'
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			mode = MiseANiveau.objects.filter(attributed=True,account=request.user)[0].mode
		if mode in ['aucun','special_needs','kid', 'ado']:
			if Annonce.objects.filter(creator=request.user,typeannonce='urgence',created__month=datetime.today().month).count() == 2:
				urgencestate = True
			else:
				urgencestate = False
		if mode == 'secure':
			if Annonce.objects.filter(creator=request.user,typeannonce='urgence',created__month=datetime.today().month).count() == 5:
				urgencestate = True
			else:
				urgencestate = False
		if mode in ['online_seller','entreprise']:
			if Annonce.objects.filter(creator=request.user,typeannonce='urgence',created__month=datetime.today().month).count() == 15:
				urgencestate = True
			else:
				urgencestate = False
	if 'new-post' in request.POST:
		imgs = []

		creator = request.user
		title = request.POST.get('title')
		description = request.POST.get('description')
		prix = request.POST.get('price')
		categorie = request.POST.get('categorie')
		typeannonce = request.POST.get('type')
		sous_categorie = request.POST.get('souscategorie')
		sexe = 'both'
		if request.POST.get('sexe'):
			sexe = request.POST.get('sexe')
		if not request.POST.get('wilaya'):
			wilaya = ''
		else:
			wilaya = request.POST.get('wilaya')
		if request.POST.get('online_seller_post') == 'on':
			online_seller_post = True
		else:
			online_seller_post = False
		age_min = 7
		age_max = 99
		if request.POST.get('age_min'):
			age_min = request.POST.get('age_min')
		if request.POST.get('age_max'):
			age_max = request.POST.get('age_max')
		livraison = True if request.POST.get('livraison') == 'on' else False
		deplacement = True if request.POST.get('deplacement') == 'on' else False
		echange = True if request.POST.get('echange') == 'on' else False
		annonce = Annonce.objects.create(creator=creator,
								slug= title.replace(" ","") + datetime.now().strftime('%Y%m%d%H%M%S'),
								title=title,
								description=description,
								prix=prix,
								categorie=categorie,
								sous_categorie=sous_categorie,
								typeannonce=typeannonce,
								sexe = sexe,
								age_min = age_min,
								age_max = age_max,
								wilaya =wilaya,
								vendeur_en_ligne=online_seller_post,
								echange=echange,
								deplacement=deplacement,
								livraison=livraison)
		if not online_seller_post:
			for i in range(1,int(request.POST.get('imgnum'))+1):
				if request.FILES.get("img"+str(i)) != '':
					img = PostImages.objects.create(image=request.FILES.get("img"+str(i)))
					annonce.images.add(img)
					annonce.save()
		return redirect('core:index')
	context = {
		'urgence' : urgencestate
	}
	return render(request, template, context)

def emptysearch(request):
	template = "search2.html"
	mode = 'aucun'
	if request.user.is_authenticated:
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			mode = MiseANiveau.objects.filter(attributed=True,account=request.user)[0].mode
	results = Annonce.objects.filter(
	                        Q(title__icontains="") | Q(description__icontains="")  | Q(creator__username__icontains="")   
	                        )
	if request.user.is_authenticated:
		results = results.filter(age_min__lte=age(request),age_max__gte=age(request))
		results = results.filter(Q(wilaya='') | Q(wilaya=request.user.wilaya))
		results = results.filter(Q(sexe='both') | Q(sexe=request.user.sexe))
		if mode == "ado":
			results = results.filter(price__lte=99999)
	else:
		results = results.filter(age_min=7, age_max=99,wilaya='',sexe='both')

	if 'filter' in request.POST:
		wilaya=request.POST.get('wilaya')
		age_min=request.POST.get('age_min')
		age_max=request.POST.get('age_max')
		sexe=request.POST.get('sexe')
		current = now().date()
		min_date = date(current.year - age_min, current.month, current.day)
		max_date = date(current.year - age_max, current.month, current.day)

		if sexe == 'h':
			results = results.filter(creator__sexe='h')
		elif sexe == 'f':
			results = results.filter(creator__sexe='f')
		results = results.filter(creator__birth_date__gte=max_date,creator__birth_date__lte=min_date)

		if wilaya != '':
			results = results.filter(wilaya=wilaya)

	context = {
		'query':"",
		'results':results
	}
	return render(request,template,context)

def conditions(request):
	template = "conditions.html"
	context = {
	}
	return render(request,template,context)

def politiques(request):
	template = "politiques.html"
	context = {
	}
	return render(request,template,context)

def search(request, query):
	template = "search2.html"
	mode = 'aucun'
	if request.user.is_authenticated:
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			mode = MiseANiveau.objects.filter(attributed=True,account=request.user)[0].mode
	results = Annonce.objects.filter(
	                        Q(title__icontains=query) | Q(description__icontains=query)  | Q(creator__username__icontains=query)   
	                        )
	if request.user.is_authenticated:
		results = results.filter(age_min__lte=age(request),age_max__gte=age(request))
		results = results.filter(Q(wilaya='') | Q(wilaya=request.user.wilaya))
		results = results.filter(Q(sexe='both') | Q(sexe=request.user.sexe))
		if mode == "ado":
			results = results.filter(price__lte=99999)
	else:
		results = results.filter(age_min=7, age_max=99,wilaya='',sexe='both')

	if 'filter' in request.POST:
		wilaya=request.POST.get('wilaya')
		age_min=request.POST.get('age_min')
		age_max=request.POST.get('age_max')
		sexe=request.POST.get('sexe')
		current = now().date()
		min_date = date(current.year - age_min, current.month, current.day)
		max_date = date(current.year - age_max, current.month, current.day)

		if sexe == 'h':
			results = results.filter(creator__sexe='h')
		elif sexe == 'f':
			results = results.filter(creator__sexe='f')
		results = results.filter(creator__birth_date__gte=max_date,creator__birth_date__lte=min_date)

		if wilaya != '':
			results = results.filter(wilaya=wilaya)
			
	context = {
		'query':query,
		'results':results
	}
	return render(request,template,context)

def post(request,slug):
	template = 'post.html'
	product = get_object_or_404(Annonce,slug=slug)

	if request.user.is_authenticated:
		mode = 'aucun'
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			mode = MiseANiveau.objects.filter(attributed=True,account=request.user)[0].mode
		if(product.age_min <= age(request) and product.age_max>=age(request)):
			if(product.wilaya=='' or product.wilaya==request.user.wilaya):
				if not (product.sexe=='both' or product.sexe==request.user.sexe):
					redirect('core:index')
			else:
				redirect('core:index')
		else:
			redirect('core:index')

		if mode == "ado":
			if product.price >99999:
				redirect('core:index')
	deleted = False
	if DeleteRequest.objects.filter(post=product).exists():
		deleted = True

	if request.user.is_authenticated:
		if SavedItem.objects.filter(creator=request.user,post=product):
			saved = True
		else:
			saved = False
	else:
		saved = False
	if request.POST:
		if request.POST.get('action') == 'save':
			SavedItem.objects.create(creator=request.user,post=product)
		elif  request.POST.get('action') == 'unsave':
			SavedItem.objects.get(creator=request.user,post=product).delete()
		elif request.POST.get('action') == 'signal':
			Signal.objects.create(creator=request.user,
				raison=request.POST.get('raison'),
				post=product,
				decision='en attente')
		elif request.POST.get('action') == 'buyeridentif':
			if request.POST.get('place') == 'site':
				if Account.objects.filter(username=request.POST.get('content')).exists():
					HistoryItem.objects.create(buyer=request.user,post=product)
					product.buyer = request.POST.get('content')
					product.save()
					return JsonResponse({'status':'success'})
				else:
					return JsonResponse({'status':'user_not_found'})
			elif request.POST.get('place') == 'hors-site':
				product.buyer = request.POST.get('content')
				product.save()
				return JsonResponse({'status':'success'})
		elif 'deletepost' in request.POST:
			if (product.buyer != '') or product.vendeur_en_ligne:
				archive = AnnonceArchive.objects.create(creator=product.creator,
								slug= product.slug,
								title=product.title,
								description=product.description,
								prix=product.prix,
								categorie=product.categorie,
								sous_categorie=product.sous_categorie,
								typeannonce=product.typeannonce,
								sexe = product.sexe,
								age_min = product.age_min,
								age_max = product.age_max,
								wilaya =product.wilaya)
				for i in product.images.all():
					archive.images.add(i)
				archive.save() 
				product.delete()
				return redirect('core:index')
			else:
				DeleteRequest.objects.create(post=product)
				for i in DemandeContact.objects.filter(post=product):
					notif = notification.objects.create(notified=i.creator,
												content='Avez vous acheté ce produit ?',
												link='././post/'+i.product.slug)
					notif.link = '/post/'+i.post.slug+'/'+notif.pk
				for i in SavedItem.objects.filter(post=product):
					notif = notification.objects.create(notified=i.creator,
												content='Avez vous acheté ce produit ?',
												link='/post/'+i.post.slug)
					notif.link = '/post/'+i.post.slug+'/'+notif.pk

		elif request.POST.get('action') == 'demandecontact':
			if request.user.is_authenticated:
				DemandeContact.objects.create(creator=request.user,post=product)
				return JsonResponse({'number':product.creator.phone_number})
			else:
				return JsonResponse({'respone':'rejected'})
		elif 'send-parent' in request.POST:
			notification.objects.create(notified=Account.objects.filter(username=Enfant.objects.filter(child=request.user)[0].parent.username)[0],
										content='Votre enfant vous a envoyé une publication',
										link="post/"+slug)
		elif 'adviceform' in request.POST:
			conseil.objects.create(creator=request.user,content=request.POST.get('content'))

	context = {
		'product':product,
		'savd':saved,
		'deleted':deleted,
		'conseils':conseil.objects.filter(decision=True)
	}
	return render(request, template, context)

def filtering(request, cat, query):
	template = 'search2.html'
	mode = 'aucun'
	if request.user.is_authenticated:
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			mode = MiseANiveau.objects.filter(attributed=True,account=request.user)[0].mode
	if cat == 'c':
		results = Annonce.objects.filter(categorie=query)
	if cat == 'f':
		results = Annonce.objects.filter(creator__wilaya=query)
	if cat == 's':
		results = Annonce.objects.filter(sous_categorie=query)

	if request.user.is_authenticated:
		results = results.filter(age_min__lte=age(request),age_max__gte=age(request))
		results = results.filter(Q(wilaya='') | Q(wilaya=request.user.wilaya))
		results = results.filter(Q(sexe='both') | Q(sexe=request.user.sexe))
		if mode == "ado":
			results = results.filter(price__lte=99999)
	else:
		results = results.filter(age_min=7, age_max=99,wilaya='',sexe='both')
			
	if 'filter' in request.POST:
		wilaya=request.POST.get('wilaya')
		age_min=request.POST.get('age_min')
		age_max=request.POST.get('age_max')
		sexe=request.POST.get('sexe')
		current = now().date()
		min_date = date(current.year - age_min, current.month, current.day)
		max_date = date(current.year - age_max, current.month, current.day)

		if sexe == 'h':
			results = results.filter(creator__sexe='h')
		elif sexe == 'f':
			results = results.filter(creator__sexe='f')
		results = results.filter(creator__birth_date__gte=max_date,creator__birth_date__lte=min_date)

		if wilaya != '':
			results = results.filter(wilaya=wilaya)
			
	context = {
		'filter': True,
		'results':results,
		'cat': cat,
		'quer':query
	}
	return render(request, template, context)

@login_required
def notifications(request):
	template='notifications.html'
	if request.POST:
		notif = notification.objects.filter(pk=request.POST.get('notif')).first()
		notif.seen=True
		notif.save()
		return redirect('././'+notif.link)
	context = {
		'notifications':notification.objects.filter(notified=request.user)
	}
	return render(request, template, context)

def signaler_arnaque(request):
	if request.POST:
		Arnaque.objects.create(creator=request.user,content=request.POST.get('content'))
		return JsonResponse({})

def bought_confirm(request,slug,pk):
	if Annonce.objects.filter(slug=slug).exists() and notification.objects.filter(pk=pk).exists():
		product = get_object_or_404(Annonce,slug=slug)
		notif = get_object_or_404(notification,pk=pk)
		if request.user.is_authenticated and notif.notified==request.user and (DemandeContact.objects.filter(post=product,creator=request.user).exists() or SavedItem.objects.filter(post=product,creator=request.user).exists()):
			template = 'bought_confirm.html'
			if request.POST:
				if 'no' in request.POST:
					notification.objects.get(pk=pk).delete()
					redirect('core:index')
				if 'oui' in request.POST:
					product.buyer = request.user.username

					for i in DemandeContact.objects.filter(post=product):
						for j in notification.objects.filter(notified=i.creator,content='Avez vous acheté ce produit ?'):
							j.objects.delete()

					for i in SavedItem.objects.filter(post=product):
						for j in notification.objects.filter(notified=i.creator,content='Avez vous acheté ce produit ?'):
							j.objects.delete()

					HistoryItem.objects.create(buyer=request.user,post=product)

					if DeleteRequest.objects.filter(post=product).exists():
						archive = AnnonceArchive.objects.create(creator=product.creator,
										slug= product.slug,
										title=product.title,
										description=product.description,
										prix=product.prix,
										categorie=product.categorie,
										sous_categorie=product.sous_categorie,
										typeannonce=product.typeannonce,
										sexe = product.sexe,
										buyer = product.buyer,
										age_min = product.age_min,
										age_max = product.age_max,
										wilaya =product.wilaya)
						for i in product.images.all():
							archive.images.add(i)
						archive.save() 
						product.delete()
						DeleteRequest.objects.get(post=product).attributed=True
			context = {
				'product':product,
			}
			return render(request,template,context)
		else:
			return redirect('core:index')
	else:
		return redirect('core:index')
