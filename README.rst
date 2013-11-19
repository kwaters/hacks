marginal hacks
==============

A dumping ground for various sundry hacks.

To quote jwz,

  The following are mostly small utility scripts, rather than full-fledged
  applications. These are tools that I wrote for myself to fill a personal
  need.  This means that they are not necessarily very polished, but possibly
  you'll find some of them useful. Please take most them in the context of
  "one-hour hacks that have lived on far longer than expected."

gb-logic-decoder
----------------

A frame decoder to parse the logic analyser dump from
http://flashingleds.wordpress.com/2010/10/26/intercepting-the-gameboy-lcd/.
Mostly an excuse to play with NumPy.

tsuro
-----

List the unique tiles in the boardgame Tsuro.  I don't think there is an "easy"
way to compute this numer, because neither the tiles nor the rotations are
normal subgroups of P_8.  Then again my algebra is poor.

unpack-rftg.py
--------------

Unpack the images from http://www.keldon.net/rftg/ so I can read the cards.

link-a-pix.py
-------------

Link-a-pix solver.  Works by reducing the problem to exact cover.

ff-13-2-clock
-------------

Solver for the Clock puzzle in FF XIII-2.  There are many like it, but this one's mine.

toposort
--------

Playing with a basic topological sort.  Outputs random graphs in .dot format.
