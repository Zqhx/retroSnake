"""
Author: Arron Poucher

This file contains a system for more performant and programmer-firendly
text rendering with PyGame.
"""

import pygame
from pygame.locals import *
from pygame.color import THECOLORS as colour


class Memoize:
    """ Memoize callable object. """
    def __init__( self, func ):
        self.func = func
        self.memory = {}
    def __call__( self, *args ):
        if not args in self.memory:
            self.memory[args] = self.func( *args )
        return self.memory[args]


@Memoize
def loadFont( name, size ):
    """ Return PyGame font. """
    return pygame.font.SysFont( name, size )

@Memoize
def write( font, colour, text ):
    """ Return rendered text. """
    return font.render( text, 0, colour )

def printf( font, textColour, fmt, *items ):
    """ Return rendered text, supports c-like format string. """
    # Accept font object or 2-tuple
    if type( font ).__name__ == "tuple" and len( font ) == 2:
        font = loadFont( font[0], font[1] )
    elif not type( font ).__name__ == "Font":
        raise ValueError, "Expected 2-tuple or font object."
    if type( textColour ) == type( "" ):
        textColour = colour[textColour]
    lineSize = font.get_linesize()

    # Split string on newlines, substitute values
    lines = fmt.split( '\n' )
    place = 0
    for i in range( len( lines ) ):
        line = lines[i][:]
        lines[i] = line % tuple( items[place:place+line.count( '%' )] )

    # Render each line to a surface
    surfs = []
    for line in lines:
        surf = write( font, textColour, line )
        surfs.append( surf )

    # Blit each surface onto a new master surface
    finalW = max( [surf.get_rect().width for surf in surfs] )
    finalH = sum( [surf.get_rect().height for surf in surfs] )
    final = pygame.Surface( (finalW, finalH) )
    final.fill( colour["magenta"] )
    for i in range( len( surfs ) ):
        final.blit( surfs[i], (0,lineSize*i) )
    final.set_colorkey( colour["magenta"] )

    return final


if __name__ == "__main__":
    print "This is a library file, try running 'main.py' instead."

