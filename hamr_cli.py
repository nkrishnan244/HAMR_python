#! /usr/bin/env python
import hamr_messenger as hm

class HamrCLI(object):
    """A CLI App for the HAMR.

    Attributes:
        messenger: An instance of the HamrMessenger object.
        do_next_iter: A boolean that determines whether the app continues.
    """
    def __init__(self):
        self.messenger = hm.HamrMessenger()
        self.do_next_iter = True

    def opening(self):
        print '/****************************/'
        print '/* Welcome to the HAMR CLI! */'
        print '/****************************/'
        print 'Be sure to verify that the HAMR is on and you are connected to its Access Point.'

    def show_options(self):
        print 'Would you like to: '
        print '1) Send a holonomic message'
        print '2) Send a dif drive message'
        print '3) Stop all motors?'
        print '4) Exit?'
        print 'Input the corresponding number to make a choice'
        return raw_input('')

    def handle_decision(self, decision):
        if decision == '1':
            print 'You selected Holonomic Drive.'
            self.holo_drive()
        elif decision == '2':
            print 'You selected Dif Drive.'
            self.dif_drive()
        elif decision == '3':
            print 'Killing Motors.\n'
            # self.messenger.kill_motors()
        elif decision == '4':
            # self.messenger.kill_motors()
            self.do_next_iter = False
            print 'Stopping the HAMR and the interface.\n'
        else:
            print 'Not a valid message!\n'

    def holo_drive(self):
        x = raw_input('What x?\n')
        y = raw_input('What y?\n')
        r = raw_input('What r?\n')
        dvect = (float(x), float(y), float(r))
        print('Sending vector ' + str(dvect) + '\n')
        self.messenger.send_holonomic_command(dvect[0], dvect[1], dvect[2])

    def dif_drive(self):
        left = raw_input('Desired Left Motor velocity?\n')
        right = raw_input('Desired Right Motor velocity?\n')
        turret = raw_input('Desired Turret Motor velocity?\n')
        dvect = (float(left), float(right), float(turret))
        print('Sending vector ' + str(dvect) + '\n')
        self.messenger.send_dif_drive_command(dvect[0], dvect[1], dvect[2])

if __name__ == '__main__':
    cli = HamrCLI()
    cli.opening()
    while cli.do_next_iter:
        option = cli.show_options()
        cli.handle_decision(str(option))

