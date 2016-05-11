# JetBrains BioLabs project

## Synopsis

This is term research project goals to develop benchmark prototype for comprehensive tool comparison, which is easy to extend with new tools and tests.

## Motivation

ChIP-seq has become a widely adopted genomic assay in recent years to determine binding sites for transcription factors or
enrichments for specific histone modifications. Many different tools have been developed and published in recent years. However, a comprehensive comparison and review of these tools is still missing.

## Installation
* clone this repo
* install ChIP-seq tools for comparisons(see supported tools below)
* prepare datasets 
* create config files in YAML format(see config/example___...Config.yaml)

## Important links

The idea of this project based on recent research made by Sebastian Steinhauser, Nils Kurzawa, Roland Eils and Carl Herrmann.
See the paper [A comprehensive comparison of tools for differential
ChIP-seq analysis](http://bib.oxfordjournals.org/content/early/2016/01/12/bib.bbv110.full)


## Project Roadmap
* Base
    - epigenetics
    - ChIP-Seq
    - peak calling
* Wrap tools CHip-Seq analysis
* Develop prototype of benchmark
* Make some service for benchmarking tools(optional)

## GSM's used in development
* GSM1534712
* GSM1534713
* GSM1534714
* GSM1534715
* GSM1534736
* GSM1534737
* GSM1534738
* GSM1534739

## Currently supported tools

* Zinbra
* Chipdiff
* MACS2
* SICER
* MAnorm