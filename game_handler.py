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


# todo change this to communicate with client through socket instead of using input()
# todo add support for paired instances that will share a seed
def main():
    instances = []
    while True:
        found = False
        query = str(input())
        print(query)
        name, command = query.split(',')
        for x in instances:
            if x.name == name:
                print(x.command(command))
                found = True
        if not found:
            new_instance = Instance(name)
            print(new_instance.command(command))
            instances.append(new_instance)


if __name__ == "__main__":
    main()
