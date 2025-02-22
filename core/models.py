from django.db import models
from account.models import Account

# Create your models here.

TYPE_CHOICES = [
		('achat','Achat'),
		('vente', 'Vente'),
		('urgence', 'Urgence'),
		('covoiturage', 'Covoiturage')
]

SEXE_CHOICES = [
		('both','Les deux'),
		('f','Femme'),
		('h', 'Homme'),
]

CATEGORIES = [
		('Téléphones','Téléphones'),
		('Véhicules','Véhicules'),
		('Immobilier','Immobilier'),
		('Electronique & Electroménager','Electronique & Electroménager'),
		('Emploi','Emploi'),
		('Informatique','Informatique'),
		('Mode & Beauté','Mode & Beauté'),
		('Maison & Fournitures','Maison & Fournitures'),
		('Loisirs & Divertissements','Loisirs & Divertissements'),
		('Matériaux & Equipement','Matériaux & Equipement'),
		('Voyages','Voyages'),
		('Services','Services'),
		('Divers','Divers'),
]

WILAYA_CHOICES = [('Adrar','Adrar'),('Chlef','Chlef'),('Laghouat','Laghouat'),
					('Oum El Bouaghi','Oum El Bouaghi'),('Batna','Batna'),
					('Béjaïa','Béjaïa'),('Biskra','Biskra'),('Béchar','Béchar'),
					('Blida','Blida'),('Bouira','Bouira'),('Tamanrasset','Tamanrasset'),
					('Tébessa' ,'Tébessa'),('Tlemcen','Tlemcen'),('Tiaret','Tiaret'),
					('Tizi Ouzou','Tizi Ouzou'),('Alger','Alger'),('Djelfa','Djelfa'),
					('Jijel','Jijel'),('Sétif','Sétif'),('Saïda','Saïda'),
					('Skikda','Skikda'),('Sidi Bel Abbès','Sidi Bel Abbès'),
					('Annaba','Annaba'),('Guelma','Guelma'),('Constantine','Constantine'),
					('Médéa','Médéa'),('Mostaganem','Mostaganem'),("M'Sila","M'Sila"),
					('Mascara','Mascara'),('Ouargla','Ouargla'),('Oran','Oran'),
					('El Bayadh','El Bayadh'),('Illizi','Illizi'),('Bordj Bou Arreridj','Bordj Bou Arreridj'),
					('Boumerdès','Boumerdès'),('El Tarf','El Tarf'),('Tindouf','Tindouf'),
					('Tissemsilt','Tissemsilt'),('El Oued','El Oued'),('Khenchela','Khenchela'),
					('Souk Ahras','Souk Ahras'),('Tipaza','Tipaza'),('Mila','Mila'),
					('Aïn Defla','Aïn Defla'),('Naâma','Naâma'),('Aïn Témouchent','Aïn Témouchent'),
					('Ghardaïa','Ghardaïa'),('Relizane','Relizane')]

class PostImages(models.Model):
	image = models.ImageField(upload_to="useruploads")

class Annonce(models.Model):
	creator = models.ForeignKey(Account, on_delete=models.CASCADE)
	title = models.CharField(max_length=256, default='')
	categorie = models.CharField(max_length=256, choices=CATEGORIES)
	sous_categorie = models.CharField(max_length=256, default="")
	slug = models.CharField(max_length=256, default='', unique=True)
	description = models.TextField()
	prix = models.IntegerField()
	deplacement = models.BooleanField(default=False)
	livraison = models.BooleanField(default=False)
	echange = models.BooleanField(default=False)
	images = models.ManyToManyField(PostImages)
	typeannonce = models.CharField(max_length=256, choices=TYPE_CHOICES)
	sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
	buyer = models.CharField(max_length=256, default="", blank=True)
	age_min = models.IntegerField()
	age_max = models.IntegerField()
	vendeur_en_ligne = models.BooleanField(default=False)
	wilaya = models.CharField(max_length=25, choices=WILAYA_CHOICES)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.slug

class SavedItem(models.Model):
	creator = models.ForeignKey(Account, on_delete=models.CASCADE)
	post = models.ForeignKey(Annonce, on_delete=models.CASCADE)

	def __str__(self):
		return self.creator.username + ' -> ' + self.post.slug

DECISION_CHOICES = [
	('en attente', 'En attente'),
	('accepté', 'Accepté'),
	('refusé', 'Refusé')
]

class Signal(models.Model):
	creator = models.ForeignKey(Account, on_delete=models.CASCADE)
	post = models.ForeignKey(Annonce, on_delete=models.CASCADE)
	raison = models.TextField()
	decision = models.CharField(max_length=10,choices=DECISION_CHOICES)

	def __str__(self):
		return self.creator.username + ' -> ' + self.post.slug

class conseil(models.Model):
	creator = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField()
	decision = models.BooleanField(default=False)

	def __str__(self):
		return self.creator.username + ' -> ' + str(self.decision)

class DemandeContact(models.Model):
	creator = models.ForeignKey(Account, on_delete=models.CASCADE)
	post = models.ForeignKey(Annonce, on_delete=models.CASCADE)
	creation = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.creation.strftime('%Y-%m-%d %H:%M:%S') + ' / ' + self.creator.username + ' -> ' + self.post.creator.username

class notification(models.Model):
	notified = models.ForeignKey(Account,blank=False,null=False,on_delete=models.CASCADE,related_name='notifications')
	content = models.CharField(max_length=256,default='')
	link = models.CharField(max_length=256,default='')
	created = models.DateTimeField(auto_now_add=True)
	seen = models.BooleanField(default=False)
	class Meta:
		ordering = ['-created']

		def __unicode__(self):
			return u'%s'% self.notified.username
	def __str__(self):
		return self.notified.username

class Arnaque(models.Model):
	creator = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering = ['-created']

		def __unicode__(self):
			return u'%s'% self.creator.username
	def __str__(self):
		return self.creator.username

class DeleteRequest(models.Model):
	post = models.ForeignKey(Annonce, on_delete=models.CASCADE)
	attributed = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering = ['-created']

		def __unicode__(self):
			return u'%s'% self.post.title
	def __str__(self):
		return self.post.title

class AnnonceArchive(models.Model):
	creator = models.ForeignKey(Account, on_delete=models.CASCADE)
	title = models.CharField(max_length=256, default='')
	categorie = models.CharField(max_length=256, choices=CATEGORIES)
	sous_categorie = models.CharField(max_length=256, default="")
	slug = models.CharField(max_length=256, default='', unique=True)
	description = models.TextField()
	notice = models.CharField(max_length=256, default="")
	prix = models.IntegerField()
	images = models.ManyToManyField(PostImages)
	typeannonce = models.CharField(max_length=256, choices=TYPE_CHOICES)
	sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
	buyer = models.CharField(max_length=256, default="")
	age_min = models.IntegerField()
	age_max = models.IntegerField()
	wilaya = models.CharField(max_length=25, choices=WILAYA_CHOICES)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.slug

class HistoryItem(models.Model):
	buyer = models.ForeignKey(Account, on_delete=models.CASCADE)
	post = models.ForeignKey(Annonce, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering = ['-created']

		def __unicode__(self):
			return u'%s'% self.post.title
	def __str__(self):
		return self.post.title
