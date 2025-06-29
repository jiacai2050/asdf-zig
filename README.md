<div align="center">

# asdf-zig [![Build](https://github.com/zigcc/asdf-zig/actions/workflows/build.yml/badge.svg)](https://github.com/zigcc/asdf-zig/actions/workflows/build.yml)

[asdf-zig](https://github.com/zigcc/asdf-zig) plugin for the [asdf version manager](https://asdf-vm.com).

</div>

# Contents

- [Dependencies](#dependencies)
- [Install](#install)
- [Contributing](#contributing)
- [License](#license)

# Dependencies

- `bash`, `python3`, `tar`, and [POSIX utilities](https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html).
- asdf 0.16+

# Install

Plugin:

```shell
asdf plugin add zig https://github.com/zigcc/asdf-zig.git
```

asdf-zig:

```shell
# Show all installable versions
asdf list-all zig

# Install specific version
asdf install zig latest

# Set a version globally (on your ~/.tool-versions file)
asdf set --home zig latest

# Now asdf-zig commands are available
zig version
```

Check [asdf](https://github.com/asdf-vm/asdf) readme for more instructions on how to
install & manage versions.

# License

See [LICENSE](LICENSE) © [zigcc](https://github.com/zigcc/)
