from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from scraper.api_scraper.models import Details, DetailsTable


def home(request):
    print "got here"
    all_det = Details.objects.all().order_by('category')
    table = DetailsTable(all_det)
    return render(request, "single_table.html",
                  {'details_table': table})
    