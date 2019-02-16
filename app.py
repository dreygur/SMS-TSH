#!/usr/bin/env python

########################################################################
#   SMS API - Python 3.6
#   Copyright (C) 2019 by Rakibul Yeasin Totul
#   URI      - https://www.rytotul.xyz/about
#   Facebook - https://www.facebook.com/rytotul
#   Github   - https://www.github.com/rytotul
#
#   Distributed Under Mozilla Public License 2.0
#   You may have downloaded the LICENCE file along with this document
#   If not then please find it on: <https://www.mozilla.org/en-US/MPL/>
#
########################################################################

# importing modules
import sys
import os
import getpass
from optparse import OptionParser
from urllib import request as req
from urllib import parse as prs
#import untangle as ut

# Preventig from writing bytecodes
sys.dont_write_bytecode = True

# Calling from modules...
parser = OptionParser()

# Parser options...
parser.add_option("-t", "--text", help="To send a short SMS", action="store_true")
parser.add_option("-l", "--long", help="To send a long SMS", action="store_true")
parser.add_option("-r", "--report", help="For finding Delivery Reports", action="store_true")
parser.add_option("-b", "--balance", help="Command to check the current balance", action="store_true")
parser.add_option("-i", "--id", help="User ID(s)", action="store_true")

# Gathering all parser-options in a variable
(args, _) = parser.parse_args()


class bcls:
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

class SMS_API:
    # Initialization
    def __init__(self):
        self._username   = str(input(bcls.OKGREEN + "\tYour Username: " + bcls.ENDC))
        self._password   = str(getpass.getpass(bcls.OKGREEN + "\tPassword: " + bcls.ENDC))
        self.sms_id      = '3706682'

        # Base domain name
        _base_domain = 'esms.dianahost.com'

        # API Key Retrieval API
        _api_key_url = 'http://{0}/getkey/{1}/{2}'.format(_base_domain, self._username, self._password)

        # Retrieved API Key
        self._api_key = req.urlopen(_api_key_url).read().decode('UTF-8')
        if ":" in self._api_key:
            _, self._api_key = self._api_key.split(":", 1)

        # Credit Balance API
        self._api_credit_url = 'http://{0}/miscapi/{1}/getBalance'.format(_base_domain, self._api_key)

        # Delivery Report API
        self._api_delivery_report_url = 'http://{0}/miscapi/{1}/getDLR/'.format(_base_domain, self._api_key)

        # Send SMS API
        self._api_sms_url = 'http://{0}/smsapi'.format(_base_domain)

        # UserID Retrieve API
        self._api_userid_url = 'http://{0}/miscapi/{1}/getDLR/{2}'.format(_base_domain, self._api_key, self.sms_id)

    # Convert the xml to Dictionary
    # def res_clean(self, response):
    #     obj = ut.parse(response)
    #     return  obj.dlr.message.MSISDN + '\n' + \
    #             obj.dlr.message.SMS + '\n' + \
    #             obj.dlr.message.SMSSent + '\n' + \
    #             obj.dlr.message.DLRReceived + '\n' + \
    #             obj.dlr.message.DLRStatus + '\n'

    # We can retrieve our remaining credit balance with this function
    def balance(self):
        url = self._api_credit_url
        result = req.urlopen(url)
        # converting the result to string
        response = result.read()
        response = response.decode('UTF-8')
        return response

    # We can retrieve our remaining credit balance with this function
    def sms(self, gsm, message, _sender_ID, t_type='text'):
        # We will make a Dictionary with all our Data
        _argv = {'api_key'  : str(self._api_key),
                 'contacts' : str(gsm),
                 'msg'      : str(message),
                 'senderid' : str(_sender_ID),
                 'type'     : str(t_type)}

        # Base url to send a short SMS
        url = self._api_sms_url
        # encoding the Data as url
        enc_url = prs.urlencode(_argv)
        # joining base url and encoded url
        request = url + '?' + enc_url
        # opening the url to run the commands
        result = req.urlopen(request)
        # Converting from bytes to string
        response = (result.read()).decode('UTF-8')
        return response

    def delivery_report(self, delivery_id=''):
        # Delivery Report
        if delivery_id == '':
            url = self._api_delivery_report_url + 'getAll'
            result = req.urlopen(url)
            # converting the result to string
            response = result.read()
            # Converting from bytes to string
            response = response.decode('UTF-8')
            #response = self.res_clean(response.decode('UTF-8'))
            return response
        else:
            url = self._api_delivery_report_url + delivery_id
            result = req.urlopen(url)
            # converting the result to string
            response = result.read()
            # Converting from bytes to string
            response = response.decode('UTF-8')
            return response
    
    def get_id(self):
        url = self._api_delivery_report_url
        result = req.urlopen(url)
        response = result.read().decode('UTF-8')
        return response

class Main_Class:
    def __init__(self):
        # Initializing Class
        pass

    def banner(self):
        # Application Banner
        os.system('clear')
        lol = bcls.OKGREEN +  """

            .dP"Y8 8b    d8 .dP"Y8     888888 .dP"Y8 88  88 
            `Ybo." 88b  d88 `Ybo."       88   `Ybo." 88  88 
            o.`Y8b 88YbdP88 o.`Y8b       88   o.`Y8b 888888 
            8bodP' 88 YY 88 8bodP'       88   8bodP' 88  88 

    \t----------------------------------------------------------
            Version: 0.0.3 (Alpha)
            For help: -h
            Bug report: rytotul@gmail.com
    \t----------------------------------------------------------
            """ + bcls.ENDC
        # Tool: http://patorjk.com/software/taag/
        # Font: 4Max
        print(lol)

    # User Input Message
    def message(self):
        # Getting Message Text from the user
        print(bcls.OKGREEN + '\n\tEnter your Message (max 160 chars for short 1080 for long):' + bcls.ENDC)
        text = str(input('\t'))
        return text

    # User Input Phone number
    def number(self):
        # Getting Contact Number from the user
        print(bcls.OKGREEN + '\n\tEnter the phone number where to send SMS: (Use 88 before the number)' + bcls.ENDC)
        gsm = str(input('\t'))
        return gsm

    # Check Responses by response code
    def sms_check(self, res):
        # Checking response code and type
        if res == '1002':
            response = 'Sender Id/Masking Not Found'
        elif res == '1003':
            response = 'API Not Found'
        elif res == '1004':
            response = 'SPAM Detected'
        elif res == '1005':
            response = 'Internal Error'
        elif res == '1006':
            response = 'Internal Error'
        elif res == '1007':
            response = 'Balance Insufficient'
        elif res == '1008':
            response = 'Message is empty'
        elif res == '1009':
            response = 'Message Type Not Set (text/unicode)'
        elif res == '1010':
            response = 'Invalid User & Password'
        elif res == '1011':
            response = 'Invalid User Id'
        else:
            response = bcls.OKGREEN + 'Request Success...\n\t' + res

        return response

# The function to show help message
def help():
    help_message = bcls.OKGREEN +  """
        No Arguments Passed!
        PLease See the help menu below to know how to use this script.

        Usage: app.py [options]

        Options:
        -h, --help         Show this help message and exit
        -t, --text         To send a short SMS
        -l, --long         To send a long SMS
        -r, --report       For finding Delivery Reports
        -b, --balance      Command to check the current balance
        -i, --id           Get the Sender ID(s)
        """ + bcls.ENDC

    print(help_message)
    sys.exit()

#The main function starts...
def main():
    """ The Main Function """
    m   = Main_Class()      # main class
    m.banner()              # Prints the Banner
    api = SMS_API()         # sms api class

    # Check Balance
    if args.balance is True:
        bal = api.balance()
        print(bcls.OKGREEN + '\n\t{0}\n'.format(bal) + bcls.ENDC)
    
    # Send a short SMS
    if args.text is True:
        sender_ID  = str(input(bcls.OKGREEN + "\tYour Sender ID: " + bcls.ENDC))
        text = m.message()
        gsm = m.number()
        t_type = 'text'
        verify = str(input(bcls.OKGREEN + '\n\n\tSMS Text: {0} \n\tReciever: {1}\n\n\tYes to Confirm, No to discard: '.format(text, gsm) + bcls.ENDC))
        verify = verify[:1]
        # Verification from user
        if verify.lower() == 'y':
            response = api.sms(gsm, text, sender_ID, t_type)
            response = response
            ans = m.sms_check(response)
            bal = api.balance()
            print(bcls.WARNING + '\n\t{0}\n\t{1}\n'.format(ans, bal) + bcls.ENDC)
            sys.exit()

    # Fetching Delivery reports
    if args.report is True:
        delivery_id = str(input(bcls.OKGREEN + '\tEnter Delivery ID: (Skip for All)' + bcls.ENDC))
        bal = api.delivery_report(delivery_id)
        print('\n\t{0}\n'.format(bal))

    if args.id is True:
        user_id = api.get_id()
        print('{0}'.format(user_id))


# Starting the program from here...
if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Show Help if no arguement is passed
        # not implemented yet
        help()
    else:
        try:
            # Calling main() function
            main()

        except IOError:
            # Escaping Network connection Error
            print (bcls.FAIL + '\n\tNot connected to Internet. Connect to internet first...\n'+ bcls.ENDC)
            sys.exit()
            pass

        except KeyboardInterrupt:
            # Exit when Keyboard Interrupt happens
            print(bcls.WARNING + '\n\tKeyboard Interrupt Occured. Exiting...\n' + bcls.ENDC)
            sys.exit()

# end..............................................