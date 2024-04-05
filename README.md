<div align="center">

# asdf-zig [![Build](https://github.com/jiacai2050/asdf-zig/actions/workflows/build.yml/badge.svg)](https://github.com/jiacai2050/asdf-zig/actions/workflows/build.yml) [![Lint](https://github.com/jiacai2050/asdf-zig/actions/workflows/lint.yml/badge.svg)](https://github.com/jiacai2050/asdf-zig/actions/workflows/lint.yml)

[zig](https://github.com/jiacai2050/zig) plugin for the [asdf version manager](https://asdf-vm.com).

</div>

# Contents

- [Dependencies](#dependencies)
- [Install](#install)
- [Contributing](#contributing)
- [License](#license)

# Dependencies

**TODO: adapt this section**

- `bash`, `curl`, `tar`, and [POSIX utilities](https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html).
- `SOME_ENV_VAR`: set this environment variable in your shell config to load the correct version of tool x.

# Install

Plugin:

```shell
asdf plugin add zig
# or
asdf plugin add zig https://github.com/jiacai2050/asdf-zig.git
```

zig:

```shell
# Show all installable versions
asdf list-all zig

# Install specific version
asdf install zig latest

# Set a version globally (on your ~/.tool-versions file)
asdf global zig latest

# Now zig commands are available
--version
```

Check [asdf](https://github.com/asdf-vm/asdf) readme for more instructions on how to
install & manage versions.

# Contributing

Contributions of any kind welcome! See the [contributing guide](contributing.md).

[Thanks goes to these contributors](https://github.com/jiacai2050/asdf-zig/graphs/contributors)!

# License

See [LICENSE](LICENSE) © [Jiacai Liu](https://github.com/jiacai2050/)
