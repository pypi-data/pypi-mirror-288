from .abstract_channel import AbstractChannel


class WhatsappTemplateMessageSender(AbstractChannel):

    def __init__(self, phone_number, template_id, wa_params, name, provider_account_name=None):
        self.set_phone_number(phone_number)
        self.set_template_id(template_id)
        self.set_wa_params(wa_params)
        self.set_name(name)
        self.set_provider_account_name(provider_account_name)

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def set_template_id(self, template_id):
        self.template_id = template_id

    def set_wa_params(self, wa_params):
        self.wa_params = wa_params

    def set_name(self, name):
        self.name = name

    def set_provider_account_name(self, provider_account_name):
        self.provider_account_name = provider_account_name

    def notif_type(self):
        return 'SEND_TEMPLATE_MESSAGE'

    def json(self):
        return {
            'phone_number': self.phone_number,
            'template_id': self.template_id,
            'wa_params': self.wa_params,
            'name': self.name,
            'provider_account_name': self.provider_account_name
        }

    def attachments(self):
        return []


class WhatsappTemplateMessageSenderV3(AbstractChannel):

    def __init__(self, phone_number, template_name, wa_params):
        self.set_phone_number(phone_number)
        self.set_template_name(template_name)
        self.set_wa_params(wa_params)

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def set_template_name(self, template_name):
        self.template_name = template_name

    def set_wa_params(self, wa_params):
        self.wa_params = wa_params

    def notif_type(self):
        return 'SEND_TEMPLATE_MESSAGE_V3'

    def json(self):
        return {
            'phone_number': self.phone_number,
            'template_name': self.template_name,
            'wa_params': self.wa_params,
        }

    def attachments(self):
        return []
