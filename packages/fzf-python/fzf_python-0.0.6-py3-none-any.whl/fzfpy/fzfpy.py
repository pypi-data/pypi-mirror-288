import subprocess


# %%
def fzf(iterable, opts=[]):
    process = subprocess.Popen(
        ["fzf"] + opts,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    stdout, stderr = process.communicate("\n".join(map(str, iterable)).encode())
    if stdout:
        return stdout.decode().rstrip().split("\n")


# %%
class Fzf:
    def __init__(self, iterable, opts=[]):
        self.iterable = iterable
        self.opts = opts + [
            "--multi",
            "--bind=enter:select-all+accept",
        ]
        self.queries = []

    def __call__(self, query=None, interactive=True):
        if not self.iterable:
            return self
        if query:
            if not isinstance(query, list) and not isinstance(query, tuple):
                query = [str(query)]

            to_filter = query[: -1 if interactive else None]
            for qq in to_filter:
                q = str(qq)
                self.queries += [q]
                self.iterable = fzf(self.iterable, [f"--filter={q}"] + self.opts)

        if not interactive or not self.iterable:
            return self
        q_opt = [f"--query={query[-1]}"] if query else []
        opts = ["--print-query"] + q_opt + self.opts
        result = fzf(self.iterable, opts)
        q = result[0]
        if q:
            self.queries += [q]
        self.iterable = result[1:]
        return self

    def __repr__(self):
        return f"Fzf(\nqueries={self.queries},\niterable={self.iterable}\n,opts={self.opts}\n)"


if __name__ == "__main__":
    iterable = map(str, range(10000))
    f = Fzf(iterable)
    f([1, 2, 9, 4], interactive=False)
    print(f)
