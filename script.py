import sys;
import os;
from PIL import Image;
from PIL.ExifTags import TAGS
import time
"""
REFERENCES
-----------------------------------------------------------------------------------------------------
stackoverflow.com/questions/68033479/how-to-show-all-the-metadata-about-images
https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image
https://www.geeksforgeeks.org/python/python-pillow-a-fork-of-pil/
https://github.com/ianare/exif-samples
https://www.geeksforgeeks.org/python/python-os-stat-method/
https://www.geeksforgeeks.org/python/how-to-get-file-creation-and-modification-date-or-time-in-python/
https://docs.python.org/fr/3.8/library/os.html
https://github.com/ianare/exif-samples
-----------------------------------------------------------------------------------------------------

"""

images=[]
dictdate={}
dictinfo={}
fileinfo={}
arg= sys.argv[1]
#Parcourir récursivement un répertoire et collecter toutes les images JPG/PNG/JPEG  
def collecterImage(param):
	for f in os.listdir(param):
		path = os.path.join(param, f)
		if os.path.isdir(path):
			collecterImage(path)
		else:
			#if ".png" in f or ".jpg" in f:
			if f.lower().endswith(('.png', '.jpg', '.jpeg')):
				images.append(path)
	return images

def dateImage(param):
	listeimages= collecterImage(param)
	for imagename in listeimages:
		image = Image.open(imagename)
		exif_data = image._getexif()
		date_utilisee = None
#Recupérer la date à partir des exifdata
		if exif_data:
			for tag_id, value in exif_data.items():
				tag = TAGS.get(tag_id, tag_id)
				if tag == "DateTimeOriginal":
					date_utilisee = value.replace(":","-",2)
#Recupérer la date si l'image n'a pas d'exifdata
		if date_utilisee ==  None:
			print("Aucune donnée EXIF Trouvée")			
			stat_info = os.path.getctime(imagename)
			c_ti = time.ctime(stat_info)
			t_obj = time.strptime(c_ti)
			date_utilisee = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)
		fileinfo[imagename]= [date_utilisee]
		fileinfo[imagename].append("Date originale - extraite des metadonnées exif" if exif_data else "Date de création - pas de metadonnées exif")
		annee=date_utilisee.split(' ')[0].split('-')[0]
		mois=date_utilisee.split(' ')[0].split('-')[1]
#Vérifier si l'année est presente dans le dictionnaire  
		if annee not in dictdate:
			dictdate[annee]= {mois:[imagename]}
		else:
#Vérifier le mois
			if mois not in dictdate[annee]:
				dictdate[annee][mois]= [imagename]
			else:
				dictdate[annee][mois].append(imagename)
	return dictdate

def deplacerImage(param):
#Emplacement racine des répertoires créés
	baseurl='/home/'+os.getlogin()+'/Pictures'
	dictdate= dateImage(param)
	for annee in dictdate.keys():
		if annee not in os.listdir(baseurl):
			for dictmois in dictdate[annee]:
				dest_dir= os.path.join(baseurl, annee, dictmois)
				os.makedirs(dest_dir)
				for img in dictdate[annee][dictmois]:
					nom= os.path.basename(img)
					destination= os.path.join(dest_dir, nom)
					dictinfo[nom]=[img, destination, fileinfo[img][0], fileinfo[img][1]]
#Déplacer l'image
					os.replace(img,destination)
		else:
			for mois in dictdate[annee].keys():
				if mois not in os.listdir(baseurl+'/'+annee):
					os.mkdir(baseurl+"/"+annee+"/"+mois)
					dest_dir= os.path.join(baseurl, annee, mois)
					for img in dictdate[annee][mois]:
						nom= os.path.basename(img)
						destination= os.path.join(dest_dir, nom)
						dictinfo[nom]=[img, destination, fileinfo[img][0], fileinfo[img][1]]
#Déplacer l'image
						os.replace(img,destination)
				else:
					for img in dictdate[annee][mois]:
						nom= os.path.basename(img)
						dest_dir= os.path.join(baseurl, annee, mois)
						destination= os.path.join(dest_dir, nom)
						dictinfo[nom]=[img, destination, fileinfo[img][0], fileinfo[img][1]]
#Déplacer l'image
						os.replace(img,destination)

	return dictinfo


#Ecriture du fichier CSV
def writefilecsv(param):
	deplacerImage(param)
	rows = []
	csvfile= "listePhotos.csv"
	if os.path.exists(csvfile):
		with open(csvfile, "r", encoding="utf-8") as f:
			lines = f.readlines()
			if len(lines) > 1:
				rows = [line.strip().split(";") for line in lines[1:]]  # skip header

#Ajouter les nouvelles données
	for element in dictinfo.keys():
		row = [element] + [str(x) for x in dictinfo[element]]
		rows.append(row)

#Fonction de tri par  date
	def date_key(r):
		date_part, time_part = r[3].split(" ")
		year, month, day = map(int, date_part.split("-"))
		hour, minute, second = map(int, time_part.split(":"))
		return (year, month, day, hour, minute, second)

#Trier toutes les données dans l'ordre décroissant
	rows = sorted(rows, key=date_key, reverse= True)

#Réécriture du fichier CSV avec les données triées
	with open(csvfile, "w", encoding="utf-8") as f:
		f.write("Image;OriginalPath;Moved to;Date;Note\n")
		for row in rows:
        		f.write(";".join(row) + "\n")


#Lancement du script
writefilecsv(arg)
