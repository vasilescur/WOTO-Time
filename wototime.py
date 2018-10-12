import urllib.request
import smtplib
import configparser

# Read config data
config = configparser.ConfigParser()
config.read('config.ini')

EMAIL = config['GMAIL_CREDENTIALS']['email']
PASS = config['GMAIL_CREDENTIALS']['pass']

NUMBER = config['PHONE_NUM']['number']

GATEWAY = config['CARRIER_GATEWAY']['gateway']

WOTO_URLS = config['WOTOS']['wotos'].split(',')


def send(target_number, message):
	to_number = target_number + GATEWAY
	auth = (EMAIL, PASS)

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(auth[0], auth[1])

	# Send text message through SMS gateway of destination number
	server.sendmail(auth[0], to_number, message)


def check(url):
    """ Check if the WOTO is open. """
    page = urllib.request.urlopen(url)
    bytes_page = page.read()

    page_str = bytes_page.decode("utf8")
    page.close()

    if 'no longer accepting responses' in page_str:
        return False
    else:
        return True


# Parse wotos
wotos = []

for url in WOTO_URLS:
    wotos.append(
        {
            'url': url,
            'activated': False
        }
    )

# Main loop

print('Checking for ' + str(len(wotos)) + ' wotos ...')
print('You\'ll get a text message at ' + NUMBER)

while True:
    for woto in wotos:
        if woto['activated'] == False:
            is_open = check(woto['url'])

            if is_open:
                print('WOTO TIME! ' + woto['url'])
                woto['activated'] = True

                send(NUMBER, 'WOTO TIME!')
                send(NUMBER, woto['url'][14:])  #HACK: AT&T blocks links!
                # The reason for splitting this string on 14: is to eliminate the 
                # bit.ly part, thus making sure the link isn't blocked or screwed up.
