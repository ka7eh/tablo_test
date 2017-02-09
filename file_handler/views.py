from django.core.urlresolvers import reverse_lazy
from django.db import connection
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.views import generic

from tablo.models import FeatureService

from .forms import ImportForm
from .models import FileHolder


class ImportView(generic.FormView):
    template_name = 'upload.html'
    form_class = ImportForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


class ListView(generic.ListView):
    template_name = 'list.html'
    model = FileHolder
    context_object_name = 'files'


class AccessView(generic.TemplateView):
    template_name = 'access.html'

    def get(self, request, *args, **kwargs):
        obj = FileHolder.objects.get(id=self.kwargs['pk'])
        response = HttpResponse(obj.file.read(), content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(obj.file.name)
        return response


class DatasetView(generic.TemplateView):
    template_name = 'datasets.html'

    def get_context_data(self, **kwargs):
        ctx = super(DatasetView, self).get_context_data(**kwargs)
        q = """
          SELECT table_name, find_srid('public', table_name, 'dbasin_geom')
          FROM information_schema.tables
          WHERE table_type = 'BASE TABLE' AND table_name LIKE 'db_%'
        """

        with connection.cursor() as c:
            c.execute(q)
            dataset_names = c.fetchall()
            ctx['datasets'] = map(
                lambda d: {
                    'name': d[0],
                    'feature_service': self._get_dataset_featureservice(d[0]),
                    'srid': d[1],
                    'geom_type': self._get_geom_type(d[0])
                },
                dataset_names
            )
        return ctx

    def _get_dataset_featureservice(self, dataset):
        try:
            return FeatureService.objects.get(featureservicelayer__table=dataset).id
        except FeatureService.DoesNotExist:
            return

    def _get_geom_type(self, table):
        with connection.cursor() as c:
            q = 'SELECT GeometryType(dbasin_geom) FROM {table} LIMIT 1'
            c.execute(q.format(table=table))
            return c.fetchall()[0][0]


class AddFeatureView(generic.TemplateView):
    template_name = 'add_feature.html'
