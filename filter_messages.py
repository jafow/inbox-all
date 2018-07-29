import atexit
import mailbox

from email.generator import Generator
from functools import reduce
from time import clock

from bs4 import BeautifulSoup

mbox = mailbox.mbox('./data/all_mail.mbox')
outbox = open('big_output_00.txt', 'w')
g = Generator(outbox)


def main(box):
    for i, m in box.iteritems():
        if from_a_to_me(m) or from_me_to_a(m):
            if m.is_multipart() is True:
                for part in m.walk():
                    descend(part)
            else:
                g.write(m.get_payload())


def descend(msg):
    ''' climb down the message tree '''
    preferred_content_types = {'text/plain', 'text/html', 'text/directory'}
    p = msg.get_payload()
    if isinstance(p, list):
        for m in p:
            descend(m)
    else:
        content_type = msg.get_content_type()
        if content_type in preferred_content_types:
            return write_content(content_type, p)


def write_content(c_type, msg):
    ''' write message body based on content type '''
    if c_type == 'text/html':
        doc = BeautifulSoup(msg, 'html.parser', from_encoding='utf-8')
        return g.write(doc.get_text())
    else:
        return g.write(msg)


def from_to(msg=None, send=None, receive=None):
    assert msg is not None
    return send in msg.get('from', None) and receive in msg.get('to', None)


def from_a_to_me(m):
    ''' if a message is from a to me '''
    fr = m.get('from', None)
    if fr is not None:
        return 'annie' in fr.lower()


def from_me_to_a(m):
    t = to(m)
    if t is not None:
        return 'annie' in t.lower()


def to(m):
    x = m.get('to', None) or m.get('To', None)
    return x


def neither(cb1, cb2):
    ''' true for neither of two methods '''
    def _neither(msg):
        return not cb1(msg) and not cb2(msg)

    return _neither


def seconds_to_str(t):
    time_str = reduce(
            lambda ll,
            b: divmod(ll[0], b) + ll[1:],
            [(t * 1000,), 1000, 60, 60]
        )
    return "%d:%02d:%02d.%03d" % time_str


def endlog():
    end = clock()
    passed_time = start - end
    print('done: ')
    print(seconds_to_str(passed_time))


if __name__ == '__main__':
    start = clock()
    atexit.register(endlog)
    print('starting')
    main(mbox)
    outbox.close()
