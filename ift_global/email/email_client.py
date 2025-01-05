"""
.. email

E-Mail Client Abstraction (:mod: `ift_global.cluster.hierarchy`)
================================================================

.. currentmodule:: ift_global.email.email_client

Abstraction functionality to send e-mail

.. autosummary::
   :toctree: generated/

   EmailClient



"""
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from smtplib import SMTP
from typing import Union

from ift_global.credentials.email_cr import MailConfig
from ift_global.email.css_stylesheets import stylesheets
from ift_global.email.html_tools import inject_stylesheet, jinja_to_html


class EmailClient:
    """
    E-Mail Functionality used to send e-mail.
    """

    def __init__(self, template_dir : str = None, template_name : str = None, loc_vars=vars(), **kwargs):
        """
        E-Mail class functionality to send e-mail.

        Args:
        :param template_dir: file path to folder where the body template is stored.
        :type template_dir: str
        :param template_name: name for the file used to generate e-mail body.
            if jinja2 is provided, it will build the template
            with `jinja_to_html` method.
        :type template_name: str

        Kwargs:
        
        :param attachments: file path to attachments.
        :type attachments:  Union[str, list] 
        :param style_sheet: '1', '2' or '3' depending on which stylesheet,
            if None selects '1'
        :type style_sheet: str
        :param smtp_server: smtp server address.
        :type smtp_server: str
        :param smtp_por: smtp server port.
        :type smtp_port: str
        :Examples:
            >>> from ift_global import EmailClient
            >>> mail_client = EmailClient(
            ...                 smtp_server='smtpin.biz.com',
            ...                 smtp_port=25
            ...                )
            >>> mail_client.send_mail(msg_from='no_reply_ift@ucl.ac.uk',
            ...                       msg_to="f.bar@ucl.ac.uk",
            ...                       mail_subject='UCL-IFT Auto Testing'
            ...                       )

        """
        self._mail_config = MailConfig(smtp_server=kwargs.get('smtp_server'),
                                       smtp_port=kwargs.get('smtp_port'))
        self.template_dir = template_dir
        self.template_name = template_name
        self.attachments = kwargs.get('attachments')
        self.style_sheet = kwargs.get('style_sheet') or '1'
        self._body_template = self.get_email_body(loc_vars)

    @property
    def body_template(self):
        return self._body_template

    @body_template.setter
    def body_template(self, body_string):
        self._body_template = inject_stylesheet(
            body_string,
            self._load_stylesheet()
            )

    def _load_stylesheet(self):
        """
        Select the css stylesheet.
        """
        if not self.style_sheet:
            self.style_sheet = '1'
        return stylesheets.get(self.style_sheet)

    def get_email_body(self, loc_vars):
        """
        Builds e-mail body - if None creates blank html.
        """
        if not self.template_name:
            return '<html></html>'
        else:
            return jinja_to_html(self.template_dir,
                                 self.template_name,
                                 stylesheet=self._load_stylesheet(),
                                 loc_vars=loc_vars)

    def _email_client(self, msg_from, msg_to, msg_body):
        """
        Establish connection to smtp server and sends e-mail.
        """
        try:
            server = SMTP(self._mail_config.smtp_server, self._mail_config.smtp_port)
            server.starttls()
            server.sendmail(msg_from, msg_to, msg_body)
            return 200
        except ConnectionError as e:
            print(f'failed to establish connection with smtp server as error : {e}')
        finally:
            server.quit()
        return server

    def _build_email_message(self, mail_subject, msg_from, msg_to):
        """
        Builds MIME message for mail client.
        """
        message = MIMEMultipart()
        message['Subject'], message['From'], message['To'] = mail_subject, msg_from, msg_to
        message.attach(MIMEText(self._body_template, "html"))
        if self.attachments:
                for f in self.attachments:
                    with open(f, "rb") as fil:
                        part = MIMEApplication(
                            fil.read(),
                            Name=os.path.basename(f)
                        )
                    # After the file is closed
                    part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
                    message.attach(part)

        msg_body = message.as_string()

        return msg_body

    def send_mail(self, msg_from : str, msg_to : Union[str, list], mail_subject : str):
        """
        Send e-mail.

        :param msg_from: string e-mail address of the sender
        :type msg_from: str
        :param msg_to: can be a string or a list of strings
            containing mail address of receiver
        :type msg_to: Union[str, list]
        :param mail_subject: a string with mail subject
        :type mail_subject: str
        :return: 200 is message is sent with success
        :rtype: int
        """
        if isinstance(msg_to, list):
            msg_to = COMMASPACE.join(msg_to)

        msg_body = self._build_email_message(mail_subject, msg_from, msg_to)
        server = self._email_client(msg_from, msg_to, msg_body)
        return server
