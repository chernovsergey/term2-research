# JetBrains BioLabs project

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

## Running

```
[term2-research]$ python src/Main.py -h

usage: Main.py [-h] [-t TOOLCONFIG] [-d DATACONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -t TOOLCONFIG, --toolconfig TOOLCONFIG
                        YAML file with tool config. See example in <config> folder
  -d DATACONFIG, --dataconfig DATACONFIG
                        YAML file with data config. See example in <config> folder
```

## How to add new tool for benchmarking

To begin comparison with new tool you have to proceed the following steps:
* Create ```tool_name.py``` file in ```src/tools``` which implements interface ```AbstractTool```. Precicely you need to implement only three methods:
     - ```configure_data```
     - ```configure_run_params```
     - ```run```
     In the configuration methods you are free to pass any arguments you want to be saved as tool state

* Add running method in the ```src/tools/running.py``` to be able to start your tool with given params from outside
* Add method with signature ```___extract_newtoolname(self)``` inside of class ```src/dataprocessing/dr_extractor.py``` which has access to data you work with and configuration params you
* Append YAML configuration block for your tool which contains any keys you need(see ```config/example__toolConfig```)

## How to extend benhmarking set
You havе to provide just another method of class ```Benchmark``` which is placed in ```src/bench/benchmarking.py``` with name ```__show_smth_you_want(self)```. This method will be started automatically with another tests after peak extraction. 
