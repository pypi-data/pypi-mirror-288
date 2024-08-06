import requests, json

routeUrl = "https://www.biginsight.ca/api/track"

def fetch(url, info):
  resp = requests.post(
    url,
    json=info["body"],
    headers=info["headers"]
  )

  return resp

class BigInsight:
  def __init__(self, apiKey, projectToken):
    self.apiKey = apiKey
    self.projectToken = projectToken
  
  def track(self, info):
    # page visits, user actions
    userInfo = info["userInfo"] # email or user id or any other id to identify a specific user
    page = info["page"] # optional
    action = info["action"]
    body = { "userInfo": userInfo, "page": page, "action": action }

    if self.apiKey == "":
      return "API Key is missing"
    
    if self.projectToken == "":
      return "Project Token is missing"
    
    if "log_error" in info:
      body["log_error"] = True

    resp = fetch(routeUrl + "/track", {
      "headers": { "Content-Type": "application/json" },
      "body": { 
        "apiKey": self.apiKey,
        "projectToken": self.projectToken,
        **body
      }
    })

    if resp.status_code == 200:
      return resp.json()
    else:
      return resp.json(), 400
  
biginsight = BigInsight(__name__, __name__)
