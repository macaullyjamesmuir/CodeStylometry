from urllib import urlopen
from urllib import urlretrieve
import json
import sys
import os
import zipfile
import shutil
import multiprocessing
import requests
import StringIO

#
# Scrapes Google Code Jam data, and extracts the C/C++/Python source files.
#
# The directory structure and naming convention of the data is as follows:
#
# ./solutions/   |--> c/   | --> username0 | --> p[problem_number].[user_name]0.c
#                |         |               | --> p2453486.Bob0.c
#                |         |               | --> etc...
#                |         |
#                |         | --> name0     | --> etc...
#                |         |               | --> etc...
#                |         |               | --> etc...
#                |         |
#                |         | --> another0  | --> etc...
#                |                         | --> etc...
#                |
#                |--> cpp/ | --> etc...    | --> etc...
#                |         |               | --> etc...             
#                |         |
#                |         | --> etc...    | --> etc...
#

# returns the URL to download the user submission
def get_download_url(round_id, problem_id, username):
    return "http://code.google.com/codejam/contest/scoreboard/do?cmd=GetSourceCode&contest=" \
                + round_id \
                + "&problem=" \
                + problem_id \
                + "&io_set_id=0&username=" \
                + username

# scrapes the C/C++/Python files of the given round
def scrape(round_id, round_desc, problems, script_path):
    totalErrors = 0
    print "START: {}".format(round_desc)

    # load list of users
    user_file = open(script_path + '/users/' + round_id + '.txt', 'r')
    users = user_file.read().splitlines()
    
    # loop through problems in the round
    for problem_json in problems:
        problem_id = problem_json['id']

        # loop through users who participated in the round
        for username in users:

            # download and read zip
            # try-except in case of a bad header
            try:
                download_url = get_download_url(round_id, problem_id, username)
                request = requests.get(download_url, stream=True)
                my_zip = zipfile.ZipFile(StringIO.StringIO(request.content))

                # loop through each file in the zip file
                for my_file in my_zip.namelist():

                    # check for C/C++/Python source
                    if my_file.endswith(('.c', '.cpp')):
                        target_source = username + '0' # destination of source files
                        file_newname = 'p' + problem_id + '.' + username + '0.' # appropriate name for file
                        if my_file.endswith('.c'):
                            file_newname += 'c'
                            target_source = 'c/' + target_source
                        elif my_file.endswith('.cpp'):
                            file_newname += 'cpp'
                            target_source = 'cpp/' + target_source
                        target_source = 'solutions/' + target_source

                        # make directory for language and author
                        if not os.path.exists(target_source):
                            os.makedirs(target_source)

                        # extract and rename source file
                        f = open(os.path.join(target_source, file_newname), 'wb')
                        f.write(my_zip.read(my_file))
                        f.close()
                        
            except:
                totalErrors += 1

    print "DONE: {} (Errors: {})".format(year, round_desc, totalErrors)

# main section of script
if __name__ == '__main__':
    script_path = os.path.dirname(os.path.realpath(__file__))
    metadatafile = open(script_path + "/metadata.json").read()
    metadata = json.loads(metadatafile)

    # loop through years
    for year_json in metadata['competitions']:

        # loop through rounds
        for round_json in year_json['round']:
            round_id = round_json['contest']
            round_desc = round_json['desc']
            problems = round_json['problems']

            # run scraper on current round
            scraper = multiprocessing.Process(target=scrape, args=(round_id, round_desc, problems, script_path))
            scraper.start()
