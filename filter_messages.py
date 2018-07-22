import mailbox
from email.generator import Generator

mbox = mailbox.mbox('./data/Mail/messages.mbox')
outbox = open('output04.txt', 'w')
g = Generator(outbox)


def main(box):
    preferred_content = {'text/plain', 'text/html'}

    def walk_msg(m):
        '''
        iterates through a message object for multipart or lists of
        messages and prints them out
        '''
        if m is None:
            return None

        if not from_a_to_me(m) or not from_me_to_a(m):
            return None

        if m.is_multipart() is False:
            # single message; write & return
            return g.write(m.get_payload(decode=True))
        else:
            # multipart
            for part in m.walk():
                payload = m.get_payload(decode=True)
                if isinstance(payload, list):
                    g.write(g.flatten(payload))
                    # for mm in payload:
                    # walk_msg(mm)
                elif payload is not None:
                    return g.write(payload)

    for m in box.itervalues():
        if m.is_multipart() is True:
            walk_msg(m)
        elif from_a_to_me(m) or from_me_to_a(m):
            # try:
                # g.write(p)
            # except TypeError as e:
                # print('error: ', e, ' for p: ', p)
            g.write(m.get_payload())
        else:
            continue


def from_a_to_me(m):
    f = m_from(m)
    return 'annie' in f.lower()


def from_me_to_a(m):
    t = to(m) or 'annie'
    return 'annie' in t.lower()


def m_from(m):
    x = m.get('from', None) or m.get('From', None) or m.get_from()
    return x


def to(m):
    x = m.get('to', None) or m.get('To', None)
    return x


if __name__ == '__main__':
    main(mbox)
    outbox.close()
