import httpx
from prefect import flow, task


@task
def fetch_cat_fact(max_len=140):
    return httpx.get("https://catfact.ninja/fact?max_length=max_len").json()["fact"]


@task(persist_result=True)
def formatting(fact: str):
    print(fact.title())
    return fact.title()

@task
def write_fact(fact: str):
    with open("fact.txt", "w") as f:
        f.write(fact)
    return "Success!"

@flow
def pl_fetch_cat_fact_v2():
    fact = fetch_cat_fact()
    formatted_fact = formatting(fact)
    msg = write_fact(formatted_fact)
    print(msg)

if __name__ == "__main__":
    pl_fetch_cat_fact_v2()