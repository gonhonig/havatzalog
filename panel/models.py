from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment


class Parameter(models.Model):
    name = models.CharField(max_length=250, verbose_name="שם")
    CATEGORY = (
        ('התנהלות מקצועית', 'התנהלות מקצועית'),
        ('חשיבה והצגה', 'חשיבה והצגה'),
        ('ערכים', 'ערכים'),
        ('פיקוד ומנהיגות', 'פיקוד ומנהיגות'),
        ('קבוצה ובין אישי', 'קבוצה ובין אישי'),
        ('יעדים', 'יעדים'),
        ('אחר', 'אחר'),
    )
    category = models.CharField(max_length=250, choices=CATEGORY, verbose_name="קטגוריה")

    def __str__(self):
        return self.name


class Pupil(models.Model):
    name = models.CharField(max_length=250, verbose_name="שם")
    YEARS = (
        (1, 'א'),
        (2, 'ב'),
    )
    year = models.IntegerField(choices=YEARS, verbose_name="שנה")
    PLATOONS = (
        (1, '1'),
        (2, '2'),
    )
    platoon = models.IntegerField(choices=PLATOONS, verbose_name="מחלקה")
    can_read = models.ManyToManyField(User, verbose_name="מורשים")
    goals = models.ManyToManyField(Parameter, blank=True, verbose_name="יעדים")
    details = models.TextField(verbose_name="פרטים", blank=True)

    def __str__(self):
        return self.name



class Event(models.Model):
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, verbose_name="חניך")
    headline = models.CharField(max_length=40, verbose_name="כותרת")
    details = models.TextField(verbose_name="פירוט")
    date = models.DateField(verbose_name="תאריך")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="עודכן על ידי", default=None)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.headline


class Cut(models.Model):
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, verbose_name="חניך")
    parameter = models.ManyToManyField(Parameter, verbose_name="פרמטרים")
    headline = models.CharField(max_length=40, verbose_name="כותרת", blank=True)
    details = models.TextField(verbose_name="פירוט")
    STATUSES = (
        ('primary', 'מתאים ביותר'),
        ('success', 'מתאים'),
        ('warning', 'דרוש שיפור'),
        ('danger', 'לא עובר סף'),
    )
    status = models.CharField(max_length=250, choices=STATUSES, verbose_name="סטטוס", blank=True)
    updated_time = models.DateTimeField(verbose_name="תאריך")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="עודכן על ידי")
    tags = TaggableManager(verbose_name="תגיות", blank=True)
    private = models.BooleanField(default=False, blank=True, verbose_name="עדכון פרטי")
    event = models.ForeignKey(Event, blank=True, null=True)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.headline

    def post_time(self):
        return str(self.updated_time.hour) + ':' + str(self.updated_time.minute) + ' - ' + str(self.updated_time.day) + '/' + str(self.updated_time.month)

    def get_content_type(self):
        return ContentType.objects.get_for_model(self.__class__)



