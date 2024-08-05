import requests
from bs4 import BeautifulSoup

from typing import Union, List, Dict, Any

from .exceptions import *

class Swarmbytes:
	def __init__(self, API_PREFIX_URL: str = "", API_VERSION: str = "", API_DOMAIN: str = "https://dashboard.swarmbytes.com", API_AJAX_PREFIX_URL: str = "/ajax") -> None:
		"""Initialise Swarmbytes API Client. """
		self.set_api_version(API_VERSION, reload = False)
		self.set_api_prefix_url(API_PREFIX_URL, reload = False)
		self.set_api_domain(API_DOMAIN, reload = False)
		self.set_api_ajax_prefix_url(API_AJAX_PREFIX_URL, reload = True)
		self.__session = requests.Session()
		self.set_default_headers()
		self.remove_proxy()

	def set_default_headers(self, headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
	}):
		self.__default_headers = headers

	def set_api_version(self, version: str, reload = True):
		self.API_VERSION = version

		if reload:
			self.reload_urls()

	def set_api_domain(self, domain: str, reload = True):
		self.API_DOMAIN = domain

		if reload:
			self.reload_urls()

	def set_api_prefix_url(self, prefix_url: str, reload = True):
		self.API_PREFIX_URL = prefix_url

		if reload:
			self.reload_urls()

	def set_api_ajax_prefix_url(self, ajax_prefix_url: str, reload = True):
		self.API_AJAX_PREFIX_URL = ajax_prefix_url

		if reload:
			self.reload_urls()

	def reload_urls(self):
		self.API_BASE_URL = f'{self.API_DOMAIN}{self.API_PREFIX_URL}{self.API_VERSION}'
		self.API_AJAX_BASE_URL = f'{self.API_DOMAIN}{self.API_PREFIX_URL}{self.API_VERSION}{self.API_AJAX_PREFIX_URL}'

	def __make_base_request(self, req_type: str, url: str, headers: dict = {}, *args, **kwargs):
		"""Helper function to make regular requests. """
		return self.__session.request(req_type, f'{url}', proxies = self.proxy_conf, headers = {
			**self.__default_headers, **headers
		}, *args, **kwargs)

	def __make_dashboard_request(self, req_type: str, endpoint: str, headers: dict = {}, *args, **kwargs):
		"""Helper function to make regular requests. """
		return self.__make_base_request(req_type, f'{self.API_BASE_URL}{endpoint}', headers, *args, **kwargs)

	def __make_ajax_request(self, req_type: str, endpoint: str, headers: dict = {}, *args, **kwargs):
		"""Helper function to make AJAX requests. """
		return self.__make_base_request(req_type, f'{self.API_AJAX_BASE_URL}{endpoint}', headers, *args, **kwargs)

	def set_proxy(self, proxy_str: Union[str, None] = None) -> bool:
		"""Sets the proxy for future API requests. """
		if proxy_str is None:
			return False
		
		proxy = proxy_str.split(":")

		if len(proxy) > 2:
			ip, port, username, password = proxy

			self.proxy_conf = {
				"http": f"socks5://{username}:{password}@{ip}:{port}",
				"https": f"socks5://{username}:{password}@{ip}:{port}",
			}
		else:
			ip, port = proxy

			self.proxy_conf = {
				"http": f"socks5://{ip}:{port}",
				"https": f"socks5://{ip}:{port}",
			}

		return True

	def remove_proxy(self) -> bool:
		"""Removes the proxy for future API requests. """
		self.proxy_conf = None
		return True

	def __get_csrf_token_for_login(self) -> str:
		"""Gets CSRF token for login. """
		r = self.__make_dashboard_request("GET", "/login")

		soup = BeautifulSoup(r.text, "html.parser")

		input_elem = soup.find("input", attrs = {"name": "_csrf_token"})

		return input_elem.get("value")

	def login(self, username: str, password: str) -> Union[bool, None]:
		"""Logs in using the username and password. """
		csrf_token = self.__get_csrf_token_for_login()

		r = self.__make_dashboard_request("POST", "/login", data = {
			"username": username,
			"password": password,
			"_csrf_token": csrf_token,
		})

		if r.status_code == 302:
			return self.is_logged_in()

		return None

	def is_logged_in(self) -> Union[bool, None]:
		"""Checks if the Swarmbytes object session still contains the login using simple strategy to visit the Swarmbytes dashboard page and check if data is still visible. """
		r = self.__make_dashboard_request("GET", "/", allow_redirects = False)

		if r.status_code == 302:
			return False
		
		if r.status_code == 200:
			return True

		return None

	def get_recent_activity(self) -> Dict[str, Any]:
		"""Gets recent activity. """
		return self.__make_ajax_request("GET", "/recent_activity").json()

	def get_daily_country_averages(self) -> Dict[str, Any]:
		"""Gets daily averages of countries. """
		return self.__make_ajax_request("GET", "/daily_country_averages").json()

	def get_daily_usage_averages(self) -> Dict[str, Any]:
		"""Gets daily averages of usage. """
		return self.__make_ajax_request("GET", "/daily_usage_averages").json()

	def get_monthly_country_averages(self) -> Dict[str, Any]:
		"""Gets monthly averages of countries. """
		return self.__make_ajax_request("GET", "/monthly_country_averages").json()

	def get_monthly_type_averages(self) -> Dict[str, Any]:
		"""Gets monthly averages of types. """
		return self.__make_ajax_request("GET", "/monthly_type_averages").json()

	def get_monthly_usable_totals(self) -> Dict[str, Any]:
		"""Gets monthly usable totals. """
		return self.__make_ajax_request("GET", "/monthly_usable_totals").json()

	def get_api_key(self):
		r = self.__make_dashboard_request("GET", "/")

		if r.status_code != 200:
			return False

		soup = BeautifulSoup(r.text, "html.parser")

		code_elem = soup.select_one("div.api-key code")
		
		if not code_elem:
			return False

		api_key = code_elem.get_text().strip()

		return api_key

	def download_invoice(self, accounting_invoice_link: str, path: str):
		r = self.__make_dashboard_request("GET", accounting_invoice_link, stream = True, allow_redirects = False)

		if not r.ok:
			return False

		with open(path, "wb") as f:
			for content in r.iter_content(chunk_size = 1024):
				f.write(content)

		return True

	def get_accounting_data(self) -> List[Dict[str, Any]]:
		r = self.__make_dashboard_request("GET", "/accounting")

		if r.status_code != 200:
			return False
		
		soup = BeautifulSoup(r.text, "html.parser")

		accounting_rows_elems = soup.find("div", class_ = "box-body").find_all("tr")[1:]

		accounting_data = []

		accounting_row_sequence = ["date", "macip", "price", "status", "invoice_link"]

		for accounting_row_elem in accounting_rows_elems:
			column_elems = accounting_row_elem.find_all("td")

			accounting_row_dict = {}

			for i, column_elem in enumerate(column_elems, start = 0):
				key = accounting_row_sequence[i]

				if key == "invoice_link":
					invoice_link_a = column_elem.find("a")
					
					if invoice_link_a:
						value = invoice_link_a["href"]
					else:
						value = None
				else:
					value = column_elem.get_text().strip()

				accounting_row_dict[key] = value

			accounting_data.append(accounting_row_dict)

		return accounting_data

	def logout(self) -> bool:
		r = self.__make_dashboard_request("GET", "/logout")

		if r.status_code == 302:
			return not self.is_logged_in()
		
		return None

	def __repr__(self):
		return f"<{self.__class__.__name__} object at: {hex(id(self))}>"
