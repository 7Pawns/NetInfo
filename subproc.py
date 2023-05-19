import subprocess as sp
import csv

# To run commands in cmd (ipconfig and hostname)
def run_command(cmd):
    return sp.Popen(cmd,
    shell=True,
    stdout=sp.PIPE,
    stderr=sp.PIPE,
    stdin=sp.PIPE).communicate()

# Get information from cmd by header name
# Distance between header and value is constant
# Which allows us to add 36 to get it
def find_header(header_name, start = 0):
    i = 0
    header_value = ''
    i = output.find(header_name, start) + 36
    if i == -1:
        return None
    while (output[i] not in ['(', '\n']):
        header_value += output[i]
        i += 1
    return header_value

def os_find_header(header_name, start = 0):
    i = 0
    header_value = ''
    i = bonus_output.find(header_name, start) + 27
    if i == -1:
        return None
    while (bonus_output[i] not in ['(', '\n']):
        header_value += bonus_output[i]
        i += 1
    return header_value

# CSV File Open in Write
with open('headers.csv', 'w', newline='') as headers_file:
    headers_names = ['Name', 'State', 'Physical Address', 'DHCP Enabled']

    headers_writer = csv.writer(headers_file , delimiter = '\t')
    headers_writer.writerow(headers_names)


    headers_writer.writerow(['Computer Information: NIC'])

    # IPCONFIG /ALL Command decoded in UTF-8
    output = run_command('ipconfig /all')[0].decode('utf-8')

    # WLAN
    wlan_index = output.find('Wi-Fi:')
    if (wlan_index == -1): # if not shown
        headers_writer.writerow(['WLAN', 'Disconnected', '?', '?'])
    else:
        media = output.find('Media State', wlan_index, wlan_index + 36)
        if media == -1:
            media = 'Connected'
        else:
            media = 'Disconnected'
        headers_writer.writerow(['WLAN', media, find_header('Physical Address', wlan_index).strip(),
                                 find_header('DHCP Enabled', wlan_index).strip()])

    # ETHERNET
    ethernet_index = output.find('Ethernet:')
    if (ethernet_index == -1): # if not shown
        headers_writer.writerow(['Ethernet', 'Disconnected', '?', '?'])
    else:
        media = output.find('Media State', ethernet_index, ethernet_index + 36)
        if media == -1:
            media = 'Connected'
        else:
            media = 'Disconnected'
        headers_writer.writerow(['Ethernet', media, find_header('Physical Address', ethernet_index).strip(),
                                 find_header('DHCP Enabled', ethernet_index).strip()])

    headers_writer.writerow(['Computer Information: IP'])

    # IP
    header = 'IPv4 Address'
    if (output.find(header) == -1): # when disconnected
        headers_writer.writerow([header, '?'])
    else:
        headers_writer.writerow([header, find_header(header)])

    # Gateway
    header = 'Default Gateway'
    if (output.find(header) == -1): # when disconnected
        headers_writer.writerow([header, '?'])
    else:
        headers_writer.writerow([header, find_header(header).strip()])

    # Host Name
    hostname = run_command('hostname')[0].decode('utf-8')
    headers_writer.writerow(['Host Name',hostname.strip()])

    # Bonus
    headers_writer.writerow(['Computer Information: OS (BONUS)'])
    headers_writer.writerow(['Name', 'Version', 'Manufacturer', 'Configuration'])
    bonus_output = run_command('systeminfo')[0].decode('utf-8')
    headers_writer.writerow([os_find_header('OS Name').strip()[2:], os_find_header('OS Version').strip(),
                             os_find_header('OS Manufacturer').strip(), os_find_header('OS Configuration').strip()])

# Read from CSV File
with open('headers.csv', 'r') as headers_file:
    headers_reader = csv.reader(headers_file, delimiter = '\t')

    for line in headers_reader:
        for value in line:
            print(value, end= ' '*(30-len(value))) # To align the columns
        print()



