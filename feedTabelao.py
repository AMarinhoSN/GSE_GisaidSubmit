import pandas as pd
import argparse
import os

# --- FUNCTIONS ---------------------------------------------------------------
def get_IAMnum(row):
    if row["cod"].startswith("IAM"):
        return int(row["cod"].split("_")[0][3 : len(row["cod"])])
    else:
        return 0


def get_IAMlabel(row):
    return "IAM" + str(row["iam_number"])


def is_minor(row):
    if row["taxon"].endswith("_minor"):
        return False
    else:
        return True


def roundIt(row):
    return str(round(row["coverage"], 4) * 100).replace(".", ",")


def floatfy(row):
    return float(row["coverage"].replace(",", "."))


# check if all sample number are sequential
def printSequentials(iam_narr):
    for i in range(0, len(iam_narr)):
        if iam_narr[i] == 0:
            continue
        d = iam_narr[i] - iam_narr[i - 1]
        if d == 0:
            print(f"{d} = {iam_narr[i]} - {iam_narr[i-1]}")
            continue
        if d > 1:
            print(f"{d} = {iam_narr[i]} - {iam_narr[i-1]}")
            print(f"NON SEQUENTIAL AT {iam_narr[i]}")


# -----------------------------------------------------------------------------
# --- INPUT PROCESSING --------------------------------------------------------
dsc = """
Get a sub dataframe containing only ready to submit sequences from THE TABELAO.
"""


parser = argparse.ArgumentParser(description=dsc)
parser.add_argument(
    "major_summary_csv", type=str, help="path of major summary csv file"
)
parser.add_argument(
    "--outName",
    default="short_sorted.csv",
    type=str,
    help="name for output csv (default = short_sorted.csv)",
)

parser.add_argument(
    "-negControlLabels",
    nargs="+",
    default=[
        "cont-neg-placa1_S96_L001",
        "cont-neg-placa2_S192_L001",
        "cont-neg-placa3_S240_L001",
    ],
    help="negative control labels.",
)
parser.add_argument(
    "-outDir", default=os.getcwd() + "/", help="output dir (default= working dir)"
)
args = parser.parse_args()

# -----------------------------------------------------------------------------
print(" Fiocruz Genomic Surveillance Engine :: feed tabelao module")
print(" v.0.0.1 : Prototype")
print("                     APP: Pre_feedTabelao")
print(" Given compile output files from viralflow processing, prepare a csv ")
print(" containing only major sequences information for each sample processed")
print(" the output files can be opened editor (ex: Excel/LibreOffice) and ")
print(" columns copied directly on the google forms*")
print(" !! THE GOOGLE FORMS IS PROVISIONAL, WE SHOULD GET A BETTER SOLUTION !!")
print(" ---------------------------------------------------------------------")

# --- INPUT -------------------------------------------------------------------
print("@ processing input...")
to_feed = pd.read_csv(args.major_summary_csv)
# get contamination
control_labels = args.negControlLabels
outdir = args.outDir
outname = args.outName
# -----------------------------------------------------------------------------
print("@ preparing sorted csv...")
# prepare columns
to_feed["iam_number"] = to_feed.apply(get_IAMnum, axis=1)
to_feed["iam_label"] = to_feed.apply(get_IAMlabel, axis=1)
# get only major
final_df = to_feed.loc[to_feed.apply(is_minor, axis=1)]
final_df = final_df.sort_values(by="iam_number")
# round coverage values
final_df["coverage"] = final_df.apply(roundIt, axis=1)
print("@ writing output file")
# final_df = final_df.loc[~bad_df]
final_df.to_csv("./feed_tabelao/short_sorted.csv")
print("@ checking for non sequentials to be aware of...")
# check for nonsequential IAM
printSequentials(final_df["iam_number"].values)
print(":: DONE ::")
