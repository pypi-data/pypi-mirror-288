import json

from passbolt import PassboltAPI
import hashlib
import json
import os
import time

pbcache_path = os.path.expanduser("~/.pbcached")
try:
    caches = json.load(open(pbcache_path))
except json.decoder.JSONDecodeError:
    caches = {}
except FileNotFoundError:
    caches = {}

def get_credentials(key_fd, passphrase, search_name):
    cache_key = passphrase +  ":" + search_name
    cached = caches.get(cache_key)
    if cached:
        rightnow = int(time.time())
        ex = cached.get("ex")
        if ex > rightnow:
            return cached

    key = key_fd.read()
    config = {
        "base_url": "https://pass.getnitro.co.in",
        "private_key": key,
        "passphrase": passphrase,
    }

    p = PassboltAPI(dict_config=config)

    resource = next((item for item in p.get_resources() if item["name"] == search_name), None)

    if resource is not None:
        res = (
            config.get("gpg_library", "PGPy") == "gnupg"
            and json.loads(p.decrypt(p.get_resource_secret(resource["id"])).data)
            or json.loads(p.decrypt(p.get_resource_secret(resource["id"])))
        )

        username = resource.get("username")
        res["username"] = username
        ex = int(time.time()) + 3600
        res["ex"] = ex
        caches[cache_key] = res
        open(pbcache_path, "w").write(json.dumps(caches))
        return res


if __name__ == "__main__":
    print (get_credentials(open("passbolt.asc"), "52y", "Minio"))

