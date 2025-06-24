import av

# Returns an OrderedDict keyed by codec name → av.codec.Codec object
codecs = av.codecs_available

for codec in codecs:
    print(f"{codec:20} ")
