import trafilatura


def extract_text(url: str, min_length=300):

    downloaded = trafilatura.fetch_url(url)

    if downloaded is None:
        return None

    text = trafilatura.extract(
        downloaded,
        include_tables=True,
        include_comments=False,
        include_links=False,
        favor_precision=True,
        favor_recall=False
    )

    if text is None:
        return None

    text = text.strip()

    if len(text) < min_length:
        return None

    metadata = trafilatura.extract_metadata(downloaded)

    return {
        "text": text,
        "title": metadata.title if metadata else "",
        "date": metadata.date if metadata else "",
        "url": url
    }