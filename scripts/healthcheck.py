import sys
import urllib.request
import urllib.error
from datetime import datetime

DEFAULT_URL = "http://192.168.1.116/health"
DEFAULT_LOG = "healthcheck.log"
TIMEOUT = 5  


def check(url: str) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            if response.status == 200:
                return True, "OK"
            return False, f"FAIL (HTTP {response.status})"
    except urllib.error.HTTPError as e:
        return False, f"FAIL (HTTP {e.code})"
    except urllib.error.URLError as e:
        return False, f"FAIL (URLError: {e.reason})"
    except TimeoutError:
        return False, f"FAIL (Timeout after {TIMEOUT}s)"
    except OSError as e:
        return False, f"FAIL (OSError: {e})"


def write_log(path: str, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} {message}\n"
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError as e:
        print(f"Не удалось записать лог в {path}: {e}", file=sys.stderr)


def main() -> int:
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    log_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_LOG

    ok, message = check(url)
    write_log(log_path, message)

    print(f"{url} -> {message}")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())