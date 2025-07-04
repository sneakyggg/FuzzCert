import sys
import atheris

g_benchAdapter = None


def strip_fuzzcert_args(argv):
    """Remove fuzzcert-specific args that Atheris doesn't understand"""
    cleaned = []
    skip_next = False
    for i, arg in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        if arg in ("--bench", "--input", "--config"):
            skip_next = True  # Skip next argument (e.g., value after --bench)
            continue
        if arg.startswith("--bench=") or arg.startswith("--input=") or arg.startswith("--config="):
            continue
        cleaned.append(arg)
    return cleaned



def TestOneInput(data: bytes) -> None:
    """
    Atheris fuzzing entry point. Deserializes and runs verifier on input.
    """

    try:
        # deserialize
        #region, area = adapter.deserialize(data, adapter.input_dtype)
        config=g_benchAdapter.config_obj
        #print(config)
        #print("1111111111111111111111111111111111111111111111111111111111")
        partitions=g_benchAdapter.partitions
        #print(partitions)
        #print("2222222222222222222222222222222222222222222222222222222222")
        from_=g_benchAdapter.from_
        #print(from_)
        #print("3333333333333333333333333333333333333333333333333333333333")
        sets=g_benchAdapter.sets
        #print(sets)
        #print("4444444444444444444444444444444444444444444444444444444444")

        for strategy in config["strategy"].values():
            strategy.set_config(config)


        for partition in partitions:
            falsify(config,partition,sets['reporter'].get_area(partition),sets,from_=from_)


        for strategy in config["strategy"].values():
            strategy.shutdown()

        # serialize
        #data = adapter.serialize(data, adapter.input_dtype)

    except Exception:
        pass


def start_fuzzing(benchAdapter, corpus_dir: str) -> None:
    """
    Initializes benchmark adapter and starts fuzzing with Atheris.

    Args:
        benchAdapter: A subclass instance of BenchAdapter (e.g., VerapakAdapter).
        corpus_dir: Path to fuzzing corpus directory.
    """
    global g_benchAdapter
    benchAdapter.initialize(corpus_dir)
    g_benchAdapter = benchAdapter
    #print(g_benchAdapter.partitions)
    #print(1111111111111111111111111111111)
    cleaned_argv=strip_fuzzcert_args(sys.argv)
    # Use adapter’s own custom_mutator
    atheris.Setup(
        cleaned_argv,
        TestOneInput,
        custom_mutator=benchAdapter.mutate,
        enable_python_coverage=True,
    )
    atheris.Fuzz()
