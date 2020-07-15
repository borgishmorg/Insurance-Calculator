from tariff import tariff, base_tariff

TARIFFS = {
    'base': base_tariff.BaseTariff
}

tariff_container = tariff.TariffContainer()
for tariff_type, tariff_class in TARIFFS.items():
    tariff_container.add(tariff_type, tariff_class(f'./app/tariff/{tariff_type}_tariff.json'))
