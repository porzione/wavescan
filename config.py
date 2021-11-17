#!/usr/bin/env python
# -*- coding: utf-8 -*-

# LSP limits
MAX_INSTRUMENTS = 48
MAX_SAMPLES = 8

instruments = [
    ["laser", 27],
    ["(Acoustic.?Bass.?Drum|Kick.?Drum.?2|Kik_Brother)", 35],
    ["(kick|kik|BassDrum)", 36],
    ["(side|rim)", 37],
    ["(esnare|electr.+snare|snare.+electr)", 40],
    ["snare", 38],
    ["clap", 39],
    ["(low.?fl.*tom|tom.?low.?fl)", 41],
    ["(CHH|HHC|Hat.?c|HH.*c~/Music/SFZ/5pin_DrumKit.sfzl|Cl.*Hat|\\WCH)", 42],
    ["hi.?fl.*tom", 43],
    ["(hh.*foot|hihat.*foot|foot.*hh|pedal.*hat)", 44],
    ["(low.?tom|tom.?low)", 45],
    ["(OHH|HHO|Hat.*Op|HH.*Op|Op.*Hat|Op.*HH|\\WOH)", 46],
    ["low.*mid.*tom", 47],
    ["hi.*mid.*tom", 48],
    ["crash", 49],
    ["(hi.*tom|tom.?hi)", 50],
    ["ride", 51],
    ["chin(a|e)", 52],
    ["tamb", 54],
    ["splash", 55],
    ["cowbell", 56],
    ["vibra", 58],
    ["(hi.*bongo|bongo.*hi)", 60],
    ["bongo", 61],
    ["(mut.*conga|conga.*mut)", 62],
    ["(open.*conga|conga.*open)", 63],
    ["hi.*conga", 62],
    ["conga", 64],
    ["(high.*timbale|timbale.*high)", 65],
    ["(low.*timbale|timbale.*low)", 66],
    ["(hi.*agogo|agogo.*hi)", 67],
    ["agogo", 68],
    ["cabasa", 69],
    ["mara?cas", 70],
    ["(sho.*whistle|whistle.*sho)", 71],
    ["whistle", 72],
    ["(lon.*guiro|guiro.*lon)", 73],
    ["(guiro)", 74],
    ["clav", 75],
    ["hi.*woodblock", 76],
    ["woodblock", 77],
    ["(open.*cuica|cuica.*open)", 79],
    ["cuica", 78],
    ["shaker", 82],
    ["(mut.*triangl|triangl.*mut)", 80],
    ["triangl", 81],
    # 1000 => "some hihat"
    ["hat", 1000],
    # other doubtful drums
    ["fl.*tom", 41],
    ["tom", 45],
    ["cym", 51],
    ["\\WBD", 36],
    ["bass", 36],
    ["\\WSD", 38],
]

IGNORE = ".*(\\Wvital\\W|wavetable).*"
SAMPLE = ".+\\.(wav|flac|aiff?|aifc)$"

names = {
    27: "High Q / Laser",
    28: "Slap / Whip",
    29: "Scratch Push",
    30: "Scratch Pull",
    31: "Sticks",
    32: "Square Click",
    33: "Metronome Click",
    34: "Metronome Bell",
    35: "Kick 2",
    36: "Kick 1",
    37: "Side",
    38: "Snare",
    39: "Clap",
    40: "ESnare",
    41: "Low Floor Tom",
    42: "Closed HH",
    43: "High Floor Tom",
    44: "Pedal Hi-Hat",
    45: "Low Tom",
    46: "Open HH",
    47: "Low-Mid Tom",
    48: "Hi Mid Tom",
    49: "Crash Cymbal",
    50: "High Tom",
    51: "Ride Cymbal",
    52: "Chinese Cymbal",
    53: "Ride Bell",
    54: "Tambourine",
    55: "Splash Cymbal",
    56: "Cowbell",
    57: "Crash Cymbal 2",
    58: "Vibraslap",
    59: "Ride Cymbal 2",
    60: "Hi Bongo",
    61: "Low Bongo",
    62: "Mute Hi Conga",
    63: "Open Hi Conga",
    64: "Low Conga",
    65: "High Timbale",
    66: "Low Timbale",
    67: "High Agogo",
    68: "Low Agogo",
    69: "Cabasa",
    70: "Maracas",
    71: "Short Whistle",
    72: "Long Whistle",
    73: "Short Guiro",
    74: "Long Guiro",
    75: "Claves",
    76: "Hi Wood Block",
    77: "Low Wood Block",
    78: "Mute Cuica",
    79: "Open Cuica",
    80: "Mute Triangle",
    81: "Open Triangle",
    82: "Shaker",
    83: "Jingle Bell",
    84: "Belltree",
    85: "Castanets",
    86: "Mute Surdo",
    87: "Open Surdo",
}

# only LSP for now
ordering = [
    36,  # Kick 1/2
    42,  # HHC 3/4
    46,  # HHO 5/6
    39,  # Clap 7/8
    38,  # Snare 9/10
    75,  # Claves 11/12
    82,  # Shaker 13/14
    50,  # High Tom 15/16
    45,  # Low Tom 17/18
    49,  # Crash 19/20
    51,  # Ride 21/22
    55,  # Splash 23/24
]
