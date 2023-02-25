import requests

# format -> full_url = http(s):// (PROTOCOL) + randomword (SUBDOMAIN) + domain.tld (DOMAIN)

# The construction of the final URL to request to the server
PROTOCOL = "https://" # Protocol
WORD_LIST = open("subdomain-finder/wordlist_subd.txt") # All the possible subdomains
DOMAIN = ".python.org" # domain.tld
# Select the file to write the results and open it
RESULT_LIST = open("subdomain-finder/subdomains.txt", "w+")
SUBDOMAINS = WORD_LIST.readlines()

# Tries to connect to the current subdomain of the host and then prints it if exists and writes on the file of results
for subdomain in SUBDOMAINS:
    for sub in subdomain.split("\n"):
        full_url = PROTOCOL + sub + DOMAIN
        try:
            request = requests.get(full_url, auth=('user', 'pass'))
            if request.status_code == 200:
                print(full_url)
                RESULT_LIST.write(full_url)
                RESULT_LIST.write("\n")               
        except:
            continue

# Close the files when the directory searching is complete
WORD_LIST.close()
RESULT_LIST.close()
