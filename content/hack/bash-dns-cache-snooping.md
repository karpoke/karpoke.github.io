Title: Bash DNS Cache Snooping
Date: 2010-09-25 04:21
Author: Nacho Cano
Tags: dig, dns cache snooping, identificación de servicios, nslookup, script
Slug: bash-dns-cache-snooping

__DNS Cache Snooping__ consiste en realizar una serie de peticiones de
resolución de nombres de dominio a la caché de un servidor DNS, con la
finalidad de conocer si los usuarios de ese servidor han visitado esos
dominios. Hay que tener en cuenta que las entradas en la caché tienen un
tiempo de caducidad, y si durante ese tiempo no ha habido una petición a
un dominio, éste es eliminado.

Para conocer qué servidores DNS hay bajo un dominio:

    $ nslookup -type=ns google.com

    Server:     192.168.1.1
    Address:    192.168.1.1#53

    Non-authoritative answer:
    google.com  nameserver = ns2.google.com.
    google.com  nameserver = ns1.google.com.
    google.com  nameserver = ns4.google.com.
    google.com  nameserver = ns3.google.com.

    Authoritative answers can be found from:
    ns4.google.com  internet address = 216.239.38.10
    ns1.google.com  internet address = 216.239.32.10
    ns3.google.com  internet address = 216.239.36.10
    ns2.google.com  internet address = 216.239.34.10

Del resultado, nos interesará los que vienen identificados como
_nameserver_, por ejemplo, `ns1.google.com`.

Para saber si algún usuario que realiza las peticiones de resolución de
nombres a este DNS ha visitado una página concreta, por ejemplo
`yahoo.com`:

    $ nslookup -type=a -norecurse yahoo.com ns1.google.com

    Server:     ns3.google.com
    Address:    216.239.36.10#53
    ** server can’t find yahoo.es: REFUSED

En este caso, Google bloquea este tipo de peticiones. Probemos con el
servidor DNS de otro dominio:

    $ nslookup -type=a -norecurse yahoo.com ns1.renfe.es

    Server:     ns1.renfe.es
    Address:    213.144.33.254#53
    Non-authoritative answer:
    _*_ Can’t find yahoo.com: No answer

Este servidor sí ha respondido: nadie ha visitado `yahoo.com`, al menos
en el tiempo de caducidad de una entrada en la caché del servidor DNS.
Hacemos una prueba más:

    $ nslookup -type=a -norecurse google.com ns1.renfe.es

    Server:     ns1.renfe.es
    Address:    213.144.33.254#53

    Non-authoritative answer:
    Name:   google.com
    Address: 74.125.39.106
    Name:   google.com
    Address: 74.125.39.147
    Name:   google.com
    Address: 74.125.39.99
    Name:   google.com
    Address: 74.125.39.103
    Name:   google.com
    Address: 74.125.39.104
    Name:   google.com
    Address: 74.125.39.105

Ahora sí, vemos que `google.com` sí ha sido visitado.

Vamos a automatizar el proceso de comprobación de cada página en el
script `dns-cache-snooping.sh`. Primero, supongamos que tenemos un
fichero con una [lista de páginas][] a comprobar. La metemos en una
lista:

    $ urls=()
    $ f="sites.txt"
    $ if [ -r $f ]; then
    >     while read line; do
    >         urls+=( $line )
    >     done > "$f"
    > fi

Recorrermos la lista realizando las peticiones y mostrando el resultado
en verde o rojo, según si ha sido encontrada la página en la caché o no:

    $ ns=ns1.renfe.es
    $ for url in ${urls[*]}; do
    >     if [ -n "$(nslookup -type=a -norecurse $url $ns | grep 'Name:')" ]; then
    >         echo $url
    >     fi
    > done

- Inspirado en un artículo de [El maligno][]
- Más información: [DNS Cache Snooping][]

  [lista de páginas]: http://terminus.ignaciocano.com/wp-uploads/linked/sites.txt
    "lista de páginas"
  [El maligno]: http://elladodelmal.blogspot.com/2010/07/foca-dns-cache-snooper.html
    "El maligno"
  [DNS Cache Snooping]: http://www.rootsecure.net/content/downloads/pdf/dns_cache_snooping.pdf
    "DNS Cache Snooping"
