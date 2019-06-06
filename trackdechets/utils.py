

# import asyncio
# from concurrent.futures import ThreadPoolExecutor

# import requests
# from bs4 import BeautifulSoup


# def parse_html_icpe_detail(html):
#     """
#     parse the table `Situation administrative` from an icpe
#     detail page like this one
#     http://www.installationsclassees.developpement-durable.gouv.fr/
#     ficheEtablissement.php?champEtablBase=30&champEtablNumero=12015
#     """
#     soup = BeautifulSoup(html, 'html5lib')
#     h2 = soup.find('h2', text='Situation administrative')
#     table = h2.find_next('table')
#     tbody = table.find('tbody')
#     ths = tbody.find_all('th')
#     headers = []
#     for th in ths:
#         headers.append(th.text.strip())
#     trs = tbody.find_all('tr')
#     rows = []
#     for tr in trs:
#         tds = tr.find_all('td')
#         if len(tds) > 0:
#             cells = []
#             for td in tds:
#                 cells.append(td.text)
#             row = dict(zip(headers, cells))
#             rows.append(row)
#     return rows


# def fetch_urls_icpe_detail(urls):
#     """ return the html of a list of icpe detail url """

#     def fetch(session, url):
#         response = session.get(url)
#         data = response.text
#         if response.status_code != 200:
#             print('Failure %s' % url)
#         return data

#     async def inner():

#         with ThreadPoolExecutor(max_workers=10) as executor:

#             with requests.Session() as session:

#                 loop = asyncio.get_event_loop()

#                 tasks = [
#                     loop.run_in_executor(
#                         executor,
#                         fetch,
#                         *(session, url)
#                     )
#                     for url in urls
#                 ]

#                 return await asyncio.gather(*tasks)

#     loop = asyncio.get_event_loop()
#     return loop.run_until_complete(inner())
