#!/usr/bin/env python3
import argparse, os, sys
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt

def parse_xy(path):
    """Read XY points (one 'x y' per line). Blank lines or 'nan nan' separate polygons."""
    polys, xs, ys = [], [], []
    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                if xs:
                    polys.append((xs, ys))
                    xs, ys = [], []
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                x, y = float(parts[0]), float(parts[1])
            except ValueError:
                continue
            # treat NaN separators like blank lines
            if (x != x) or (y != y):  # NaN check
                if xs:
                    polys.append((xs, ys))
                    xs, ys = [], []
                continue
            xs.append(x); ys.append(y)
    if xs:
        polys.append((xs, ys))
    return polys

def build_names(delta, folder):
    s = f"{float(delta):.2f}"  # matches your "%3.2f" in C without spaces
    f1 = os.path.join(folder, f"f1_init-{s}.dat")
    f2 = os.path.join(folder, f"f2_init-{s}.dat")
    return f1, f2, s

def main():
    ap = argparse.ArgumentParser(description="Plot f1_init and f2_init shapes.")
    ap.add_argument("--delta", type=float, help="Delta used in filenames (e.g., 0.01)")
    ap.add_argument("--f1", type=str, help="Explicit path to f1_init file")
    ap.add_argument("--f2", type=str, help="Explicit path to f2_init file")
    ap.add_argument("--folder", type=str, default=".", help="Folder containing the files")
    ap.add_argument("--out", type=str, help="Output image filename (PNG)")
    args = ap.parse_args()

    if args.f1 and args.f2:
        f1_path, f2_path = args.f1, args.f2
        suffix = ""
    elif args.delta is not None:
        f1_path, f2_path, suffix = build_names(args.delta, args.folder)
    else:
        print("ERROR: Provide either --delta or both --f1 and --f2.", file=sys.stderr)
        sys.exit(2)

    if not os.path.isfile(f1_path):
        print(f"ERROR: File not found: {f1_path}", file=sys.stderr); sys.exit(1)
    if not os.path.isfile(f2_path):
        print(f"ERROR: File not found: {f2_path}", file=sys.stderr); sys.exit(1)

    polys1 = parse_xy(f1_path)
    polys2 = parse_xy(f2_path)

    fig, ax = plt.subplots(figsize=(6, 6))
    first = True
    for xs, ys in polys1:
        ax.plot(xs, ys, linewidth=1.5, label="f1" if first else None)
        first = False
    first = True
    for xs, ys in polys2:
        ax.plot(xs, ys, linewidth=1.5, linestyle="--", label="f2" if first else None)
        first = False

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")

    out = args.out or (f"init_shapes-{suffix}.png" if suffix else "init_shapes.png")
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")

if __name__ == "__main__":
    main()
