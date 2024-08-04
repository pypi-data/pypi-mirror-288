"""Connector for mail."""
import logging
import re

import pydantic
import redmail

import multi_notifier.connectors.exceptions
import multi_notifier.connectors.interface

MODULE_LOGGER = logging.getLogger(__name__)


class MailConfig(pydantic.BaseModel):
	"""Config for mail connector"""
	user: str
	password: str
	smtp_host: str
	smtp_port: int


class Mail(multi_notifier.connectors.interface.Interface):
	"""Class to send e-mails."""

	__html_pattern = re.compile(r"<[^<]+?>")

	def __init__(self, mail_config: MailConfig):
		"""Init Mail class.

		:param mail_config: config for mail connector
		:raises multi_notifier.connectors.exceptions.ConnectorConfigurationException: If mail configuration is faulty
		"""
		self.mail_sender = redmail.EmailSender(mail_config.smtp_host, mail_config.smtp_port, mail_config.user, mail_config.password)

	def send_message(self, recipient: str | list[str], message: str, subject: str | None = None, images: dict[str, str] | None = None) -> None:
		"""Send a message to one or multiple recipients

		:param recipient: one or multiple recipients. (Must be mail addresses!)
		:param message: Message which should be sent
		:param subject: Subject of the mail
		:param images: Images which will be added to the mail
		:raises multi_notifier.connectors.exceptions.ConnectorException: if mail could not be sent
		"""
		if images is None:
			images = {}

		# check if content of message is HTML and set text / HTML
		is_html = bool(self.__html_pattern.search(message))
		text = message if not is_html else None
		html = message if is_html else None

		try:
			self.mail_sender.send(
				subject=subject,
				receivers=recipient,
				text=text,
				html=html,
				body_images=images
			)
		except Exception as exc:
			MODULE_LOGGER.exception(msg := f"Could not send mail | Reason: {exc}")
			raise multi_notifier.connectors.exceptions.ConnectorException(msg)

	@staticmethod
	def is_valid_recipient(recipient: str) -> bool:
		"""Check if the given recipient is valid.
		:param recipient: Single recipient which should be checked
		:return: True if recipient has a supported format, else False
		"""
		if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", recipient):
			return True
		MODULE_LOGGER.warning(f"The recipient '{recipient}' is not valid !")
		return False
