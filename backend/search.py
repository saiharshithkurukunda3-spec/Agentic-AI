from ddgs import DDGS

TRUSTED_DOMAINS = {
    "who.int",
    "nature.com",
    "nih.gov",
    "reuters.com",
    "bbc.com",
    ".gov",
    ".edu",
}


def search_web(query: str):
    with DDGS() as ddgs:

        results = list(ddgs.text(query, max_results=5))

        formatted_results = []

        for result in results:

            url = result.get("href", "")

            if any(domain in url for domain in TRUSTED_DOMAINS):

                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": url,
                    "snippet": result.get("body", ""),
                    "source": "Trusted"
                })

        # Fill remaining slots if trusted results are few
        if len(formatted_results) < 5:

            existing = {x["url"] for x in formatted_results}

            for result in results:

                url = result.get("href", "")

                if url not in existing:

                    formatted_results.append({
                        "title": result.get("title", ""),
                        "url": url,
                        "snippet": result.get("body", ""),
                        "source": "DDGS"
                    })

                if len(formatted_results) >= 10:
                    break

        return formatted_results