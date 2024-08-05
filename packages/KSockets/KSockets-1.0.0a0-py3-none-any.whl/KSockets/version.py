# Simply following the Python markdown's versioning format since it is good enough for me.
# __version_info__ format:
#     (major, minor, patch, dev/alpha/beta/rc/final, #)
#     (1, 1, 2, 'dev', 0) => "1.1.2.dev0"
#     (1, 1, 2, 'alpha', 1) => "1.1.2a1"
#     (1, 2, 0, 'beta', 2) => "1.2b2"
#     (1, 2, 0, 'rc', 4) => "1.2rc4"
#     (1, 2, 0, 'final', 0) => "1.2.0"
# Taken from CFSession

__version_info__ = (1, 0, 0, 'alpha', 0)
__protocol_version_info__ = (1, 0)

def _get_version(version_info, explicit_versioning = True):
    " Returns a PEP 440-compliant version number from version_info. "
    assert len(version_info) == 5
    assert version_info[3] in ('dev', 'alpha', 'beta', 'rc', 'final')

    if explicit_versioning:
        parts = 3 #I want explicit versioning
    else:
        parts = 2 if version_info[2] == 0 else 3
    v = '.'.join(map(str, version_info[:parts]))

    if version_info[3] == 'dev':
        v += '.dev' + str(version_info[4])
    elif version_info[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc'}
        v += mapping[version_info[3]] + str(version_info[4])
    return v

__version__ = _get_version(__version_info__)
__protocol_version__ = '.'.join(map(str, __protocol_version_info__))