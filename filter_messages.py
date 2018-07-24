import mailbox
from email.generator import Generator

mbox = mailbox.mbox('./data/Mail/messages.mbox')
outbox = open('output_text_only_04.txt', 'w')
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
    if not isinstance(p, list):
        if msg.get_content_type() in preferred_content_types:
            return g.write(p)
    else:
        for m in p:
            descend(m)


def from_a_to_me(m):
    return 'annie' in m.get('from', None).lower()


def from_me_to_a(m):
    t = to(m) or 'annie'
    return 'annie' in t.lower()


def m_from(m):
    x = m.get('from', None) or m.get_from()
    return x


def to(m):
    x = m.get('to', None) or m.get('To', None)
    return x


if __name__ == '__main__':
    main(mbox)
    outbox.close()
