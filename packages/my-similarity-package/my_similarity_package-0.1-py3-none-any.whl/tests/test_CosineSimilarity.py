# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 11:27:49 2024

@author: 90545
"""

import unittest
from my_unique_project_name.CosineSimilarity import CosineSimilarity

class TestCosineSimilarity(unittest.TestCase):

    def test_cosine_similarity(self):
        sentences = [
            "A new World Bank report holds out similar fears.",
            "In India, Mexico, and Peru, firms that operate for 40 years typically double in size."
        ]
        similarity = CosineSimilarity(sentences)
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)

if __name__ == '__main__':
    unittest.main()
