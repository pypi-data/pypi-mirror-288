## netauth-python

A [NetAuth](https://netauth.org) client library for Python.

### Installation

```
pip install netauth
```

### Usage

netauth-python centers around the `NetAuth` object:

```py
na = netauth.NetAuth("netauth.example.org")

try:
    resp = na.system_status()
    print(resp)
except netauth.error.NetAuthRpcError as e:
    print(f"Request failed: {e}")

na.close()
```

`NetAuth` can also be used as a context manager and be initialized from a NetAuth configuration file:

```py
with netauth.NetAuth.with_config(Path("/etc/netauth/config.toml")) as na:
    try:
        resp = na.system_status()
        print(resp)
    except netauth.error.NetAuthRpcError as e:
        print(f"Request failed: {e}")
```

For interactive or dynamic applications, operations that require authentication can use a callback to retrieve the user's secret:

```py
def secret_cb() -> str:
    return getpass(prompt="Secret: ")

with netauth.NetAuth("netauth.example.org", entity="demo", secret=secret_cb) as na:
    try:
        na.entity_kv_add("demo", "foo", ["bar", "baz"])
    except error.NetAuthRpcError as e:
        print(e)
```

For more information, see the [API documentation](https://python.netauth.org).

