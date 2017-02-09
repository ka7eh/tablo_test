from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from tablo.models import TemporaryFile, FeatureService


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['tablo_csv_files'] = TemporaryFile.objects.all()
        ctx['featureServices'] = FeatureService.objects.all()
        return ctx


class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        ctx = super(MapView, self).get_context_data(**kwargs)
        ctx['featureServiceUrl'] = reverse('fs_arcgis_featureservice', kwargs={'service_id': self.kwargs['id']})
        return ctx
