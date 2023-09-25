from app.ext.zipcode.abc import ZipCodeData, ZipcodeExternalService


class StaticZipcodeExternalService(ZipcodeExternalService):
    suitable_for_production = False
    fail: bool = False

    def query(self, zip_code: str) -> list[ZipCodeData]:
        if self.fail:
            return []
        return [
            ZipCodeData(
                line="Rua da Guarda",
                district="Centro",
                city="Santa Rosa de Lima",
                federal_unity="SC",
                zip_code=zip_code,
            )
        ]
