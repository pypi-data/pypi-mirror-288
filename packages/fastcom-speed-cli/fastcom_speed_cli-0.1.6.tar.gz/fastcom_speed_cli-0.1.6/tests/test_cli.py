import json
import sys

from io import StringIO

import pytest

from fast_speedtest.cli import camel_to_snake
from fast_speedtest.cli import fast_config_t
from fast_speedtest.cli import main
from fast_speedtest.cli import parse_arguments
from fast_speedtest.cli import snake_to_camel


def test_snake_to_camel():
    assert snake_to_camel("hello_world") == "helloWorld"
    assert snake_to_camel("hello-world", sep="-") == "helloWorld"


def test_camel_to_snake():
    assert camel_to_snake("helloWorld") == "hello_world"
    assert camel_to_snake("helloWorld", sep="-") == "hello-world"


def test_parser_help(monkeypatch: pytest.MonkeyPatch):
    # Simulate command-line arguments
    monkeypatch.setattr(sys, 'argv', ['cli', '-h'])
    
    # Capture output
    captured_output = StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)
    with pytest.raises(SystemExit) as excinfo:
        # Call the main function which will trigger SystemExit
        parse_arguments()
    assert excinfo.value.code == 0


def test_parser_no_args(monkeypatch: pytest.MonkeyPatch):
    # Simulate command-line arguments
    monkeypatch.setattr(sys, 'argv', ['cli'])
    
    # Call the main function which will trigger SystemExit
    config, auto_install_browsers, output_json, = parse_arguments()
    assert config.fast_config == fast_config_t()
    assert auto_install_browsers
    assert not output_json


def test_parser_with_args(monkeypatch: pytest.MonkeyPatch):
    # Simulate command-line arguments
    monkeypatch.setattr(sys, 'argv', ['cli', '--max-duration', '5'])
    
    # Call the main function which will trigger SystemExit
    config, auto_install_browsers, output_json, = parse_arguments()
    assert auto_install_browsers
    assert not output_json
    assert config.fast_config == fast_config_t(maxDuration=5)


def test_main(monkeypatch: pytest.MonkeyPatch):
    # Simulate command-line arguments
    args = [
        'cli',
        '--min-duration', "1",
        '--max-duration', '2',
        '--max-connections', '1',
        '--no-upload',
        '--interval', '1',
        '--json'
    ]
    monkeypatch.setattr(sys, 'argv', args)
    
    # Capture output
    captured_output = StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)
    main()
    captured_output.seek(0)
    output = captured_output.getvalue()
    result = json.loads(output)[-1]
    assert not result["isDone"]
    assert result["downloadSpeed"] > 0
    assert result["uploadSpeed"] > 0
    assert len(result["serverLocation"]) > 0
