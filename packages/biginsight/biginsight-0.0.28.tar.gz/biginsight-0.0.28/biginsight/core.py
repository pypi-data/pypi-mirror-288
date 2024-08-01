import requests, json

routeUrl = "http://10.0.0.60:5002/api/track"

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

  def welcome(self):
    return "Welcome to BigInsight Library"

  # def register(self, userInfo):
  #   # userInfo: email, user id

  #   if self.apiKey == "":
  #     return "API Key is missing"
    
  #   if self.projectToken == "":
  #     return "Project Token is missing"

  #   resp = fetch(routeUrl + "/track_register", {
  #     "headers": { "Content-Type": "application/json" },
  #     "body": { "projectToken": self.projectToken, "userInfo": userInfo }
  #   })

  #   if resp.status_code == 200:
  #     return resp.json()

  #   return False
  
  # def login(self, userInfo):
  #   # userInfo: email, user id

  #   if self.apiKey == "":
  #     return "API Key is missing"
    
  #   if self.projectToken == "":
  #     return "Project Token is missing"
    
  #   resp = fetch(routeUrl + "/track_login", {
  #     "headers": { "Content-Type": "application/json" },
  #     "body": { "projectToken": self.projectToken, "userInfo": userInfo }
  #   })

  #   if resp.status_code == 200:
  #     return resp.json()
    
  #   return False
  
  def track(self, 
    userInfo, 
    type, 
    name, 
    action
  ):
    # page visits, user actions

    if self.apiKey == "":
      return "API Key is missing"
    
    if self.projectToken == "":
      return "Project Token is missing"

    resp = fetch(routeUrl + "/track_action", {
      "headers": { "Content-Type": "application/json" },
      "body": { 
        "apiKey": self.apiKey,
        "projectToken": self.projectToken,
        "userInfo": userInfo,
        "type": type, "name": name, "action": action
      }
    })

    if resp.status_code == 200:
      return True
    
    return False
  
  def track_error(self, type, name, action, info):
    # track any error if occurred

    if self.apiKey == "":
      return "API Key is missing"
    
    resp = fetch(routeUrl + "/track_error", {
      "headers": { "Content-Type": "application/json" },
      "body": { "type": type, "name": name, "action": action, "info": json.dumps(info) }
    })

    if resp.status_code == 200:
      return resp.json()
    
    return False
  
biginsight = BigInsight(__name__, __name__)
