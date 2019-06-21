Title: Caching with Twemcache
Date: 2012-07-11 00:36
Author: Ignacio Cano
Slug: caching-with-twemcache

> We built Twemcache because we needed a more robust and manageable
> version of Memcached, suitable for our large-scale production
> environment. Today, we are open-sourcing Twemcache under the New BSD
> license. As one of the largest adopters of Memcached, a popular open
> source caching system, we have used Memcached over the years to help
> us scale our ever-growing traffic. Today, we have hundreds of
> dedicated cache servers keeping over 20TB of data from over 30
> services in-memory, including crucial data such as user information
> and Tweets. Collectively these servers handle almost 2 trillion
> queries on any given day (that’s more than 23 million queries per
> second). As we continued to grow, we needed a more robust and
> manageable version of Memcached suitable for our large scale
> production environment.
>
> We have been running Twemcache in production for more than a year and
> a half. Twemcache is based on a fork of Memcached v1.4.4 that is
> heavily modified to improve maintainability and help us monitor our
> cache servers better. We improved performance, removed code that we
> didn’t find necessary, refactored large source files and added
> observability related features. The following sections will provide
> more details on why we did this and what those new features are.

- Chris Aniszczyk | [engineering.twitter.com][]

  [engineering.twitter.com]: http://engineering.twitter.com/2012/07/caching-with-twemcache.html
    "Caching with Twemcache"
