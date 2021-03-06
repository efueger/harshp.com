"""Models for Blog
"""

from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.utils.text import slugify


class BlogPost(models.Model):

    """BlogPost

    single blog post

    post id: primary key, autoincrements
    title(str): length=250
    body: ckeditor field
    published(date)
    modified(date)
    tags: sitedata.Tag
    slug(slugfield)
    headerimage(url): image at top of post
    """

    # basic post
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250,)
    body = RichTextField()
    published = models.DateTimeField()

    # additional stuff
    modified = models.DateTimeField()
    tags = models.ManyToManyField('sitedata.Tag')
    slug = models.SlugField(max_length=50, unique=True)
    headerimage = models.URLField(max_length=200, blank=True)

    def __str__(self):
        """string representation of blog post

        Args:
            self(BlogPost)

        Returns:
            str: title of blog post

        Raises:
            None
        """
        return self.title

    class Meta:

        """verbose name for blog posts
        """
        verbose_name = 'Blog post'
        verbose_name_plural = 'Blog posts'

    def save(self, *args, **kwargs):
        """save blog post to database

        check for duplicates, and update modified timestamps

        Args:
            self(BlogPost)
            *args: arguments
            **kwargs: parameters

        Returns:
            BlogPost.super()

        Raises:
            None
        """
        if not self.post_id:
            self.created = timezone.now()
            # check if slug is a duplicate
            dup = BlogPost.objects.filter(title=self.title)
            if len(dup) > 0:  # objects with the same slug exist -> duplicate!
                nos = str(len(dup))  # append number of duplicates as modifier
                self.slug = slugify(self.title[:49 - len(dup)] + '-' + nos)
            else:
                self.slug = slugify(self.title[:50])
        self.modified = timezone.now()

        return super(BlogPost, self).save(*args, **kwargs)
