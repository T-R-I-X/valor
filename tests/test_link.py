import json
import pytest
from valor import Service
from .fixtures import schema, session

def test_link_interpolate_args(schema, session):
    link = Service(schema, session).app.destroy
    assert link.interpolate_args(['my-app']) == 'https://api.heroku.com/apps/my-app'

def test_link_interpolate_args_too_few(schema, session):
    link = Service(schema, session).app.destroy
    with pytest.raises(TypeError):
        link.interpolate_args([])

def test_link_interpolate_args_too_many(schema, session):
    link = Service(schema, session).app.destroy
    with pytest.raises(TypeError):
        link.interpolate_args(['foo', 'bar'])

def test_link_construct_body(schema, session):
    link = Service(schema, session).app.create
    body = link.construct_body({'stack': 'cedar'})
    assert json.loads(body) == {'stack': 'cedar'}

def test_link_construct_body_no_body(schema, session):
    link = Service(schema, session).app.destroy
    assert link.construct_body({}) is None
    with pytest.raises(TypeError):
        link.construct_body({'bad': 'arg'})

def test_link_construct_body_unexpected_arg(schema, session):
    link = Service(schema, session).app.create
    with pytest.raises(TypeError):
        link.construct_body({'stack': 'cedar', 'bad': 'arg'})

def test_link_construct_body_missing_required_arg(schema, session):
    link = Service(schema, session).app.create
    link._link['schema']['required'] = ['stack']
    with pytest.raises(TypeError):
        link.construct_body({})