import requests
import xml.etree.ElementTree as ET


class PubMedAPI:
    """
    Simple PubMed API client using NCBI E-utilities.

    Workflow:
    1. ESearch: search PubMed and return PMIDs
    2. EFetch: retrieve article metadata and abstracts
    """

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def search_pubmed(
        self,
        query: str,
        max_results: int = 10,
        start_year: int | None = None,
        end_year: int | None = None,
        article_type: str | None = None,
    ):
        if not query or not query.strip():
            return []

        final_query = self._build_query(
            query=query,
            start_year=start_year,
            end_year=end_year,
            article_type=article_type,
        )

        pmids = self._search_pmids(query=final_query, max_results=max_results)

        if not pmids:
            return []

        articles = self._fetch_articles(pmids)
        return articles

    def _build_query(
        self,
        query: str,
        start_year: int | None = None,
        end_year: int | None = None,
        article_type: str | None = None,
    ):
        query_parts = [query.strip()]

        if start_year and end_year:
            query_parts.append(f'("{start_year}"[Date - Publication] : "{end_year}"[Date - Publication])')

        article_type_map = {
            "Systematic Review": "systematic review[Publication Type]",
            "Clinical Trial": "clinical trial[Publication Type]",
            "Review": "review[Publication Type]",
            "Meta-Analysis": "meta-analysis[Publication Type]",
            "Randomized Controlled Trial": "randomized controlled trial[Publication Type]",
        }

        if article_type and article_type != "Any Article Type":
            mapped_type = article_type_map.get(article_type)
            if mapped_type:
                query_parts.append(mapped_type)

        return " AND ".join(query_parts)

    def _search_pmids(self, query: str, max_results: int = 10):
        url = f"{self.BASE_URL}/esearch.fcgi"

        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "relevance",
        }

        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()

        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])

    def _fetch_articles(self, pmids):
        url = f"{self.BASE_URL}/efetch.fcgi"

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.text)
        articles = []

        for article in root.findall(".//PubmedArticle"):
            medline = article.find("MedlineCitation")
            if medline is None:
                continue

            pmid_node = medline.find("PMID")
            pmid = pmid_node.text if pmid_node is not None else "N/A"

            article_node = medline.find("Article")
            if article_node is None:
                continue

            title_node = article_node.find("ArticleTitle")
            title = (
                "".join(title_node.itertext()).strip()
                if title_node is not None
                else "No title available"
            )

            journal_node = article_node.find("Journal/Title")
            journal = journal_node.text if journal_node is not None else "Journal not listed"

            year = "Year not listed"
            year_node = article_node.find("Journal/JournalIssue/PubDate/Year")
            medline_date_node = article_node.find("Journal/JournalIssue/PubDate/MedlineDate")

            if year_node is not None:
                year = year_node.text
            elif medline_date_node is not None:
                year = medline_date_node.text

            publication_types = []
            for pub_type in article_node.findall(".//PublicationType"):
                if pub_type.text:
                    publication_types.append(pub_type.text)

            abstract_parts = []
            for abstract_text in article_node.findall(".//AbstractText"):
                label = abstract_text.attrib.get("Label")
                text = "".join(abstract_text.itertext()).strip()

                if text:
                    if label:
                        abstract_parts.append(f"{label}: {text}")
                    else:
                        abstract_parts.append(text)

            abstract = "\n".join(abstract_parts) if abstract_parts else "No abstract available."

            articles.append(
                {
                    "pmid": pmid,
                    "title": title,
                    "journal": journal,
                    "year": year,
                    "publication_types": publication_types,
                    "abstract": abstract,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                }
            )

        return articles


if __name__ == "__main__":
    api = PubMedAPI()
    results = api.search_pubmed(
        query="diabetes readmission risk",
        max_results=3,
        start_year=2020,
        end_year=2026,
        article_type="Systematic Review",
    )

    for article in results:
        print("=" * 80)
        print(article["pmid"])
        print(article["title"])
        print(article["journal"])
        print(article["year"])
        print(article["publication_types"])
        print(article["url"])