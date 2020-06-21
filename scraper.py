from bs4 import BeautifulSoup
import requests, urllib, sys, json

def create_url(query, count='10'):
    global url
    url = "https://medium.com/search/posts?q="+urllib.parse.quote(query)+"&count="+count

def do_medium():
    create_url(query, count)
    print("[+] Finding articles on medium...")
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    # print(page.content)
    print("[+] FOUND")
    print("[+] Listing articles...")
    for divs in soup.find_all('div', class_='postArticle-content'):
        for anchors in divs.find_all('a'):
            print(anchors['href'])

type = sys.argv[1]
query = sys.argv[2]
count = sys.argv[3]

def do_hackerone():

    global query
    query=r"""
    {"operationName":"HacktivityPageQuery","variables":{"querystring":"%s","where":{"report":{"disclosed_at":{"_is_null":false}}},"orderBy":{"field":"popular","direction":"DESC"},"secureOrderBy":null,"count":%s,"maxShownVoters":10,"cursor":"MTI1"},"query":"query HacktivityPageQuery($querystring: String, $orderBy: HacktivityItemOrderInput, $secureOrderBy: FiltersHacktivityItemFilterOrder, $where: FiltersHacktivityItemFilterInput, $count: Int, $cursor: String, $maxShownVoters: Int) {\n  me {\n    id\n    __typename\n  }\n  hacktivity_items(first: $count, after: $cursor, query: $querystring, order_by: $orderBy, secure_order_by: $secureOrderBy, where: $where) {\n    total_count\n    ...HacktivityList\n    __typename\n  }\n}\n\nfragment HacktivityList on HacktivityItemConnection {\n  total_count\n  pageInfo {\n    endCursor\n    hasNextPage\n    __typename\n  }\n  edges {\n    node {\n      ... on HacktivityItemInterface {\n        id\n        databaseId: _id\n        ...HacktivityItem\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HacktivityItem on HacktivityItemUnion {\n  type: __typename\n  ... on HacktivityItemInterface {\n    id\n    votes {\n      total_count\n      __typename\n    }\n    voters: votes(last: $maxShownVoters) {\n      edges {\n        node {\n          id\n          user {\n            id\n            username\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    upvoted: upvoted_by_current_user\n    __typename\n  }\n  ... on Undisclosed {\n    id\n    ...HacktivityItemUndisclosed\n    __typename\n  }\n  ... on Disclosed {\n    id\n    ...HacktivityItemDisclosed\n    __typename\n  }\n  ... on HackerPublished {\n    id\n    ...HacktivityItemHackerPublished\n    __typename\n  }\n}\n\nfragment HacktivityItemUndisclosed on Undisclosed {\n  id\n  reporter {\n    id\n    username\n    ...UserLinkWithMiniProfile\n    __typename\n  }\n  team {\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    id\n    ...TeamLinkWithMiniProfile\n    __typename\n  }\n  latest_disclosable_action\n  latest_disclosable_activity_at\n  requires_view_privilege\n  total_awarded_amount\n  currency\n  __typename\n}\n\nfragment TeamLinkWithMiniProfile on Team {\n  id\n  handle\n  name\n  __typename\n}\n\nfragment UserLinkWithMiniProfile on User {\n  id\n  username\n  __typename\n}\n\nfragment HacktivityItemDisclosed on Disclosed {\n  id\n  reporter {\n    id\n    username\n    ...UserLinkWithMiniProfile\n    __typename\n  }\n  team {\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    id\n    ...TeamLinkWithMiniProfile\n    __typename\n  }\n  report {\n    id\n    title\n    substate\n    url\n    __typename\n  }\n  latest_disclosable_action\n  latest_disclosable_activity_at\n  total_awarded_amount\n  severity_rating\n  currency\n  __typename\n}\n\nfragment HacktivityItemHackerPublished on HackerPublished {\n  id\n  reporter {\n    id\n    username\n    ...UserLinkWithMiniProfile\n    __typename\n  }\n  team {\n    id\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    ...TeamLinkWithMiniProfile\n    __typename\n  }\n  report {\n    id\n    url\n    title\n    substate\n    __typename\n  }\n  latest_disclosable_activity_at\n  severity_rating\n  __typename\n}\n"}
    """ % (query, count)
    #print(query)

    print("[+] Finding public reports on Hackerone...")
    headers = {"content-type": "application/json"}
    request = requests.post('https://hackerone.com/graphql', data=query, headers=headers)
    if request.status_code == 200:
        print("[+] FOUND")
        print("[+] Listing reports...")
        json_response = json.loads(json.dumps(request.json()))
        for i in range(len(json_response['data']['hacktivity_items']['edges'])):
            print(json_response['data']['hacktivity_items']['edges'][i]['node']['report']['title'] +": " + json_response['data']['hacktivity_items']['edges'][i]['node']['report']['url'])
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, request.headers))

if(type == 'medium'):
    do_medium()
else:
    do_hackerone()