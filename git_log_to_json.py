#imort csv and json library, these should be part of standard Python libraries, but if necessary you can run 'pip install csv json'
import csv  
import json

#define funtion for creating and populating json file tracking the amount of each change type
def create_change_count_json(csv_file_path, json_change_count_file_path):
    change_count = {'features': 0, 'fixes': 0, 'refactors': 0, 'docs': 0, 'tests': 0}

    #open csv file and read by row
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)


        for row in csv_reader:
            commit_message = row["commit_message"]

            #if commit contains relevant prefix then update the count of change type, could check for changes with no prefix in future
            if 'feat:' in commit_message.lower():
                change_count['features'] += 1
            if 'fix:' in commit_message.lower():
                change_count['fixes'] += 1
            if 'refactor:' in commit_message.lower():
                change_count['refactors'] += 1
            if 'doc:' in commit_message.lower():
                change_count['docs'] += 1
            if 'test:' in commit_message.lower():
                change_count['tests'] += 1

    #write to json file
    with open(json_change_count_file_path, 'w') as json_file:
        json.dump(change_count, json_file, indent=4)

#define funtion for creating and populating json file tracking the amount commits and their accompanying messages made by each user
def create_author_commits_json(csv_file_path, json_author_commits_file_path):
    author_commits = {}

    #follow similar process as previous funtion for opening and reading csv file
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            author = row['author_name']
            commit_message = row['commit_message']

            #if new author then create data and if existing user then append with new commit message and volume
            if author in author_commits:
                author_commits[author]['total_changes'] += 1
                author_commits[author]['commits'].append(commit_message)
            else:
                author_commits[author] = {'total_changes': 1, 'commits': [commit_message]}

    with open(json_author_commits_file_path, 'w') as json_file:
        json.dump(author_commits, json_file, indent=4)

#paths may need changing to match directory structure
csv_file_path = 'git_log.csv'
json_change_count_file_path = 'change_type.json'
json_author_commits_file_path = 'author_commits.json'

#run both functions to create both json files containing all necessary data
create_change_count_json(csv_file_path, json_change_count_file_path)
create_author_commits_json(csv_file_path, json_author_commits_file_path)