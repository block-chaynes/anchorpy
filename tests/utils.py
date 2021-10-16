from pytest import fixture
import psutil
from xprocess import ProcessStarter


def get_localnet(path, scope="module"):
    @fixture(scope=scope)
    def localnet_fixture(xprocess):
        class Starter(ProcessStarter):
            # startup pattern
            pattern = "JSON RPC URL"
            terminate_on_interrupt = True
            # command to start process
            args = ["anchor", "localnet"]
            popen_kwargs = {"cwd": path}

        # ensure process is running and return its logfile
        logfile = xprocess.ensure("localnet", Starter)
        yield logfile

        xprocess.getinfo("localnet").terminate()
        # That call to .terminate() fails to stop solana-test-validator,
        # So we do it ourselves
        for proc in psutil.process_iter(["name", "cmdline"]):
            if proc.info["name"] == "solana-test-validator":
                if ".anchor/test-ledger" in proc.info["cmdline"]:
                    proc.terminate()

    return localnet_fixture
