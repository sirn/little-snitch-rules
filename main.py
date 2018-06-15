import copy
import json
import os
import re
import sys

import strictyaml


SCHEMA_MANIFEST = strictyaml.Seq(
    strictyaml.Map(
        {
            "name": strictyaml.Str(),
            "description": strictyaml.Str(),
            "src": strictyaml.Str(),
        }
    )
)


SCHEMA_RULE = strictyaml.Seq(
    strictyaml.Map(
        {
            "process": strictyaml.Str(),
            strictyaml.Optional("action"): strictyaml.Enum(["allow", "deny", "ask"]),
            strictyaml.Optional("codeSignature"): strictyaml.Enum(["ignore"]),
            strictyaml.Optional("direction"): strictyaml.Enum(["incoming", "outgoing"]),
            strictyaml.Optional("disabled"): strictyaml.Bool(),
            strictyaml.Optional("notes"): strictyaml.Str(),
            strictyaml.Optional("ports"): strictyaml.Regex(
                "^(any|\d+((\s+)?\-(\s+)?\d+)?)$"
            ),
            strictyaml.Optional("priority"): strictyaml.Enum(["regular", "high"]),
            strictyaml.Optional("protocol"): strictyaml.Int() | strictyaml.Str(),
            strictyaml.Optional("remote"): strictyaml.Enum(
                ["any", "local-net", "multicast", "broadcast", "bonjour", "dns-servers"]
            ),
            strictyaml.Optional("remote-addresses"): strictyaml.Seq(strictyaml.Str()),
            strictyaml.Optional("remote-domains"): strictyaml.Seq(strictyaml.Str()),
            strictyaml.Optional("remote-hosts"): strictyaml.Seq(strictyaml.Str()),
            strictyaml.Optional("via"): strictyaml.Str(),
        }
    )
)


def _atoi(text):
    return int(text) if text.isdigit() else text


def _natural_keys(text):
    return [_atoi(c) for c in re.split("\d+", text)]


def generate(src, name, description):
    """Generate a lsrules JSON from files in src directory."""
    rules = []
    srcs = []

    for prefix, _dirs, files in os.walk(src):
        for filename in sorted(files, key=_natural_keys):
            if filename.endswith(".yml"):
                path = os.path.join(prefix, filename)
                srcs.append(path)

    for path in srcs:
        with open(path) as f:
            rs = strictyaml.load(f.read(), SCHEMA_RULE, label=path)
            for r in rs:
                rule = copy.copy(r.data)
                if "remote-addresses" in rule:
                    rule["remote-addresses"] = ",".join(rule["remote-addresses"])
                for field in ("remote-addresses", "ports", "protocol"):
                    if field in rule:
                        rule[field] = str(rule[field]).replace(" ", "")
                rules.append(rule)

    return json.dumps(
        {"name": name, "description": description, "rules": rules},
        indent=4,
        sort_keys=True,
    )


def main(manifest_path, dest_path):
    """Read the manifest.yml and feed it to generator."""
    print("Reading %s..." % (manifest_path,))
    os.makedirs(dest_path, exist_ok=True)
    with open(manifest_path) as f:
        manifest = strictyaml.load(f.read(), SCHEMA_MANIFEST, label=manifest_path)
        print("Total of %i lsrules to generate." % (len(manifest),))
        for src in manifest:
            data = src.data
            dest_file = os.path.join(dest_path, "%s.lsrules" % (data["src"],))
            sys.stdout.write("Generating %s -> %s... " % (data["src"], dest_file))
            sys.stdout.flush()
            out = generate(data["src"], data["name"], data["description"])
            with open(dest_file, "wb") as f:
                f.write(out.encode("utf-8"))
                print("Done.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("%s [source] [dest]" % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
