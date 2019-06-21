Title: f2fs: introduce flash-friendly file system
Date: 2012-10-06 13:54
Author: Nacho Cano
Slug: f2fs-introduce-flash-friendly-file-system

> NAND flash memory-based storage devices, such as SSD, eMMC, and SD
> cards, have
>  been widely being used for ranging from mobile to server systems.
> Since they are
>  known to have different characteristics from the conventional
> rotational disks,
>  a file system, an upper layer to the storage device, should adapt to
> the changes
>  from the sketch.
>
> F2FS is a new file system carefully designed for the NAND flash
> memory-based storage
>  devices. We chose a log structure file system approach, but we tried
> to adapt it
>  to the new form of storage. Also we remedy some known issues of the
> very old log
>  structured file system, such as snowball effect of wandering tree and
> high cleaning
>  overhead.
>
> Because a NAND-based storage device shows different characteristics
> according to
>  its internal geometry or flash memory management scheme aka FTL, we
> add various
>  parameters not only for configuring on-disk layout, but also for
> selecting allocation
>  and cleaning algorithms.

- Jaegeuk Kim | [lkml.org][]

  [lkml.org]: https://lkml.org/lkml/2012/10/5/205
    "f2fs: introduce flash-friendly file system"
