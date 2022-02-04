from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Listing
from .choices import price_choices, bedroom_choices, state_choices, besoin_choices, bien_choices


# Create your views here.
def index(request):

    # Most recent listings should be first and only those published will be shown
    listingsAll = Listing.objects.order_by(
        '-list_date').filter(is_published=True)

    paginator = Paginator(listingsAll, 3)

    # 'page' is the URL parameter that we are looking for
    page = request.GET.get('page')
    paged_listingsAll = paginator.get_page(page)

    context = {
        'listings': paged_listingsAll
    }

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):

    # If it doesn't exist it will return 404
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)


def search(request):

    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords in the search form
    if 'Motcle' in request.GET:
        Motcle = request.GET['Motcle']  # 'keywords' is the form field
        if Motcle:
            queryset_list = queryset_list.filter(
                description__icontains=Motcle)

    # Besoin
    if 'besoin' in request.GET:
        besoin = request.GET['besoin']
        if besoin:
            queryset_list = queryset_list.filter(besoin__iexact=besoin)

     # Bien
    if 'bien' in request.GET:
        bien = request.GET['bien']
        if bien:
            queryset_list = queryset_list.filter(bien__iexact=bien)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            # 'lte' can be used for "less than and equal to"
            queryset_list = queryset_list.filter(bedrooms__iexact=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            # 'lte' can be used for "less than and equal to"
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'besoin_choices': besoin_choices,
        'bien_choices': bien_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
