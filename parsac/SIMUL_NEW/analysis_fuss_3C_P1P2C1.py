from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

try:
	import pickle
except Exception as exc:
	raise RuntimeError("Unable to import pickle module") from exc


def load_pickle(path):
	try:
		with open(path, "rb") as infile:
			return pickle.load(infile)
	except ValueError as err:
		if "unsupported pickle protocol" in str(err):
			try:
				import pickle5 as pickle_compat

				with open(path, "rb") as infile:
					return pickle_compat.load(infile)
			except Exception:
				raise RuntimeError(
					"This pickle requires protocol 5. Use Python >= 3.8 or install pickle5."
				) from err
		raise


pkname = "fussmann3C_P1P2C1.pickle"
new_dict = load_pickle(pkname)

y = new_dict["Y"]
x = new_dict["X"]

flag_chaos = y[:, 0]
flag_neg = y[:, 1]
flag_ss = y[:, 2]
flag_extin = y[:, 3]

puntiplot = 10000
flag_chaos = flag_chaos[-puntiplot:]
flag_neg = flag_neg[-puntiplot:]
flag_ss = flag_ss[-puntiplot:]
flag_extin = flag_extin[-puntiplot:]

x = np.asarray(x)
if x.ndim == 1:
	x = x.reshape(-1, 1)

if x.shape[1] >= 2:
	combinations = x[-puntiplot:, [0, 1]]
else:
	one_col = x[-puntiplot:, 0]
	combinations = np.column_stack((one_col, one_col))

fig, ax = plt.subplots(figsize=(6, 6))
point_size = 56
scatter_rasterized = True

for i, (dx, dc) in enumerate(combinations):
	current_flag_chaos = flag_chaos[i]
	current_flag_neg = flag_neg[i]
	current_flag_extin = flag_extin[i]
	current_flag_ss = flag_ss[i]

	if current_flag_extin == 1:
		ax.scatter(dx, dc, color="black", alpha=0, s=point_size, rasterized=scatter_rasterized)
	elif current_flag_neg == 1:
		ax.scatter(dx, dc, color="black", alpha=0, s=point_size, rasterized=scatter_rasterized)
	elif current_flag_ss == 1:
		ax.scatter(dx, dc, color="green", s=point_size, rasterized=scatter_rasterized)
	elif current_flag_chaos == 1:
		ax.scatter(
			dx,
			dc,
			color=(1.0, 100 / 255, 0 / 255),
			s=point_size,
			rasterized=scatter_rasterized,
		)
	else:
		ax.scatter(dx, dc, color="gold", s=point_size, rasterized=scatter_rasterized)

# Same layout requested for this series.
ax.set_xlim(0.05, 1.7)
ax.set_ylim(0.0, 0.4)
ax.set_box_aspect(1)
ax.tick_params(axis="both", which="major", labelsize=24)

output_dir = Path(__file__).resolve().parent / "PLOT_PAPERFINALI"
output_dir.mkdir(parents=True, exist_ok=True)
output_file_png = output_dir / "Result3C_P1P2C1_paper.png"
output_file_pdf = output_dir / "Result3C_P1P2C1_paper.pdf"

plt.savefig(output_file_png, dpi=300)
plt.savefig(output_file_pdf, dpi=300)
plt.show()

print(f"Plot salvato in: {output_file_png}")
print(f"Plot salvato in: {output_file_pdf}")
