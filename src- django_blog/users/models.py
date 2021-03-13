from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	""" if the user is deleted, the profile will also get deleted.
	If we delete the profile it won't delete the user """
	image = models.ImageField(default = "default.jpg", upload_to = "profile_pics")

	def __str__(self):
		return f"{self.user.username} Profile"

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img = Image.open(self.image.path)

		if img.height > 300 and img.width > 300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)

		""" This method gets run after our model is saved. It is present by default in
		the parent class. we will override it to add some other functionalities.
		To run the parent class save(), we use super().save()."""