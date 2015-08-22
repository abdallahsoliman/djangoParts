from django.db import models
from django.contrib.auth.models import User as DjangoUser


class Person(models.Model):
    django_user = models.OneToOneField(DjangoUser)
    email = models.CharField(max_length=200,null=False)
    
    def create(self,password):
        if not self.email:
            raise Exception("must have an email")
        #Create django user
        django_user = DjangoUser.objects.create_user(username=self.email[:30],
                                                     email=self.email,
                                                     password=password)
        self.django_user = django_user
        try:
            self.save()
        except Exception,e:
            self.django_user.delete()
            raise Exception("could not create person: {0}".format(e))

    def setPassword(self,password):
        self.django_user.set_password(password)
        self.django_user.save()

    def save(self):
        self.django_user.username = self.email[:30]
        self.django_user.email = self.email
        self.django_user.save()
        models.Model.save(self)

    def delete(self):
        self.django_user.delete()

    def __unicode__(self):
        return str(self.email)
