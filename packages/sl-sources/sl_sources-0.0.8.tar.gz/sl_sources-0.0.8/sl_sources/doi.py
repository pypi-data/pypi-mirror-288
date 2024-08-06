import asyncio
import json
import re
from typing import Optional

from .google_scholar import download_from_google_scholar, search_google_scholar
from .search import search_google
from .papers import likely_pdf
from .http import ThrottledClientSession, get_header
import xml.etree.ElementTree as ET


def validate_doi(doi: str) -> Optional[str]:
    """We check that the DOI can be resolved by
    `official means <http://www.doi.org/factsheets/DOIProxy.html>`_. If so, we
    return the resolved URL, otherwise, we return ``None`` (which means the
    DOI is invalid).

    :param doi: Identifier.
    :returns: The URL assigned to the DOI or ``None``.
    """
    from urllib.error import HTTPError
    import urllib.request
    import json

    url = "https://doi.org/api/handles/{doi}".format(doi=doi)
    print("handle url %s", url)
    request = urllib.request.Request(url)

    try:
        result = json.loads(urllib.request.urlopen(request).read().decode())
    except HTTPError:
        raise ValueError("HTTP 404: DOI not found")
    else:
        urls = [v["data"]["value"] for v in result["values"] if v.get("type") == "URL"]
        return urls[0] if urls else None


def get_real_url_from_doi(doi: str) -> Optional[str]:
    """Get a URL corresponding to a DOI.

    :param doi: Identifier.
    :returns: A URL for the DOI. If the DOI is invalid, return ``None``.
    """
    url = validate_doi(doi)
    if url is None:
        return url

    m = re.match(r".*linkinghub\.elsevier.*/pii/([A-Z0-9]+).*", url, re.I)
    if m:
        return "https://www.sciencedirect.com/science/article/abs/pii/{pii}".format(
            pii=m.group(1)
        )
    return url


def get_clean_doi(doi: str) -> str:
    """Check if the DOI is actually a URL and in that case just get
    the exact DOI.

    :param doi: String containing a DOI.
    :returns: The extracted DOI.
    """
    doi = re.sub(r"%2F", "/", doi)
    # For pdfs
    doi = re.sub(r"\)>", " ", doi)
    doi = re.sub(r"\)/S/URI", " ", doi)
    doi = re.sub(r"(/abstract)", "", doi)
    doi = re.sub(r"\)$", "", doi)
    return doi


async def resolve_doi(doi_url_or_doi, resolve_url=False):
    """Resolve a DOI to an object.
    If the DOI is a publication, return the publication title
    If the DOI is a paper, return the paper title, abstract, authors and, if resolve_url is true, a best-attempt at the PDF URL
    """
    # first, validate doi, return None if it is invalid
    doi = get_clean_doi(doi_url_or_doi)
    print(f"Cleaned DOI: {doi}")
    validated_doi = validate_doi(doi)
    if validated_doi is None:
        print(f"Invalid DOI: {doi}")
        return None

    print(f"Validated DOI: {validated_doi}")

    result = None
    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_header()
    ) as session:
        # get the metadata from Crossref
        crossref_url = f"https://doi.org/{doi}"
        print(f"Crossref URL: {crossref_url}")
        async with session.get(
            crossref_url, headers={"Accept": "application/vnd.crossref.unixsd+xml"}
        ) as response:
            if response.status == 200:
                data = await response.text()

                # Parse the XML data
                root = ET.fromstring(data)

                journal_metadata_element = root.find(".//journal_metadata")
                if journal_metadata_element is not None:
                    # Publication case
                    journal_title_element = journal_metadata_element.find("full_title")
                    journal_title = (
                        journal_title_element.text
                        if journal_title_element is not None
                        else None
                    )

                    year_element = root.find(".//publication_date/year")
                    year = int(year_element.text) if year_element is not None else None

                    resource_element = root.find(".//doi_data/resource")
                    url = (
                        resource_element.text if resource_element is not None else None
                    )

                    result = {
                        "id": doi,
                        "source_type": "publication",
                        "url": url,
                        "publication": journal_title,
                    }
                    return result
                else:
                    # Paper case
                    journal_article_element = root.find(".//journal_article")
                    if journal_article_element is not None:
                        title_element = journal_article_element.find(".//title")
                        title = (
                            title_element.text if title_element is not None else None
                        )

                        abstract_element = journal_article_element.find(".//abstract")
                        abstract = (
                            abstract_element.text
                            if abstract_element is not None
                            else None
                        )

                        year_element = journal_article_element.find(
                            ".//publication_date/year"
                        )
                        year = (
                            int(year_element.text) if year_element is not None else None
                        )

                        resource_element = journal_article_element.find(
                            ".//doi_data/resource"
                        )
                        url = (
                            resource_element.text
                            if resource_element is not None
                            else None
                        )

                        authors = []
                        contributors_element = journal_article_element.find(
                            ".//contributors"
                        )
                        if contributors_element is not None:
                            for person_element in contributors_element.findall(
                                ".//person_name"
                            ):
                                given_name = person_element.find("given_name").text
                                surname = person_element.find("surname").text
                                authors.append(f"{given_name} {surname}")

                        result = {
                            "id": doi,
                            "title": title,
                            "source_type": "google_scholar",
                            "abstract": abstract,
                            "url": url,
                            "authors": authors,
                            "year": year,
                        }
            else:
                print(f"Crossref request failed with status: {response.status}")

            # If crossref fails, search on Google Scholar
            if result is None:
                search_query = f'"{doi}"'
                search_results = await search_google_scholar(
                    search_query, num_results=5
                )
                if len(search_results) == 0:
                    search_results = await search_google(search_query, num_results=5)
                # Iterate through the results and look for one with a matching DOI
                for search_result in search_results:
                    if doi in search_result.get("url", ""):
                        result = search_result
                        break
                # otherwise just bring back the first result
                if result is None:
                    result = search_results[0]

            if result is None:
                print(f"Error: Unable to resolve DOI: {doi}")
                return None

            if resolve_url:
                sci_hub_url = f"https://sci.bban.top/pdf/{doi}.pdf"
                async with session.get(sci_hub_url, allow_redirects=True) as r:
                    if r.status == 200 and await likely_pdf(r):
                        url = sci_hub_url if resolve_url else None
                        result["url"] = url

                if result.get("url") is None:
                    search_query = f'"{result["title"]}" "{doi}"'
                    search_results = await search_google(
                        search_query, file_type="pdf", num_results=5
                    )
                    # for each result, if it is likely a pdf, return it
                    for search_result in search_results:
                        async with session.get(
                            search_result["url"], allow_redirects=True
                        ) as r:
                            if r.status == 200 and await likely_pdf(r):
                                result["url"] = search_result["url"]
                                break

                if result.get("url") is None:
                    result["url"] = validated_doi

        return result


async def download_from_doi(doi_url_or_doi):
    """Download a PDF from a DOI."""
    resolved_doi = await resolve_doi(doi_url_or_doi, resolve_url=True)
    if resolved_doi is None:
        print(f"Unable to resolve DOI: {doi_url_or_doi}")
        return None
    return await download_from_google_scholar(resolved_doi)


async def test_resolve_doi():
    test_dois = [
        "10.1080/15265161.2011.634487",
        "10.1002/biot.v3:12",
        "10.1016/j.biopsych.2005.02.031",
        "10.1080/2326263x.2016.1210989",
        "10.1088/1741-2560/13/2/021002",
    ]

    for doi in test_dois:
        result = await resolve_doi(doi)
        assert result is not None
        assert "id" in result
        assert "title" in result
        assert "source_type" in result

        # if source type is publication, assert title
        if result["source_type"] == "publication":
            assert "publication" in result
        else:
            assert "abstract" in result
            assert "url" in result

    print("resolve_doi tests passed!")


async def test_download_from_doi():
    test_dois = [
        "10.1088/1741-2560/13/2/021002",
        "10.3389/fneng.2014.00004",
        "10.1001/jama.1995.03520280069043",
        "10.1001/jama.1992.03480160079038",
        "10.1111/j.1532-5415.2010.03030.x",
        "10.1162/jocn.2009.21010",
    ]

    for doi in test_dois:
        result = await download_from_doi(doi)
        # if result is None, print the doi
        if result is None:
            print(f"Unable to download from DOI: {doi}")
        else:
            assert result is not None
            assert "full_text" in result
            assert len(result["full_text"]) > 0

    print("download_from_doi tests passed!")


async def main():
    dois_to_resolve = [
        "10.1080/2326263x.2016.1210989",
        "10.1088/1741-2560/13/2/021002",
        "10.1080/15265161.2011.634487",
        "10.1080/15265160500394556",
        "10.1080/15265161.2011.634481",
        "10.1001/jama.1995.03520280069043",
        "10.1001/jama.1992.03480160079038",
        "10.1111/j.1532-5415.2010.03030.x",
        "10.1111/j.1747-7093.2002.tb00396.x",
        "10.1037/0735-7044.118.5.897",
        "10.1126/science.1068749",
        "10.1007/s00213-005-2215-5",
        "10.1038/nn1176",
        "10.1515/9780691236629",
        "10.1038/nn0303-207",
        "10.1162/0898929052879987",
        "10.2307/3528418",
        "10.1097/00001756-200106130-00024",
        "10.1016/j.neuroimage.2005.01.035",
        "10.1038/nrn1405",
        "10.1038/nn0303-205",
        "10.1080/15265160590923358",
        "10.1126/science.306.5695.373",
        "10.1016/j.cognition.2007.07.017",
        "10.1162/089892900562552",
        "10.1038/nrn1609",
        "10.1006/cogp.2000.0733",
        "10.1126/science.1093535",
        "10.1016/j.ijpsycho.2005.01.010",
        "10.1038/sj.mp.4001367",
        "10.1162/jocn.2008.20040",
        "10.1080/15265160590923367",
        "10.1162/jocn.2006.18.6.923",
        "10.1016/bs.dnb.2020.03.001",
        "10.1080/2326263x.2016.1210989",
        "10.5621/sciefictstud.40.2.0382",
    ]

    results = []
    for doi in dois_to_resolve:
        try:
            result = await resolve_doi(doi, resolve_url=True)
            if result:
                results.append(result)
        except Exception as e:
            print(f"Error resolving DOI {doi}: {str(e)}")

    with open("doi_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"Resolved {len(results)} DOIs and saved results to doi_results.json")

    with open("doi_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"Resolved {len(results)} DOIs and saved results to doi_results.json")


if __name__ == "__main__":
    # asyncio.run(test_resolve_doi())
    # asyncio.run(test_download_from_doi())
    asyncio.run(main())
