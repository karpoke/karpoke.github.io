Title: Iniciar sesión en DynDNS desde el terminal
Date: 2013-06-10 01:00
Author: Nacho Cano
Tags: dominio dinámico, dyndns, mechanize, python, script
Slug: iniciar-sesion-en-dyndns-desde-el-terminal
Related: asignar-la-ip-que-queramos-a-un-dominio-de-dyndns,dyndns-e-inadyn,subdominios-dinamicos-en-un-alojamiento-con-dominio-dinamico-en-ovh,arrancar-y-parar-instancias-minicloud-de-ovh-desde-el-terminal

Hace un par de semanas, DynDNS cambió su política de uso de las cuentas
gratuitas para incluir una cláusula por la cual es necesario hacer
mínimo un login al mes si no se quieren perder los dominios que
tengamos:

> Starting now, if you would like to maintain your free Dyn account, you
> must log into your account once a month. Failure to do so will result
> in expiration and loss of your hostname. This activity helps us
> eliminate hostnames that are no longer needed and/or dormant. Note
> that an update client will not suffice for this monthly login.

El siguiente _script_ permite iniciar sesión haciendo uso de la librería
`mechanize` para Python:

```python
#!/usr/bin/env python

import mechanize
import cookielib

LOGIN_URL = "https://account.dyn.com/entrance/"
USERNAME = "username"
PASSWORD = "password"

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Open some site, let's pick a random one, the first that pops in mind:
r = br.open(LOGIN_URL)
html = r.read()

# Select the second (index one) form
br.select_form(nr=1)
br.form["username"] = USERNAME
br.form["password"] = PASSWORD
br.submit()

if br.response().read().find(USERNAME) >= 0:
    print("OK")
else:
    print("KO")
```

* * * * *

#### Actualización a 22 de septiembre de 2013

Actualizada la URL en la que encontraremos el formulario de _login_.

* * * * *

Referencias
-----------

» [Emulating a Browser in Python with mechanize][]

  [Emulating a Browser in Python with mechanize]: http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/
    "Emulating a Browser in Python with mechanize"
