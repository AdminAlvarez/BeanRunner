"""Ayudante experimental para cargar los nombres de trabajos de prueba."""


def get_tests_paths ():
    """Devuelve las rutas listadas en job_names.txt."""
    # Se espera ejecutar esta utilidad desde la raíz del repositorio.
    path = 'src/job_tests/'
    with open(path+"job_names.txt", "r") as file:
        # Cada línea corresponde al nombre de un script de prueba.
        names = [path+line.strip() for line in file.readlines()]
    return names