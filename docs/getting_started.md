Luckily, getting started with the Sagardotegi Optimization Challenge is not a challenge at all!
You only need a working Python installation and a few files.

:orange-badge[⚠️ NOTE] Instructions assume a Linux operating system (any distro should be ok). Instructions might also work in MacOS and any other UNIX. If you are a Windows user, please consider installing Linux.

#### Step 1️⃣: Create a Python environment

This section guides you to create a Python environment, feel free to skip to the next section if
you have already created one or want to use another method.

First, create a directory for the challenge, for example:

```bash
mkdir sop_challenge
cd sop_challenge
```

Now, run the following command inside the newly created directory, it will create a Python environment (named `venv`) in the local directory:

```bash
python -m venv venv
```

If venv is not available, we might need to install it. On Debian-based systems (like Ubuntu), we can install it using:

```bash
sudo apt-get install python3-venv
```

Now, we need to activate the environment, select one of the following commands depending on your shell:

```bash
source venv/bin/activate      # if you use bash or zsh (most cases)
source venv/bin/activate.fish # if you use fish
```

Note that you'll have to activate the environment whenever you close the current shell (or open a new one).

### Step 2️⃣: Setup dependencies

Once the virtual environment is ready, we can install the required dependencies. Run one of the commands below:

```bash
pip install numpy # minimal dependencies
pip install numpy matplotlib PyQt6 networkx # includes optional packages to visualize solutions
```

Beyond Python dependencies, we need an extra few files to get started with the challenge: the library and the SOP instance.

You can download them to the current directory from the terminal running these commands:

```bash
wget https://github.com/vadel/maeb_soc/raw/refs/heads/main/sagardotegi_problem.py
wget https://github.com/vadel/maeb_soc/raw/refs/heads/main/instance.txt
wget https://github.com/vadel/maeb_soc/raw/refs/heads/main/author_names.txt
```

or you can get them manually from [github](https://github.com/vadel/maeb_soc):
[library](https://github.com/vadel/maeb_soc/raw/refs/heads/main/sagardotegi_problem.py),
[instance](https://github.com/vadel/maeb_soc/raw/refs/heads/main/instance.txt),
and [names list](https://github.com/vadel/maeb_soc/raw/refs/heads/main/author_names.txt).

After completing the instructions above, you should have the files `sagardotegi_problem.py`, `instance.txt`, and `author_names.txt` in the challenge's directory (created with the first command of Step 1️⃣).

Feel free to open and explore these files! `sagardotegi_problem.py` contains a base class (`SagardotegiProblem`) with documentation, and a simple random search example at the bottom.

### Step 3️⃣: A last check

We're almost done! Before implementing an amazing algorithm inspired by your favorite animal (🤪), let's check if everything is working as expected.

In this step, we'll also guide you through the functionalities implemented in the challenge's library (`sagardotegi_problem.py`).

Create and open a new file (`main.py` for example) in the challenge's directory and paste this contents:

```python
from sagardotegi_problem import SagardotegiProblem
import numpy as np

problem = SagardotegiProblem()  # load the instance

solution = np.arange(problem.size)  # `problem.size` is the number of authors

fitness = problem.evaluate(solution)  # the input to `evaluate` must be a numpy array (a permutation of size 133) and not a Python list

print("The fitness of the identity permutation is:", fitness)
```

Run the script using `python main.py`, and check if the printed fitness is 285.38364, if not, please notify the organizers.

Finally, `SagardotegiProblem` comes with a few utility methods that you might find useful (or fun 🤠).

The first one is, `check_solution`. Given an input numpy array, returns `True` if the array is a valid solution to the problem, and `False` otherwise.

For example, add this code to the end of `main.py`:

```python
foo = np.random.permutation(problem.size)
bar = np.random.permutation(42)
egg = np.arange(problem.size)
egg[-1] = 0

print("Is the identity a valid solution?", problem.check_solution(solution))
print("Is foo a valid solution?", problem.check_solution(foo))
print("Is bar a valid solution?", problem.check_solution(bar))
print("Is egg a valid solution?", problem.check_solution(egg))
```

`SagardotegiProblem` also has a couple of visualization-related methods: `solution_to_layout` and `visualize_solution`. Paste the following to the end of `main.py`:

```python
problem.solution_to_layout(foo)
```

Now, the script should output a list of sagardotegi tables, with a set of authors per table.

The last method is `visualize_solution`. Just append the following line to `main.py` and see what happens:

```python
problem.visualize_solution(foo)
```

A matplotlib window will pop up showing many nodes (each corresponding to one author). Nodes are placed (note that the placing isn't deterministic) based on keyword similarity, while colors indicate the 19 sagardotegi tables.

And this is it! Now you can implement the winning algorithm to find who you will be sitting with tonight!🍻
