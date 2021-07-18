import requests
import json
import csv


class FetchIssues:
    __json_file_name = 'bug_issues_with_pr.json'
    __csv_file_name = 'bug_issues_with_pr.csv'

    def __init__(self, user, password, repo):
        self.__auth = (user, password)
        self.__url = "https://api.github.com/search/issues?q=repo:" + repo + " is:closed linked:pr label:bug"
        # self.__url = 'https://api.github.com/search/issues?q=repo:' + repo + ' linked:pr label:bug'

    def fetch_issues(self):
        items = []
        r = requests.get(self.__url, auth=self.__auth)
        json_file = open(self.__json_file_name, 'w')

        def extend_to_array(request):
            if not r.status_code == 200:
                raise Exception(r.status_code)

            items.extend(request.json().get("items"))

        # write the firts page data
        extend_to_array(r)

        # getting data from the next pages
        if 'link' in r.headers:
            pages = dict(
                [(rel[6:-1], url[url.index('<') + 1:-1]) for url, rel in
                 [link.split(';') for link in
                  r.headers['link'].split(',')]])

            while 'last' in pages and 'next' in pages:
                pages = dict(
                    [(rel[6:-1], url[url.index('<') + 1:-1]) for url, rel in
                     [link.split(';') for link in
                      r.headers['link'].split(',')]])

                r = requests.get(pages['next'], auth=self.__auth)
                extend_to_array(r)
                if pages['next'] == pages['last']:
                    break

        json.dump(items, json_file, indent=4)
        json_file.close()
        items.clear()

    def write_to_csv(self):
        json_file = json.load(open(self.__json_file_name))

        csv_file = open(self.__csv_file_name, 'w')
        csv_out = csv.writer(csv_file)
        csv_out.writerow(
            ('Id', 'Title', 'Body', 'Created_At', 'Closed_At', 'State', 'Labels', 'MileStone_URL', 'URL', 'MileStone'))

        for data in json_file:
            csv_out.writerow([
                data.get('number'),
                data.get('title').encode('utf-8'),
                data.get('body').encode('utf-8'),
                data.get('created_at'),
                'null' if data.get('closed_at') == None else data.get('closed_at'),
                data.get('state'),
                [label.get("name") for label in data.get('labels')],
                'null' if data.get('milestone') == None else data.get('milestone').get('html_url'),
                data.get('html_url'),
                'null' if data.get('milestone') == None else data.get('milestone').get('title').split(" ")[0],

            ])

        csv_file.close()


fetch_issues = FetchIssues(user='username', password='password', repo='ankidroid/Anki-Android')
fetch_issues.fetch_issues()
fetch_issues.write_to_csv()
