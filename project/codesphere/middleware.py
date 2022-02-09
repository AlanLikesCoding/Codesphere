import datetime
from .libs import Colors

def CodesphereMiddleware(get_response):
  def middleware(request):

    response = get_response(request)
    # # IP Address
    # ip = request.META.get("REMOTE_ADDR")
    # # User Agent
    # user_agent = request.META.get("HTTP_USER_AGENT")
    # # Username (if logged in)
    # username = "[NOT LOGGED IN]"
    # if request.user.username in globals():
    #   username = request.user.username
    # # Path to Requested Webpage
    # endpoint = request.get_full_path()
    # # Response Code
    # response_code = response.status_code
    # # Method
    # method = request.method
    # # Date
    # date = datetime.datetime.now()
    # print(Colors.BLUE + Colors.BOLD + "[REQUEST]" + Colors.ENDC)
    # print(Colors.BLUE + Colors.BOLD + "   [TIME]  " + Colors.ENDC + Colors.CYAN + str(date))
    # print(Colors.BLUE + Colors.BOLD + "   [" + method + "] => " + Colors.ENDC + Colors.CYAN + "'" + endpoint + "' "+ str(response_code) + Colors.ENDC)
    # print(Colors.BLUE + Colors.BOLD + "   [" + str(ip) + "]" + " => " + Colors.ENDC + Colors.BLUE + username + Colors.CYAN + " | " + user_agent + Colors.ENDC)
    # print("\n")

    return response

  return middleware