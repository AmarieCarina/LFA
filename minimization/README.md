
## Visual Representation of `minimization.in`, before processing
```mermaid
graph LR
    q0((q0))
    q1((q1))
    q2(((q2)))
    q3((q3))
    q4((q4))
    q5((q5))
    q6(((q6)))
    
    q0 -->|a| q0
    q0 -->|a| q1
    q0 -->|&lambda;, b| q2
    q0 -->|&lambda;| q3
    q1 -->|&lambda;| q2
    q2 -->|&lambda;| q4
    q2 -->|a| q3
    q3 -->|b| q3
    q3 -->|&lambda;| q5
    q3 -->|a, b| q6
    q5 -->|&lambda;, b| q2
    q5 -->|&lambda;| q6
    q5 -->|a| q6
    q4 -->|b| q5
    q4 -->|&lambda;, a| q6
    q6 -->|b| q6
```

## Visual Representation of `minimization.out`, after first processing
```mermaid
graph LR
    Q0(((Q0: q0, q1, q2, q3, q4, q5, q6)))
    Q1(((Q1: q0, q2, q3, q4, q5, q6)))
    Q2(((Q2: q2, q3, q4, q5, q6)))
    
    Q0 -->|a| Q0
    Q0 -->|b| Q2
    Q1 -->|a| Q0
    Q1 -->|b| Q2
    Q2 -->|a| Q2
    Q2 -->|b| Q2
```
## Visual Representation of `minimization.out`, after second processing
```mermaid
graph LR
    Q0_minim(((Q0)))
    
    Q0_minim -->|a, b| Q0_minim

```