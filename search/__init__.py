from geonode.contrib.dynamic.models import ModelDescription
from django.contrib.gis.geos import Polygon
from django.db import connection

from geonode.api.resourcebase_api import CommonModelApi

cursor = connection.cursor()

def filter_bbox(self, queryset, bbox):
    """
    modify the queryset q to limit to data that intersects with the
    provided bbox

    bbox - 4 tuple of floats representing 'southwest_lng,southwest_lat,
    northeast_lng,northeast_lat'
    returns the modified query
    """

    bbox = [float(coord) for coord in bbox.split(',')]
    search_box = Polygon.from_bbox(bbox)
    for model in ModelDescription.objects.all():
        django_model = model.get_django_model()
        
        sql = """SELECT "{layername}"."fid" FROM "{layername}" \
                 WHERE ST_Intersects("{layername}"."the_geom", ST_Transform(ST_GeomFromEWKT('srid=4326;{bbox_ewkt}'), \
                {projection})) LIMIT 1;""".format(
                                layername=model.name,
                                bbox_ewkt=search_box.ewkt,
                                projection=django_model.objects.first().the_geom.srid
                                )
        try:
            cursor.execute(sql)

            if not cursor.fetchone():
                queryset = queryset.exclude(id=model.layer_id)
        except:
            pass

    return queryset

CommonModelApi.filter_bbox = filter_bbox