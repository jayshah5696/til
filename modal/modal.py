import modal
print(modal.__version__)
app = modal.App('example-get-started')

@app.function()
def square(x):
    return x**2

@app.local_entrypoint()
def main():
    print("square is", square.remote(99))
