# This test is for the hello_test.py file.

from app.hello import hello

def test_say_hello():
    assert hello.say_hello("Ryan") == "Hello from the dev environment!"
