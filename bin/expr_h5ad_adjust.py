#!/usr/bin/env python3
from argparse import ArgumentParser
from enum import Enum
from pathlib import Path
from os import fspath

import anndata
import muon as mu
import manhole


class AnnDataLayer(str, Enum):
    SPLICED = "spliced"
    UNSPLICED = "unspliced"
    SPLICED_UNSPLICED_SUM = "spliced_unspliced_sum"


class Assay(Enum):
    def __new__(
        cls,
        key: str,
        salmon_option: str,
        secondary_analysis_layer: AnnDataLayer,
        barcode_adj_performed: bool,
        barcode_adj_r1_r2: bool,
        keep_all_barcodes: bool,
    ):
        obj = object.__new__(cls)
        obj._value_ = key
        obj.salmon_option = salmon_option
        obj.secondary_analysis_layer = secondary_analysis_layer
        obj.barcode_adj_performed = barcode_adj_performed
        obj.barcode_adj_r1_r2 = barcode_adj_r1_r2
        obj.keep_all_barcodes = keep_all_barcodes
        return obj

    def __str__(self):
        return self.value

    CHROMIUM_V2 = (
        "10x_v2",
        "--chromium",
        AnnDataLayer.SPLICED,
        False,
        False,
        False,
    )
    CHROMIUM_V3 = (
        "10x_v3",
        "--chromiumV3",
        AnnDataLayer.SPLICED,
        False,
        False,
        False,
    )
    CHROMIUM_V2_SN = (
        "10x_v2_sn",
        "--chromium",
        AnnDataLayer.SPLICED_UNSPLICED_SUM,
        False,
        False,
        False,
    )
    CHROMIUM_V3_SN = (
        "10x_v3_sn",
        "--chromiumV3",
        AnnDataLayer.SPLICED_UNSPLICED_SUM,
        False,
        False,
        False,
    )
    CHROMIUM_V3_PROBES = (
        "10x_v3_probes",
        "--chromiumV3_probes",
        AnnDataLayer.SPLICED,
        False,
        False,
        False,
    )
    SNARESEQ = (
        "snareseq",
        "--snareseq",
        AnnDataLayer.SPLICED_UNSPLICED_SUM,
        True,
        False,
        True,
    )
    SCISEQ = (
        "sciseq",
        "--sciseq",
        AnnDataLayer.SPLICED_UNSPLICED_SUM,
        True,
        True,
        True,
    )
    SLIDESEQ = (
        "slideseq",
        "--slideseq",
        AnnDataLayer.SPLICED_UNSPLICED_SUM,
        True,
        False,
        False,
    )


def main(assay: Assay, expr_matrix: Path):
    adata = mu.read(f"{fspath(expr_matrix)}/rna") if expr_matrix.suffix == ".h5mu" else anndata.read_h5ad(expr_matrix)

    if assay.secondary_analysis_layer in adata.layers:
        print("Replacing AnnData.X with layer", assay.secondary_analysis_layer)
        adata.X = adata.layers[assay.secondary_analysis_layer]
    elif assay in {assay.CHROMIUM_V3_PROBES}:
        print("Using AnnData.X as is")
    else:
        raise ValueError(f"Layer {assay.secondary_analysis_layer} not found")

    adata.write_h5ad("expr.h5ad")


if __name__ == "__main__":
    manhole.install(activate_on="USR1")

    p = ArgumentParser()
    p.add_argument("assay", choices=list(Assay), type=Assay)
    p.add_argument("expr_h5ad", type=Path)
    args = p.parse_args()

    main(args.assay, args.expr_h5ad)
