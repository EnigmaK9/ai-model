```markdown
```mermaid
graph TD
    %% Custom Styling
    classDef startup fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#000;
    classDef process fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#000;
    classDef validation fill:#ede7f6,stroke:#5e35b1,stroke-width:2px,color:#000;
    classDef success fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#000;
    classDef error fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000;
    classDef shutdown fill:#eceff1,stroke:#455a64,stroke-width:2px,color:#000;

    subgraph Lifespan_Management [Section 1: Lifecycle Management]
        A[Start: Uvicorn Server Starts] --> B[lifespan Context Manager]
        B --> C{On Startup: Load Model?}
        
        C -->|Success| D[Load Tokenizer & Model into Memory]
        D --> E[Print Success & Yield Control]
        
        C -->|Failure| F[Print Error & Raise Exception]
        F --> G([Server Fails to Start])
        
        H[Trigger: On Shutdown] --> I[Unload Model & Tokenizer]
        I --> J[Clear GPU/CPU Cache]
        J --> K([Server Stops])
    end

    subgraph API_Execution [Section 2: /chat Endpoint Execution]
        E --> L[Receive POST /chat Request]
        L --> M{Validate Prompt: Is it empty?}
        
        M -->|Yes| N[400 Bad Request]
        M -->|No| O{Check Model State: Is loaded?}
        
        O -->|No| P[503 Service Unavailable]
        O -->|Yes| Q[Pipeline: Define Messages System + User]
        
        Q --> R[tokenizer.apply_chat_template]
        R --> S[tokenizer.encode to Tensors]
        S --> T[model.generate with torch.no_grad]
        T --> U[tokenizer.decode output tokens]
        
        U --> V{Exception Caught?}
        V -->|Yes| W[500 Internal Server Error]
        V -->|No| X[200 OK: Return AgentResponse]
    end

    %% Apply Styles
    class A,B,D,E startup;
    class F,G,I,J,K shutdown;
    class L,Q,R,S,T,U process;
    class C,M,O,V validation;
    class X success;
    class N,P,W error;
