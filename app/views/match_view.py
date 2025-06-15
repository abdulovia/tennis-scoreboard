from jinja2 import Environment, FileSystemLoader, select_autoescape

class MatchView:
    env = Environment(loader=FileSystemLoader("templates/"), autoescape=select_autoescape())

    def render_index(self):
        template = self.env.get_template("index.html")
        buf = template.render()
        return buf

    def render_new_match(self):
        template = self.env.get_template("new-match.html")
        buf = template.render()
        return buf

    def render_match_score_page(self, match):
        template = self.env.get_template("match-score.html")
        buf = template.render(match=match)
        return buf

    def render_matches_page(self, matches, pages, player):
        template = self.env.get_template("matches.html")
        buf = template.render(matches=matches, pages=pages, player=player)
        return buf

    def render_style_css(self):
        template = self.env.get_template("static/css/style.css")
        buf = template.render()
        return buf

    def render_not_found(self):
        template = self.env.get_template("404.html")
        buf = template.render()
        return buf
