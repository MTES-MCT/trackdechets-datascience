
from .models import ICPE, Rubrique
from .scrapers import IcpeScraper, fetch_parallel


def create_rubriques():
    query = ICPE.select(ICPE.code_s3ic, ICPE.url_fiche)
    scrapers = [IcpeScraper(icpe.url_fiche) for icpe in query]
    fetch_parallel(scrapers)
    for scraper in scrapers:
        scraper.parse()
        scraper.find_rubriques()
    rubriques_list = [scraper.rubriques for scraper in scrapers]
    codes_s3ic = [icpe.code_s3ic for icpe in query]
    codes_s3ic_zip_rubriques = list(zip(codes_s3ic, rubriques_list))
    for (code_s3ic, rs) in codes_s3ic_zip_rubriques:
        for r in rs:
            rubrique = Rubrique.from_rubrique_scraped(code_s3ic, r)
            rubrique.save()
