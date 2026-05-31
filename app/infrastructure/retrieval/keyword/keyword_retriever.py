class KeywordRetriever:

    def __init__(self, tickets):
        self.tickets = tickets

    def search(
        self,
        query: str,
        top_k: int = 5
    ):
        query_words = [
            w for w in query.lower().split()
            if len(w) > 2
        ]

        if not query_words:
            return []

        results = []

        for ticket in self.tickets:

            if ticket.get("status", "open") != "open":
                continue

            text = (
                ticket["title"] + " " + ticket["description"]
            ).lower()

            raw_score = sum(
                1 for word in query_words
                if word in text
            )

            if raw_score > 0:
                normalized_score = raw_score / len(query_words)

                results.append({
                    "item":          ticket,
                    "keyword_score": normalized_score
                })

        results.sort(
            key=lambda x: x["keyword_score"],
            reverse=True
        )
        return results[:top_k]
