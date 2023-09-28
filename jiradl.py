from jira import JIRA
import requests
import argparse

def login_jira(username, password, server):
    options = {'server': server}
    return JIRA(options, basic_auth=(username, password))

def get_issue_content(jira, issue_key, server):
    url = f"{server}/si/jira.issueviews:issue-html/{issue_key}/{issue_key}.html"
    response = requests.get(url, auth=(jira._session.auth))
    return response.text

def save_html(issue_key, html_content):
    with open(f"{issue_key}.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='Download Jira tickets as HTML.')
    parser.add_argument('--issue', type=str, help='Specific issue key to download')
    args = parser.parse_args()

    username = "USERNAME"
    password = "PASSWORD"
    server = "https://jira.url"
    project = "PROJECT"
    specific_issue = args.issue

    jira = login_jira(username, password, server)

    if specific_issue:
        issue_keys = [specific_issue]
    else:
        jql_query = 'project="{}"'.format(project)
        issues = jira.search_issues(jql_query, maxResults=False)
        issue_keys = [issue.key for issue in issues]

    for issue_key in issue_keys:
        html_content = get_issue_content(jira, issue_key, server)
        save_html(issue_key, html_content)
        print(f"Saved {issue_key}.html")

if __name__ == "__main__":
    main()


