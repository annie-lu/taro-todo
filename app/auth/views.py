# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..database.models.account import Account
from ..database.models.pet import Pet


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        new_account = Account(
                            username=form.username.data,
                            password=form.password.data)
        db.session.add(new_account)  # Adds new User record to database
        db.session.commit()  # Commits all changes

        new_pet = Pet(type=form.type.data, account_id=new_account.get_id())
        db.session.add(new_pet)
        db.session.commit()  # Commits all changes

        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        account = Account.query.filter_by(username=form.username.data).first()
        if account is not None and account.verify_password(
                form.password.data):
            # log employee in
            login_user(account)

            # redirect to the dashboard page after login
            return redirect(url_for('list'))

        # when login details are incorrect
        else:
            flash('Invalid username or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))