import sys
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
from rich.console import Console


scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from Shared import certoraValidateFuncs as Vf
from Shared import certoraUtils as Util
from Shared import certoraAttrUtil as AttrUtil
from Mutate import mutateConstants as Constants


MUTATION_DOCUMENTATION_URL = 'https://docs.certora.com/en/latest/docs/gambit/mutation-verifier.html#cli-options'


@dataclass
class MutateAttribute(AttrUtil.AttributeDefinition):
    affects_build_cache_key: bool = False
    disables_build_cache: bool = False


class MutateAttributes(AttrUtil.Attributes):

    ORIG_RUN = MutateAttribute(
        help_msg="A link to a previous run of the Prover, will be used as the basis for the "
                 "generated mutations",
        default_desc="",
        attr_validation_func=Vf.validate_orig_run,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    MSG = MutateAttribute(
        help_msg="Add a message description to your run",
        attr_validation_func=Vf.validate_msg,
        default_desc="No message",
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    SERVER = MutateAttribute(
        attr_validation_func=Vf.validate_server_value,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    PROVER_VERSION = MutateAttribute(
        attr_validation_func=Vf.validate_prover_version,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    DEBUG = MutateAttribute(
        flag='--debug',    # added to prevent dup with DUMP_CSV
        arg_type=AttrUtil.AttrArgType.BOOLEAN,
        argparse_args={
            'action': AttrUtil.STORE_TRUE
        }
    )

    COLLECT_MODE = MutateAttribute(
        flag='--collect_mode',    # added to prevent dup with DEBUG
        arg_type=AttrUtil.AttrArgType.BOOLEAN,
        argparse_args={
            'action': AttrUtil.STORE_TRUE
        }
    )

    ORIG_RUN_DIR = MutateAttribute(
        help_msg="Download files from the original run link to the given folder",
        default_desc="Downloads files to the directory `.certora_mutate_sources`",
        # attr_validation_func=Vf.validate_writable_path,
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    OUTDIR = MutateAttribute(
        help_msg="Specify the output directory for Gambit",
        default_desc=f"Gambit generates mutants inside the directory `{Constants.GAMBIT_OUT}`",
        # attr_validation_func=Vf.validate_writable_path,
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    GAMBIT_ONLY = MutateAttribute(
        arg_type=AttrUtil.AttrArgType.BOOLEAN,
        help_msg="Stop processing after generating mutations with Gambit",
        default_desc="Runs a verification job on each mutant and generates a test report from the results",
        argparse_args={
            'action': AttrUtil.STORE_TRUE
        }
    )

    DUMP_FAILED_COLLECTS = MutateAttribute(
        # This flag is hidden on purpose, the following code line help explain what it does
        # attr_validation_func=Vf.validate_writable_path,
        # help_msg="Path to the log file capturing mutant collection failures.",
        # default_desc="log will be stored at collection_failures.txt",
        flag="--dump_failed_collects",
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    # Sets a file that will store the object sent to mutation testing UI (useful for testing)
    UI_OUT = MutateAttribute(
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    DUMP_LINK = MutateAttribute(
        flag='--dump_link',    # added to prevent dup with DUMP_CSV
        # todo - validation can write the file
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    DUMP_CSV = MutateAttribute(
        attr_validation_func=Vf.validate_writable_path,
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    # Synchronous mode
    # Run the tool synchronously in shell
    SYNC = MutateAttribute(
        arg_type=AttrUtil.AttrArgType.BOOLEAN,
        argparse_args={
            'action': AttrUtil.STORE_TRUE
        }
    )

    '''
    The file containing the links holding certoraRun report outputs.
    In async mode, run this tool with only this option.
    '''
    COLLECT_FILE = MutateAttribute(
        flag='--collect_file',    # added to prevent dup with DUMP_CSV
        # attr_validation_func=Vf.validate_readable_file,
        argparse_args={
            'nargs': AttrUtil.SINGLE_OR_NONE_OCCURRENCES,
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    '''
   The max number of minutes to poll after submission was completed,
    and before giving up on synchronously getting mutation testing results
   '''
    POLL_TIMEOUT = MutateAttribute(
        flag='--poll_timeout',    # added to prevent dup with REQUEST_TIMEOUT
        attr_validation_func=Vf.validate_positive_integer,
        arg_type=AttrUtil.AttrArgType.INT,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    # The maximum number of retries a web request is attempted
    MAX_TIMEOUT_ATTEMPTS_COUNT = MutateAttribute(
        arg_type=AttrUtil.AttrArgType.INT,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    # The timeout in seconds for a web request
    REQUEST_TIMEOUT = MutateAttribute(
        attr_validation_func=Vf.validate_positive_integer,
        arg_type=AttrUtil.AttrArgType.INT,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    GAMBIT = MutateAttribute(
        arg_type=AttrUtil.AttrArgType.MAP,
        argparse_args={
            'nargs': '*',
            'action': AttrUtil.NotAllowed
        }
    )
    # todo vvvv - parse_manual_mutations, change warnings to exceptions
    MANUAL_MUTANTS = MutateAttribute(
        arg_type=AttrUtil.AttrArgType.MAP,
        attr_validation_func=Vf.validate_manual_mutants,
        flag='--manual_mutants',  # added to prevent dup with GAMBIT
        argparse_args={
            'nargs': '*',
            'action': AttrUtil.NotAllowed
        }
    )

    '''
    Add this if you wish to wait for the results of the original verification.
    Reasons to use it:
    - Saves resources - all the mutations will be ignored if the original fails
    - The Prover will use the solver data from the original run to reduce the run time of the mutants
    Reasons to not use it:
    - Run time will be increased
    '''
    #
    WAIT_FOR_ORIGINAL_RUN = MutateAttribute(
        arg_type=AttrUtil.AttrArgType.BOOLEAN,
        flag='--wait_for_original_run',
        argparse_args={
            'action': AttrUtil.STORE_TRUE
        }
    )

    TEST = MutateAttribute(
        attr_validation_func=Vf.validate_test_value,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )


# set the all attribute that is a list of all attributes with their names
MutateAttributes.set_attribute_list()


def get_args(args_list: List[str]) -> Dict:

    def formatter(prog: Any) -> argparse.HelpFormatter:
        return argparse.HelpFormatter(prog, max_help_position=100, width=96)  # TODO - use the constant!

    parser = MutationParser(prog="certora-cli arguments and options", allow_abbrev=False,
                            formatter_class=formatter,
                            epilog="  -*-*-*   You can find detailed documentation of the supported options in "
                                   f"{MUTATION_DOCUMENTATION_URL}   -*-*-*")
    attrs = MutateAttributes.attribute_list

    parser.add_argument("conf_no_flag", nargs='?', type=Path)
    parser.add_argument("--conf", type=Path)

    for attr in attrs:
        flag = attr.get_flag()
        if attr.arg_type == AttrUtil.AttrArgType.INT:
            parser.add_argument(flag, help=attr.help_msg, type=int, **attr.argparse_args)
        else:
            parser.add_argument(flag, help=attr.help_msg, **attr.argparse_args)
    return vars(parser.parse_args(args_list))


class MutationParser(AttrUtil.ContextAttributeParser):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def format_help(self) -> str:
        console = Console()
        console.print("\n\nThe Certora Mutate - A tool for generating and verifying mutations")
        sys.stdout.write("\n\nUsage: certoraMutate <flags>\n\n")  # Print() would color the word <flags> here

        console.print("[bold][underline]Flag Types[/bold][/underline]\n")

        console.print("[bold]1. boolean (B):[/bold] gets no value, sets flag value to true "
                      "(false is always the default)")
        console.print("[bold]2. string (S):[/bold] gets a single string as a value, "
                      "note also numbers are of type string\n\n")

        MutateAttributes.print_attr_help()
        console.print("\n\nYou can find detailed documentation of the supported flags "
                      f"{Util.print_rich_link(MUTATION_DOCUMENTATION_URL)}\n\n")
        return ''
