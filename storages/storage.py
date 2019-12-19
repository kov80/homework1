import logging

logger = logging.getLogger(__name__)


class Storage(object):
    @staticmethod
    def save(i, t, text, ref):
        print('%s%s: %s\n%s%s' % ('\t' * t, i + 1, text, '\t' * (t + 1), ref))