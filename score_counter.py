from score_dto import ScoreDTO, Game, Set, TotalScore


MAX_SETS = 2  # best-of-three


class ScoreUpdater:
    def __init__(self, score: ScoreDTO):
        self.score = score

    def game_set_match(self):
        t = self.score.total
        return t.player1 == MAX_SETS or t.player2 == MAX_SETS

    def update_score(self, player1_winner: bool):
        cur_set = self.score.sets[-1]
        is_tiebreak = cur_set.is_tiebreak()

        if player1_winner:
            self.update_game_points_player1(is_tiebreak)
            self.update_set_player1(is_tiebreak)
        else:
            self.update_game_points_player2(is_tiebreak)
            self.update_set_player2(is_tiebreak)

        self.update_total_score()

    def update_game_points_player1(self, is_tiebreak):
        game = self.score.game
        if is_tiebreak:
            p1_points, p2_points = self.get_tiebreak_points(game.player1, game.player2)
        else:
            p1_points, p2_points = self.get_game_points(game.player1, game.player2)
        self.score.game = Game(p1_points, p2_points)

    def update_game_points_player2(self, is_tiebreak):
        game = self.score.game
        if is_tiebreak:
            p2_points, p1_points = self.get_tiebreak_points(game.player2, game.player1)
        else:
            p2_points, p1_points = self.get_game_points(game.player2, game.player1)
        self.score.game = Game(p1_points, p2_points)

    def get_game_points(self, winner_points: str, loser_points: str):
        under_40 = ["0", "15", "30"]
        if (
            winner_points == "40" and loser_points in under_40
        ) or winner_points == "Ad":
            return ("0", "0")  # game ends
        elif winner_points == "40" and loser_points == "40":
            return ("Ad", "40")
        elif winner_points == "40" and loser_points == "Ad":
            return ("40", "40")
        else:
            add_points_map = {"0": "15", "15": "30", "30": "40"}
            new_winner_points = add_points_map[winner_points]
            return (new_winner_points, loser_points)

    def get_tiebreak_points(self, winner_points: str, loser_points: str):
        winner = int(winner_points)
        loser = int(loser_points)
        return (str(winner + 1), str(loser))

    def update_set_player1(self, is_tiebreak):
        cur_set = self.score.sets[-1]

        p1 = self.score.game.player1
        p2 = self.score.game.player2
        if is_tiebreak:
            if int(p1) >= 7 and int(p1) - int(p2) >= 2:
                self.score.game = Game("0", "0")
                self.score.sets[-1] = Set(cur_set.player1 + 1, cur_set.player2)
        else:
            if p1 == "0" and p2 == "0":
                self.score.sets[-1] = Set(cur_set.player1 + 1, cur_set.player2)

    def update_set_player2(self, is_tiebreak):
        cur_set = self.score.sets[-1]

        p1 = self.score.game.player1
        p2 = self.score.game.player2
        if is_tiebreak:
            if int(p2) >= 7 and int(p2) - int(p1) >= 2:
                self.score.game = Game("0", "0")
                self.score.sets[-1] = Set(cur_set.player1, cur_set.player2 + 1)
        else:
            if p1 == "0" and p2 == "0":
                self.score.sets[-1] = Set(cur_set.player1, cur_set.player2 + 1)

    def update_total_score(self):
        t = self.score.total
        s = self.score.sets[-1]
        s1, s2 = s.player1, s.player2
        if (s1 == 6 and s2 <= 4) or s1 == 7:
            self.score.total = TotalScore(t.player1 + 1, t.player2)
            if t.player1 + 1 < MAX_SETS:
                self.score.sets.append(Set(0, 0))
        elif (s2 == 6 and s1 <= 4) or s2 == 7:
            self.score.total = TotalScore(t.player1, t.player2 + 1)
            if t.player2 + 1 < MAX_SETS:
                self.score.sets.append(Set(0, 0))
