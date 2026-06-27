### Implementation & Input Processing

---
The logic in `DFA.py` mirrors the structure of the input file (`DFA.in`) and simulates the automaton using the following approach:

* **Data Parsing:** 

The file structure is dynamically parsed into local variables. The transition table $\delta$ is efficiently modeled as a nested dictionary (`delta[current_state][input_symbol] = next_state`).


* **Simulation & Validation:** 

The `verif(word)` function processes each word character by character, tracking the active path. A word is accepted (`DA`) if the simulation halts successfully in a final state $F \in \text{set}(F)$, otherwise it is rejected (`NU`).

* **Bonus Tracking:** 

The execution path is saved dynamically during evaluation and printed to the console for accepted words.
  * **Transitions Path**:

The alphabet ($\Sigma$) is dynamically reconstructed from the transition table keys at runtime using a dictionary comprehension.
  
---

### Visual Representation of `DFA.in`, after processing

---
```mermaid
graph LR
    q1((q1))
    q4(((q4)))
    q2((q2))
    q3((q3))
    q5((q5))
    
    q1 -->|0| q2
    q1 -->|1| q5
    q2 -->|0| q1
    q2 -->|1| q3
    
    q3 -->|0, 1| q4
    
    q4 -->|0, 1| q4
    q5 -->|0, 1| q5
```