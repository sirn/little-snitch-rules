# Little Snitch Rule Group

This repository provides [rule groups](https://help.obdev.at/littlesnitch/#/lsc-rule-group-subscriptions) for [**Little Snitch 4.1**](https://obdev.at/products/littlesnitch/).

## Available rule group

#### [First Party Rules](dist/first-party-rules.lsrules)

Provides basic rules for Apple softwares to fully function. To install:

```text
https://raw.githubusercontent.com/sirn/little-snitch-rules/master/dist/first-party-rules.lsrules
```

#### [Opinionated Defaults](dist/opinionated-defaults.lsrules)

Provides an opinionated default rules for third party softwares. To install:

```text
https://raw.githubusercontent.com/sirn/little-snitch-rules/master/dist/opinionated-defaults.lsrules
```

## Limitations

-   Custom rule group can only belongs to "Anyone" (and not "System" or "User", etc.)

## Contributing

1.  Make sure Python 3 and Pip is installed.
2.  Clone this repository, run `make install`
3.  To generate the lsrules, run `make`

Running `make install` will install pre-commit hook which will run the following rules by default:

-   Auto-generate rules in `dist/`
-   Format Python code with [black](https://github.com/ambv/black)
-   Run Python code through [flake8](http://flake8.pycqa.org)

## License

Public domain
