from submitter import JobSubmitter

def main():
    submitter = JobSubmitter()
    print("=== Módulo de Envío de Trabajos (JobRunner - RF-01 & RF-02) ===")

    # Casos de prueba típicos
    test_cases = [
        "sleep 10",                                  # Válido
        "python3 -c \"print('Hola Mundo')\"",       # Válido con argumentos
        ["ls", "-l", "/var/log"],                   # Válido como lista
        "",                                         # Inválido: Vacío
        "   ",                                      # Inválido: Espacios
        'echo "comillas sin cerrar',                # Inválido: Malformado
    ]

    for cmd in test_cases:
        print(f"\nProcesando entrada: {repr(cmd)}")
        try:
            job_id, job = submitter.submit_job(cmd)
            print(f"  [PASS] Asignado ID Único: {job_id}")
            print(f"  [INFO] Estado inicial: {job.status.value}")
        except ValueError as err:
            print(f"  [RECHAZADO] Error detectado (RF-02): {err}")

if __name__ == "__main__":
    main()