Title: Descargando torrents en modo paranoico con Transmission
Date: 2012-12-19 18:15
Author: Nacho Cano
Tags: bittorrent, dht, p2p, pex, privacidad, torrent, transmission
Slug: descargando-torrents-en-modo-paranoico-con-transmission

Si utilizamos Transmission para descargar _torrents_ podemos activar dos
características interesantes: cifrado de la conexión y uso de listas de
bloqueo de IPs.

![Preferencias del Transmission]({static}/images/preferencias-transmission-300x173.png)

Vamos al menú Editar > Preferencias > Privacidad:

-   Lista de bloqueos
    -   Activar lista de bloqueo:
        <http://list.iblocklist.com/?list=bt_level1&fileformat=p2p&archiveformat=gz>
    -   Activar actualizaciones automáticas
-   Privacidad
    -   Modo de cifrado: Requerir cifrado
    -   Usar PEX para buscar más pares
    -   Usar DHT para buscar más pares
    -   Usar el descubridor de pares locales para buscar más pares

* * * * *

#### Actualizado el 12 de abril de 2015

En las versiones actuales de Transmission, las opciones de PEX y DHT
están en la pestaña de Red.

* * * * *

Las listas de bloqueo se pueden obtener de [iblocklist.com][]. Éste es
un servicio que recopila listados de IPs, disponibles en diferentes
formatos, y que puede utilizarse con varios programas, incluyendo
gestores de descargas, para bloquear dichas direcciones.

Una de las listas más utilizadas es [ésta][]. Contiene un listado de IPs
asociadas a gobiernos, compañías u organizaciones en contra de la
compartición de archivos y de las redes P2P.

Por otro lado, DHT se utiliza para encontrar direcciones IP de las que
descargar los mismos archivos sin comunicárselo al rastreador central.
Asímismo, PEX también se utiliza para encontrar direcciones IP
consultando a direcciones IP a las que ya estemos conectados.

Referencias
-----------

» [¿El futuro de BitTorrent? DHT, PEX y Enlaces Magnéticos
explicados.][]

  [iblocklist.com]: http://iblocklist.com
    "iblocklist.com"
  [ésta]: http://www.iblocklist.com/list.php?list=bt_level1
    "ésta"
  [¿El futuro de BitTorrent? DHT, PEX y Enlaces Magnéticos explicados.]:
    http://www.bittorrentyp2p.com/%C2%BFel-futuro-de-bittorrent-dht-pex-y-enlaces-magneticos-explicados
