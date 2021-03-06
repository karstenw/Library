"""Split a treelang.log file into chunks of warnings separated by language"""
#
# (C) Rob W.W. Hooft, 2003
#
# Distribute under the terms of the PSF license.
#
__version__ = '$Id: splitwarning.py,v 1.1 2003/12/21 09:32:28 hooft Exp $'
#
files={}
for line in open('treelang.log'):
    if line[:8] == 'WARNING:':
        code = line[9:11]
        if not files.has_key(code):
            files[code] = open('warning_%s.log' % code, 'w')
        files[code].write(line)
