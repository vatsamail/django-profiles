from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from core.forms import HomeForm


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get(self, request):
        form = HomeForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            return redirect('ui:profile')
            args = {'form': form, 'text': text}
            return render(request, self.template_name, args)
