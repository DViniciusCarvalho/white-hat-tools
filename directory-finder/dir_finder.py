import requests

# PROTOCOL_PLUS_DOMAIN format -> protocol://domain/
PROTOCOL_PLUS_DOMAIN = 'https://python.org/'
WORD_LIST = open('directory-finder/wordlist_dir.txt', 'r')
RESULT_LIST = open('directory-finder/directories.txt', 'w+')
DIRECTORIES = WORD_LIST.readlines()

for line in DIRECTORIES:
    for directory in line.split("\n"):
        full_url = PROTOCOL_PLUS_DOMAIN + directory + "/"
        request = requests.get(full_url, auth = ('user', 'pass'))
        if request.status_code == 200:           
            print(full_url)
            RESULT_LIST.write(full_url)
            RESULT_LIST.write("\n")
        elif request.status_code == 403:
            print(full_url, ' (DENIED)')           
            RESULT_LIST.write(full_url)
            RESULT_LIST.write(' (DENIED)')
            RESULT_LIST.write("\n")
        else:
            continue

WORD_LIST.close()
RESULT_LIST.close()