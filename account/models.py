from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
	def create_user(self,email,username,first_name,last_name,phone_number,
			birth_date,sexe,wilaya,commune,password=None):
		if not email:
			raise ValueError("Users must have a email")
		if not username:
			raise ValueError("Users must have a username")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			first_name=first_name,
			last_name=last_name,
			phone_number=phone_number,
			sexe=sexe,
			wilaya=wilaya,
			commune=commune,
			birth_date=birth_date
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password,first_name,birth_date,last_name,phone_number,sexe,wilaya,commune):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			first_name=first_name,
			last_name=last_name,
			phone_number=phone_number,
			sexe=sexe,
			wilaya=wilaya,
			commune=commune,
			birth_date=birth_date
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


SEXE_CHOICES = [
		('h', 'Homme'),
		('f', 'Femme')
	]

RATING_CHOICES = [
		('p', 'Positive'),
		('n', 'Négative')
	]

DURATION_CHOICES = [
		('1', '1 Mois'),
		('3', '3 Mois'),
		('6', '6 Mois'),
		('12', '12 Mois'),
	]

TYPE_CHOICES = [
		('aucun','Aucun'),
		('secure', 'Sécurisé'),
		('online_seller', 'Vendeur en ligne'),
		('kid', 'Enfant'),
		('ado', 'Adolescent'),
		('entreprise', 'Entreprise'),
		('special_needs', 'Besoins spéciaux'),
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

class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	profile_pic = models.ImageField(upload_to="profile_pics")
	phone_number = models.CharField(max_length=15, blank=True, null=True)
	first_name = models.CharField(max_length=80)
	last_name = models.CharField(max_length=80)
	wilaya = models.CharField(max_length=80,choices=WILAYA_CHOICES)
	commune = models.CharField(max_length=80)
	sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
	mode = models.CharField(max_length=30, default='aucun', choices=TYPE_CHOICES)
	birth_date= models.DateField()
	identite_confirme = models.BooleanField(default=False)
	is_online = models.IntegerField(default=0)
	date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email','first_name','birth_date','last_name','phone_number','sexe','wilaya','commune']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self,app_label):
		return True

class subscriptions(models.Model):
    subscriber = models.ForeignKey(Account,blank=False,null=False,on_delete = models.CASCADE, related_name='subscriber')
    subscribed_to = models.ForeignKey(Account,blank=False,null=False,on_delete = models.CASCADE, related_name='subscribed_to')
    def __str__(self):
        return self.subscriber.username + " ==> " + self.subscribed_to.username
    class Meta:
        verbose_name_plural = "subscriptions"
        
class MiseANiveau(models.Model):
	account = models.ForeignKey(Account,on_delete=models.CASCADE)
	attachement = models.ImageField(upload_to='preuves')
	attributed = models.BooleanField(default=False)
	mode = models.CharField(choices=TYPE_CHOICES, max_length=15)
	created = models.DateTimeField(auto_now_add=True)
	date_attribution = models.DateField(null=True, blank=True)
	NIN = models.CharField(max_length=25)
	duree = models.CharField(max_length=5, choices=DURATION_CHOICES)
	adresse = models.CharField(max_length=100)
	code_confirmation = models.CharField(max_length=6)

	def __str__(self):
		return self.account.username

class Rating(models.Model):
	voter = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="voter")
	account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='account')
	rating = models.CharField(max_length=1,choices=RATING_CHOICES)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.account.username

class Enfant(models.Model):
	parent = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="parent")
	child = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="child")
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return (self.parent.username + ' => ' + self.child.username)