graph TD;
    A[Début] --> B{Décision ?};
    A --> C[Option C];
    B --> D[Fin B];
    C --> D;

    %% Styles
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#f66,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
    style D fill:#ffb,stroke:#333,stroke-width:2px
