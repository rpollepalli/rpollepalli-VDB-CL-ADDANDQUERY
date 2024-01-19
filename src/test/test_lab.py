import unittest
from src.main.lab import sample
from src.main.lab import add_file
from src.main.lab import chroma_client
from src.main.lab import collection
from src.main.lab import get_relevant_file


class ChromaTests(unittest.TestCase):

    """
    Prior to every test, reset the games collection
    (at time of writing, convenient truncation of collection does not exist...)
    """

    def setUp(self):
        collection = chroma_client.get_collection("games")
        alldocs = collection.get()
        for ids in alldocs.get("ids"):
            collection.delete(ids=ids)

    """
    This test verifies that ChromaDB's basic functionality works by running the
    provided sample code. If this test fails (possibly due to insufficient computer
    resources), the lab may not be completable.
    """

    def test_chroma_sanity_check(self):
        result = sample()
        self.assertIn("tennis", result.get("ids")[0][0])

    """
    Test that files may be added to the games collection via the add_file function you
    have written.
    """

    def test_add_file(self):
        add_file("src/resources/checkers.md", {"type": "sport"}, "checkers")
        result = collection.get(
            ids="checkers"
        )
        self.assertIn("checkers", result.get("ids")[0])

    """
    Test that your querying function works off of sample's files
    """

    def test_query_file(self):
        sample()
        result = collection.query(
            query_texts="rules of castling"
        )
        self.assertIn("chess", result.get("ids")[0])

    """
    Test that your code for adding and querying files works simultaneously.
    """

    def test_add_and_query_files(self):
        add_file("src/resources/checkers.md", {"type": "board game"}, "checkers")
        add_file("src/resources/hockey.md", {"type": "sport"}, "hockey")
        add_file("src/resources/baseball.md", {"type": "sport"}, "baseball")
        add_file("src/resources/tennis.md", {"type": "sport"}, "tennis")
        add_file("src/resources/chess.md", {"type": "board game"}, "chess")
        result = collection.query(
            query_texts="what is a home run"
        )
        self.assertIn("hockey", result.get("ids")[0])

    def test_get_relevant_file(self):
        add_file("src/resources/checkers.md", {"type": "board game"}, "checkers")
        add_file("src/resources/hockey.md", {"type": "sport"}, "hockey")
        add_file("src/resources/baseball.md", {"type": "sport"}, "baseball")
        add_file("src/resources/tennis.md", {"type": "sport"}, "tennis")
        add_file("src/resources/chess.md", {"type": "board game"}, "chess")
        result = get_relevant_file("what is a home run")
        self.assertIn("baseball", result.get("ids")[0])

if __name__ == '__main__':
    unittest.main()
