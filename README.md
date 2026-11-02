# UCAB Lab 5: fronteras y modelos de despliegue

Laboratorio de la Unidad V de Computación en la Nube. La práctica utiliza una arquitectura pequeña en AWS para distinguir el modelo de despliegue de otras propiedades como acceso, región, servicio y proveedor.

La idea central es sencilla: **un recurso sin acceso público puede seguir perteneciendo a una nube pública**. De manera similar, utilizar varios recursos de AWS no convierte una solución en híbrida, comunitaria o multinube.

## Propósito

Al finalizar la práctica podrás:

1. Diferenciar nube pública, privada, híbrida y comunitaria.
2. Explicar por qué multinube es una estrategia de proveedores y no un modelo NIST adicional.
3. Separar los conceptos de acceso privado, nube privada, región y proveedor.
4. Clasificar arquitecturas a partir de evidencia explícita.
5. Justificar una decisión considerando datos, demanda, capacidad operativa, economía y dependencia.
6. Reconocer al menos una contrapartida de la alternativa seleccionada.

## Escenario

Una organización recibe observaciones ficticias para un proyecto universitario. Algunos registros cumplen la política de publicación y otros contienen campos restringidos o datos con formato inválido.

La arquitectura mantiene dos fronteras lógicas:

- **Recepción:** conserva el conjunto original para poder auditarlo.
- **Aprobados:** recibe únicamente los registros que superan la política local.

Ambas fronteras se implementan con buckets privados de Amazon S3 en la misma cuenta, proveedor y región. La separación es útil para gobernar datos, pero no crea una nube híbrida.

## Arquitectura

```text
CloudShell en Ohio
       │
       ├──> S3 recepción ──> política Python ──> S3 aprobados
       │
       ├──> inventario de cuenta, región y controles
       │
       └──> análisis de escenarios de despliegue
```

## Servicios y herramientas

| Componente | Uso en el laboratorio |
|---|---|
| AWS CloudShell | Terminal con credenciales temporales y herramientas preinstaladas. |
| AWS CloudFormation | Creación y eliminación reproducible de la infraestructura. |
| Amazon S3 | Almacenamiento versionado de los datos recibidos y aprobados. |
| AWS STS | Identificación de la cuenta y del principal activo. |
| AWS CLI | Inspección y operación de los servicios desde CloudShell. |
| Python | Política de datos, inventario y clasificación de escenarios. |

CloudFormation organiza los recursos, pero estos siguen generando los cargos normales de sus respectivos servicios. La práctica almacena pocos kilobytes y realiza pocas solicitudes. Aun así, la limpieza final es obligatoria.

## Región obligatoria

Todos los recursos se crean exclusivamente en **US East (Ohio), `us-east-2`**. Los scripts y la plantilla rechazan cualquier otra región antes de crear infraestructura.

## Controles incluidos

Los dos buckets declaran explícitamente:

- Block Public Access completo.
- Cifrado SSE-S3.
- Versionado.
- Object Ownership con ACL deshabilitadas.
- Etiquetas de curso, laboratorio, propósito, proveedor y modelo.

Estos controles protegen los recursos, pero no cambian el hecho de que están alojados en la nube pública de AWS.

## Prerrequisitos

- Cuenta AWS del curso con acceso a Ohio.
- AWS CloudShell disponible en `us-east-2`.
- Permisos para STS, CloudFormation y S3.
- Navegador capaz de descargar o copiar las evidencias del informe.

No se necesitan credenciales locales, Docker, servidores virtuales ni servicios fuera de Ohio.

## Organización del repositorio

| Ruta | Contenido |
|---|---|
| `LAB_GUIDE.md` | Único procedimiento paso a paso de la práctica. |
| `TROUBLESHOOTING.md` | Diagnóstico de errores frecuentes y recuperación segura. |
| `app/` | Política de datos, inventario, clasificación y resumen técnico. |
| `data/` | Registros ficticios válidos y mezclados. |
| `scenarios/` | Cinco arquitecturas para analizar. |
| `infra/` | Plantilla CloudFormation limitada a Ohio. |
| `scripts/` | Diagnóstico, despliegue, experimento, verificación y limpieza. |
| `tests/` | Pruebas automatizadas del código y de las restricciones. |
| `evidence/` | Plantilla opcional para organizar el informe. |
| `generated/` | Resultados locales creados durante la práctica; Git los ignora. |

## Desarrollo y validación

El proyecto usa solamente la biblioteca estándar de Python. La validación automatizada cubre la política de datos, los escenarios, el inventario, la limpieza de buckets versionados, la plantilla y la barrera regional. El flujo de integración continua añade análisis de scripts y de CloudFormation.

## Realización de la práctica

El procedimiento completo, los comandos, las salidas esperadas, las preguntas y los requisitos del informe se encuentran únicamente en [LAB_GUIDE.md](LAB_GUIDE.md).
