import logging
from typing import Any, Literal, TypedDict, cast

import requests

from app.ext.zipcode.abc import ZipCodeData, ZipcodeExternalService


class _CorreiosZipCodeDataSchema(TypedDict):
    uf: str
    localidade: str
    locNoSem: Literal[""]
    locNu: Literal[""]
    localidadeSubordinada: Literal[""]
    logradouroDNEC: str
    logradouroTextoAdicional: Literal[""]
    logradouroTexto: Literal[""]
    bairro: str
    baiNu: Literal[""]
    nomeUnidade: Literal[""]
    cep: str
    tipoCep: str
    numeroLocalidade: Literal[""]
    situacao: Literal[""]
    faixasCaixaPostal: list[Any]
    faixasCep: list[Any]


class _CorreiosZipCodeSchema(TypedDict):
    dados: list[_CorreiosZipCodeDataSchema]
    erro: bool
    mensagem: bool
    total: int


class _CorreiosHttpClient:
    BASE_URL = "https://buscacepinter.correios.com.br{path}"

    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            }
        )

    def post_zip_code_search(self, zip_code: str) -> _CorreiosZipCodeSchema:
        # load cookies
        referer_page_url = self.BASE_URL.format(path="/app/endereco/index.php")
        self.s.get(referer_page_url, timeout=5)

        response = self.s.post(
            url=self.BASE_URL.format(path="/app/endereco/carrega-cep-endereco.php"),
            data={
                "pagina": "/app/endereco/index.php",
                "cepaux": "",
                "mensagem_alerta": "",
                "endereco": zip_code,
                "tipoCEP": "ALL",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Referer": referer_page_url,  # trick the service that we're a browser
            },
            timeout=10,
        )
        response.raise_for_status()
        return cast(_CorreiosZipCodeSchema, response.json())


logger = logging.getLogger(__name__)


class CorreiosZipcodeExternalService(ZipcodeExternalService):
    suitable_for_production = True

    def __init__(self):
        self.client = _CorreiosHttpClient()

    def query(self, zip_code: str) -> list[ZipCodeData]:
        try:
            search = self.client.post_zip_code_search(zip_code)
        except requests.HTTPError as e:
            logger.warning(f"Failed to communicate with Correios, reason {e}")
            return []

        if search["erro"]:
            logger.warning(f"Failed to get the zipcode data, error message: {search['mensagem']}")
            return []

        return [
            ZipCodeData(
                line=z["logradouroDNEC"],
                district=z["bairro"],
                city=z["localidade"],
                federal_unity=z["uf"],
                zip_code=z["cep"],
            )
            for z in search["dados"]
        ]
