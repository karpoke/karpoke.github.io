Title: namebench, benchmarking de servidores DNS
Date: 2011-08-01 19:40
Author: Nacho Cano
Tags: API, benchmarking, dns, google, google chart api
Slug: namebench-benchmarking-de-servidores-dns

Mediante [`namebench`][namebench] se puede comprobar la velocidad de nuestros
DNSs y compararla con los servidores DNS de Google y los mejores
servidores DNS que pueda encontrar para nuestra localización. Para
realizar las pruebas, se utiliza un listado compuesto por los dominios
más visitados según el ranking de Alexa y las páginas visitadas que se
encuentren en el historial de nuestro navegador, incluyendo a Firefox o
Chromium. Tiene la opción de poder [utilizarse desde el terminal][].

Lo descargarmos, instalamos y ejecutamos, en este caso, en un entorno
gráfico:

    $ wget https://namebench.googlecode.com/files/namebench-1.3.1-source.tgz
    $ tar xvzf namebench-1.3.1-source.tgz
    $ namebench-1.3.1/namebench.py

Para ejecutarlo desde el terminal, debemos pasarle el argumento `-x`.
Además, vamos a utilizar el listado de servidores DNS de la página
[adslayuda.com][]:

    $ namebench-1.3.1/namebench.py -x $(w3m -dump http://www.adslayuda.com/dns.html | grep -Eo '([0-9]{1,3}\.){3}[0-9]' | sort -t. -nk1 -nk2 -nk3 -nk4 | tr '\n' ' ')

Esta es la lista final con la que se realizará el _benchmarking_:

    Final list of nameservers considered:
    ------------------------------------------------------------------------------
    192.168.5.1     Internal 192-5-1   39  ms | twitter.com appears incorrect: 199.59.149.198, static.ak.fbcdn.net appears incorrect: 62.208.24.72
    62.151.2.8      Ya.com ES          60  ms | twitter.com appears incorrect: 199.59.148.10, 199.59.149.198, 199.59.149.230, www.paypal.com is hijacked: 173.0.84.2, 173.0.84.34, 173.0.88.2, 173.0.88.34
    212.36.64.16    ADAM ES            61  ms | twitter.com appears incorrect: 199.59.148.10, 199.59.149.198, 199.59.149.230, www.paypal.com is hijacked: 173.0.84.2, 173.0.84.34, 173.0.88.2, 173.0.88.34
    213.172.33.35   NeoSky-2 ES        63  ms | twitter.com appears incorrect: 199.59.149.230, 199.59.149.198, 199.59.148.82, www.paypal.com is hijacked: 173.0.84.2, 173.0.84.34, 173.0.88.2, 173.0.88.34
    80.58.0.33      SYS-80.58.0.33     64  ms | www.paypal.com is hijacked: 173.0.84.2, 173.0.84.34, 173.0.88.2, 173.0.88.34, twitter.com appears incorrect: 199.59.149.198, 199.59.148.10, 199.59.149.230
    8.8.4.4         Google Public DNS- 68  ms | Replica of Google Public DNS [8.8.8.8], www.facebook.com appears incorrect: 69.171.228.11, www.paypal.com is hijacked: 173.0.84.2, 173.0.84.34, 173.0.88.2, 173.0.88.34, twitter.com appears incorrect: 199.59.149.198, 199.59.148.82, 199.59.149.230
    208.67.222.222  OpenDNS-2          71  ms | twitter.com appears incorrect: 199.59.149.230, 199.59.149.198, 199.59.148.82, www.facebook.com appears incorrect: 69.171.229.16, www.paypal.com is hijacked: 173.0.84.2, 173.0.84.34, 173.0.88.2, 173.0.88.34
    156.154.70.1    UltraDNS           80  ms | twitter.com appears incorrect: 199.59.149.198, 199.59.148.10, 199.59.148.82, NXDOMAIN Hijacking, www.paypal.com is hijacked: 173.0.84.2, 173.0.84.34, 173.0.88.2, 173.0.88.34
    216.146.36.36   DynGuide-2         90  ms | www.facebook.com appears incorrect: 69.171.242.13, NXDOMAIN Hijacking, twitter.com appears incorrect: 199.59.149.230, 199.59.148.82, 199.59.148.10, www.paypal.com is hijacked: 173.0.88.34, 173.0.84.2, 173.0.84.34, 173.0.88.2
    195.5.64.2      landsraad ES       96  ms | twitter.com appears incorrect: 199.59.149.230, 199.59.148.82, 199.59.149.198, www.paypal.com is hijacked: 173.0.84.2, 173.0.84.34, 173.0.88.2, 173.0.88.34
    195.5.64.6      195.5.64.6         98  ms | twitter.com appears incorrect: 199.59.148.82, 199.59.149.198, 199.59.149.230, www.paypal.com is hijacked: 173.0.88.2, 173.0.88.34, 173.0.84.2, 173.0.84.34

El tiempo de respuesta más rápido:

    Fastest individual response (in milliseconds):
    ----------------------------------------------
    Internal 192-5-1 ## 1.75309
    Adam-2 ES        ############################# 44.50703
    landsraad ES     ################################### 53.90787
    Telefonica Movis #################################### 55.42493
    Ya.com ES        ##################################### 56.76293
    SYS-80.58.0.33   ##################################### 56.80299
    195.5.64.6       ########################################## 64.96215
    Google Public DN ############################################ 67.76404
    UltraDNS         ############################################## 70.23096
    OpenDNS-2        ############################################## 70.60385
    DynGuide-2       ##################################################### 82.16095

El tiempo medio de respuesta:

    Mean response (in milliseconds):
    --------------------------------
    Internal 192-5-1 ############### 59.90
    Ya.com ES        ###################### 91.22
    Google Public DN ######################### 102.36
    UltraDNS         ############################## 122.45
    DynGuide-2       ################################ 131.89
    OpenDNS-2        ################################ 133.27
    SYS-80.58.0.33   ###################################### 155.00
    Adam-2 ES        ###################################### 157.71
    Telefonica Movis ####################################### 159.40
    landsraad ES     ######################################## 164.57
    195.5.64.6       ###################################################### 221.42

Este el gráfico mostrado utilizando la API de Google:

![Google API](http://chart.apis.google.com/chart?cht=lxy&chs=720x415&chxt=x,y&chg=10,20&chxr=0,0,3500|1,0,100&chd=t:0,2,2,2,2,2,2,2,2,2,3,3,3,4,4,6,8,45|0,0,13,25,30,47,59,62,67,70,75,79,82,86,90,93,97,100|0,2,2,2,2,2,2,3,3,3,4,4,5,5,6,7,7,8,9,14,65|0,0,7,22,38,43,47,52,56,60,63,67,70,74,78,82,86,90,93,97,100|0,2,2,2,2,2,2,2,3,4,4,4,5,6,7,8,8,8,9,10,11,12,14,18,62|0,0,5,16,24,30,34,37,41,45,48,52,56,60,64,68,72,75,79,82,86,90,93,97,100|0,2,2,2,2,3,3,3,3,4,5,5,6,7,8,10,18|0,0,5,22,49,60,64,68,71,75,79,82,86,90,93,97,100|0,2,2,2,2,2,3,3,3,3,4,5,5,6,7,8,10,14,21|0,0,17,39,50,54,58,62,65,69,73,76,80,84,88,91,95,98,100|0,2,2,2,2,2,2,3,3,3,3,4,4,5,5,6,7,10,14,14|0,0,12,33,46,50,54,58,62,66,69,73,76,81,84,89,92,96,100,100|0,2,2,2,2,2,2,2,2,3,3,5,6,8,29|0,0,5,24,49,61,68,75,78,82,86,89,93,97,100|0,2,2,2,2,2,2,3,3,3,4,5,6,6,7,7,8,9,11,12,18,39|0,0,16,32,40,44,47,51,55,59,62,66,70,73,77,80,84,88,91,95,98,100|0,1,1,1,1,1,2,2,2,2,2,3,3,3,4,5,5,6,6,7,7,8,10,11,16,52|0,0,6,16,20,25,29,33,38,42,46,50,54,57,61,65,69,72,76,80,84,88,91,95,98,100|0,0,0,2,2,2,2,2,2,2,3,5,11|0,0,15,26,47,60,73,80,86,89,93,96,100|0,2,2,2,2,2,2,3,3,3,4,4,4,4,5,6,6,6,7,8,9,11,100|0,0,6,24,30,35,39,43,47,50,54,58,62,66,70,74,78,82,86,89,93,96,100&chco=ff9900,1a00ff,ff00e6,80ff00,00e6ff,fae30a,BE81F7,9f5734,000000,ff0000,3090c0&chxt=x,y,x,y&chxl=2:||Duration+in+ms||3:||%25|&chdl=Google+Public+DNS|SYS-80.58.0.33|195.5.64.6|DynGuide-2|OpenDNS-2|UltraDNS|Ya.com+ES|landsraad+ES|Adam-2+ES|Internal+192-5-1|Telefonica+Movistar-2+ES)


Recomendación final:

    Recommended configuration (fastest + nearest):
    ----------------------------------------------
    nameserver 192.168.5.1     # Internal 192-5-1
    nameserver 212.36.64.17    # Adam-2 ES
    nameserver 212.73.32.3     # Vodafone/Airtel ES

  [namebench]: http://code.google.com/p/namebench/
    "namebench"
  [utilizarse desde el terminal]: http://code.google.com/p/namebench/wiki/UsingNameBenchCommandLine
    "utilizarse desde el terminal"
  [adslayuda.com]: http://www.adslayuda.com/dns.html
    "adslayuda.com"
