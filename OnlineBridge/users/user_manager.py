from flask_user import UserManager
from flask import request, redirect, url_for, render_template, flash, current_app, abort
import flask_user.signals as signals
from urllib.parse import quote
from datetime import datetime
from OnlineBridge.users.forms import (
    MyRegisterForm,
    MyLoginForm,
    MyResendEmailConfirmationForm
)
from OnlineBridge.users.models import Role, Member
from OnlineBridge import mail, app
from flask_mail import Message


class MyUserManager(UserManager):

    def customize(self, app):

        # Configure customized forms
        self.RegisterFormClass = MyRegisterForm
        self.LoginFormClass = MyLoginForm
        self.ResendEmailConfirmationFormClass = MyResendEmailConfirmationForm


    def register_view(self):
        """ Display registration form and create new User."""

        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_LOGIN_ENDPOINT)
        safe_reg_next_url = self._get_safe_next_url('reg_next', self.USER_AFTER_REGISTER_ENDPOINT)

        # Initialize form
        login_form = self.LoginFormClass()  # for login_or_register.html
        register_form = self.RegisterFormClass(request.form)  # for register.html

        # invite token used to determine validity of registeree
        invite_token = request.values.get("token")

        # require invite without a token should disallow the user from registering
        if self.USER_REQUIRE_INVITATION and not invite_token:
            flash("Registration is invite only", "error")
            return redirect(url_for('user.login'))

        user_invitation = None
        if invite_token and self.db_manager.UserInvitationClass:
            data_items = self.token_manager.verify_token(invite_token, self.USER_INVITE_EXPIRATION)
            if data_items:
                user_invitation_id = data_items[0]
                user_invitation = self.db_manager.get_user_invitation_by_id(user_invitation_id)

            if not user_invitation:
                flash("Invalid invitation token", "error")
                return redirect(url_for('user.login'))

            register_form.invite_token.data = invite_token

        if request.method != 'POST':
            login_form.next.data = register_form.next.data = safe_next_url
            login_form.reg_next.data = register_form.reg_next.data = safe_reg_next_url
            if user_invitation:
                register_form.email.data = user_invitation.email

        # Process valid POST
        if request.method == 'POST' and register_form.validate():
            user = self.db_manager.add_user()
            register_form.populate_obj(user)
            user_email = self.db_manager.add_user_email(user=user, is_primary=True)
            register_form.populate_obj(user_email)

            # Store password hash instead of password
            user.password = self.hash_password(user.password)

            # fill additional fields
            role_player = Role.query.filter_by(name='Player').first()
            user.roles.append(role_player)

            oebv_nr = register_form.oebv_nr.data
            guest_nr = register_form.guest_nr.data
            member = None

            not_valid_mess = 'Abgleich mit Spielertabelle fehlgeschlagen'
            already_exist_mess = 'Zu diesem Spieler gibt es schon einen Benutzer'

            if oebv_nr and oebv_nr > 0:
                member = Member.query.filter_by(fed_nr=oebv_nr).first()
            elif guest_nr:
                member = Member.query.filter_by(guest_nr=guest_nr).first()

            if not member:
                abort(404)

            user.first_name = member.first_name
            user.last_name = member.last_name
            user.member_id = member.id

            # Email confirmation depends on the USER_ENABLE_CONFIRM_EMAIL setting
            request_email_confirmation = self.USER_ENABLE_CONFIRM_EMAIL
            # Users that register through an invitation, can skip this process
            # but only when they register with an email that matches their invitation.
            if user_invitation:
                if user_invitation.email.lower() == register_form.email.data.lower():
                    user_email.email_confirmed_at=datetime.utcnow()
                    request_email_confirmation = False

            self.db_manager.save_user_and_user_email(user, user_email)
            self.db_manager.commit()

            # Send 'registered' email and delete new User object if send fails
            if self.USER_SEND_REGISTERED_EMAIL:
                try:
                    # Send 'confirm email' or 'registered' email
                    # self._send_registered_email(user, user_email, request_email_confirmation)
                    self.send_registered_email(user)
                except Exception as e:
                    # delete new User object if send  fails
                    self.db_manager.delete_object(user)
                    self.db_manager.commit()
                    raise

            # Send user_registered signal
            signals.user_registered.send(current_app._get_current_object(),
                                         user=user,
                                         user_invitation=user_invitation)

            # Redirect if USER_ENABLE_CONFIRM_EMAIL is set
            if self.USER_ENABLE_CONFIRM_EMAIL and request_email_confirmation:
                safe_reg_next_url = self.make_safe_url(register_form.reg_next.data)
                return redirect(safe_reg_next_url)

            # Auto-login after register or redirect to login page
            if 'reg_next' in request.args:
                safe_reg_next_url = self.make_safe_url(register_form.reg_next.data)
            else:
                safe_reg_next_url = self._endpoint_url(self.USER_AFTER_CONFIRM_ENDPOINT)
            if self.USER_AUTO_LOGIN_AFTER_REGISTER:
                return self._do_login_user(user, safe_reg_next_url)  # auto-login
            else:
                return redirect(url_for('user.login') + '?next=' + quote(safe_reg_next_url))  # redirect to login page

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_REGISTER_TEMPLATE,
                      form=register_form,
                      login_form=login_form,
                      register_form=register_form)


    def resend_email_confirmation_view(self):
        """Prompt for email and re-send email conformation email."""

        # Initialize form
        form = self.ResendEmailConfirmationFormClass(request.form)

        # Process valid POST
        if request.method == 'POST' and form.validate():

            # Find user by email
            email = form.email.data
            user, user_email = self.db_manager.get_user_and_user_email_by_email(email)

            # Send confirm_email email
            if user:
                self._send_confirm_email_email(user, user_email)

            # Redirect to the login page
            return redirect(self._endpoint_url(self.USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT))

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_RESEND_CONFIRM_EMAIL_TEMPLATE, form=form)


    def send_registered_email(self, user):

        email = user.email

        # Generate a confirm_email_link
        object_id = user.id
        token = self.generate_token(object_id)
        confirm_email_link = url_for('user.confirm_email', token=token, _external=True)

        context = {
            'app_name': app.config['USER_APP_NAME'],
            'user': user,
            'confirm_email_link': confirm_email_link
        }

        subject = render_template('flask_user/emails/registered_subject.txt', **context)
        body = render_template('flask_user/emails/registered_message.html', **context)

        message = Message(subject=subject, recipients=[email])
        message.html = body
        mail.send(message)