import multiprocessing

from main import start_instance


def main():

    parent_conn, child_conn = multiprocessing.Pipe(duplex=True)
    p = multiprocessing.Process(target=start_instance, args=(child_conn,))
    p.start()
    while True:
        parent_conn.send(str(input()))
        print(parent_conn.recv())


if __name__ == "__main__":
    main()
