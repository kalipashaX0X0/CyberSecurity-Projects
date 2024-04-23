import requests

def insecure_request(url):
    # This function makes an insecure HTTP request without proper error handling
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        print("Request successful")
        return response.text
    else:
        print("Request failed")

def vulnerable_function(user_input):
    # This function is vulnerable to SQL injection
    query = "SELECT * FROM users WHERE username='" + user_input + "'"
    # Execute query...

def main():
    # Hardcoded password - sensitive information exposed
    password = "admin123"

    # Unhandled exception
    try:
        result = 10 / 0
    except Exception as e:
        print("An error occurred:", e)

    # Calling insecure function with user-controlled input
    user_url = input("Enter a URL: ")
    insecure_request(user_url)

    # Calling vulnerable function with user-controlled input
    username = input("Enter a username: ")
    vulnerable_function(username)

if __name__ == "__main__":
    main()
