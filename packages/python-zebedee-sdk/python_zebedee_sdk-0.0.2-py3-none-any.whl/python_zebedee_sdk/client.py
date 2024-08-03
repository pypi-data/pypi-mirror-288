from typing import Optional
from aiohttp import ClientSession
from pydantic import BaseModel

from .utils import millisatoshis

class Client:
    def __init__(self, apikey: str):
        self.apikey = apikey
        self._base_url = 'https://api.zebedee.io'
        self._session = ClientSession(headers={'apikey': apikey})

    async def close(self):
        await self._session.close()

    class Gamertag:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

        async def send_payment(self, amount: millisatoshis, gamertag: str, description: str) -> dict:
            async with self._session.post(
                f"{self._base_url}/v0/gamertag/send_payment",
                json={'amount': str(amount), 'gamertag': gamertag, 'description': description}
            ) as response:
                return await response.json()

        async def transaction(self, zbd_id: str) -> dict:
            async with self._session.get(f"{self._base_url}/v0/gamertag/transaction/{zbd_id}") as response:
                return await response.json()

        async def charges(
            self, 
            amount: millisatoshis, 
            gamertag: str, 
            description: str = 'Requesting Charge for Gamertag',
            expiresIn: int = 1800,
            internalId: Optional[str] = None,
            callbackUrl: Optional[str] = None
        ) -> dict:
            json = {
                'amount': str(amount),
                'gamertag': gamertag,
                'description': description,
                'expiresIn': expiresIn
            }
            if internalId:
                json['internalId'] = internalId
            if callbackUrl:
                json['callbackUrl'] = callbackUrl
            async with self._session.post(f"{self._base_url}/v0/gamertag/charges", json=json) as response:
                return await response.json()

        async def get_id(self, gamertag: str) -> dict:
            async with self._session.get(f"{self._base_url}/user-id/gamertag/{gamertag}") as response:
                return await response.json()

        async def get_gamertag(self, zbd_id: str) -> dict:
            async with self._session.get(f"{self._base_url}/v0/gamertag/user-id/{zbd_id}") as response:
                return await response.json()

    class Lightning:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

        async def send_payment(
            self, 
            amount: millisatoshis, 
            lnAddress: str, 
            comment: str = 'Sending to a Lightning Address',
            internalId: Optional[str] = None,
            callbackUrl: Optional[str] = None
        ) -> dict:
            json = {'amount': str(amount), 'lnAddress': lnAddress, 'comment': comment}
            if internalId:
                json['internalId'] = internalId
            if callbackUrl:
                json['callbackUrl'] = callbackUrl
            async with self._session.post(f"{self._base_url}/v0/ln-address/send-payment", json=json) as response:
                return await response.json()

        async def validate(self, lnAddress: str) -> dict:
            async with self._session.get(f"{self._base_url}/v0/ln-address/validate/{lnAddress}") as response:
                return await response.json()

        async def create_charge(self, lnaddress: str, amount: millisatoshis, description: str = '') -> dict:
            async with self._session.post(
                f"{self._base_url}/v0/ln-address/fetch-charge",
                json={'lnaddress': lnaddress, 'amount': str(amount), 'description': description}
            ) as response:
                return await response.json()

    class Email:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

        async def send_payment(self, amount: millisatoshis, email: str, comment: str = 'Sending to an email') -> dict:
            async with self._session.post(
                f"{self._base_url}/v0/email/send-payment",
                json={'amount': str(amount), 'email': email, 'comment': comment}
            ) as response:
                return await response.json()

    class Payments:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

        async def send_payment(
            self,
            invoice: str,
            amount: millisatoshis = 0,
            description: str = 'Custom Payment Description',
            internalId: Optional[str] = None,
            callbackUrl: Optional[str] = None
        ) -> dict:
            json = {'invoice': invoice, 'description': description}
            if internalId:
                json['internalId'] = internalId
            if callbackUrl:
                json['callbackUrl'] = callbackUrl
            if amount:
                json['amount'] = str(amount)
            async with self._session.post(f"{self._base_url}/v0/payments", json=json) as response:
                return await response.json()

        async def get_payment(self, zbd_id: str) -> dict:
            async with self._session.get(f"{self._base_url}/v0/payments/{zbd_id}") as response:
                return await response.json()

    class Charge:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

        async def create_charge(
            self,
            amount: millisatoshis,
            description: str = 'My Charge Description',
            expiresIn: int = 1800,
            internalId: Optional[str] = None,
            callbackUrl: Optional[str] = None
        ) -> dict:
            json = {
                'amount': str(amount),
                'description': description,
                'expiresIn': expiresIn
            }
            if internalId:
                json['internalId'] = internalId
            if callbackUrl:
                json['callbackUrl'] = callbackUrl
            async with self._session.post(f"{self._base_url}/v0/charges", json=json) as response:
                return await response.json()

        async def get_charge(self, zbd_id: str) -> dict:
            async with self._session.get(f"{self._base_url}/v0/charges/{zbd_id}") as response:
                return await response.json()

        async def decode_charge(self, invoice: str) -> dict:
            async with self._session.get(f"{self._base_url}/v0/decode-invoice/{invoice}") as response:
                return await response.json()

    class Withdrawal:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

        async def create_withdrawal(
            self,
            amount: millisatoshis,
            description: str = 'Withdraw QR!',
            expiresIn: int = 1800,
            internalId: Optional[str] = None,
            callbackUrl: Optional[str] = None
        ) -> dict:
            json = {
                'amount': str(amount),
                'description': description,
                'expiresIn': expiresIn
            }
            if internalId:
                json['internalId'] = internalId
            if callbackUrl:
                json['callbackUrl'] = callbackUrl
            async with self._session.post(f"{self._base_url}/v0/withdrawal-requests", json=json) as response:
                return await response.json()

        async def get_withdrawal(self, zbd_id: str) -> dict:
            async with self._session.get(f"{self._base_url}/v0/withdrawal-requests/{zbd_id}") as response:
                return await response.json()

    class Voucher:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

        async def create_voucher(self, amount: millisatoshis, description: str = 'Voucher for user.') -> dict:
            async with self._session.post(
                f"{self._base_url}/v1/create-voucher",
                json={'amount': str(amount), 'description': description}
            ) as response:
                return await response.json()

        async def get_voucher(self, voucher_id: str) -> dict:
            async with self._session.get(f"{self._base_url}/v0/vouchers/{voucher_id}") as response:
                return await response.json()

        async def redeem_voucher(self, code_voucher: str) -> dict:
            async with self._session.post(
                f"{self._base_url}/v0/redeem-voucher",
                json={'code': code_voucher}
            ) as response:
                return await response.json()

        async def revoke_voucher(self, code_voucher: str) -> dict:
            async with self._session.post(
                f"{self._base_url}/v0/revoke-voucher",
                json={'code': code_voucher}
            ) as response:
                return await response.json()

    class Wallet:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

        async def get_wallet(self) -> dict:
            async with self._session.get(f"{self._base_url}/v0/wallet") as response:
                return await response.json()

    class Static:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

        async def create_static_charges(
            self,
            minAmount: millisatoshis,
            maxAmount: millisatoshis,
            description: str = 'Static Charge Client',
            successMessage: str = 'Success',
            allowedSlots: int = 1000,
            internalId: Optional[str] = None,
            callbackUrl: Optional[str] = None,
            identifier: Optional[str] = None
        ) -> dict:
            json = {
                'minAmount': str(minAmount),
                'maxAmount': str(maxAmount),
                'description': description,
                'successMessage': successMessage,
                'allowedSlots': allowedSlots
            }
            if internalId:
                json['internalId'] = internalId
            if identifier:
                json['identifier'] = identifier
            if callbackUrl:
                json['callbackUrl'] = callbackUrl
            async with self._session.post(f"{self._base_url}/v0/static-charges", json=json) as response:
                return await response.json()

        async def get_static_charge(self, zbd_id: str) -> dict:
            async with self._session.get(f"{self._base_url}/v0/static-charges/{zbd_id}") as response:
                return await response.json()

        async def update_static_charge(
            self,
            zbd_id: str,
            minAmount: millisatoshis,
            maxAmount: millisatoshis,
            description: str = 'Static Charge Client',
            successMessage: str = 'Success',
            allowedSlots: int = 1000,
            internalId: Optional[str] = None,
            callbackUrl: Optional[str] = None,
            identifier: Optional[str] = None
        ) -> dict:
            json = {
                'minAmount': str(minAmount),
                'maxAmount': str(maxAmount),
                'description': description,
                'successMessage': successMessage,
                'allowedSlots': allowedSlots
            }
            if internalId:
                json['internalId'] = internalId
            if identifier:
                json['identifier'] = identifier
            if callbackUrl:
                json['callbackUrl'] = callbackUrl
            async with self._session.patch(f"{self._base_url}/v0/static-charges/{zbd_id}", json=json) as response:
                return await response.json()

    class Keysend:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session

    class Utility:
        def __init__(self, api_instance: 'Client'):
            self._api = api_instance
            self._base_url = api_instance._base_url
            self._session = api_instance._session
