"""Draw the three stages of the mtcars table used in the data science chapter.

The values are a subset of R's mtcars dataset (mpg, cyl, hp, wt, qsec, am).
Country of origin is not in mtcars; it was added by hand from each car's make.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# name, mpg, cyl, hp, wt (1000 lbs), qsec, am (0 = automatic, 1 = manual), origin
CARS = [
    ("Mazda RX4", 21.0, 6, 110, 2.620, 16.46, 1, "Japan"),
    ("Mazda RX4 Wag", 21.0, 6, 110, 2.875, 17.02, 1, "Japan"),
    ("Datsun 710", 22.8, 4, 93, 2.320, 18.61, 1, "Japan"),
    ("Hornet 4 Drive", 21.4, 6, 110, 3.215, 19.44, 0, "US"),
    ("Hornet Sportabout", 18.7, 8, 175, 3.440, 17.02, 0, "US"),
    ("Valiant", 18.1, 6, 105, 3.460, 20.22, 0, "US"),
    ("Duster 360", 14.3, 8, 245, 3.570, 15.84, 0, "US"),
    ("Merc 240D", 24.4, 4, 62, 3.190, 20.00, 0, "Europe"),
    ("Merc 230", 22.8, 4, 95, 3.150, 22.90, 0, "Europe"),
    ("Merc 280", 19.2, 6, 123, 3.440, 18.30, 0, "Europe"),
    ("Merc 280C", 17.8, 6, 123, 3.440, 18.90, 0, "Europe"),
    ("Merc 450SE", 16.4, 8, 180, 4.070, 17.40, 0, "Europe"),
    ("Merc 450SL", 17.3, 8, 180, 3.730, 17.60, 0, "Europe"),
    ("Merc 450SLC", 15.2, 8, 180, 3.780, 18.00, 0, "Europe"),
    ("Cadillac Fleetwood", 10.4, 8, 205, 5.250, 17.98, 0, "US"),
    ("Lincoln Continental", 10.4, 8, 215, 5.424, 17.82, 0, "US"),
    ("Chrysler Imperial", 14.7, 8, 230, 5.345, 17.42, 0, "US"),
    ("Fiat 128", 32.4, 4, 66, 2.200, 19.47, 1, "Europe"),
    ("Honda Civic", 30.4, 4, 52, 1.615, 18.52, 1, "Japan"),
    ("Toyota Corolla", 33.9, 4, 65, 1.835, 19.90, 1, "Japan"),
    ("Toyota Corona", 21.5, 4, 97, 2.465, 20.01, 0, "Japan"),
    ("Dodge Challenger", 15.5, 8, 150, 3.520, 16.87, 0, "US"),
    ("AMC Javelin", 15.2, 8, 150, 3.435, 17.30, 0, "US"),
    ("Camaro Z28", 13.3, 8, 245, 3.840, 15.41, 0, "US"),
    ("Pontiac Firebird", 19.2, 8, 175, 3.845, 17.05, 0, "US"),
    ("Fiat X1-9", 27.3, 4, 66, 1.935, 18.90, 1, "Europe"),
    ("Porsche 914-2", 26.0, 4, 91, 2.140, 16.70, 1, "Europe"),
    ("Lotus Europa", 30.4, 4, 113, 1.513, 16.90, 1, "Europe"),
    ("Ford Pantera L", 15.8, 8, 264, 3.170, 14.50, 1, "US"),
    ("Ferrari Dino", 19.7, 6, 175, 2.770, 15.50, 1, "Europe"),
    ("Maserati Bora", 15.0, 8, 335, 3.570, 14.60, 1, "Europe"),
    ("Volvo 142E", 21.4, 4, 109, 2.780, 18.60, 1, "Europe"),
]
SHOWN = ["Mazda RX4", "Hornet 4 Drive", "Merc 240D",
         "Toyota Corona", "Camaro Z28", "Volvo 142E"]
REGIONS = ["US", "Europe", "Japan"]
NUMERIC = ["MPG", "Cylinders", "Horsepower", "Weight", "Quarter mile"]


def base_rows():
    return [dict(zip(["Model"] + NUMERIC + ["Transmission", "Origin"],
                     [name, mpg, cyl, hp, wt, qsec,
                      "Manual" if am else "Automatic", origin]))
            for name, mpg, cyl, hp, wt, qsec, am, origin in CARS]


def encode(rows):
    encoded = []
    for row in rows:
        new = {k: row[k] for k in ["Model"] + NUMERIC}
        new["Manual"] = int(row["Transmission"] == "Manual")
        for region in REGIONS:
            new[region] = int(row["Origin"] == region)
        encoded.append(new)
    return encoded


def rescale(rows):
    """Min-max scale every numeric column to [0, 1] using all 32 cars."""
    scaled = [dict(row) for row in rows]
    for col in NUMERIC:
        lo = min(row[col] for row in rows)
        hi = max(row[col] for row in rows)
        for row in scaled:
            row[col] = (row[col] - lo) / (hi - lo)
    return scaled


def draw_table(rows, formats, filename, highlight=()):
    """Draw selected rows with an ellipsis row in the middle.

    Each group of columns in highlight gets its own dashed box.
    """
    columns = list(formats)
    shown = [row for row in rows if row["Model"] in SHOWN]
    cells = [[row["Model"]] + [formats[c](row[c]) for c in columns]
             for row in shown]
    cells.insert(len(cells) // 2, ["..."] * (len(columns) + 1))
    header = [""] + columns

    row_height, pad = 0.32, 0.18
    fig = plt.figure()
    renderer = fig.canvas.get_renderer()

    def text_width(text, bold):
        t = fig.text(0, 0, text, fontsize=11,
                     fontweight="bold" if bold else "normal")
        width = t.get_window_extent(renderer).width / fig.dpi
        t.remove()
        return width

    widths = [max(text_width(r[i], r is header or i == 0)
                  for r in [header] + cells) + pad
              for i in range(len(header))]
    xs = [sum(widths[:i]) for i in range(len(widths) + 1)]
    n_rows = len(cells) + 1
    fig.set_size_inches(xs[-1] + 0.1, n_rows * row_height + 0.1)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-0.05, xs[-1] + 0.05)
    ax.set_ylim(n_rows * row_height + 0.05, -0.05)
    ax.axis("off")

    for r, row in enumerate([header] + cells):
        y = (r + 0.5) * row_height
        for c, text in enumerate(row):
            bold = r == 0 or c == 0
            ax.text(xs[c] + pad / 2, y, text, va="center", fontsize=11,
                    fontweight="bold" if bold else "normal")
    for r in range(n_rows + 1):
        ax.plot([0, xs[-1]], [r * row_height] * 2, color="black", lw=0.8)
    for x in xs:
        ax.plot([x, x], [0, n_rows * row_height], color="black", lw=0.8)

    for group in highlight:
        first = columns.index(group[0]) + 1
        last = columns.index(group[-1]) + 1
        ax.add_patch(Rectangle((xs[first] + 0.03, -0.03),
                               xs[last + 1] - xs[first] - 0.06,
                               n_rows * row_height + 0.06,
                               fill=False, edgecolor="#cc2222", lw=2,
                               linestyle="--"))
    fig.savefig(Path(__file__).resolve().parents[1] / "images" / filename)


one = "{:.1f}".format
two = "{:.2f}".format
three = "{:.3f}".format
whole = str

rows = base_rows()
draw_table(rows, {"MPG": one, "Cylinders": whole, "Horsepower": whole,
                  "Weight": three, "Quarter mile": two,
                  "Transmission": str, "Origin": str}, "CarsBase.pdf")

encoded = encode(rows)
binary = {"Manual": whole, **{region: whole for region in REGIONS}}
draw_table(encoded, {"MPG": one, "Cylinders": whole, "Horsepower": whole,
                     "Weight": three, "Quarter mile": two, **binary},
           "CarsOneHot.pdf", highlight=[["Manual"], ["US", "Japan"]])

draw_table(rescale(encoded), {**{col: two for col in NUMERIC}, **binary},
           "CarsScaled.pdf")
