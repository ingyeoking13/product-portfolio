import pytest
import re
from pathlib import Path
from src.utils.yaml.settings import replace_env_from_yaml
import yaml

def test_load_yaml(monkeypatch):
    _yaml = """
        test:
            name: hello
            env: ${{ exist_env }}:noworld
            source: ${{ none_env }}

        test2:
            name: bye:flah
            env: ${{ exist_env }}
            source: ${{ none_env}}:noworld
        test3: 
            name: ${{ exist_env }}/log.log
            env: ${{ none_env}}/log.log:log.log
    """
    monkeypatch.setenv('exist_env', 'hello world')
    result = replace_env_from_yaml(yaml.safe_load(_yaml))
    assert result == {
        'test': {
            'name': 'hello',
            'env': 'hello world',
            'source': None
        },
        'test2': {
            'name': 'bye:flah',
            'env': 'hello world',
            'source': 'noworld'
        },
        'test3': {
            'name': 'hello world/log.log',
            'env' : 'log.log'
        }
    }
