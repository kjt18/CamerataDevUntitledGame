import multiprocessing

from main import start_instance


class Instance:

    def __init__(self, name):
        self.name = name
        parent_conn, child_conn = multiprocessing.Pipe(duplex=True)
        self.pipe = parent_conn
        p = multiprocessing.Process(target=start_instance, args=(child_conn,))
        p.start()

    def command(self, command) -> str:
        self.pipe.send(command)
        return self.pipe.recv()


# TODO add shared seed support in init
class Match:

    def __init__(self, match_id, players):
        self.match_id = match_id
        self.players = players
        self.instances = []
        for player in players:
            self.instances.append(Instance(player))

    def command(self, player, command) -> str:
        if player in self.players:
            for instance in self.instances:
                if instance.name == player:
                    return instance.command(command)
        else:
            return "Player not in match."


# TODO add flags for finished game and winner
class GameHandler:
    def __init__(self):
        self.matches = []

    def new_match(self, match_id, player1):
        players = [player1]
        self.matches.append(Match(match_id, players))

    def end_match(self, match_id):
        for match in self.matches:
            if match.match_id == match_id:
                self.matches.remove(match)
                return True
        return False

    def command(self, match_id, player, command):
        for match in self.matches:
            if match.match_id == match_id:
                return match.command(player, command)
        return None

    def join_match(self, match_id, player2):
        for match in self.matches:
            if match.match_id == match_id:
                if len(match.players) < 2:
                    match.players.append(player2)
                    return True
                else:
                    return False
        return False


#
def main():
    game_handler = GameHandler()
    while True:
        query = str(input())
        if query.find("newmatch:") > -1:
            discard, query = query.split(':')
            match, player1 = query.split(',')
            game_handler.new_match(match, player1)
            print("Created match!")
        else:
            match, player, command = query.split(',')
            console = game_handler.command(match, player, command)
            if console is None:
                print("Match not found")
            else:
                print(console)


if __name__ == "__main__":
    main()
