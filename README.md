# API Coinmarket compraventa

## Instalación 
1. Ejecutar
```
pip install -r requirements.txt 

```

2. Crear `config_template.py`

Renombrar config_template.py a config.py e informar correctamente sus claves.

3. Informar correctamente .env (solo para desarrollo)

Renombrar .env_template a .env e informar las claves

- FLASK_APP=run.py
- FLASK_ENV=el que quieras de `development` o `production``

4. Crear BD

Ejecutar migrations.sql con sqlite3 en el fichero elegido como base de datos