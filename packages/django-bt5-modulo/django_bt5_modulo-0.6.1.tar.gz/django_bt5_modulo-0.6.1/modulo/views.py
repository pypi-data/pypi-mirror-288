from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView

from modulo.clases.select2 import Select2JSONResponseMixin
from modulo.clases.table_lista import TableListView
from modulo.forms import TestDataForm
from modulo.models import TestData


# Create your views here.

class SuccessView(View):

    def get(self, request, pk):
        return JsonResponse({
            "success": True,
            "mensaje": "Guardado Correctamente",
            "pk": pk
        })


class HomeView(TemplateView):
    template_name = "modulo/test/vista.html"


class ListaView(ListView):
    model = TestData
    template_name = "modulo/test/lista.html"
    paginate_by = 5
    ordering = ['id']

    def get_queryset(self):
        query = super(ListaView, self).get_queryset()
        search = self.request.GET.get("search")
        pagination = self.request.GET.get("pagination")
        if pagination:
            self.paginate_by = int(pagination)
        if search:
            query = query.filter(
                Q(name__icontains=search)
            )
        return query


class TableListaView(TableListView):
    model = TestData
    template_name = "modulo/test/table_lista.html"
    paginate_by = 5
    ordering = ['id']
    headers = ['Nombre', "Activo"]

    def get_queryset(self):
        query = super(TableListView, self).get_queryset()
        search = self.request.GET.get("search")
        pagination = self.request.GET.get("pagination")
        if pagination:
            self.paginate_by = int(pagination)
        if search:
            query = query.filter(
                Q(name__icontains=search)
            )
        return query


class CrearView(CreateView):
    model = TestData
    form_class = TestDataForm
    template_name = "modulo/formulario/formulario.html"


class Crear2View(CreateView):
    model = TestData
    form_class = TestDataForm
    template_name = "modulo/test/form.html"


class EditarView(UpdateView):
    model = TestData
    form_class = TestDataForm
    template_name = "modulo/formulario/formulario.html"


class EliminarView(DeleteView):
    model = TestData
    template_name = "modulo/formulario/eliminar.html"
    success_url = reverse_lazy('modulo:success', kwargs={'pk': 0})


class ComboView(Select2JSONResponseMixin, TemplateView):
    model = TestData
    filters = ['name']

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class VistaMaterialView(TemplateView):
    template_name = 'modulo/test/material/vista_material.html'


class TablaComponetsView(View):
    def get(self, request):
        testdata = TestData.objects.all().order_by('id')
        page_number = request.GET.get("page")
        paginacion = request.GET.get("paginacion", 10)
        paginator = Paginator(testdata, paginacion)  # Show 25 contacts per page.
        page_obj = paginator.get_page(page_number)
        # print(page_obj.__dict__)
        rows = []
        for obj in page_obj:
            obj_data = {
                "id": obj.id,
                "name": obj.name,
                "is_enable": obj.is_enable,
            }
            rows.append(obj_data)
        pages = {
            "number ": page_obj.number,
            "num_pages ": page_obj.paginator.num_pages,
            "page_range": [page for page in page_obj.paginator.page_range],
            "has_previous": page_obj.has_previous(),
            "previous_page_number ": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "has_next": page_obj.has_next(),
            "next_page_number  ": page_obj.next_page_number() if page_obj.has_next() else None,
        }
        data = {
            "headers": ["Nombre", "Activo"],
            "rows": rows,
            "pages": pages,
        }
        return JsonResponse(data)
