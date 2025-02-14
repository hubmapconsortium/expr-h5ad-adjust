#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: DockerRequirement
    dockerPull: hubmap/expr-h5ad-adjust:latest
baseCommand: /opt/expr_h5ad_adjust.py

inputs:
  assay:
    type: string
    inputBinding:
      position: 1
  matrix:
    type: File
    inputBinding:
      position: 2

outputs:
  matrix_adj:
    type: File
    outputBinding:
      glob: "expr.h5ad"
  counts_matrix:
    type: File
    outputBinding:
      glob: "counts_matrix.mtx.gz"
  features:
    type: File
    outputBinding:
      glob: "features.tsv.gz"
  barcodes:
    type: File
    outputBinding:
      glob: "barcodes.tsv.gz"
