Title: Moving persistent data out of Redis
Date: 2017-01-14 14:36
Author: Nacho Cano
Tags: caché, LRU, Redis, datos persistentes, datos temporales
Slug: moving-persistent-data-out-of-redis

> Transitioning all that information transparently involved planning and
> coordination. For each problem domain using persistent Redis, we considered
> the volume of operations, the structure of the data, and the different access
> patterns to predict the impact on our current MySQL capacity, and the need
> for provisioning new hardware.
>
> For the majority of callsites, we replaced persistent Redis with GitHub::KV,
> a MySQL key/value store of our own built atop InnoDB, with features like key
> expiration. We were able to use GitHub::KV almost identically as we used
> Redis: from trending repositories and users for the explore page, to rate
> limiting to spammy user detection.

» Bryana Knight and Miguel Fernández | [github.com][]

  [github.com]: http://githubengineering.com/moving-persistent-data-out-of-redis/
    "Moving persistent data out of Redis"
