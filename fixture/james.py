from telnetlib import Telnet

from fixture.session import SessionHelper


class JamesHelper:

    def __init__(self, app):
        self.app = app

    def ensure_user_exists(self, username, password):
        james_cfg = self.app.config['james']
        session = self.Session(
            host=james_cfg['host'], port=james_cfg['port'], username=james_cfg['user'], password=james_cfg['password'])
        if session.is_user_registered(username):
            session.reset_password(username, password)
        else:
            session.create_user(username, password)
        session.quit()



    class Session:
        def __init__(self, host, port, username, password):
            self.telnet = Telnet(host, port, 5)
            self.read_until('Login id:')
            self.write(f'{username}\n')
            self.read_until('Password:')
            self.write(f'{password}\n')
            self.read_until(f'Welcome {username}. HELP for a list of commands')

        def is_user_registered(self, username):
            self.write(f'verify {username}\n')
            result = self.telnet.expect([b'exists', b'not exist'], 5)
            return result[0] == 0

        def create_user(self, username, password):
            self.write(f'adduser {username} {password}\n')
            self.read_until(f'User {username} added')


        def reset_password(self, username, new_password):
            self.write(f'setpassword {username} {new_password}\n')
            self.read_until(f'Password for {username} reset')

        def quit(self):
            self.write('quit\n')

        def read_until(self, text):
            self.telnet.read_until(text.encode('ascii'), 5)

        def write(self, text):
            self.telnet.write(text.encode('ascii'))