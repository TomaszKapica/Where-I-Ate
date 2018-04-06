from django.utils.text import slugify # pragma: no cover
import random # pragma: no cover
import string # pragma: no cover

cant_use = ['create'] # pragma: no cover


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits): # pragma: no cover
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None): # pragma: no cover
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    if slug in cant_use:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug