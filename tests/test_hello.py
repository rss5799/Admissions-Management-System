# This test is for the hello_test.py file.

from app.hello import say_hello

def test_say_hello():
    assert say_hello("Ryan") == "Hello, Ryan!"
