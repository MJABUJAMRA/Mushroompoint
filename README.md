# Mushroompoint

Guia de bolso para consultar rapidamente observações de cogumelos. Use o CLI
para filtrar por habitat, estação e comestibilidade ou listar as opções
existentes antes de aplicar qualquer filtro.

## Pré-requisitos

- Python 3.10 ou superior (não há dependências externas além da biblioteca
  padrão).

## Como executar

1) Dentro do repositório, chame o módulo do CLI diretamente:

```bash
python -m mushroompoint.cli --help
```

2) Para visualizar todas as opções disponíveis e a contagem de registros
carregados do dataset local (`mushroompoint/data/mushrooms.json`):

```bash
python -m mushroompoint.cli --listar
```

3) Para filtrar resultados por habitat, estação ou comestibilidade, combine as
flags conforme necessário. Exemplos práticos:

```bash
# Habitat e estação
python -m mushroompoint.cli --habitat forest --season autumn

# Apenas cogumelos comestíveis em pinheiros
python -m mushroompoint.cli --habitat pine --edible yes

# Verificar se existe algum registro tóxico em troncos
python -m mushroompoint.cli --habitat logs --edible no
```

Se nenhum registro corresponder, o CLI exibirá uma mensagem em português
sugerindo ampliar a busca.

## Exemplos de saída

### Listagem (sem filtros)
```
Opções disponíveis:
  Habitat: coniferous, forest, logs, pine
  Estações: autumn, spring, summer, winter
  Registros comestíveis: 3 | tóxicos: 2
```

### Resultado filtrado
```
Chanterelle — comestível
  habitat: forest, coniferous
  estações: summer, autumn
  notas: Fruity aroma with ridged gills and a golden hue.
```

## Desenvolvimento

Instale ferramentas e rode os testes:

```bash
python -m pip install --upgrade pip
python -m pip install pytest
pytest
```
