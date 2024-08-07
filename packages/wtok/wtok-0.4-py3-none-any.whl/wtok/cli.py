import click
import re
import sys
import tiktoken
from whisper.tokenizer import get_tokenizer

@click.command()
@click.version_option()
@click.option("-i", "--input", "input", type=click.File("r"))
@click.option(
    "-t", "--truncate", "truncate", type=int, help="Truncate to this many tokens"
)
@click.option("-m", "--model", default="multilingual", help="Which model to use")
@click.option("-l", "--language", default="en", help="Prepend multilingual prompt for given language to each string")
@click.option(
    "as_digits", "-d", "--digits", is_flag=True, help="Output token integers"
)
@click.option(
    "decode_tokens", "--decode", is_flag=True, help="Convert token integers to text"
)
@click.option("as_counts", "-c", "--counts", is_flag=True, help="Output token counts")
@click.option("-s", "--allow-special", is_flag=True, help="Do not error on special tokens")
def cli(
    input,
    truncate,
    model,
    language,
    as_digits,
    decode_tokens,
    as_counts,
    allow_special,
):
    """
    Convert sentences into whisper tokens one line at a time

    To count tokens from stdin:

        cat sentences.txt | wtok -c

    To truncate each sentence to 100 tokens:

        cat sentences.txt | wtok -t 100

    To truncate each sentence to 100 tokens using the English-only model named "gpt2":

        cat sentences.txt | wtok -t 100 -m gpt2

    To view token integers:

        cat sentences.txt | wtok --encode

    To convert tokens back to text:

        echo 9906 1917 | wtok --decode

    To see the details of the tokens:

        echo hello world | wtok
    """
    try:
        tokenizer = get_tokenizer(multilingual=model == "multilingual", language=language)
        encoding = tokenizer.encoding
    except KeyError as e:
        raise click.ClickException(f"Invalid model: {model}, available: multilingual and gpt2 (see openai-whisper)") from e

    for text in sys.stdin:
        text = text.strip()

        if decode_tokens:
            tokens = [int(token) for token in re.findall(r"\d+", text)]
            if as_digits:
                click.echo(encoding.decode(tokens))
            else:
                click.echo(encoding.decode_tokens_bytes(tokens))
            return

        # Tokenize it
        kwargs = {}
        if allow_special:
            kwargs["allowed_special"] = "all"
        try:
            tokens = encoding.encode(text, **kwargs)
        except ValueError as ex:
            ex_str = str(ex)
            if "disallowed special token" in ex_str and not allow_special:
                # Just the first line, then add a hint
                ex_str = (
                    ex_str.split("\n")[0]
                    + "\n\nUse --allow-special to allow special tokens"
                )
            raise click.ClickException(ex_str)

        # Prepend the prompt
        if tokens:
            tokens = list(tokenizer.sot_sequence_including_notimestamps) + tokens
        else:
            tokens = [tokenizer.sot, tokenizer.no_speech]

        if truncate:
            tokens = tokens[:truncate]

        # Append the epilogue
        tokens = tokens + [tokenizer.eot]

        def render(t, s):
            try:
                return s.decode('utf-8').replace(' ', '▁')
            except UnicodeDecodeError:
                return str(t)

        if as_counts:
            click.echo(len(tokens))
        elif as_digits:
            click.echo(" ".join(str(t) for t in tokens))
        else:
            click.echo(" ".join(render(t, s) for t, s in zip(tokens, encoding.decode_tokens_bytes(tokens))))
