Title: Encontrar los dominios que comparten IP con otro dado
Date: 2011-06-14 21:34
Author: Nacho Cano
Tags: bing, footprinting, ip, resolveip
Slug: encontrar-los-dominios-que-comparten-ip-con-otro-dado

Éste es algo viejuno, pero lo no había probado. Se trata del _script_
`bing-ip2hosts`, que permite [encontrar los dominios que comparten IP][]
con un dominio dado utilizando Bing:

    $ ./bing-ip2hosts -p ubuntu.com
    http://brainstorm.ubuntu.com
    http://kubuntu.org
    http://search.ubuntu.com
    http://www.ubuntu.com

Con el argumento `-p` se incluye el prefijo `http://`, lo cual viene bien
para poder clicar directamente en el terminal.

Este _script_ utiliza el comando `resolveip` para encontrar la IP del
dominio dado:

    $ resolveip google.com
    IP address of google.com is 209.85.146.147
    IP address of google.com is 209.85.146.99
    IP address of google.com is 209.85.146.104
    IP address of google.com is 209.85.146.106
    IP address of google.com is 209.85.146.103
    IP address of google.com is 209.85.146.105

    $ resolveip -s google.com
    209.85.229.147

Y parsea los resultados del buscador Bing pasándole como parámetro la IP
recién obtenida:

    http://m.bing.com/search/search.aspx?A=webresults&Q=ip%3a209.85.229.147&D=Web&SI=0

  [encontrar los dominios que comparten IP]: http://seifreed.com/2010/04/10/enumerar-todos-los-host-en-dominio-con-la-direccin-ip-bing/
    "encontrar los dominios que comparten IP"
