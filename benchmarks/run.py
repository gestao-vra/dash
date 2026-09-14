"""Run against homologation only; emits a reproducible cold/warm timing record."""
import json, os
from statistics import quantiles
from time import perf_counter
from urllib.request import urlopen
url = f"http://127.0.0.1:{os.environ.get('APP_PORT', '8050')}/"
def sample(count=20):
    values=[]
    for _ in range(count):
        start=perf_counter()
        with urlopen(url, timeout=15) as response: response.read()
        values.append(round((perf_counter()-start)*1000, 1))
    return values
if __name__ == "__main__":
    cold, warm = sample(1), sample()
    report={"target":"page p95 <= 8000ms", "cold_ms":cold, "warm_ms":warm, "warm_p95_ms":quantiles(warm, n=20)[18]}
    with open("benchmark-report.json", "w", encoding="utf-8") as report_file: json.dump(report, report_file, indent=2)
    print(json.dumps(report, indent=2))
