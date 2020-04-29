Title: Automating with convention: Introducing sub
Date: 2012-10-28 12:38
Author: Nacho Cano
Slug: automating-with-convention-introducing-sub

> When I started my on-call shifts, we had pretty little in the way of
> automation for day-to-day issues. Tasks like SSH’ing into our cluster,
> starting a Rails console, or doing a deep search through our gigantic
> mail directories, were either shelved away in someone’s bashrc,
> history log, or just ingrained into someone’s memory. This pain was
> also felt by a few other of my fellow programmers, and we started
> cobbling together a Git repo simply named ”37s shell scripts”.
>
> This repo started very innocently: a little Ruby script named console
> that mapped a product name (basecamp) to a server name inside of our
> cluster (jobs-03), SSH’d in, and then ran a production Rails console.
> Several more bash and Ruby scripts started to trickle in as we started
> to share more of our personal code that we used when on-call.
> Eventually Sam laid down a foundation of bash scripts and directories
> borrowed from rbenv, and dubbed it ”37”.

» Nick | [37signals.com][]

  [37signals.com]: https://37signals.com/svn/posts/3264-automating-with-convention-introducing-sub
    "Automating with convention: Introducing sub"
