
from .models import ICPE, Rubrique
from .scrapers import IcpeScraper, fetch_parallel


def create_rubriques():
    query = ICPE.select(ICPE.id, ICPE.url_fiche)
    scrapers = [IcpeScraper(icpe.url_fiche) for icpe in query]
    fetch_parallel(scrapers)
    for scraper in scrapers:
        scraper.parse()
        scraper.find_rubriques()
    rubriques_list = [scraper.rubriques for scraper in scrapers]
    ids = [icpe.id for icpe in query]
    icpe_zip_rubriques = list(zip(ids, rubriques_list))
    rubriques = []
    for (icpe, rs) in icpe_zip_rubriques:
        for r in rs:
            rubrique = Rubrique.from_rubrique_scraped(icpe, r)
            rubriques.append(rubrique)
    Rubrique.bulk_create(rubriques)
