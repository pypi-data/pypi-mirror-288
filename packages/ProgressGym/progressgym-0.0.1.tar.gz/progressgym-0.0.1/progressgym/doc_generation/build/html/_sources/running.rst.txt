Running the benchmark
=====================

Installation
------------

First install Progress-Gym using pip. Notice that, in order to perform accelerated inference using *vllm* and resolve resulting conflicts, 
we strictly require *python* version of ``3.8`` and *vllm* version of ``0.4.0.post1``. Therefore, make sure you have ``python3.8`` installed, and run:

.. code-block:: console
   $ python3.8 -m venv .venv
   (.venv) $ pip install progressgym

Or install by cloning the github repository:

.. code-block:: console

   $ git clone https://github.com/ProgressAlign/ProgressAlign.git
   $ python3.8 -m venv .venv
   (.venv) $ pip install -r src/config/requirements-pip.txt


Basic Usage
-----------
**Building Dataset**

Running 

.. code-block:: python

   python ./build_dataset.py 

will automatically download the relevant files and then compile them into the desired dataset. Specifically, it will...
  - Download and decompress raw data files from multiple sources, placing them in ``./dataset/raw_downloads``
  - Organize downloaded data into an unified format, and the resulting historical text dataset is saved as a series of files ``./dataset/dataset_textseq/[century_num]/[year_num].json``
  - Train a series of historical language models  ``./dataset/dataset_modelseq/[century_num]`` using the historical text dataset.

**Running The Benchmarks**

Running 

.. code-block:: python

   python ./run_benchmark.py --challenge [challenge_name] --testtaker [path_to_tested_system]
   
will produce the benchmark results. Omitting 
 
.. code-block:: python
  
   --challenge [challenge_name]
 
will default to testing all challenges. Results will be saved to ``[output_directory]/[test_name].json``, with
``[output_directory]`` set to default as ``./output/benchmark_results``. For each test, results are saved as a dictionary. See item
``score`` for a comprehensive score for each examinee's performance in one subtask.

See annotations of 'run_benchmark.py' for a detailed usage of the command line arguments.




