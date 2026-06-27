## Implementation & Input Processing


The logic in `NFA.py` mirrors the structure of the input file (`NFA.in`) and simulates the automaton using the following approach:

* **Data Parsing:** 

The file structure is dynamically parsed into local variables. Since this is an NFA, the transition table $\delta$ is modeled as a nested dictionary mapping to a **list of next states** (`delta[current_state][input_symbol] = [next_state1, next_state2, ...]`).

* **Simulation & Validation:** 

The `verif(word)` function implements a parallel path simulation using set operations. For each character, it dynamically updates a set of all active states (`stari_curente`). A word is accepted (`DA`) if the intersection between the final active states and the accepting states set is not empty ($S_{\text{active}} \cap F \neq \emptyset$), otherwise it is rejected (`NU`).

* **Alphabet Extraction:**

The alphabet ($\Sigma$) is dynamically reconstructed from the transition table keys at runtime using a dictionary comprehension.

## Visual Representation of `NFA.in`, after processing


```mermaid
graph LR
    q1((q1))
    q2((q2))
    q3((q3))
    q4(((q4)))
    
    q1 -->|a, b| q1
    q1 -->|a| q2
    q2 -->|a| q3
    q3 -->|a| q4
    q4 -->|a, b| q4
