## Implementation & Input Processing


The logic in `LNFA.py` mirrors the structure of the input file (`yNFA.in`) and simulates the $\lambda$-NFA using the following approach:

* **Data Parsing:** 

The file structure is dynamically parsed into local variables. The transition table $\delta$ is modeled as a nested dictionary mapping to a list of next states (`delta[current_state][input_symbol] = [next_state1, next_state2, ...]`), including the special key `'lambda'` for non-deterministic spontaneous transitions.

* **Simulation & Validation:** 

The simulation handles $\lambda$-transitions using an explicit $\lambda$-closure mechanism:

**$\lambda$-Closure (`lambda_inchidere`):** A DFS/BFS depth search utilizing a stack dynamically computes the set of all states reachable from the current states using only $\lambda$-transitions.

**Word Verification (`verif`):** The automaton starts at the $\lambda$-closure of the initial state $q_0$. For each character, it jumps to the next possible states and immediately computes their $\lambda$-closure. A word is accepted (`DA`) if the final set of active states intersects with the final states set $F$ ($S_{\text{active}} \cap F \neq \emptyset$), otherwise it is rejected (`NU`).


* **Alphabet Extraction:** 

The alphabet ($\Sigma$) is dynamically reconstructed from the transition table keys at runtime using a dictionary comprehension.

## Visual Representation of `yNFA.in`, after processing


```mermaid
graph LR

    q1((q1))
    q2(((q2)))

    q1 -->|a| q1
    q1 -->|&lambda;| q2
    q2 -->|b| q2