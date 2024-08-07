# wtok: ttok for Whisper

[![PyPI](https://img.shields.io/pypi/v/wtok.svg)](https://pypi.org/project/wtok/)
[![Changelog](https://img.shields.io/github/v/release/proger/wtok?include_prereleases&label=changelog)](https://github.com/proger/wtok/releases)
[![Tests](https://github.com/proger/wtok/workflows/Test/badge.svg)](https://github.com/proger/wtok/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/proger/wtok/blob/master/LICENSE)

Count and truncate text based on tokens

## Background

Large language and speech models such as GPT-3.5 and GPT-4 work in terms of tokens.

This tool can count tokens, using OpenAI's [tiktoken](https://github.com/openai/tiktoken) library.

It can also truncate text to a specified number of tokens.

## Installation

Install this tool using `pip`:
```bash
pip install wtok
```
## Counting tokens

Provide text as arguments to this tool to count tokens:

```bash
wtok Hello world
```
```
2
```
You can also pipe text into the tool:
```bash
echo -n "Hello world" | wtok
```
```
2
```
Here the `echo -n` option prevents echo from adding a newline - without that you would get a token count of 3.

To pipe in text and then append extra tokens from arguments, use the `-i -` option:

```bash
echo -n "Hello world" | wtok more text -i -
```
```
6
```
## Different models

By default, the tokenizer model for GPT-3.5 and GPT-4 is used.

To use the model for GPT-2 and GPT-3, add `--model gpt2`:

```bash
wtok boo Hello there this is -m gpt2
```
```
6
```
Compared to GPT-3.5:
```bash
wtok boo Hello there this is
```
```
5
```
Further model options are [documented here](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb).

## Truncating text

Use the `-t 10` or `--truncate 10` option to truncate text to a specified number of tokens:

```bash
wtok This is too many tokens -t 3
```
```
This is too
```

## Viewing tokens

The `--encode` option can be used to view the integer token IDs for the incoming text:

```bash
wtok Hello world --encode
```
```
9906 1917
```
The `--decode` method reverses this process:

```bash
wtok 9906 1917 --decode
```
```
Hello world
```
Add `--tokens` to either of these options to see a detailed breakdown of the tokens:

```bash
wtok Hello world --encode --tokens
```
```
[b'Hello', b' world']
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

```bash
cd wtok
python -m venv venv
source venv/bin/activate
```

Now install for editing:

```bash
pip install -e .
```
