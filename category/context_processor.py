from .models import Category


def menu_links(request): # Def created to manage the links from Categoris
    links = Category.objects.all()
    return dict(links=links)