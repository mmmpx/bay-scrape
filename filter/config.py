import re


RE_REJECT = [
    r'^.*?(intel|amd|ryzen|[^a-z]i[3579]).*$',
    r'^.*?box only.*$',
    r'^.*?empty box.*$',
    r'^.*?adapt[eo]rs?.*$',
    r'^.*?coolers? +only.*$',
    r'^.*fans? +only.*$',
    r'^.*?faulty?.*$',
    r'^.*?error +([0-9]+|code).*$',
    r'^.*?gaming (pc|computer|box).*$',
    r'^.*?wholesale.*$',
    r'^.*?only +for +\$.*$',
    r'^.*?\. *\(com\).*$'
]


def validate(s):
    return all((not re.match(p, s, re.I) for p in RE_REJECT))


query_filters = {
    'Radeon RX 6400':
        lambda o: re.match(r'^.*?6400($|(?! *xt).*$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6500 XT':
        lambda o: re.match(r'^.*?6500 *xt([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6600':
        lambda o: re.match(r'^.*?6600($|(?! *xt).*$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6600 XT':
        lambda o: re.match(r'^.*?6600 *xt([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6650 XT':
        lambda o: re.match(r'^.*?6650 *xt([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6700':
        lambda o: re.match(r'^.*?6700($|(?! *xt).*$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6700 XT':
        lambda o: re.match(r'^.*?6700 *xt([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6750 XT':
        lambda o: re.match(r'^.*?6750 *xt([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6800':
        lambda o: re.match(r'^.*?6800($|(?! *xt).*$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6800 XT':
        lambda o: re.match(r'^.*?6800 *xt([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6900 XT':
        lambda o: re.match(r'^.*?6900 *xt([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 6950 XT':
        lambda o: re.match(r'^.*?6950 *xt([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 7900 XT':
        lambda o: re.match(r'^.*?7900 *xt([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'Radeon RX 7900 XTX':
        lambda o: re.match(r'^.*?7900 *xtx([ !,.;|:].*$|$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 3050':
        lambda o: re.match(r'^.*?3050($|(?! *ti).*$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 3060':
        lambda o: re.match(r'^.*?3060($|(?! *ti).*$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 3060 Ti':
        lambda o: re.match(r'^.*?3060 *ti([ !,.;:].*$|$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 3070':
        lambda o: re.match(r'^.*?3070($|(?! *ti).*$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 3070 Ti':
        lambda o: re.match(r'^.*?3070 *ti([ !,.;:].*$|$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 3080':
        lambda o: re.match(r'^.*?3080($|(?! *ti).*$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 3080 Ti':
        lambda o: re.match(r'^.*?3080 *ti([ !,.;:].*$|$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 3090':
        lambda o: re.match(r'^.*?3090($|(?! *ti).*$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 3090 Ti':
        lambda o: re.match(r'^.*?3090 *ti([ !,.;:].*$|$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 4070':
        lambda o: re.match(r'^.*?4070($|(?! *ti).*$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 4070 Ti':
        lambda o: re.match(r'^.*?4070 *ti([ !,.;:].*$|$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 4080':
        lambda o: re.match(r'^.*?4080($|(?! *ti).*$)', o['title'], re.I) and validate(o['title']),
    'GeForce RTX 4090':
        lambda o: re.match(r'^.*?4090($|(?! *ti).*$)', o['title'], re.I) and validate(o['title']),
}

