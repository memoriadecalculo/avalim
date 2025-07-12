#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

from datetime                  import datetime
from django.shortcuts          import render
from django.views.generic.edit import FormView, View
from raspagem                  import forms, Raspador, VivaRealListaSimples

class Inicio(View):
    template_name = 'inicio.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class Raspagem(FormView):
    """Raspagem"""
    
    template_name = 'raspagem.html'
    form_class    = forms.Raspagem
    
    def form_valid(self, form):
        URL = form.cleaned_data['URL']
        iniPg = form.cleaned_data['iniPg']
        nPages = form.cleaned_data['nPages']
        params = form.cleaned_data['params']
        headers = form.cleaned_data['headers']
        
        Perfil = VivaRealListaSimples(url=form.cleaned_data['URL'], \
                                      arquivo='{0}.csv'.format(datetime.now().strftime("%Y%m%d%H%M%S")), \
                                      qtdPg=form.cleaned_data['nPages'], \
                                      iniPg=form.cleaned_data['iniPg'], \
                                      headers=form.cleaned_data['headers'], \
                                      params=form.cleaned_data['params'])
        raspador = Raspador(Perfil)
        lista = pd.DataFrame(raspador.get_pags())
        return render(self.request, self.template_name, {'lista': lista,})

