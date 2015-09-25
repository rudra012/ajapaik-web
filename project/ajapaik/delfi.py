from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.core.urlresolvers import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from project.ajapaik.forms import DelfiBboxRequestForm
from project.ajapaik.models import Photo
from django.contrib.gis.geos import Point


@api_view(['GET'])
@permission_classes((AllowAny,))
def photos_bbox(request):
    form = DelfiBboxRequestForm(request.query_params)
    if form.is_valid():
        qs = Photo.objects.filter(rephoto_of__isnull=True, lat__isnull=False, lon__isnull=False,
                                  lat__gte=form.cleaned_data['top_left'].y,
                                  lon__gte=form.cleaned_data['top_left'].x,
                                  lat__lte=form.cleaned_data['bottom_right'].y,
                                  lon__lte=form.cleaned_data['bottom_right'].x
        )
        our_ref = SpatialReference(4326)
        delfi_ref = SpatialReference(3301)
        trans = CoordTransform(our_ref, delfi_ref)
        photos = []
        for p in qs:
            location = Point(x=p.lon, y=p.lat, srid=4326)
            location.transform(trans)
            photos.append({
                'latitude': location.y,
                'longitude': location.x,
                'url': request.build_absolute_uri(reverse('project.ajapaik.views.photoslug', args=(p.id, p.get_pseudo_slug()))),
                'thumbUrl': request.build_absolute_uri(reverse('project.ajapaik.views.photo_thumb', args=(p.id, 400)))
            })

        return Response(photos)

    return Response([])