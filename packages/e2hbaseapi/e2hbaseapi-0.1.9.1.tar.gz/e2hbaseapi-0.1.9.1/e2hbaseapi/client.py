import re
import json
import urllib3
import logging
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
from typing import List, Dict, Set, Any
from tenacity import retry, wait_fixed, stop_after_attempt
from pydantic import BaseModel, Field, EmailStr

urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ExtractedInfo(BaseModel):
    emails: List[EmailStr]
    phones: List[str]
    fivem_licenses: List[str]
    steam_ids: List[str]


class E2hApiClient:
    def __init__(self, api_key: str):
        """
        Initialise le client E2HBASE avec la clé API.

        :param api_key: La clé API pour accéder à E2HBASE.
        """
        self._host = "api.e2hbase.shop"
        self._api_key = api_key
        self.client = self._create_client()

    def _create_client(self) -> Elasticsearch:
        """
        Crée une instance du client E2HBASE

        :return: Instance du client E2HBASE.
        :raises ValueError: Si la clé API n'est pas fournie.
        """
        if not self._api_key:
            raise ValueError("Please provide an API key!")
        return Elasticsearch(
            [f"https://{self._host}:9200"],
            api_key=self._api_key,
            verify_certs=False,
        )

    @retry(wait=wait_fixed(10), stop=stop_after_attempt(5))
    def search_documents(
        self, search_string: str, display_filename: bool = False, size: int = 10000
    ) -> List[Dict[str, Any]]:
        """
        Recherche des documents dans E2HBASE en fonction de la chaîne de recherche fournie.
        :param search_string: La chaîne de recherche à utiliser dans la requête.
        :param display_filename: Affiche le nom du fichier si True.
        :param size: Le nombre de résultats à retourner.
        :return: Liste des documents trouvés.
        """
        search_query = {"match": {"content": search_string}}

        if display_filename:
            search_query["_source"] = ["filename", "content"]

        try:
            response = self.client.search(
                index="searcher", query=search_query, size=size
            )
            return response["hits"]["hits"]
        except RequestError as e:
            logging.error(f"Request error: {e.info}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        return []

    @staticmethod
    def _extract_information(text: str) -> Dict[str, Set[str]]:
        """
        Extrait les e-mails, numéros de téléphone, identifiants Steam et licences FiveM du texte fourni.

        :param text: Le texte à analyser.
        :return: Dictionnaire contenant les e-mails, numéros de téléphone, identifiants Steam et licences FiveM.
        """
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        phone_pattern = r"\+?\d{1,4}?[\d\s-]{8,}\d"
        steam_pattern = r"\bsteam:\w{17}\b"
        license_pattern = r"\blicense:\w{32}\b"

        emails = set(re.findall(email_pattern, text))
        phones = set(re.findall(phone_pattern, text))
        steam_ids = set(re.findall(steam_pattern, text))
        fivem_licenses = set(re.findall(license_pattern, text))

        return {
            "emails": emails,
            "phones": phones,
            "fivem_licenses": fivem_licenses,
            "steam_ids": steam_ids,
        }

    @staticmethod
    def _format_phone_number(number: str) -> str:
        """
        Formate un numéro de téléphone au format (XXX) XXX-XXXX.

        :param number: Le numéro de téléphone à formater.
        :return: Le numéro de téléphone formaté.
        """
        digits = re.sub(r"\D", "", number)
        if len(digits) != 10:
            return number
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

    def extracted_search(self, documents: List[Dict[str, Any]]) -> ExtractedInfo:
        """
        Traite les résultats de la recherche pour extraire les informations spécifiques.

        :param documents: Liste des documents trouvés.
        :return: Dictionnaire contenant les e-mails, numéros de téléphone, identifiants Steam et licences FiveM trouvés.
        """
        all_information = {
            "emails": set(),
            "phones": set(),
            "fivem_licenses": set(),
            "steam_ids": set(),
        }

        for doc in documents:
            source = doc.get("_source", {})
            content = source.get("content", "")

            info = self._extract_information(content)
            all_information["emails"].update(info["emails"])
            all_information["phones"].update(info["phones"])
            all_information["fivem_licenses"].update(info["fivem_licenses"])
            all_information["steam_ids"].update(info["steam_ids"])

            if isinstance(content, str):
                try:
                    data = json.loads(content)
                    if isinstance(data, dict):
                        identifiers = data.get("identifiers", [])
                        for identifier in identifiers:
                            if identifier.startswith("steam:"):
                                all_information["steam_ids"].add(identifier)
                            elif identifier.startswith("license:"):
                                all_information["fivem_licenses"].add(identifier)
                except json.JSONDecodeError:
                    logging.warning("JSON decoding error [WARNING]")
                except TypeError:
                    logging.error(f"Type error while processing content: {content}")

        all_information["phones"] = [
            self._format_phone_number(phone) for phone in all_information["phones"]
        ]

        return ExtractedInfo(
            emails=list(all_information["emails"]),
            phones=all_information["phones"],
            fivem_licenses=list(all_information["fivem_licenses"]),
            steam_ids=list(all_information["steam_ids"]),
        )
