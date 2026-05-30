class ScoreFusion:

    @staticmethod
    def fuse(

        semantic_results,

        keyword_results
    ):

        combined = {}

        for result in semantic_results:

            item_id = result["item"]["id"]

            combined[item_id] = {

                "item":
                    result["item"],

                "semantic_score":
                    result["semantic_score"],

                "keyword_score":
                    0
            }

        for result in keyword_results:

            item_id = result["item"]["id"]

            if item_id not in combined:

                combined[item_id] = {

                    "item":
                        result["item"],

                    "semantic_score":
                        0,

                    "keyword_score":
                        0
                }

            combined[item_id][
                "keyword_score"
            ] = result["keyword_score"]

        final_results = []

        for item in combined.values():

            final_score = (

                item["semantic_score"] * 0.7 +

                item["keyword_score"] * 0.3
            )

            final_results.append({

                "item":
                    item["item"],

                "semantic_score":
                    item["semantic_score"],

                "keyword_score":
                    item["keyword_score"],

                "final_score":
                    final_score
            })

        final_results.sort(

            key=lambda x: x["final_score"],

            reverse=True
        )

        return final_results