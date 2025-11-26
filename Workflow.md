```mermaid
graph TD;

    A[Lidar données]

    subgraph 
        B[données_test_LIDAR.py]
        C[affichage_LIDAR.py]
        D[import_LIDAR.py]
    end

    subgraph 
        E[LIDAR_numpy.py]
        F[LIDAR_DataFrame.py]
    end

    subgraph 
        G[LIDAR_MNS.py]
        I[LIDAR_couches.py]
    end

    subgraph 
        J[LIDAR_LDRAW.py]
        K[LIDAR_graphe.py]
    end

    H[MNS_TIFF.py]

    %% Main externe
    M[main.py]

    %% Connexions
    A --> B
    A --> C
    A --> D

    D --> E
    D --> F

    B --> G
    E --> G
    F --> G

    B --> I
    E --> I

    I --> J
    I --> K
    K --> J

    G --> H

    %% Main.py sur le côté
    M

    
```
