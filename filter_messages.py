import mailbox
from email.generator import Generator

mbox = mailbox.mbox('./data/Mail/messages.mbox')
outbox = open('output02.txt', 'w')
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
        if m.is_multipart() is False:
            # single message; write & return
            return g.write(m.get_payload(decode=True))
        else:
            # multipart
            for part in m.walk():
                payload = m.get_payload(decode=True)
                if isinstance(payload, list):
                    for mm in payload:
                        walk_msg(mm)
                elif payload is not None:
                    return g.write(payload)

    for k, m in box.iteritems():
        if m is not None:
            if from_a_to_me(m) or from_me_to_a(m):
                if m.is_multipart() is True:
                    return walk_msg(m)
                    # for part in m.walk():
                    #     if part.get_content_type() in preferred_content:
                    #         payload = m.get_payload()
                    #         try:
                    #             g.write(payload)
                    #         except TypeError as e:
                    #             for msg in payload:
                    #                 g.write(msg.get_payload())
                else:
                    # try:
                        # g.write(p)
                    # except TypeError as e:
                        # print('error: ', e, ' for p: ', p)
                    g.write(m.get_payload())
            else:
                print('dont care: ', m_from(m))


def from_a_to_me(m):
    f = m_from(m)
    t = to(m) or 'jared'
    return 'annie' in f.lower() and 'jared' in t.lower()


def from_me_to_a(m):
    f = m_from(m)
    t = to(m) or 'annie'
    return 'jared' in f.lower() and 'annie' in t.lower()


def m_from(m):
    x = m.get('from', None) or m.get('From', None) or m.get_from()
    return x


def to(m):
    x = m.get('to', None) or m.get('To', None)
    return x


if __name__ == '__main__':
    main(mbox)
    outbox.close()
