import multiprocessing

from main import start_instance


class Instance:

    def __init__(self, name):
        self.name = name
        self.waitingForOpponent = False
        parent_conn, child_conn = multiprocessing.Pipe(duplex=True)
        self.pipe = parent_conn
        p = multiprocessing.Process(target=start_instance, args=(child_conn,))
        p.start()

    def command(self, command) -> str:
        self.pipe.send(command)
        return self.pipe.recv()

    def set_waiting(self, waiting_flag):
        #Set to True somewhere when player goes downstairs
        self.waitingForOpponent = waiting_flag

# TODO add shared seed support in init
class Match:
    def __init__(self, match_id, players):
        self.match_id = match_id
        self.players = players
        self.instances = []
        self.players_downstairs = []
        for player in players:
            self.instances.append(Instance(player))

    def command(self, player, command) -> str:
        if player in self.players:
            for instance in self.instances:
                if instance.name == player:
                    return instance.command(command)
        else:
            return "Player not in match."

    def downstairs_players(self, player):
        #Add player that went downstairs to downstairs player list
        if player in self.players and player not in self.players_downstairs:
            self.players_downstairs.append(player)
            if len(self.players_downstairs) == len(self.players):
                #When all players are downstairs, flag is False, if only 1 then flag is True
                for instance in self.instances:
                    instance.waitingForOpponent = False
            else:
                for instance in self.instances:
                    instance.waitingForOpponent = True

# TODO add flags for finished game and winner
class GameHandler:
    def __init__(self):
        self.matches = []

    def new_match(self, match_id, player1, player2):
        players = [player1, player2]
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

    def update_downstairs_players(self, match_id, player):
        for match in self.matches:
            if match.match_id == match_id:
                match.downstairs_players(player)
                break

    def waiting_screen(self, match_id, player):
        for match in self.matches:
            if match.match_id == match_id:
                for match.players_downstairs in self.matches:
                    if player in match.players_downstairs:
                        print("waiting screen")
#
def main():
    game_handler = GameHandler()
    while True:
        query = str(input())
        if query.find("newmatch:") > -1:
            discard, query = query.split(':')
            match, player1, player2 = query.split(',')
            game_handler.new_match(match, player1, player2)
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
