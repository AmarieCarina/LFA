
## Visual Representation of `yNFA.in`, after processing


```mermaid
graph LR

    q1((q1))
    q2(((q2)))

    q1 -->|a| q1
    q1 -->|&lambda;| q2
    q2 -->|b| q2
```