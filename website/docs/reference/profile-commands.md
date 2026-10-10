---
sidebar_position: 7
---

# Profile Commands Reference

This page covers all commands related to [Hermes profiles](../user-guide/profiles.md). For general CLI commands, see [CLI Commands Reference](./cli-commands.md).

## `dxrk profile`

```bash
dxrk profile <subcommand>
```

Top-level command for managing profiles. Running `dxrk profile` without a subcommand shows help.

| Subcommand | Description |
|------------|-------------|
| `list` | List all profiles. |
| `use` | Set the active (default) profile. |
| `create` | Create a new profile. |
| `delete` | Delete a profile. |
| `show` | Show details about a profile. |
| `alias` | Regenerate the shell alias for a profile. |
| `rename` | Rename a profile. |
| `export` | Export a profile to a tar.gz archive. |
| `import` | Import a profile from a tar.gz archive. |

## `dxrk profile list`

```bash
dxrk profile list
```

Lists all profiles. The currently active profile is marked with `*`.

**Example:**

```bash
$ dxrk profile list
  default
* work
  dev
  personal
```

No options.

## `dxrk profile use`

```bash
dxrk profile use <name>
```

Sets `<name>` as the active profile. All subsequent `dxrk` commands (without `-p`) will use this profile.

| Argument | Description |
|----------|-------------|
| `<name>` | Profile name to activate. Use `default` to return to the base profile. |

**Example:**

```bash
dxrk profile use work
dxrk profile use default
```

## `dxrk profile create`

```bash
dxrk profile create <name> [options]
```

Creates a new profile.

| Argument / Option | Description |
|-------------------|-------------|
| `<name>` | Name for the new profile. Must be a valid directory name (alphanumeric, hyphens, underscores). |
| `--clone` | Copy `config.yaml`, `.env`, and `SOUL.md` from the current profile. |
| `--clone-all` | Copy everything (config, memories, skills, sessions, state) from the current profile. |
| `--clone-from <profile>` | Clone from a specific profile instead of the current one. Used with `--clone` or `--clone-all`. |
| `--no-alias` | Skip wrapper script creation. |

Creating a profile does **not** make that profile directory the default project/workspace directory for terminal commands. If you want a profile to start in a specific project, set `terminal.cwd` in that profile's `config.yaml`.

**Examples:**

```bash
# Blank profile — needs full setup
dxrk profile create mybot

# Clone config only from current profile
dxrk profile create work --clone

# Clone everything from current profile
dxrk profile create backup --clone-all

# Clone config from a specific profile
dxrk profile create work2 --clone --clone-from work
```

## `dxrk profile delete`

```bash
dxrk profile delete <name> [options]
```

Deletes a profile and removes its shell alias.

| Argument / Option | Description |
|-------------------|-------------|
| `<name>` | Profile to delete. |
| `--yes`, `-y` | Skip confirmation prompt. |

**Example:**

```bash
dxrk profile delete mybot
dxrk profile delete mybot --yes
```

:::warning
This permanently deletes the profile's entire directory including all config, memories, sessions, and skills. Cannot delete the currently active profile.
:::

## `dxrk profile show`

```bash
dxrk profile show <name>
```

Displays details about a profile including its home directory, configured model, gateway status, skills count, and configuration file status.

This shows the profile's Hermes home directory, not the terminal working directory. Terminal commands start from `terminal.cwd` (or the launch directory on the local backend when `cwd: "."`).

| Argument | Description |
|----------|-------------|
| `<name>` | Profile to inspect. |

**Example:**

```bash
$ dxrk profile show work
Profile: work
Path:    ~/.dxrk/profiles/work
Model:   anthropic/claude-sonnet-4 (anthropic)
Gateway: stopped
Skills:  12
.env:    exists
SOUL.md: exists
Alias:   ~/.local/bin/work
```

## `dxrk profile alias`

```bash
dxrk profile alias <name> [options]
```

Regenerates the shell alias script at `~/.local/bin/<name>`. Useful if the alias was accidentally deleted or if you need to update it after moving your Hermes installation.

| Argument / Option | Description |
|-------------------|-------------|
| `<name>` | Profile to create/update the alias for. |
| `--remove` | Remove the wrapper script instead of creating it. |
| `--name <alias>` | Custom alias name (default: profile name). |

**Example:**

```bash
dxrk profile alias work
# Creates/updates ~/.local/bin/work

dxrk profile alias work --name mywork
# Creates ~/.local/bin/mywork

dxrk profile alias work --remove
# Removes the wrapper script
```

## `dxrk profile rename`

```bash
dxrk profile rename <old-name> <new-name>
```

Renames a profile. Updates the directory and shell alias.

| Argument | Description |
|----------|-------------|
| `<old-name>` | Current profile name. |
| `<new-name>` | New profile name. |

**Example:**

```bash
dxrk profile rename mybot assistant
# ~/.dxrk/profiles/mybot → ~/.dxrk/profiles/assistant
# ~/.local/bin/mybot → ~/.local/bin/assistant
```

## `dxrk profile export`

```bash
dxrk profile export <name> [options]
```

Exports a profile as a compressed tar.gz archive.

| Argument / Option | Description |
|-------------------|-------------|
| `<name>` | Profile to export. |
| `-o`, `--output <path>` | Output file path (default: `<name>.tar.gz`). |

**Example:**

```bash
dxrk profile export work
# Creates work.tar.gz in the current directory

dxrk profile export work -o ./work-2026-03-29.tar.gz
```

## `dxrk profile import`

```bash
dxrk profile import <archive> [options]
```

Imports a profile from a tar.gz archive.

| Argument / Option | Description |
|-------------------|-------------|
| `<archive>` | Path to the tar.gz archive to import. |
| `--name <name>` | Name for the imported profile (default: inferred from archive). |

**Example:**

```bash
dxrk profile import ./work-2026-03-29.tar.gz
# Infers profile name from the archive

dxrk profile import ./work-2026-03-29.tar.gz --name work-restored
```

## `dxrk -p` / `dxrk --profile`

```bash
dxrk -p <name> <command> [options]
dxrk --profile <name> <command> [options]
```

Global flag to run any Hermes command under a specific profile without changing the sticky default. This overrides the active profile for the duration of the command.

| Option | Description |
|--------|-------------|
| `-p <name>`, `--profile <name>` | Profile to use for this command. |

**Examples:**

```bash
dxrk -p work chat -q "Check the server status"
dxrk --profile dev gateway start
dxrk -p personal skills list
dxrk -p work config edit
```

## `dxrk completion`

```bash
dxrk completion <shell>
```

Generates shell completion scripts. Includes completions for profile names and profile subcommands.

| Argument | Description |
|----------|-------------|
| `<shell>` | Shell to generate completions for: `bash` or `zsh`. |

**Examples:**

```bash
# Install completions
dxrk completion bash >> ~/.bashrc
dxrk completion zsh >> ~/.zshrc

# Reload shell
source ~/.bashrc
```

After installation, tab completion works for:
- `dxrk profile <TAB>` — subcommands (list, use, create, etc.)
- `dxrk profile use <TAB>` — profile names
- `dxrk -p <TAB>` — profile names

## See also

- [Profiles User Guide](../user-guide/profiles.md)
- [CLI Commands Reference](./cli-commands.md)
- [FAQ — Profiles section](./faq.md#profiles)
