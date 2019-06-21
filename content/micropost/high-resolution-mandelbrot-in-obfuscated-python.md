Title: High-Resolution Mandelbrot in Obfuscated Python
Date: 2013-01-06 01:40
Author: Ignacio Cano
Slug: high-resolution-mandelbrot-in-obfuscated-python

> Here’s a followup to last month’s post about Penrose Tiling in
> Obfuscated Python.
> The Mandelbrot set is a traditional favorite among authors of
> obfuscated code. You can find obfuscated code in C, Perl, Haskell,
> Python and many other languages. Nearly all examples render the
> Mandelbrot set as ASCII art.
>  The following Python script, on the other hand, begins as ASCII art:
>
>
> ```python
> _                                      =   (
>                                         255,
>                                       lambda
>                                V       ,B,c
>                              :c   and Y(V*V+B,B,  c
>                                -1)if(abs(V)&lt;6)else
>                (              2+c-4_abs(V)*_-0.4)/i
>                  )  ;v,      x=1500,1000;C=range(v*x
>                   );import  struct;P=struct.pack;M,\
>             j  ='<qiihhhh ',open('M.bmp','wb').write
> for X in j('BM'+P(M,v_x_3+26,26,12,v,x,1,24))or C:
>             i  ,Y=_;j(P('BBB',_(lambda T:(T_80+T__9
>                   _i-950_T  **99,T*70-880*T*_18+701_
>                  T  __9     ,T*i**(1-T*_45_2)))(sum(
>                [              Y(0,(A%3/3.+X%v+(X/v+
>                                A/3/3.-x/2)/1j)*2.5
>                              /x   -2.7,i)**2 for  \
>                                A       in C
>                                       [:9]])
>                                         /9)
>                                        )   )
> ```
>
> » Jeff Preshing | [preshing.com][]

  [preshing.com]: http://preshing.com/20110926/high-resolution-mandelbrot-in-obfuscated-python
    "High-Resolution Mandelbrot in Obfuscated Python"
