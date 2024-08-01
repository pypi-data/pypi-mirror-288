# -*- coding: utf-8 -*-

from .morph_one_or_many import MorphOneOrMany
from .result import Result


class MorphOne(MorphOneOrMany):
    def get_results(self):
        """
        Get the results of the relationship.
        """
        return self._query.first()

    def init_relation(self, models, relation):
        """
        Initialize the relation on a set of models.

        :type models: list
        :type relation: str
        """
        for model in models:
            model.set_relation(relation, Result(None, self, model))

        return models

    def match(self, models, results, relation):
        """
        Match the eagerly loaded results to their parents.

        :type models: list
        :type results: Collection
        :type relation:  str
        """
        return self.match_one(models, results, relation)
