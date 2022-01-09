from attr import has
import requests
from typing import cast
from .const import STORAGE_VERSION, STORAGE_KEY


class BaxiAPI:
    BASE_URL = "https://ruapi.remoteapp.bdrthermea.com/v1.0"
    BASE_HEADER = {
        "Accept": "application/json, text/plain, */*",
        "Connection": "keep-alive",
        "X-Requested-With": "com.bdrthermea.roomunitapplication.baxi",
        "Content-Type": "application/json;charset=UTF-8",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": "Basic cnVhcHA6V25AW1tjJF1QfjghM2AoW35BZiUnSDI/bEh3XWNpaXE6cn1MT3pqTGsueTVNSCtfcT0=",
    }
    endpoints = {
        "LOGIN": "https://remoteapp.bdrthermea.com/user/baxi/login",
        "PAIR": BASE_URL + "/pairings",
        "CONNECTION": BASE_URL + "/system/gateway/connection",
        "CAPABILITIES": BASE_URL + "/capabilities",
    }

    def __init__(self, hass, user, password, pairing_code):
        self.hass_storage = hass.helpers.storage.Store(
            STORAGE_VERSION, STORAGE_KEY, private=True, atomic_writes=True
        )
        self.hass = hass
        self._bootstraped = False
        self._user = user
        self._password = password
        self._pairing_code = pairing_code

    async def bootstrap(self):
        if self._bootstraped:
            return

        if not await self._load_stored_token():
            self._login()
            self._pair()

        await self._load_capabilities()
        await self._load_device_information()
        self._bootstraped = True

    async def _load_stored_token(self):
        data = await self.hass_storage.async_load()
        self.token = data.get("token", None) if data else None
        return bool(self.token)

    async def _store_token(self, token):
        data = {"token": token}
        await self.hass_storage.async_save(data)

    async def _login(self):
        api_endpoint = self.endpoints["LOGIN"]
        payload = {
            "username": self._user,
            "password": self._password,
        }

        response = await self.async_post_request(endpoint=api_endpoint, payload=payload)

        self.amdatu_token = response.headers.get("amdatu_token")

    async def _pair(self):
        api_endpoint = self.endpoints["PAIR"]
        payload = {
            "account": self._user,
            "brand": "baxi",
            "password": self._password,
            "device": "HomeAssistant",
            "otp": self._pairing_code,
        }

        response = await self.async_post_request(endpoint=api_endpoint, payload=payload)

        token = await response.json().get("token", None)
        self._store_token(token)

    def _sync_request(self, request, url, headers, payload=None):
        if request == "get":
            return requests.get(url=url, headers=headers)
        elif request == "put":
            return requests.put(url=url, json=payload, headers=headers)
        elif request == "post":
            return requests.post(url=url, json=payload, headers=headers)

    async def async_post_request(self, endpoint, payload, headers=BASE_HEADER):

        response = await self.hass.async_add_executor_job(
            self._sync_request, "post", endpoint, headers, payload
        )

        if not response.ok:
            # handle error
            return None
        return response

    async def async_put_request(self, endpoint, payload, headers=BASE_HEADER):

        headers = headers.copy()
        headers["X-Bdr-Pairing-Token"] = self.token

        response = await self.hass.async_add_executor_job(
            self._sync_request, "put", endpoint, headers, payload
        )

        if not response.ok:
            # handle error
            return None
        return response

    async def async_get_request(self, endpoint, headers=BASE_HEADER):

        headers = headers.copy()
        headers["X-Bdr-Pairing-Token"] = self.token

        response = await self.hass.async_add_executor_job(
            self._sync_request, "get", endpoint, headers
        )

        if not response.ok:
            # TODO handle error
            return None

        return response.json()

    async def connection_status(self):
        api_endpoint = self.endpoints["CONNECTION"]

        response = await self.async_get_request(api_endpoint)

        return response.get("status") == "connected_to_appliance"

    async def _load_capabilities(self):
        api_endpoint = self.endpoints["CAPABILITIES"]

        capabilities = await self.async_get_request(api_endpoint)

        for subsystem in capabilities.values():
            subsystem = (
                subsystem[0] if isinstance(subsystem, list) else subsystem
            )  # TODO: what if empty list?
            for function, uri in subsystem.items():
                if function.endswith("Uri") and function != "uri":
                    function = function.replace("Uri", "")
                    if function == "status" and "producers" in uri:
                        function = "producer_status"
                    self.endpoints[function] = self.BASE_URL + uri

    async def _load_device_information(self):
        api_endpoint = self.endpoints["deviceInformation"]

        self.info = await self.async_get_request(api_endpoint)

    async def get_operating_mode(self):
        api_endpoint = self.endpoints["operatingMode"]

        return await self.async_get_request(api_endpoint)

    def get_device_information(self):
        return self.info

    def is_bootstraped(self):
        return self._bootstraped

    async def get_status(self):
        api_endpoint = self.endpoints.get("status")

        return await self.async_get_request(api_endpoint)

    async def set_target_temperature(self, target_temp):
        api_endpoint = self.endpoints.get("putSetpointManual")
        payload = {
            "roomTemperatureSetpoint": target_temp,
        }
        return await self.async_put_request(api_endpoint, payload)
