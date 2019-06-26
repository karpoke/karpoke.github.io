Title: ls sin ls
Date: 2011-03-12 13:11
Author: Nacho Cano
Tags: c, closedir, ctypes, generador, listdir, opendir, python, yield
Slug: ls-sin-ls

En bash:

```bash
$ for i in *; do echo $i; done
```

![ls]({static}/images/ls-300x232.jpg)

<small>_Fuente: [nfosolutions.com][]_</small>

En [C][]:

```c
/*
 *
 * Esempio che scansiona una cartella stampando a video i file in essa
 * contenuti.
 */

#include
#include
#include
#include

int main(int argc, char *argv[])
{
    DIR *dir;
    struct dirent *drent;

    if(argc < 2)
    {
        fprintf(stderr, "%s \n", argv[0]);
        return EXIT_FAILURE;
    }

    if((dir = opendir(argv[1])) == NULL)
    {
        fprintf(stderr, "Errore opendir()\n");
        return EXIT_FAILURE;
    }

    while((drent = readdir(dir)) != NULL)
    {
        fprintf(stdout, "--> %s\n", drent->d_name);
    }

    if(closedir(dir) < 0)
    {
        fprintf(stderr, "Errore closedir()\n");
        return EXIT_FAILURE;
    }
}
```

En Python:

```python
import os
def ls(d):
   if os.path.isdir(d):
      for f in os.listdir(d):
         print "%s%s" % (f, "/" if os.path.isdir(f) else "")
```

En Python utilizando un generador que devuelve un [resultado cada vez][]:

```python
import subprocess
def listdirx(dirname='.', cmd='ls'):
    proc = subprocess.Popen([cmd, dirname], stdout=subprocess.PIPE)
    filename = proc.stdout.readline()
    while filename != '':
        yield filename.rstrip('\n')
        filename = proc.stdout.readline()
    proc.communicate()
```

Una [alternativa][] a `listdir` usando `ctypes` y `opendir, readdir`:

```python
#!/usr/bin/python
"""
An equivalent os.listdir but as a generator using ctypes
"""

from ctypes import CDLL, c_char_p, c_int, c_long, c_ushort, c_byte, c_char, Structure, POINTER
from ctypes.util import find_library

class c_dir(Structure):
    """Opaque type for directory entries, corresponds to struct DIR"""
    pass

class c_dirent(Structure):
    """Directory entry"""
    # FIXME not sure these are the exactly correct types!
    _fields_ = (
        ('d_ino', c_long), # inode number
        ('d_off', c_long), # offset to the next dirent
        ('d_reclen', c_ushort), # length of this record
        ('d_type', c_byte), # type of file; not supported by all file system types
        ('d_name', c_char * 4096) # filename
        )
c_dirent_p = POINTER(c_dirent)

c_lib = CDLL(find_library("c"))
opendir = c_lib.opendir
opendir.argtypes = [c_char_p]
opendir.restype = c_dir_p

# FIXME Should probably use readdir_r here
readdir = c_lib.readdir
readdir.argtypes = [c_dir_p]
readdir.restype = c_dirent_p

closedir = c_lib.closedir
closedir.argtypes = [c_dir_p]
closedir.restype = c_int

def listdir(path):
    """
    A generator to return the names of files in the directory passed in
    """
    dir_p = opendir(".")
    try:
        while True:
            p = readdir(dir_p)
            if not p:
                break
            name = p.contents.d_name
            if name not in (".", ".."):
                yield name
    finally:
        closedir(dir_p)

if __name__ == "__main__":
    for name in listdir("."):
        print name
```

  [nfosolutions.com]: http://nfosolutions.com/
    "nfosolutions.com"
  [C]: http://snippets.dzone.com/posts/show/2735
    "C"
  [resultado cada vez]: http://stackoverflow.com/questions/4403598/list-files-in-a-folder-as-a-stream-to-begin-process-immediately
    "resultado cada vez"
  [alternativa]: http://stackoverflow.com/questions/4403598/list-files-in-a-folder-as-a-stream-to-begin-process-immediately/4403746#4403746
    "alternativa"
