
from .models import db, ICPE, ICPE_27_35, Rubrique
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


def filter_icpe_27xx_35xx():
    query = """
    INSERT INTO icpe_27_35
        (SELECT * FROM
            (SELECT DISTINCT B.*
            FROM rubrique as A
            LEFT JOIN icpe as B
            ON A.code_s3ic = B.code_s3ic
            WHERE
                A.rubrique LIKE '27__'
                OR A.rubrique LIKE '35__')
            AS temp)
    """
    db.execute_sql(query)


def prepare_irep():
    query = """
    INSERT INTO irep_prepared
        (SELECT *, CONCAT('0', identifiant) as code_s3ic
        FROM irep)
    """
    db.execute_sql(query)


def join_icpe_irep():
    query = """
    INSERT INTO icpe_join_irep
        (SELECT
            a.*,
            b.nom_etablissement as irep_nom_etablissement,
            b.numero_siret as irep_numero_siret,
            b.adresse as irep_adresse,
            b.code_postal as irep_code_postal,
            b.commune as irep_commune,
            b.departement as irep_departement,
            b.region as irep_region,
            "b"."coordonnees_X" as irep_coordonnees_X,
            "b"."coordonnees_Y" as irep_coordonnees_Y,
            b.code_ape as irep_code_ape,
            b.libelle_ape as irep_libelle_ape,
            b.code_eprtr as irep_code_eprtr,
            b.libelle_eprtr as irep_libelle_eprtr
        FROM icpe_27_35 as a
        LEFT JOIN irep_prepared as b
        ON a.code_s3ic = b.code_s3ic)
    """
    db.execute_sql(query)


def prepare_gerep():
    query = """
    INSERT INTO gerep_prepared
        (SELECT *, CONCAT('0', code_etablissement) as code_s3ic
        FROM gerep)
    """
    db.execute_sql(query)


def join_icpe_gerep():
    pass
