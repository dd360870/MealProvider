# tests/test_auth.py
import pytest
from flask import session
from flaskr.model import User

def test_login_success(client, mocker):
    with client:
        # Mock User.validate to return a mock user
        mock_user = mocker.Mock()
        mock_user.id = 1
        mock_user.is_clerk = False
        mocker.patch('flaskr.model.User.validate', return_value=mock_user)

        # Simulate a POST request to the login endpoint
        response = client.post('/auth/login', data={'username': 'test', 'password': 'testpass'})

        # Check the response and session
        assert response.status_code == 302  # Redirect to index
        assert session['user_id'] == mock_user.id
        assert response.headers['Location'] == '/'

def test_clerk_login_success(client, mocker):
    with client:
        # Mock User.validate to return a mock user
        mock_user = mocker.Mock()
        mock_user.id = 1
        mock_user.is_clerk = True
        mock_user.restaurant_id = 1
        mocker.patch('flaskr.model.User.validate', return_value=mock_user)

        # Simulate a POST request to the login endpoint
        response = client.post('/auth/login', data={'username': 'clerk', 'password': 'clerkpass'})
        print('Location:', response.headers.get('Location'))

        # Check the response and session
        assert response.status_code == 302
        assert session['user_id'] == mock_user.id
        assert response.headers['Location'] == f'/clerk/{mock_user.restaurant_id}/'

def test_login_failure(client, mocker):
    with client:
        # Mock User.validate to return None (invalid credentials)
        mocker.patch('flaskr.model.User.validate', return_value=None)

        # Simulate a POST request to the login endpoint
        response = client.post('/auth/login', data={'username': 'test', 'password': 'wrongpass'})

        # Check the response and session
        assert response.status_code == 200  # No redirect, renders login page again
        assert b"User credential is invalid." in response.data
        assert 'user_id' not in session

def test_register_success(client, mocker):
    with client:
        mocker.patch('flaskr.model.User.new')

        response = client.post('/auth/register', data={'username': 'new_user', 'password': 'new_pass', 'password_confirm': 'new_pass'})

        assert response.status_code == 302
        assert response.headers['Location'] == '/auth/login'

def test_register_failure(client, mocker):
    with client:
        # Mock User.new to raise an exception (simulate user already registered)
        mocker.patch('flaskr.model.User.new', side_effect=Exception("User already registered"))

        # Simulate a POST request to the register endpoint with invalid data
        response = client.post('/auth/register', data={'username': 'existing_user', 'password': 'existing_pass', 'password_confirm': 'existing_pass'})

        # Check the response and session
        assert response.status_code == 200  # No redirect, renders register page again
        assert b"User already registered" in response.data
