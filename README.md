# Lab 4 — Python Requests Library

**Course:** Software Defined Networking  
**Module:** Network Automation Fundamentals • **Lab #:** 4  
**Estimated Time:** 90–120 minutes

## Repository structure

```text
Lab-4-Python-Requests-Library
├── .devcontainer
│   ├── devcontainer.json
│   ├── health_check.py
│   ├── post_create.sh
│   └── post_start.sh
├── .gitignore
├── .markdownlint.json
├── .markdownlintignore
├── .pettierrc.yml
├── INSTRUCTIONS.backup.md
├── INSTRUCTIONS.md
├── LICENSE
├── README.backup.md
├── README.md
├── data
│   └── inventory.example.yml
├── lab.yml
├── prettierrc.yml
├── requirements.txt
└── src
    ├── __init__.py
    └── main.py
```


## Lab Topics

### The Python requests Library
The `requests` library is a powerful and user-friendly HTTP library for Python. It allows you to send HTTP requests easily and 
handle responses in a straightforward manner. With `requests`, you can interact with web services and APIs, making it an essential 
tool for network automation and data retrieval tasks.

Key features of the `requests` library include:
- Simple and intuitive API for sending HTTP requests (GET, POST, PUT, DELETE, etc.).
- Automatic handling of cookies and sessions.
- Support for custom headers, query parameters, and request bodies.
- Built-in JSON support for parsing and generating JSON data.
- Easy handling of response status codes and error handling.


In our last lab we made API calls using cURL and Postman. In this lab we will move into Python and use the `requests` library to make 
similar API calls programmatically. This will allow us to automate interactions with web services and build more complex workflows. Below
is a simple example of how to use the `requests` library to make a GET request and print the response.


```python
import requests

response = requests.get("https://api.example.com/data")
print(response.json())

```

### Why Use Python for API Interactions?
Python is a versatile and widely-used programming language that is particularly well-suited for network automation
and API interactions. Here are some reasons why Python is a great choice for working with APIs:

1. **Ease of Use**: Python's syntax is clean and easy to read, making it accessible for both beginners and experienced developers.
   This allows you to quickly write and understand code that interacts with APIs.

2. **Rich Ecosystem**: Python has a vast ecosystem of libraries and frameworks that simplify API interactions. The `requests` library,
   for example, provides a simple and intuitive way to send HTTP requests and handle responses.

3. **Cross-Platform**: Python is cross-platform, meaning you can run your scripts on various operating systems without modification.

4. **Integration Capabilities**: Python can easily integrate with other tools and systems, making it ideal for building complex workflows
   that involve multiple APIs and services.

5. **Community Support**: Python has a large and active community, which means you can find plenty of resources, tutorials, and support
   when working with APIs.

Overall, Python's simplicity, rich ecosystem, and integration capabilities make it an excellent choice for automating API interactions
and building network automation solutions.


### Working with JSON Responses
When you make an API call, the response is often returned in JSON format. Python provides built-in support for working with JSON data through the `json` module.

Here are some key points to keep in mind when working with JSON responses in Python:

1. **Parsing JSON**: You can use the `json.loads()` function to parse a JSON string into a Python dictionary or list. This allows you to
   easily access and manipulate the data.

2. **Generating JSON**: You can use the `json.dumps()` function to convert a Python dictionary or list into a JSON string. This is useful
   when you need to send JSON data in an API request.

3. **Accessing Data**: Once you have parsed the JSON response, you can access specific fields using standard dictionary or list indexing.

4. **Pretty-Printing**: The `pprint` module can be used to pretty-print JSON data, making it easier to read and understand.

Below is an example of how to parse a JSON response from an API and access specific fields:


```python
import requests
import json
from pprint import pprint

response = requests.get("https://api.example.com/data")
data = json.loads(response.text)
pprint(data)

specific_field = data.get("field_name")
print(specific_field)

```

### Retreiving a Joke from the Dad Jokes API
The Dad Jokes API is a fun and simple API that provides random dad jokes. You can use this API to fetch jokes and display them in your applications.

Here are some key points about the Dad Jokes API:

1. **Endpoint**: The main endpoint for fetching a random dad joke is `https://icanhazdadjoke.com/`.

2. **Headers**: To receive a JSON response, you need to set the `Accept` header to `application/json`.

3. **Response Format**: The response will be in JSON format and will contain fields such as `id`, `joke`, and `status`.

Below is an example of how to use the Dad Jokes API to fetch a random joke using Python's `requests` library:


```python
import requests

response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
data = response.json()
print(data["joke"])

```

### Using the Deck of Cards API
The Deck of Cards API is a simple API that allows you to create and manipulate decks of playing cards. You can use this API to create a new deck, draw cards, shuffle the deck, and more.

Here are some key points about the Deck of Cards API:

1. **Base URL**: The base URL for the Deck of Cards API is `https://deckofcardsapi.com/api/deck/`.

2. **Creating a Deck**: You can create a new shuffled deck by making a GET request to `https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1`.

3. **Drawing Cards**: To draw cards from a deck, you can make a GET request to `https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}`, where `{deck_id}` is the ID of the deck and `{count}` is the number of cards to draw.

Below is an example of how to create a new deck and draw cards using Python's `requests` library:


```python
import requests

# Create a new deck
response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
data = response.json()
deck_id = data["deck_id"]
print(f"Created new deck with ID: {deck_id}")

# Draw cards from the deck
response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=2")
data = response.json()
print("Drawn cards:")
for card in data["cards"]:
    print(f"{card['value']} of {card['suit']}")

```

### Adding User Interaction
Adding user interaction to your scripts can make them more dynamic and engaging. You can use Python's built-in `input()` function to prompt the user for input and make decisions based on their responses.

Here are some key points about adding user interaction:

1. **Prompting for Input**: Use the `input()` function to display a prompt and wait for the user to enter a response.

2. **Processing Input**: You can process the user's input by normalizing it (e.g., converting to lowercase, stripping whitespace) and using conditionals to determine the next steps.

3. **Loops**: You can use loops (e.g., `while` loops) to repeatedly prompt the user until they provide valid input or choose to exit.

Below is an example of how to add user interaction to a script that fetches jokes from the Dad Jokes API:


```python
import requests

while True:
    response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    data = response.json()
    print(data["joke"])

    user_input = input("Do you want another joke? (yes/no): ").strip().lower()
    if user_input != "yes":
        break

```



## License
© 2025 Sheldon Swanson — Classroom use.
