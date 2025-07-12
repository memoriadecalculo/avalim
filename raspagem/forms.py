#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from django.forms             import Form, Textarea
from django.forms.fields      import CharField, IntegerField, URLField

cabecalho = """{
"authority": "www.imovelweb.com.br",
"method": "GET",
"path": "https://www.imovelweb.com.br/apartamentos-venda-botafogo-rio-de-janeiro-ordem-publicado-maior.html",
"scheme": "https",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Accept-Language": "pt-BR,pt;q=0.9",
"Cache-Control": "max-age=0",
"content-length": "4931",
"content-type": "application/x-www-form-urlencoded",
"cookie": "__cf_bm=l91eBxITMyUFekNrKjVPU65xqbnpzwrJAPsJ2wEOCeY-1746484012-1.0.1.1-ZuqUEb3_wrFMP5PwDrfa7cllpKvpxw3BiJ0sHYc4RlLPRvI_xgQNbkZom19JrsjgvZLuuVUzJ3u8jHq5U_HE2rF7Dz0_gP8QGSLTrlUynbmm.dONYDOIHZ8UYIoaWeZS; _cfuvid=tZj9m3Fz8u7Z5aweAtWIFPUmLnTvGNi0gyuEllh_0jg-1746484012593-0.0.1.1-604800000; cf_clearance=vicO_T1MYharb3ip6sQ_.2mJSqZ8mS39PgbTMMgtBfg-1746484144-1.2.1.1-ACcxNNIYkJR9tv3Ho10IUt87nWSlfakN4GVbg8Hko8_gaAvL9cxkZXBO3MyYgAUW5TQ7Q4ot1xTyEIu_9FRlOads5fBCDcqhWcGMNoGyT13TcWJtOp_tq28XHaHMEUBtlgI9RUD.m98TGtUv5tnZgSyrFSCpVmsr5x9IjCr_T8m_wWfCkTorZb.GnWc0uf99GyPO2wNudYApTe3GCcjP4DN.ahi5x7f_5qTPety33wawEt9lr5XXdNM_XoAucW3D9Xxsw9lUvtHSMjgHsST0hoMrPp5jwvT3_Qz4y8QvUsEGUzL8R6xFI432vw5onZVIyzI8x7MMHPb8sqWX.FYTCuAvMpM1mZmxjrAOrSA4ccRBMDkIceK7yxVyEMgJ_RZb",
"origin": "https://www.imovelweb.com.br",
"priority": "u=0, i",
"referer": "https://www.imovelweb.com.br/apartamentos-venda-botafogo-rio-de-janeiro-ordem-publicado-maior.html",
"Sec-Ch-Ua": "'Not.A/Brand';v='99', 'Chromium';v='136'",
"sec-ch-ua-arch": "'x86'",
"sec-ch-ua-bitness": "'64'",
"sec-ch-ua-full-version": "'136.0.7103.49'",
"sec-ch-ua-full-version-list": "'Not.A/Brand';v='99.0.0.0', 'Chromium';v='136.0.7103.49'",
"Sec-Ch-Ua-Mobile": "?0",
"sec-ch-ua-model": "''",
"Sec-Ch-Ua-Platform": "'Linux'",
"sec-ch-ua-platform-version": "'6.11.0'",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User": "?1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}"""

class Raspagem(Form):
    URL     = URLField(initial="", required=True, label="URL", help_text="""Endereço da página do anúncio""")
    iniPg   = IntegerField(initial=1, required=True, label='Página Inicial', help_text="""Número da página inicial a raspar""")
    nPages  = IntegerField(initial=1, required=True, label='Total de Páginas', help_text="""Quantidade total de páginas a raspar""")
    params  = CharField(initial="", required=False, widget=Textarea)
    headers = CharField(initial=cabecalho,  required=True, widget=Textarea)
    
    def clean(self):
        data = super(Raspagem, self).clean()
        data['URL']  = data.pop("URL", "")
        data['iniPg']  = data.pop("iniPg", 1)
        data['nPages']  = data.pop("nPages", 1)
        data['params']  = data.pop("params", "")
        data['headers']  = json.loads(data.pop("headers", ""))
        return data

