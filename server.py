import zerorpc


class StreamingRPC(object):
    @zerorpc.stream
    def streaming_range(self, fr, to, step):
        return range(fr, to, step)


s = zerorpc.Server(StreamingRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()


class ExceptionalRPC(object):
    def bad(self):
        raise Exception(":P")


s = zerorpc.Server(ExceptionalRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
