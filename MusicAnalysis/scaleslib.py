#!/usr/local/bin/python
""" Scaleslib.py
----------------------------
Author:    Luke Paireepinart
Copyright: Nico Schuler

Texas State University
Summer 2009
----------------------------
Brief Summary:  This is just a definition of all of the different scales the Scales program supports.
The scales are just stored in a dictionary with a mapping from scale name to a tuple containing
a list of the note steps (integers) as the first item and a list of filter keywords for the second.
"""
scales =    {
            'Major Scale'                          : ([2, 2, 1, 2, 2, 2, 1],    ["Classical","Jazz","Rock", "Pop"]),
            'Natural Minor Scale'                  : ([2, 1, 2, 2, 1, 2, 2],    ["Classical"]),
            'Minor Pentatonic Scale'               : ([3, 2, 2, 3, 2],          ["Classical"]),
            'Blues Scale'                          : ([3, 2, 1, 1, 3, 2],       ["Blues"]),
            'Harmonic Minor Scale'                 : ([2, 1, 2, 2, 1, 3, 1],    ["Jazz"]),
            'Half-Step-Minor-Third Scale'          : ([1, 3, 1, 3, 1, 3],       ["Classical"]),
            'Pentatonic Scale'                     : ([2, 2, 3, 2, 3],          ["Blues"]),
            'Octatonic-1 Scale'                    : ([1, 2, 1, 2, 1, 2, 1, 2], ["Modern Art"]),
            'Octatonic-2 Scale'                    : ([2, 1, 2, 1, 2, 1, 2, 1], ["Modern Art"]),
            'Algerian Scale'                       : ([2, 1, 2, 1, 1, 1, 3, 1], ["Exotic"]),
            'Harmonic Major Scale'                 : ([2, 2, 1, 2, 1, 3, 1],    ["Exotic"]),
            'Double Harmonic Major (Arabic) Scale' : ([1, 3, 1, 2, 1, 3, 1],    ["Exotic"]),
            'Double Harmonic Minor Scale'          : ([1, 3, 1, 1, 3, 1],       ["Exotic"]),
            'Hungarian Gypsy Scale'                : ([2, 1, 3, 1, 1, 3, 1],    ["Exotic"]),
            'Hungarian Minor Scale'                : ([2, 1, 3, 1, 1, 3, 1],    ["Exotic"]),
            'Hungarian Folk Scale'                 : ([1, 3, 1, 2, 1, 3, 1],    ["Exotic"]),
            'Phrygian Dominant (Jewish) Scale'     : ([1, 3, 1, 2, 1, 2, 2],    ["Exotic"]),
            'Egyptian Scale'                       : ([2, 1, 3, 1, 1, 3, 1],    ["Exotic"]),
            'Eskimo Tetratonic Scale'              : ([2, 2, 3, 5],             ["Exotic"]),
            'Eskimo Hexatonic Scale'               : ([2, 2, 2, 2, 1, 3],       ["Exotic"]),
            'Scottish Hexatonic Scale'             : ([2, 2, 1, 2, 2, 3],       ["Exotic"]),
            'Oriental Scale'                       : ([2, 3, 4, 1, 2],          ["Exotic"]),
            'Oriental Pentacluster Scale'          : ([1, 1, 3, 1, 6],          ["Exotic"]),
            'Chinese Scale'                        : ([4, 2, 1, 4, 1],          ["Exotic"]),
            'Balinese Scale'                       : ([1, 2, 4, 1, 4],          ["Exotic"]),
            'Raga Vutari Scale'                    : ([4, 2, 1, 2, 1, 2],       ["Exotic"]),
            'Raga Madhuri Scale'                   : ([4, 1, 2, 2, 1, 1, 1],    ["Exotic"]),
            'Raga Viyogavarali Scale'              : ([1, 2, 2, 3, 3, 1],       ["Exotic"]),
            'Shostakovich Scale'                   : ([1, 2, 1, 2, 1, 2, 2, 1], ["Exotic"]),
            'Blues Octatonic Scale'                : ([2, 1, 2, 1, 1, 2, 1, 2], ["Exotic"]),
            'Pyramid Hexatonic Scale'              : ([2, 1, 2, 1, 3, 3],       ["Exotic"]),
            'Romanian Scale'                       : ([4, 1, 3, 3, 1],          ["Exotic"]),
            'Gnossiennes Scale'                    : ([2, 1, 2, 2, 1, 3, 1],    ["Exotic"]),
            'Prometheus Scale'                     : ([2, 2, 2, 3, 1, 2],       ["Exotic"]),
            'Adonai Malakh Scale'                  : ([1, 1, 1, 2, 2, 2, 1, 2], ["Exotic"]),
            'Houzam Scale'                         : ([3, 1, 1, 2, 2, 2, 1],    ["Exotic"]),
            'Rock and Roll Scale'                  : ([3, 1, 1, 2, 2, 1, 2],    ["Exotic"]),
            'Phrgian Natural 6 Scale'              : ([1, 2, 2, 2, 2, 1, 2],    ["Jazz"]),
            'Lydian Augmented Scale'               : ([2, 2, 2, 2, 1, 2, 1],    ["Jazz"]),
            'Lydian Dominant Scale'                : ([2, 2, 2, 1, 2, 1, 2],    ["Jazz"]),
            'Ionian Scale'                         : ([2, 2, 1, 2, 2, 2, 1],    ["Medieval and Renaissance"]),
            'Dorian Scale'                         : ([2, 1, 2, 2, 2, 1, 2],    ["Medieval and Renaissance", "Modern Art"]),
            'Phrygian Scale'                       : ([1, 2, 2, 2, 1, 2, 2],    ["Medieval and Renaissance", "Modern Art"]),
            'Lydian Scale'                         : ([2, 2, 2, 1, 2, 2, 1],    ["Medieval and Renaissance", "Modern Art"]),
            'Mixolydian Scale'                     : ([2, 2, 1, 2, 2, 1, 2],    ["Jazz","Medieval and Renaissance", "Modern Art"]),
            'Aeolian Scale'                        : ([2, 1, 2, 2, 1, 2, 2],    ["Medieval and Renaissance", "Modern Art"]),
            'Locrian Scale'                        : ([1, 2, 2, 1, 2, 2, 2],    ["Jazz", "Modern Art"]),
            'Super Locrian Scale'                  : ([1, 2, 1, 2, 2, 2, 2],    ["Jazz"]),
            'Melodic Minor Scale'                  : ([2, 1, 2, 2, 2, 2, 1],    ["Jazz"]),
            'Bebop Dominant Scale'                 : ([2, 2, 1, 2, 2, 1, 1, 1], ["Jazz"]),
            'Bebop Major Scale'                    : ([2, 2, 1, 2, 1, 1, 2, 1], ["Jazz"]),
            'Bebop Melodic Minor Scale'            : ([2, 1, 1, 1, 2, 2, 1, 2], ["Jazz"]),
            'Bebop Dorian Scale'                   : ([2, 1, 1, 1, 2, 2, 1, 2], ["Jazz"]),
            'Whole Tone Scale / Interval 2 Cycle'  : ([2, 2, 2, 2, 2, 2],       ["Exotic"])
            }
