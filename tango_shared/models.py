import datetime

from PIL import Image

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
from voting.models import Vote

from tango_shared.utils.sanetize import clean_text, format_text, sanetize_text

now = datetime.datetime.utcnow()

comments_close_days    = getattr(settings, 'COMMENTS_CLOSE_AFTER', 30)
comments_moderate_days = getattr(settings, 'COMMENTS_MOD_AFTER', 30)


def set_img_path(instance, filename):
    """
    Sets upload_to dynamically
    """
    upload_path = '/'.join(['img', instance._meta.app_label, str(now.year), str(now.month), filename])
    return upload_path


class BaseContentModel(models.Model):
    """
    Defines basic fields all main content types should have.
    Used for articles, videos and photo galleries.
    """
    overline = models.CharField(
        "Kicker/Overline",
        max_length=200,
        blank=True,
        null=True,
        help_text="A short headline over the main headline."
    )
    title = models.CharField(
        'Title/Headline',
        max_length=200,
        help_text="The title for this content."
    )
    subhead = models.CharField(
        'Subhead/Deck',
        max_length=200,
        blank=True,
        help_text="A short extra headline below the main headline."
    )
    slug = models.SlugField(
        max_length=200,
        help_text="""Used for URLs and identification.
        Will auto-fill, but can be edited with caution.
        """
    )
    summary = models.TextField(
        "Summary description",
        blank=True,
        help_text="""You should summarize the content.
        It's better for search engines, and for people browsing lists of content.
        If you don't, a summary will be created. But you should.
        """
    )
    summary_formatted = models.TextField(
        blank=True,
        editable=False,
        help_text="""Stores HTML formatted, sanitized version of summary"""
    )

    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    sites = models.ManyToManyField(Site, default=[settings.SITE_ID])
    enable_comments = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    has_image = models.BooleanField(max_length=200, default=False, editable=False)

    class Meta:
        ordering = ['-created']
        abstract = True

    def comments_open(self):
        close_date = (self.created + datetime.timedelta(days=comments_close_days))
        if close_date > now:
            return True

    def comments_require_moderation(self):
        mod_date = (self.created + datetime.timedelta(days=comments_moderate_days))
        if mod_date > now:
            return True

    def save(self, *args, **kwargs):
        if not self.has_image:
            # most models will have get_image. video falls back to thumb_url
            if self.get_image() or hasattr(self, 'thumb_url'):
                self.has_image = True
        self.summary_formatted = sanetize_text(self.summary)
        super(BaseContentModel, self).save(*args, **kwargs)


class BaseSidebarContentModel(models.Model):
    """
    For sidebar-type additional info for content and sub-pages for content.

    Defines basic fields. Used for articles and happenings.
    
    Should always be attached to larger content.

    """
    title = models.CharField(max_length=300)
    slug  = models.SlugField(help_text="Only needed if this is not a sidebar")
    text  = models.TextField()
    text_formatted = models.TextField(blank=True, null=True, editable=False)
    is_sidebar = models.BooleanField(default=False)
    image = models.ImageField(upload_to=set_img_path, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.title)

    def save(self, *args, **kwargs):
        self.text_formatted = sanetize_text(self.text)
        super(BaseSidebarContentModel, self).save(*args, **kwargs)


class BaseUserContentModel(models.Model):
    """
    Generic abstract model for user-submitted content to 
    have consistent sanitization and formatting.
    
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    text_formatted = models.TextField(blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Clean text and save formatted version.
        """
        self.text = clean_text(self.text)
        self.text_formatted = format_text(self.text)
        super(BaseUserContentModel, self).save(*args, **kwargs)

    @cached_property
    def votes(self):
        """ Return vote score """
        return Vote.objects.get_score(self)['score']


class ContentImage(models.Model):
    """
    Generic image object, to be attached to other content.
    It is abstract, and must be subclassed.
    """
    image = ThumbnailerImageField(
        upload_to = set_img_path,
        help_text = "Image size should be a minimum of 720px and no more than 2000px (width or height)",
        blank=True
    )
    caption = models.CharField(max_length=255, blank=True, null=True)
    byline = models.CharField(max_length=200, blank=True, null=True)
    credit = models.CharField("Credit/source", max_length=200, blank=True, null=True)
    order = models.IntegerField(
        blank=True,
        null=True,
        help_text="For manual sorting."
    )
    thumb = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        editable=False
    )
    is_vertical = models.BooleanField(blank=True, default=False, editable=False)

    class Meta:
        ordering = ['order', '-id']
        abstract = True

    def __unicode__(self):
        return mark_safe(self.admin_thumb())

    def save(self, *args, **kwargs):
        """
        We want to do dimension checks and/or resizing BEFORE the original image is saved.
        Note that if we can't get image dimensions, it's considered an invalid image
        and we return without saving.
        If the image has changed, sets self.thumb to None, triggering post_save thumbnailer.
        """
        img = self.image
        # Check if this is an already existing photo
        try:
            old_self = self.__class__.objects.get(id=self.id)
        except ObjectDoesNotExist:
            old_self = None
        #  Run on new and changed images:
        if self.id is None or self.thumb is None or (old_self.image != img):
            try:
                height = img.height
                width  = img.width
            except Exception as error:
                # We aren't dealing with a reliable image, so....
                #print("Error getting image height or width: {}".format(error))
                return
            # If image is vertical or square (treated as vertical)...
            if height >= width:
                self.is_vertical = True
            if width > 900 or height > 1200:
                """
                The image is larger than we want.
                We're going to downsize it BEFORE it is saved,
                using PIL on the InMemoryUploadedFile.
                """
                image = Image.open(img)
                image.resize((900, 1200), Image.ANTIALIAS)
                image.save(img.path)
            try:
                ezthumb_field = get_thumbnailer(self.image)
                self.thumb = ezthumb_field.get_thumbnail({
                    'size': (80, 80),
                    'crop': ',-10'
                }).url.replace("\\", "/")
            except Exception as error:
                print("Error thumbnailing {}: {}".format(self.id, error))
        super(ContentImage, self).save(*args, **kwargs)

    def has_caption_info(self):
        if self.caption or self.byline or self.credit:
            return True

    def admin_thumb(self):
        """
        Allows for admin thumbnails
        """
        if self.thumb:
            return '<img src="{}">'.format(self.thumb)
        return None
    admin_thumb.allow_tags = True
