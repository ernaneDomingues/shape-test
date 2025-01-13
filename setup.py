from setuptools import setup, find_packages

setup(
    name="shape-test",  # Nome do projeto
    version="0.1",  # Versão inicial do projeto
    description="Sistema para scoring de modelos de machine learning com pipeline configurável",
    author="Seu Nome",  # Substitua pelo seu nome
    author_email="seuemail@exemplo.com",  # Substitua pelo seu e-mail
    url="https://github.com/seuusuario/scoring_system",  # URL do repositório (caso tenha)
    packages=find_packages(),  # Automático, encontra todos os pacotes no projeto
    install_requires=[  # Dependências do projeto
        "scikit-learn",  # Biblioteca para modelos e pipelines de ML
        "pandas",  # Biblioteca para manipulação de dados
        "numpy",  # Biblioteca para computação numérica
        "argparse",  # Biblioteca para parser de argumentos (geralmente já inclusa no Python)
        "jsonc",  # Para manipulação de arquivos JSONC (se for o caso)
        "logging",  # Para gerenciamento de logs (também geralmente já incluída no Python)
    ],
    extras_require={  # Dependências adicionais para desenvolvimento
        "dev": [
            "pytest",  # Framework para testes
            "black",  # Formatação de código
            "flake8",  # Linter de código
            "mypy",  # Verificação de tipo estático
        ],
    },
    entry_points={  # Para definir o ponto de entrada do script
        'console_scripts': [
            'run_scoring = main:main',  # 'run_scoring' será o comando para executar o main.py
        ],
    },
    classifiers=[  # Metadados do pacote (opcionais, mas ajudam na catalogação)
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Defina a licença apropriada
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Define a versão mínima do Python
)
