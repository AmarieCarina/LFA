
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
