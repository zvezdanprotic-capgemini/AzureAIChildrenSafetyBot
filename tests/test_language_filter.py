from language_filter import cleanse_output

def test_cleanse_output():
    text, modified = cleanse_output("I love you friend")
    assert modified is True
    assert "I love you" not in text
