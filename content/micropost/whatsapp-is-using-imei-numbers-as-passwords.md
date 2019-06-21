Title: WhatsApp is using IMEI numbers as passwords
Date: 2012-09-07 10:56
Author: Ignacio Cano
Slug: whatsapp-is-using-imei-numbers-as-passwords

> As you probably already heard in recent news, 1,000,001 Apple UDID’s
> were leaked. It’s unfortunate that so many apps use UDID’s to identify
> users since it’s extremely insecure.
>
> This brings me to WhatsApp, a free messaging service, used by millions
> of people. Their system runs on a modified version of XMPP (Extensible
> Messaging and Presence Protocol). There is nothing wrong with using
> XMPP, but there is a problem in how WhatsApp handle authentication.
>
> If you installed WhatsApp on an Android device for example, your
> password is likely to be an inverse of your phones IMEI number with an
> MD5 cryptographic hash thrown on top of it (without salt).
>
>     md5(strrev(’your-imei-goes-here’))

- Sam Granger | [samgranger.com][]

  [samgranger.com]: http://samgranger.com/whatsapp-is-using-imei-numbers-as-passwords/
    "WhatsApp is using IMEI numbers as passwords"
