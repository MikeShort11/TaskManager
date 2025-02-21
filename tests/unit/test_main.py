import main

def test_help_menu(monkeypatch):
    """Tests if the enter button successfully exits the help menu."""
    monkeypatch.setattr("builtins.input", lambda _: "")

    output = main.help_menu()
    assert output is None
