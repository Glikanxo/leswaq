from .models import *
from chatapp.models import *
from account.models import *
from datetime import date

def wilayas(request):
	return {
		'wilayas':['Adrar','Chlef','Laghouat','Oum El Bouaghi', 'Batna', 'Béjaïa', 'Biskra',
					'Béchar','Blida','Bouira','Tamanrasset', 'Tébessa' ,'Tlemcen' ,'Tiaret',
					'Tizi Ouzou','Alger','Djelfa','Jijel','Sétif','Saïda','Skikda','Sidi Bel Abbès',
					'Annaba','Guelma','Constantine','Médéa','Mostaganem',"M'Sila",'Mascara', 'Ouargla',
					'Oran', 'El Bayadh','Illizi','Bordj Bou Arreridj','Boumerdès', 'El Tarf','Tindouf',
					'Tissemsilt', 'El Oued','Khenchela','Souk Ahras','Tipaza','Mila', 'Aïn Defla', 'Naâma',
					'Aïn Témouchent', 'Ghardaïa','Relizane'],
		'categories':{
				"Téléphones" : ['Mélange','Smartphones','Téléphones portable','Tablettes','Téléphone Fixe',
    							'Accessoires de téléphone','Puces et Abonnements','Services de réparation'],
				"Immobilier" :['Appartements','Carcasse','Hangar','Bungalow','Usine','Immeuble','Duplex',
  								'Local','Villa','Niveau de villa','Terrain'],
  				'Véhicules' :['Mélange','Automobile','Fourgon','Semi a remorques','Camions','Remorques','Bus','Minibus',
  								'Motos','Bateaux','barques','Engin','Tracteurs','Pièces détachées','Accessoires auto',
  								'Services de réparations et diagnostics'],
				'Electronique & Electroménager' :['Mélange','Électroménagers','Appareils photo et accessoires',
							'Caméras et accessoires','Lecteurs vidéo et audio','Sécurité et surveillance',
							'GPS et navigations','Démodulateurs et décodeurs','Téléviseurs','Chaines (stéréo)',
							'Abonnement au serveur','Accessoires électroniques','Pièces de rechange',
							'Services de réparations'],
				'Emploi' :['Commercial et marketing','commerce et vente','Éducations et formations',
							'tourisme et gastronomie','Industrie et production','nettoyage et hygiène',
							'Beauté et esthétique','bureautique et secrétariat','Couture et confection',
							'informatique et internet','Compatibilité et audit','mécanique auto',
							'Graphisme et communication','agents polyvalents','Transport et chauffeurs',
							'artisanat','Électroniques et techniques','administration et management'],
				'Informatique' :['Mélange','Ordinateurs portables','Ordinateurs bureautiques','Piéces de rechange',
							'Accessoires informatiques','Impriment et scanners','Écrans et data show',
							'Réseau et connexion','Applications et logiciels','Stockage externe',
							'Onduleurs et stabilisateurs'],
  				'Vêtements' :['Mélange','Chaussures homme','prêt à porter homme','Prêt à porter femme','chaussures femme',
  							'Mariages et fêtes','prêt à porter fille','Chaussures garçon','tenues professionnelles',
  							'Chaussures fille' ,'maternité','Prêt à porter bébé','prêt à porter garçon','Chaussures bébé'],
				'Accessoire de mode' :['Mélange','Montres','lunettes','Sacs','bijoux','Ceintures'],
  				'Cosmétiques et beauté' :['Mélange','Soins','maquillage','Parfums et déodorants','produits paramédicaux',
  							'Rasage et épilations','instruments et outils','Accessoires de beauté','hygiène','Produits pour bébé'],


				'Maison & Fournitures' :['Mélange','Meubles de maison','Meubles de bureau','Décoration et aménagement',
							'Vaisselles','Literie et linge et rideaux','Jardinages','Tapis et moquettes','Services décoration maisons','Produits pour bébé','fournitures et articles scolaires'],


				'Loisirs & Divertissements' :['Mélange','Articles de sport','livres et magazines','Consoles de jeux','jeux vidéo'
							,'accessoires jeux vidéo','Jouets','chasse et pèche','Instrument de musique','média','Body building','antiquités et collections'],


				'Matériaux & Equipement' :['Mélange','Matériels professionnels','Outillage professionnel','produits hygiène',
							'Matériaux de construction','matières premières'],


				'Voyages' :['Réservations et visas','voyage organisé','Séjour','croisière','Hadj et Omra',
							'études et formations','Immigration','emploi à l’étranger'],


				'Services' :['Mélange','Construction et travaux','écoles et formations','Industrie et fabrication',
							'transport et déménagement','Décoration et aménagement','médecine et santé','Traiteurs et gâteaux','publicité et communication','Nettoyage et jardinage','froid et climatisation','Location de véhicules','projets et études','Réparation auto et diagnostic','sécurité et alarme','Menuiserie et meubles','bureautique et internet','Hôtelleries et restaurations et salle','impression et édition','Esthétique et beauté','images et son','Comptabilité et économie','couture et confection','Maintenance informatique','événements et divertissement','Paraboles et démos','réparation électroniques','Réparation électroménagers','services à l’étranger','Flashage et réparation téléphonique','installation des jeux et flashage','Juridique'],
				'Divers' :[]
			}
	}

def chat_num(request):
	usr = request.user
	count = 0
	notif_count = 0
	saved = False
	if usr.is_authenticated:
		for i in (Chat.objects.filter(creator=usr).exclude(last_message="") or Chat.objects.filter(receiver=usr).exclude(last_message="")):
			if i.creator == usr:
				if i.creator_seen == False:
					count += 1
			else:
				if i.receiver_seen == False:
					count += 1
		notif_count=notification.objects.filter(notified=request.user, seen=False).count()
	if usr.is_authenticated:
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			saved = True
		else:
			saved = False

	account_type = 'aucun'
	if request.user.is_authenticated:
		if MiseANiveau.objects.filter(attributed=True,account=request.user).exists():
			mise = MiseANiveau.objects.filter(attributed=True,account=request.user)[0]
			account_type = mise.mode
	return{'count':count,
			'notif_count':notif_count,
			'saved':saved,
			'account_type':account_type}

def age(request):
	age = 0
	if request.user.is_authenticated:
		today = date.today()
		age=int((today-request.user.birth_date).days/365.25)
	return {'age':age}