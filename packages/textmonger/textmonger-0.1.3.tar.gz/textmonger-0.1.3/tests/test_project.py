import pytest
from project import ascii, ner, Power
from readability import Readability

def test_ascii():
    result = ascii("The Text Monger")
    assert result.strip() != ""

def test_power_words():
    text = "One must act with caution and safety."
    power = Power('power_words.csv', text)
    result = power.find()
    assert len(result) > 0 

def test_ner(monkeypatch):
    text = "Barack Obama was born in Hawaii."
    def mock_displacy_serve(doc, style):
        return None
    monkeypatch.setattr('spacy.displacy.serve', mock_displacy_serve)
    ner(text)

if __name__ == "__main__":
    pytest.main()
