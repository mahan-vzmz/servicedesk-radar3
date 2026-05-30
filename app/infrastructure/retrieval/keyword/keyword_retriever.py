class KeywordRetriever:

    def __init__(

        self,

        tickets
    ):

        self.tickets = tickets

    def search(

        self,

        query: str,

        top_k: int = 5
    ):

        query_words = query.lower().split()

        results = []

        for ticket in self.tickets:

            text = (

                ticket["title"] +

                " " +

                ticket["description"]
            ).lower()

            score = 0

            for word in query_words:

                if word in text:

                    score += 1

            if score > 0:

                results.append({

                    "item": ticket,

                    "keyword_score": score
                })

        results.sort(

            key=lambda x: x["keyword_score"],

            reverse=True
        )

        return results[:top_k]