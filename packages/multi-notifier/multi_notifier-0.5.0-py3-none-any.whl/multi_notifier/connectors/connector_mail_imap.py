"""Connector for mail including imap."""
import datetime
import email.mime.text
import imaplib
import logging
import time
import typing

import multi_notifier.connectors.connector_mail
import multi_notifier.connectors.exceptions
import multi_notifier.connectors.interface

MODULE_LOGGER = logging.getLogger(__name__)

_T = typing.TypeVar("_T")


class MailImapConfig(multi_notifier.connectors.connector_mail.MailConfig):
	"""Config for mail connector with IMAP"""
	imap_host: str


class MailImap(multi_notifier.connectors.connector_mail.Mail):
	"""Class to send e-mails and connect to mail account via IMAP."""

	def __init__(self, mail_config: MailImapConfig):
		"""Init Mail class.

		:param mail_config: config for mail connector with IMAP
		:raises multi_notifier.connectors.exceptions.ConnectorConfigurationException: If mail configuration is faulty
		"""
		multi_notifier.connectors.connector_mail.Mail.__init__(self, mail_config)
		self.__config = mail_config

	@staticmethod
	def __check_imap_result(result: tuple[str, _T]) -> _T:
		"""Check the result of an imap call.

		:param result: return value of an imap call. Must be a tuple of status and result
		:return: result of the call
		:raises multi_notifier.connectors.exceptions.ConnectorException: if result is not OK.
		"""
		if not result[0] == "OK":
			MODULE_LOGGER.exception(msg := "imap result was not ok!")
			raise multi_notifier.connectors.exceptions.ConnectorException(msg)

		return result[1]

	def get_unread_mails(self) -> list[email.message.Message]:
		"""Get a list of unread mails.

		:return: list of unread mails
		:raises multi_notifier.connectors.exceptions.ConnectorException: if any imap call was not OK.
		"""
		MODULE_LOGGER.debug("Try to get unread mails")
		imap_server = imaplib.IMAP4_SSL(self.__config.imap_host, timeout=10)
		self.__check_imap_result(imap_server.login(self.__config.user, self.__config.password))
		self.__check_imap_result(imap_server.select("Inbox"))

		# get unread mails
		messages = self.__check_imap_result(imap_server.search(None, "UNSEEN"))

		# get id's of unread mails
		unread_mails_ids = messages[0].split()

		unread_mails = []
		for mail_id in unread_mails_ids:
			# download a message and parse it to a email message
			data = self.__check_imap_result(imap_server.fetch(mail_id, "(RFC822)"))
			unread_mails.append(email.message_from_bytes(data[0][1]))

		self.__check_imap_result(imap_server.close())
		imap_server.logout()

		return unread_mails

	def wait_for_incoming_mail(self, max_time: int, expected_payload: str | None = None, sender_address: str | None = None) -> None:
		"""Wait for a incoming mail.

		If expected_payload or sender_address is given only mails will be accepted which fulfill all filters.
		:param max_time: Maximum time to wait
		:param expected_payload: text which must be part of the payload
		:param sender_address: sender address which must be contained in the "from" string
		:raises multi_notifier.connectors.exceptions.ConnectorTimeoutException: If expected mail was not received in time.
		"""
		MODULE_LOGGER.debug(f"Wait for incoming mail. Max_time = {max_time} | expected_payload = {expected_payload} | sender_address = {sender_address}")
		for idx in range(max_time + 1):
			for unread_mail in self.get_unread_mails():
				if expected_payload and expected_payload not in unread_mail.get_payload():
					continue
				if sender_address and sender_address not in unread_mail["From"]:
					continue
				return

			if idx < max_time:
				time.sleep(1)
		MODULE_LOGGER.error(msg := "Expected mail did not receive in time!")
		raise multi_notifier.connectors.exceptions.ConnectorTimeoutException(msg)

	def delete_old_mails(self, days: int):
		"""Delete old mails from mailbox

		:param days: Mails which are older than the defined days will be deleted.
		:raises multi_notifier.connectors.exceptions.ConnectorException: if result is not OK.
		"""
		MODULE_LOGGER.debug(f"Delete Mails which are older than {days} days")
		imap_server = imaplib.IMAP4_SSL(self.__config.imap_host, timeout=10)
		self.__check_imap_result(imap_server.login(self.__config.user, self.__config.password))
		self.__check_imap_result(imap_server.select("Inbox"))

		date_since = (datetime.date.today() - datetime.timedelta(days=days)).strftime("%d-%b-%Y")
		mail_ids_to_delete = self.__check_imap_result(imap_server.search(None, "(ALL)", f"SENTBEFORE {date_since}"))

		for message_id in mail_ids_to_delete[0].split():
			raw_mail = self.__check_imap_result(imap_server.fetch(message_id, "(RFC822)"))
			parsed_mail = email.message_from_bytes(raw_mail[0][1])
			MODULE_LOGGER.info(f"Delete mail from '{parsed_mail['From']}' which was sent on '{parsed_mail['Date']}'")
			imap_server.store(message_id, "+FLAGS", "\\Deleted")
		self.__check_imap_result(imap_server.expunge())
		self.__check_imap_result(imap_server.close())
		imap_server.logout()
