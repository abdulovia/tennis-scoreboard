import unittest
from app.models.score import Game, Score, Set
from app.services.score_updater import ScoreUpdater


class TestScoreUpdater(unittest.TestCase):

    def setUp(self):
        self.score = Score()

    def test_deuce_player1(self):
        self.score.game = Game("40", "40")
        su = ScoreUpdater(self.score)
        su.update_score(True)
        self.assertEqual(su.score.game, Game("Ad", "40"), "incorrect score after deuce")
        self.assertEqual(su.score.sets[-1], Set(0, 0), "incorrect set score")

    def test_game_win_player2(self):
        self.score.game = Game("0", "40")
        su = ScoreUpdater(self.score)
        su.update_score(False)
        self.assertEqual(su.score.sets[-1], Set(0, 1), "incorrect score after game win")

    def test_game_points(self):
        su = ScoreUpdater(self.score)
        game_score_hist = [
            Game("15", "0"),
            Game("15", "15"),
            Game("30", "15"),
            Game("30", "30"),
            Game("40", "30"),
            Game("40", "40"),
            Game("Ad", "40"),
            Game("40", "40"),
        ]
        for i in range(len(game_score_hist) // 2):
            su.update_score(True)
            self.assertEqual(
                su.score.game,
                game_score_hist[i * 2],
                f"incorrect game score after player1 wins",
            )
            su.update_score(False)
            self.assertEqual(
                su.score.game,
                game_score_hist[i * 2 + 1],
                f"incorrect game score after player2 wins",
            )
        self.assertEqual(su.score.sets[-1], Set(0, 0), "incorrect set score")

    def test_tiebreak_game(self):
        self.score.sets[-1] = Set(6, 6)
        su = ScoreUpdater(self.score)
        for i in range(7):
            game = Game(str(i), "0")
            self.assertEqual(
                su.score.game,
                game,
                f"incorrect tiebreak score",
            )
            su.update_score(True)
        self.assertEqual(
            su.score.sets[0], Set(7, 6), "incorrect first set score after tiebreak"
        )
        self.assertEqual(
            su.score.sets[-1], Set(0, 0), "incorrect new set score after tiebreak"
        )


if __name__ == "__main__":
    unittest.main()
