# Flask Web App

## Setup & Installation

Make sure you have the latest version of Python installed.

```bash
git clone <repo-url>
```


### Create VirtulEnv. - Best way to manage the project 


```bash
py -m venv <name_of_virtual_enviroment>
```

ctrl shft p, select interpreter python  inside the Scripts folder (of the <name_of_virtual_enviroment>)

```bash
.venv/Scripts/activate
```

Una vez dentro del ambiente virtual, con el mismo activo:

```bash
pip install -r requirements.txt
```

## Running The App

```bash
python main.py
```

## Viewing The App

Go to `http://127.0.0.1:5000`



## to change between Production and Development/Testing

uncomment the corresponding config.


## Modelo MVC ?

### /models: modelado de datos
### /views: vistas, reciben las interacciones y las comunican con los services (controller), para manejar la logica
### /services: Controladores, manejan la logica. 
