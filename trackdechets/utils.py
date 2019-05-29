

from bs4 import BeautifulSoup


def parse_icpe_fiche_detail(html):
    """
    parse the table `Situation administrative` from an icpe
    detail page like this one
    http://www.installationsclassees.developpement-durable.gouv.fr/
    ficheEtablissement.php?champEtablBase=30&champEtablNumero=12015
    """
    soup = BeautifulSoup(html, 'html5lib')
    h2 = soup.find('h2', text='Situation administrative')
    table = h2.find_next('table')
    tbody = table.find('tbody')
    ths = tbody.find_all('th')
    headers = []
    for th in ths:
        headers.append(th.text.strip())
    trs = tbody.find_all('tr')
    rows = []
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) > 0:
            cells = []
            for td in tds:
                cells.append(td.text)
            row = dict(zip(headers, cells))
            rows.append(row)
    return rows
