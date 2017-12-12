from django.views.generic import DetailView

from soins_app.models.soins import Soin

class SoinDetailView(DetailView):
    """This class is based on DetailView special feature in Django"""
    model = Soin #This view is based on the model Nurse
    template_name = "soin_detail.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(SoinDetailView, self).get_context_data(**kwargs)
        return context