## Visual Representation of `RegEx.in`, before processing

```mermaid
graph LR
    %% Definition of states
    q1((q1))
    q2(((q2)))
    q3(((q3)))
    
    %% Transitions
    q1 -->|a| q1
    q1 -->|a| q2
    q1 -->|a, b| q3
    q2 -->|a| q3
    q2 -->|b| q2
```

## Visual Representation of `RegEx.out`, after processing

```regex
((a)*(a+b) + (a)*a(b)*(λ+a))
```