from shamir import ShamirSecretShare
from base64 import b32decode, b32encode, decode
import os

class Program:

    def __init__(self) -> None:
        self.shamir = ShamirSecretShare()

    def intro(self) -> None:
        print('\nVítejte! Toto je jednoduchý program na Shamirovo sdílení tajemství.\n\n')
        #print('Současné nastavení: ')
        print('Možnosti:\n\t1 zadat tajné heslo a rozdělit ho mezi několik účastníků\n'
                '\t2 zadat jednotlivé části a rekonstruovat celé tajemství\n')
        self.main_menu()

    def main_menu(self) -> None:
        r = input("Co chcete dělat? Zadejte 1 nebo 2 a stiskněte ENTER: ")
        if r == '1':
            self.split_secret()
        elif r == '2':
            self.enter_secret()
        else:
            self.cls()
            print('Musíte zadat 1 nebo 2, nic jiného. Zkuste to znovu.\n\n')
            self.main_menu()

    def split_secret(self) -> None:
        self.cls()
        secret = input("Zadejte své tajemství, které chcete rozdělit: ")
        self.shamir.set_message(secret)
        shares = self.shamir.split_secret()

        self.cls()
        print('Zadané tajemství bylo rozděleno na následující části:\n')
        for i in range(1, len(shares)+1):
            print('\t{:d}: {:s}'.format(i, self.share_to_string(shares[i])))

        print('\nPamatujte, k obnovení tajemství stačí jen {:d} z {:d} částí.'.format(self.shamir.get_threshold(), self.shamir.get_holders()))

    def enter_secret(self) -> None:
        if self.shamir.is_solvable():
            self.show_result()
            return

        print('Už mám {:d} část(i), potřebuji aspoň {:d}.\n'.format(self.shamir.get_shares_count(), self.shamir.get_threshold()))
        s = input('Zadejte 1 a ENTER k zadání další části tajemství - anebo cokoliv jiného pro ukončení programu: ')
        if s == '1':
            # secret number
            i = input('Zadejte číslo části tajemství: ')
            try:
                i = int(i)
                
                # secret value
                s = input('Zadejte část tajemství: ')

                # convert the Base32-encoded value to int and add it to the ShamirShare object
                b = b32decode(self.remove_human_readability(s))
                r = int.from_bytes(b, byteorder='big')
                self.cls()
                self.shamir.add_share(i, r)
            except:
                print('Hmm, špatné zadání, zkuste to znovu.\n\n')
            
            self.enter_secret()
        else:
            s = input('Opravdu opustit program? (y/n) ')
            if s == 'y':
                print('Ukončování...\n\n')
                quit()
            else:
                self.enter_secret()

    def show_result(self) -> None:
        if self.shamir.is_solvable():
            secret = self.shamir.reconstruct_secret()
            print('HOORAY! Podařilo se odkrýt skryté tajemství!\n\nSkrytá tajná hodnota je: {:s}\n\nA nezapomeňte: with great power comes great responsibility! :-)\n\n\n'.format(secret))
        
    
    def remove_human_readability(self, val: str):
        noDashes = val.replace('-', '').upper()
        padLen = (len(noDashes) * 5) % 8
        if padLen > 0:
            padLen = 8 - padLen
        return noDashes + ('=' * padLen)

    def string_to_human_readable(self, val: str):
        val = val.strip('=')
        r = ''
        for i in range(0, len(val), 5):
            r += val[i:i+5] + '-'
        return r[:-1]

    def share_to_string(self, share: int) -> str:
        shareBytes = self.remove_zeros((share).to_bytes(self.shamir.get_max_bytes(), byteorder='big'))
        return self.string_to_human_readable(b32encode(shareBytes).decode('utf-8'))

    def remove_zeros(self, b: bytes) -> bytes:
        if len(b) < 1:
            return b

        split = -1
        for i in range(len(b)):
            if b[i] == 0:
                split = i
            else:
                break
        
        if split >= 0:
            b = b[split+1:]
        
        return b

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')