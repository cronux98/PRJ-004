#!/bin/bash
# run_determinism.sh — PRJ-004 EVCore-MY metering golden model determinism check.
#
# Runs the golden model N times with DISTINCT seeds, writes a per-run log
# (PID + timestamp + tests MD5) for every run, and verifies the tests-array
# MD5 is identical across runs (audit rule F14: byte-identical outputs without
# run logs are forgeable -> run logs with PID+timestamp are REQUIRED).
#
# Usage:
#   ./run_determinism.sh [N]        # N = number of distinct seeds (default 3)
#
# Outputs (all in this directory):
#   golden_out_seed<SEED>.json      # per-run output
#   run_log_seed<SEED>_<PID>.txt    # per-run log with PID + timestamp + MD5
#   determinism.json                # verdict (identical: true/false)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
N=${1:-3}
SEEDS=(42 123 999 7777 54321)
RUN_START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_PID="$$"

if [ "$N" -gt "${#SEEDS[@]}" ]; then
    echo "ERROR: N=$N exceeds available seed pool (${#SEEDS[@]}). Max 5."
    exit 1
fi

echo "=== PRJ-004 EVCore-MY Golden Model Determinism Check (N=$N) ==="
echo "harness pid=$RUN_PID  started=$RUN_START  dir=$SCRIPT_DIR"
echo ""

declare -a HASHES
declare -a FILES
declare -a LOGS

for i in $(seq 0 $((N - 1))); do
    seed="${SEEDS[$i]}"
    out="golden_out_seed${seed}.json"
    log="run_log_seed${seed}_${RUN_PID}.txt"
    FILES+=("$out")
    LOGS+=("$log")

    echo "[$((i+1))/$N] Running with --seed $seed ..."

    # Run the model, capture FULL stdout/stderr into the per-run log.
    # The log therefore contains PID + timestamp + tests MD5 from the model
    # itself, plus the harness line below (non-forgeable run evidence).
    python3 "$SCRIPT_DIR/golden_model.py" --seed "$seed" --out "$SCRIPT_DIR/$out" \
        > "$SCRIPT_DIR/$log" 2>&1

    {
        echo ""
        echo "# harness: seed=$seed out=$out"
        echo "# harness: run_pid=${RUN_PID} log_start=${RUN_START} log_end=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    } >> "$SCRIPT_DIR/$log"

    # Extract tests-array MD5 (excluding _metadata) from the output JSON.
    h=$(python3 -c "
import json, hashlib, sys
with open('$SCRIPT_DIR/$out') as f:
    data = json.load(f)
tests_json = json.dumps(data['tests'], sort_keys=True)
print(hashlib.md5(tests_json.encode('utf-8')).hexdigest())
")
    HASHES+=("$h")
    echo "       tests MD5: $h  ($out)  log: $log"
done

echo ""
echo "--- Hash Comparison ---"
FIRST="${HASHES[0]}"
IDENTICAL=true
for i in $(seq 0 $((N - 1))); do
    h="${HASHES[$i]}"
    if [ "$h" != "$FIRST" ]; then
        echo "  MISMATCH: seed ${SEEDS[$i]} hash $h != $FIRST"
        IDENTICAL=false
    fi
done

if $IDENTICAL; then
    echo "  ALL IDENTICAL: $N/$N runs produce the same tests MD5 ($FIRST)"
else
    echo "  FAIL: hashes differ between runs"
fi

# Write determinism.json (verdict + per-run hashes + per-run log paths)
python3 - "$N" "$IDENTICAL" "$FIRST" "$RUN_START" "$RUN_PID" "$SCRIPT_DIR" <<'PYEOF'
import json, sys

n = int(sys.argv[1])
identical = sys.argv[2] == "true"
first = sys.argv[3]
run_start = sys.argv[4]
run_pid = sys.argv[5]
script_dir = sys.argv[6]

seeds = [42, 123, 999, 7777, 54321]
runs = []
with open(f"{script_dir}/run_determinism_seeds.txt", "w") as f:
    f.write(" ".join(str(s) for s in seeds[:n]) + "\n")

# Re-derive hashes deterministically from the output files
import hashlib
for i in range(n):
    seed = seeds[i]
    out = f"{script_dir}/golden_out_seed{seed}.json"
    with open(out) as f:
        data = json.load(f)
    tests_json = json.dumps(data["tests"], sort_keys=True)
    h = hashlib.md5(tests_json.encode("utf-8")).hexdigest()
    runs.append({
        "seed": seed,
        "file": f"golden_out_seed{seed}.json",
        "tests_md5": h,
        "run_log": f"run_log_seed{seed}_{run_pid}.txt",
    })

result = {
    "project": "PRJ-004",
    "codename": "EVCore-MY",
    "model": "metering_golden",
    "identical": identical,
    "first_hash": first,
    "n_runs": n,
    "runs": runs,
    "method": "MD5 of sorted tests JSON array (excluding _metadata); per-run logs contain PID+timestamp",
    "harness": {"pid": run_pid, "started_utc": run_start},
    "timestamp": run_start,
}
with open(f"{script_dir}/determinism.json", "w") as f:
    json.dump(result, f, indent=2)
    f.write("\n")
print(json.dumps(result, indent=2))
PYEOF

echo ""
echo "Wrote determinism.json"
exit 0
