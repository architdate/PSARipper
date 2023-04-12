# scripts to dump as text files
from psaripper.metadata import Hosters


def get_hoster_dictionary(entrydict):
    d = {}
    for k, v in entrydict.items():
        urllist = []
        for a in v.values():
            urllist += list(a)
        for u in urllist:
            h = Hosters.getHoster(u)
            if h in d.keys():
                d[h].append((k, u))
            else:
                d[h] = [(k, u)]
    return d


def pretty_print(ddl_dict):
    retval = ""
    for k, v in ddl_dict.items():
        retval += k.name + '\n\n'
        for e in v:
            retval += e[0] + ' - ' + e[1] + '\n'
        retval += '\n'
    return retval.strip()


def pretty_print_torr(torr_dict):
    retval = "Torrents\n\n"
    for k, v in torr_dict.items():
        retval += k + ' - ' + ','.join(v) + '\n'
    return retval.strip()
