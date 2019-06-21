Title: Merge branch ’x86-nuke386-for-linus’
Date: 2012-12-16 13:41
Author: Nacho Cano
Tags: Linux, 386
Slug: merge-branch-x86-nuke386-for-linus

> Pull ”Nuke 386-DX/SX support” from Ingo Molnar: ”This tree removes
> ancient-386-CPUs support and thus zaps quite a bit of complexity:
>
> 24 files changed, 56 insertions(+), 425 deletions(-)
>
> ... which complexity has plagued us with extra work whenever we wanted to
> change SMP primitives, for years.
>
> Unfortunately there’s a nostalgic cost: your old original 386 DX33 system
> from early 1991 won’t be able to boot modern Linux kernels anymore. Sniff.”
>
> I’m not sentimental. Good riddance.

- Linus Torvalds | [git.kernel.org][]

  [git.kernel.org]: http://git.kernel.org/?p=linux/kernel/git/torvalds/linux.git;a=commit;h=743aa456c1834f76982af44e8b71d1a0b2a82e21
    "Merge branch 'x86-nuke386-for-linus'"
